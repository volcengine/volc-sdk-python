from volcengine.tls.TLSService import TLSService
from volcengine.tls.producer.batch_semaphore import BatchSemaphore
from volcengine.tls.producer.producer_model import BatchLog, ProducerConfig, Attempt
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
                 memory_lock: BatchSemaphore,
                 client: TLSService,
                 retry_queue: RetryQueue):
        self.LOG = get_logger(__name__)
        self.producer_config = producer_config
        self.memory_lock = memory_lock
        self.client = client
        self.retry_queue = retry_queue
        self.batch_log = batch_log

    def run(self) -> None:
        """线程执行入口，发送请求"""
        self.send_request()

    def send_request(self) -> None:
        """构建并发送日志请求"""
        batch_key = self.batch_log.batch_key
        put_logs_request = PutLogsRequest(batch_key.topic_id, self.batch_log.log_group_list, batch_key.shard_hash)

        try:
            put_logs_response = self.client.put_logs(put_logs_request)
        except TLSException as e:
            self.handle_log_exception(e)
            return
        except Exception as e:
            self.handle_exception(e)
            return

        self.handle_success(put_logs_response)

    def handle_failure(self) -> None:
        """处理失败日志"""
        self.LOG.info(f"send batch failed, batch: {self.batch_log}")
        self.batch_log.fire_callbacks()
        self.memory_lock.release(self.batch_log.current_batch_size)

    def need_retry(self, e: TLSException) -> bool:
        """判断是否需要重试"""
        return (ProducerConfig.need_retry(e.http_code) and
                self.batch_log.attempt_count <= self.producer_config.retry_count and
                not self.retry_queue.closed)

    def handle_log_exception(self, e: TLSException) -> None:
        """处理日志异常"""
        self.LOG.error(f"send batch failed, batch:{self.batch_log}", exc_info=e)

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
        if self.need_retry(e):
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

        # 创建失败尝试记录
        fail_attempt = Attempt(
            success=False,
            error_code=e.__class__.__name__,
            error_message=str(e)
        )
        self.batch_log.add_attempt(fail_attempt)
        self.handle_failure()

    def handle_success(self, put_logs_response: PutLogsResponse) -> None:
        """处理成功响应"""
        success_attempt = Attempt(
            success=True,
            request_id=put_logs_response.request_id,
            http_code=HTTP_STATUS_OK
        )
        self.batch_log.add_attempt(success_attempt)
        self.batch_log.retry_backoff_ms = 0
        self.batch_log.fire_callbacks()
        self.memory_lock.release(self.batch_log.current_batch_size)
        self.LOG.debug(f"send batch success, batch: {self.batch_log}")
