from volcengine.tls.TLSService import TLSService
from volcengine.tls.producer.batch_semaphore import MemoryLimiter
from volcengine.tls.producer.producer_model import (
    BatchLog,
    ProducerConfig,
    Attempt,
    FailureClassifier,
    FailureController,
    FailureType,
)
from volcengine.tls.producer.retry_queue import RetryQueue
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import PutLogsRequest
from volcengine.tls.tls_responses import PutLogsResponse
from volcengine.tls.util import get_logger

# 常量定义
HTTP_STATUS_OK = 200


class SendBatchTask:
    def __init__(self,
                 batch_log: BatchLog,
                 producer_config: ProducerConfig,
                 memory_lock: MemoryLimiter,
                 client: TLSService,
                 retry_queue: RetryQueue,
                 failure_controller: FailureController = None):
        self.LOG = get_logger(__name__)
        self.producer_config = producer_config
        self.memory_lock = memory_lock
        self.client = client
        self.retry_queue = retry_queue
        self.batch_log = batch_log
        self.failure_controller = failure_controller

    def run(self) -> None:
        """线程执行入口，发送请求"""
        self.send_request()

    def send_request(self) -> None:
        """构建并发送日志请求"""
        circuit_permit_count = int(self.batch_log.circuit_permit_count)
        if self.failure_controller is not None and circuit_permit_count <= 0:
            circuit_permit_count = self.failure_controller.acquire_permit()
            if circuit_permit_count < 0:
                self.handle_local_failure(
                    "CircuitOpenException",
                    "producer circuit breaker is open",
                    FailureType.CIRCUIT_OPEN,
                    permit_count=0,
                )
                return
            self.batch_log.add_circuit_permit_count(circuit_permit_count)

        temporary_size = self.estimate_temporary_reservation_bytes()
        if not self.memory_lock.acquire_temporary(temporary_size, self.producer_config.max_block_ms):
            self.handle_local_failure(
                "MemoryLimitExceeded",
                f"failed to acquire temporary producer memory, requiredSizeInBytes={temporary_size}",
                FailureType.LOCAL_RESOURCE,
            )
            return

        batch_key = self.batch_log.batch_key
        try:
            put_logs_request = PutLogsRequest(
                batch_key.topic_id,
                self.batch_log.log_group_list,
                batch_key.shard_hash,
                log_count=self.batch_log.current_batch_count,
                earliest_log_time=self.batch_log.earliest_log_time,
                latest_log_time=self.batch_log.latest_log_time,
                enable_nanosecond=self.producer_config.enable_nanosecond,
            )

            if not self.calibrate_batch_size():
                return
            put_logs_response = self.client.put_logs(put_logs_request)
        except TLSException as e:
            self.handle_log_exception(e)
            return
        except Exception as e:
            self.handle_exception(e)
            return
        finally:
            self.memory_lock.release_temporary(temporary_size)

        self.handle_success(put_logs_response)

    def estimate_temporary_reservation_bytes(self) -> int:
        return int(self.batch_log.current_batch_size) * 2 + ProducerConfig.TEMPORARY_RESERVATION_OVERHEAD_BYTES

    def calibrate_batch_size(self) -> bool:
        estimated = int(self.batch_log.current_batch_size)
        actual = int(self.batch_log.log_group_list.ByteSize())
        delta = actual - estimated
        if delta > 0:
            if not self.memory_lock.acquire_payload(delta, self.producer_config.max_block_ms):
                self.handle_local_failure(
                    "MemoryLimitExceeded",
                    "buffer full when calibrating batch size",
                    FailureType.LOCAL_RESOURCE,
                )
                return False
            self.batch_log.reserved_bytes += delta
        elif delta < 0:
            self.memory_lock.release_payload(-delta)
            self.batch_log.reserved_bytes += delta
        self.batch_log.current_batch_size = actual
        return True

    def handle_failure(self) -> None:
        """处理失败日志"""
        self.LOG.info(f"send batch failed, batch: {self.batch_log}")
        self.batch_log.fire_callbacks()
        reserved_bytes = getattr(self.batch_log, "reserved_bytes", self.batch_log.current_batch_size)
        self.memory_lock.release_payload(reserved_bytes)
        self.batch_log.reserved_bytes = 0

    def need_retry(self, failure_type: FailureType) -> bool:
        """判断是否需要重试"""
        return (FailureClassifier.should_retry(failure_type) and
                self.batch_log.attempt_count <= self.producer_config.retry_count and
                not self.retry_queue.closed)

    def handle_log_exception(self, e: TLSException) -> None:
        """处理日志异常"""
        self.LOG.error(f"send batch failed, batch:{self.batch_log}", exc_info=e)
        failure_type = FailureClassifier.classify_exception(e)
        if self.failure_controller is not None:
            self.failure_controller.after_send(e, success=False,
                                               permit_count=self.batch_log.take_circuit_permit_count())

        # 创建失败尝试记录
        fail_attempt = Attempt(
            success=False,
            request_id=e.request_id,
            error_code=e.error_code,
            error_message=e.error_message,
            http_code=e.http_code
        )
        self.batch_log.add_attempt(fail_attempt)
        self.batch_log.handle_next_try()

        # 检查是否需要重试
        if self.need_retry(failure_type):
            try:
                self.retry_queue.add_to_retry_queue(self.batch_log)
                self.LOG.info(f"retry queue add batch success, batch: {self.batch_log}")
                return
            except TLSException as ex:
                self.LOG.warn("retry manager is closed and put batch log to failure queue", exc_info=ex)

        # 不需要重试或重试失败，处理失败日志
        self.handle_failure()

    def handle_exception(self, e: Exception) -> None:
        """处理通用异常"""
        self.LOG.error(f"send batch failed, batch:{self.batch_log}", exc_info=e)
        if self.failure_controller is not None:
            self.failure_controller.after_send(FailureType.NETWORK, success=False,
                                               permit_count=self.batch_log.take_circuit_permit_count())

        # 创建失败尝试记录
        fail_attempt = Attempt(
            success=False,
            error_code=e.__class__.__name__,
            error_message=str(e)
        )
        self.batch_log.add_attempt(fail_attempt)
        self.batch_log.handle_next_try()
        if self.need_retry(FailureType.NETWORK):
            try:
                self.retry_queue.add_to_retry_queue(self.batch_log)
                self.LOG.info(f"retry queue add batch success, batch: {self.batch_log}")
                return
            except TLSException as ex:
                self.LOG.warn("retry manager is closed and put batch log to failure queue", exc_info=ex)
        self.handle_failure()

    def handle_local_failure(self, error_code: str, error_message: str, failure_type: FailureType,
                             permit_count: int = None) -> None:
        fail_attempt = Attempt(
            success=False,
            error_code=error_code,
            error_message=error_message,
        )
        self.batch_log.add_attempt(fail_attempt)
        if self.failure_controller is not None:
            if permit_count is None:
                permit_count = self.batch_log.take_circuit_permit_count()
            self.failure_controller.after_send(failure_type, success=False, permit_count=permit_count)
        self.handle_failure()

    def handle_success(self, put_logs_response: PutLogsResponse) -> None:
        """处理成功响应"""
        if self.failure_controller is not None:
            self.failure_controller.after_send(success=True,
                                               permit_count=self.batch_log.take_circuit_permit_count())
        success_attempt = Attempt(
            success=True,
            request_id=put_logs_response.request_id,
            http_code=HTTP_STATUS_OK
        )
        self.batch_log.add_attempt(success_attempt)
        self.batch_log.retry_backoff_ms = 0
        self.batch_log.fire_callbacks()
        reserved_bytes = getattr(self.batch_log, "reserved_bytes", self.batch_log.current_batch_size)
        self.memory_lock.release_payload(reserved_bytes)
        self.batch_log.reserved_bytes = 0
        self.LOG.debug(f"send batch success, batch: {self.batch_log}")
