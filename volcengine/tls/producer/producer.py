import threading
import time
import uuid
from typing import Optional

from volcengine.tls.log_pb2 import LogGroup, LogGroupList
from volcengine.tls.producer.batch_semaphore import MemoryLimiter
from volcengine.tls.producer.log_dispatcher import LogDispatcher
from volcengine.tls.producer.mover import Mover
from volcengine.tls.producer.producer_model import ProducerConfig, CallBack
from volcengine.tls.producer.retry_queue import RetryQueue
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import PutLogsV2LogContent
from volcengine.tls.util import get_logger
from volcengine.tls._stats.producer_state import ProducerStatsState
from volcengine.tls.stats.snapshot import project_snapshot


class TLSProducer:
    """TLS Producer的实现类"""
    _instance_id = 0
    _instance_id_lock = threading.Lock()

    def __init__(self, producer_config: ProducerConfig):
        producer_config.valid_config()
        self.producer_config = producer_config

        # 生成实例名称
        with TLSProducer._instance_id_lock:
            TLSProducer._instance_id += 1
            self.name = f"tls-{TLSProducer._instance_id}"

        self.memory_limiter = MemoryLimiter(
            producer_config.max_producer_memory_bytes,
            producer_config.total_size_in_bytes,
        )
        producer_config.memory_limiter = self.memory_limiter
        self.memory_lock = self.memory_limiter

        # 健康观测状态（默认关闭，按实例配置固定）
        from volcengine import VERSION as _sdk_version
        self.stats_state = ProducerStatsState(
            metrics_level=producer_config.metrics_level,
            instance_id="producer-{}".format(uuid.uuid4().hex),
            sdk_version=_sdk_version,
            memory_limiter=self.memory_limiter,
            max_sender_count=producer_config.max_thread_count,
        )
        producer_config.stats_state = self.stats_state
        producer_config._producer_owner = self

        # 初始化组件
        self.retry_queue = RetryQueue()
        self.dispatcher = LogDispatcher(producer_config, self.name, self.memory_limiter, self.retry_queue)
        self.mover = Mover(f"{self.name}-mover", producer_config, self.dispatcher, self.retry_queue)
        self.LOG = get_logger(__name__)
        self._close_lock = threading.Lock()
        self._close_in_progress = False
        self._close_finalizer_lock = threading.Lock()
        self._close_finalizer = None
        self._worker_threads_lock = threading.Lock()
        self._worker_threads = set()
        # bind queue depth providers for snapshots (read-only, O(1))
        self.stats_state.bind_queue_providers(
            retry=self.retry_queue.stats_snapshot,
        )

    @staticmethod
    def default_producer(endpoint: str, region: str, access_key: str,
                         access_secret: str, token: Optional[str] = None,
                         api_key: Optional[str] = None) -> 'TLSProducer':
        """创建默认的Producer实例"""
        config = ProducerConfig(endpoint, region, access_key, access_secret, token, api_key)
        return TLSProducer(config)

    def send_log_v2(self, hash_key: Optional[str], topic_id: str, source: Optional[str],
                    filename: Optional[str], log: PutLogsV2LogContent, callback: Optional[CallBack]) -> None:
        """发送单条日志（新版本）"""
        self.send_logs_v2(hash_key, topic_id, source, filename, [log], callback)

    def send_logs_v2(self, hash_key: Optional[str], topic_id: str, source: Optional[str],
                     filename: Optional[str], logs: [PutLogsV2LogContent], callback: Optional[CallBack]) -> None:
        """发送多条日志（新版本）"""
        stats = self.stats_state
        stats_on = stats is not None and stats.enabled
        # 检查参数
        if not topic_id or not logs:
            if stats_on:
                stats.on_rejected("invalid")
            raise TLSException(error_code="InvalidArgument", error_message=f"topic id: {topic_id}, log group: {logs}")
        if (hasattr(self.dispatcher, "reject_by_open_circuit") and
                self.dispatcher.reject_by_open_circuit(callback)):
            if stats_on:
                stats.on_rejected("circuit")
            return

        max_log_group_count = ProducerConfig.MAX_LOG_GROUP_COUNT
        max_log_group_size = ProducerConfig.MAX_BATCH_SIZE

        def _varint_len(x: int) -> int:
            if x < 0:
                return 10
            n = 1
            while x >= (1 << 7):
                n += 1
                x >>= 7
            return n

        def _tag_len(field_number: int) -> int:
            return _varint_len((field_number << 3) | 2)

        log_groups_field_number = LogGroup.DESCRIPTOR.fields_by_name["logs"].number
        log_group_list_groups_field_number = LogGroupList.DESCRIPTOR.fields_by_name["log_groups"].number

        log_group = LogGroup()
        if source is not None:
            log_group.source = source
        if filename is not None:
            log_group.filename = filename

        base_group_size = log_group.ByteSize()
        current_estimated_group_size = base_group_size
        current_count = 0
        for v in logs:
            new_log = getattr(log_group, "logs").add()
            new_log.time = v.time
            if v.time_ns is not None and hasattr(new_log, "TimeNs"):
                new_log.TimeNs = v.time_ns
            for key in v.log_dict.keys():
                log_content = new_log.contents.add()
                log_content.key = str(key)
                log_content.value = str(v.log_dict[key])

            current_count += 1
            log_size = new_log.ByteSize()
            current_estimated_group_size += _tag_len(log_groups_field_number) + _varint_len(log_size) + log_size
            group_size = current_estimated_group_size
            entry_size = _tag_len(log_group_list_groups_field_number) + _varint_len(group_size) + group_size
            if entry_size > max_log_group_size:
                if current_count == 1:
                    actual_group_size = log_group.ByteSize()
                    actual_entry_size = _tag_len(log_group_list_groups_field_number) + _varint_len(actual_group_size) + actual_group_size
                    if stats_on:
                        stats.on_rejected("invalid")
                    raise TLSException(
                        error_code="InvalidArgument",
                        error_message=f"log size {actual_entry_size} is larger than MAX_LOG_SIZE {max_log_group_size}"
                    )
                getattr(log_group, "logs").pop()
                current_count -= 1
                current_estimated_group_size -= _tag_len(log_groups_field_number) + _varint_len(log_size) + log_size
                self.dispatcher.add_batch(hash_key, topic_id, source, filename, log_group, callback)
                log_group = LogGroup()
                if source is not None:
                    log_group.source = source
                if filename is not None:
                    log_group.filename = filename
                base_group_size = log_group.ByteSize()
                new_log = getattr(log_group, "logs").add()
                new_log.time = v.time
                if v.time_ns is not None and hasattr(new_log, "TimeNs"):
                    new_log.TimeNs = v.time_ns
                for key in v.log_dict.keys():
                    log_content = new_log.contents.add()
                    log_content.key = str(key)
                    log_content.value = str(v.log_dict[key])
                current_count = 1
                current_estimated_group_size = base_group_size
                log_size = new_log.ByteSize()
                current_estimated_group_size += _tag_len(log_groups_field_number) + _varint_len(log_size) + log_size
                group_size = current_estimated_group_size
                entry_size = _tag_len(log_group_list_groups_field_number) + _varint_len(group_size) + group_size
                if entry_size > max_log_group_size:
                    actual_group_size = log_group.ByteSize()
                    actual_entry_size = _tag_len(log_group_list_groups_field_number) + _varint_len(actual_group_size) + actual_group_size
                    if stats_on:
                        stats.on_rejected("invalid")
                    raise TLSException(
                        error_code="InvalidArgument",
                        error_message=f"log size {actual_entry_size} is larger than MAX_LOG_SIZE {max_log_group_size}"
                    )

            if current_count >= max_log_group_count:
                self.dispatcher.add_batch(hash_key, topic_id, source, filename, log_group, callback)
                log_group = LogGroup()
                if source is not None:
                    log_group.source = source
                if filename is not None:
                    log_group.filename = filename
                current_count = 0
                base_group_size = log_group.ByteSize()
                current_estimated_group_size = base_group_size

        if current_count > 0:
            self.dispatcher.add_batch(hash_key, topic_id, source, filename, log_group, callback)

    def reset_access_key_token(self, access_key: str, secret_key: str, security_token: Optional[str]) -> None:
        """重置访问密钥和令牌"""
        if not access_key or not secret_key:
            raise TLSException(
                error_code="InvalidArgument",
                error_message="reset access key failed: access key and secret key must be non-empty"
            )
        self.dispatcher.reset_access_key_token(access_key, secret_key, security_token)

    def reset_api_key(self, api_key: str) -> None:
        self.dispatcher.reset_api_key(api_key)

    def start(self) -> None:
        """启动Producer"""
        try:
            self.dispatcher.start()
            self.mover.start()
        except Exception:
            self.stats_state.set_dispatcher_running(0)
            self.stats_state.set_mover_running(0)
            self.stats_state.mark_failed("lifecycle")
            raise
        self.stats_state.set_dispatcher_running(1)
        self.stats_state.set_mover_running(1)
        self.stats_state.mark_started()
        self.LOG.info(f"producer {self.name} started")

    def get_stats(self, options):
        """Return a bounded immutable view of the local health snapshot."""
        return project_snapshot(self.stats_state.get_stats(), options)

    def set_metrics_level(self, level) -> None:
        """Change metrics collection while the producer is running."""
        self.stats_state.set_metrics_level(level)

    def _work_started(self) -> None:
        with self._worker_threads_lock:
            self._worker_threads.add(threading.get_ident())

    def _work_finished(self) -> None:
        with self._worker_threads_lock:
            self._worker_threads.discard(threading.get_ident())

    def _is_current_worker(self) -> bool:
        with self._worker_threads_lock:
            return threading.get_ident() in self._worker_threads

    def _all_work_settled(self) -> bool:
        if self.mover.is_alive() or self.stats_state.sender_tasks_pending() != 0:
            return False
        try:
            return self.memory_limiter.used() == 0
        except Exception:
            return False

    def close(self, timeout_ms: int = 30000) -> None:
        """关闭Producer"""
        # A callback may call close while another close/finalizer is waiting
        # for that sender task. Never contend on _close_lock from a sender:
        # mark Closing, make the one-shot finalizer responsible for resources,
        # then return so the callback can unwind.
        if self._is_current_worker():
            self.stats_state.mark_closing()
            self._start_close_finalizer()
            raise TLSException(
                error_code="ProducerError",
                error_message="producer close called from an active sender task")
        with self._close_lock:
            if getattr(self.stats_state, "_frozen", False):
                return
            self._close_in_progress = True
            try:
                self._close_with_deadline(timeout_ms)
            except Exception:
                # A deadline only affects the caller. Close ownership remains
                # with this instance and the one-shot finalizer joins real
                # workers before freezing; callers must not issue close again.
                self._start_close_finalizer()
                raise
            finally:
                self._close_in_progress = False

    def _close_with_deadline(self, timeout_ms: int) -> None:
        self.stats_state.mark_closing()
        self.stats_state.set_dispatcher_running(0)
        feedback_exception = None

        try:
            timeout_ms = self._close_mover(timeout_ms)
        except TLSException as e:
            feedback_exception = e
        finally:
            self.stats_state.set_mover_running(1 if self.mover.is_alive() else 0)

        try:
            if feedback_exception is None:
                timeout_ms = self._close_executor_service(timeout_ms)
                if not self._all_work_settled():
                    feedback_exception = TLSException(
                        error_code="ProducerError",
                        error_message="producer work did not settle before close")
        except TLSException as e:
            if feedback_exception is None:
                feedback_exception = e

        self.stats_state.set_mover_running(1 if self.mover.is_alive() else 0)
        if feedback_exception is not None:
            # The state remains Closing/weak until the one-shot finalizer has
            # joined every worker and released the real resources.
            raise feedback_exception
        self._settle_owned_on_close()
        self.stats_state.freeze()
        self.LOG.info(f"producer {self.name} closed")

    def _start_close_finalizer(self) -> None:
        with self._close_finalizer_lock:
            if getattr(self.stats_state, "_frozen", False):
                return
            if self._close_finalizer is not None and self._close_finalizer.is_alive():
                return
            finalizer = threading.Thread(
                target=self._run_close_finalizer,
                name="{}-close-finalizer".format(self.name),
                daemon=True)
            self._close_finalizer = finalizer
            finalizer.start()

    def _run_close_finalizer(self) -> None:
        """Complete a timed-out close after the actual workers settle.

        This is created only by close(), performs no observation work and exits
        after one join/freeze pass. It never holds an observation lock around
        a join, transport operation or user callback.
        """
        with self._close_lock:
            if getattr(self.stats_state, "_frozen", False):
                return
            self._close_in_progress = True
            try:
                self.stats_state.mark_closing()
                self.stats_state.set_dispatcher_running(0)
                self._close_mover_unbounded()
                self.stats_state.set_mover_running(0)
                self._close_executor_service_unbounded()
                if not self._all_work_settled():
                    raise RuntimeError("producer work did not settle during close finalization")
                self._settle_owned_on_close()
                self.stats_state.freeze()
                self.LOG.info(f"producer {self.name} closed")
            except Exception:
                # The initiating close already surfaced its timeout/failure to
                # the caller. Keep the lifecycle non-final instead of freezing
                # an incomplete snapshot if an unexpected close error occurs.
                self.LOG.error("producer close finalizer failed", exc_info=True)
            finally:
                self._close_in_progress = False

    def _settle_owned_on_close(self) -> None:
        """Attribute any residual owned logs/groups to force_close before freeze.

        Only current-collection owned work may be settled here. Older accepted
        counters are intentionally retained without a compensating terminal,
        so a close after Off -> On cannot fabricate a new-generation drop.
        """
        try:
            token = self.stats_state.token()
            if token == 0:
                return
            owned_logs, owned_groups = self.stats_state.current_owned_counts()
            if owned_logs > 0 or owned_groups > 0:
                if self.stats_state.on_terminal(
                        "dropped", owned_logs, owned_groups, token=token):
                    self.stats_state.on_dropped_reason(
                        "force_close", owned_logs, owned_groups, token=token)
        except Exception:
            # Stats accounting must never break close.
            pass

    def _close_mover(self, timeout_ms: int) -> int:
        start_ms = time.time() * 1000

        self.dispatcher.close()
        self.retry_queue.close()
        mover_was_alive = self.mover.is_alive()
        self.mover.close()
        if mover_was_alive:
            self.mover.join(timeout_ms / 1000)  # 转换为秒
        else:
            try:
                self.mover.drain_remaining()
            except Exception as e:
                raise TLSException(
                    error_code="ProducerError",
                    error_message="producer could not drain accepted batches: {}"
                    .format(e))

        if self.mover.is_alive():
            self.LOG.warning("producer mover thread is still alive")
            raise TLSException(error_code="ProducerError", error_message="producer mover thread is still alive")

        self.LOG.info("producer mover is closed")

        now_ms = time.time() * 1000
        return max(0, int(timeout_ms - (now_ms - start_ms)))

    def _close_executor_service(self, timeout_ms: int) -> int:
        start_ms = time.time() * 1000

        executor_service = self.dispatcher.executor_service
        if executor_service:
            # Do not wait without a bound inside ThreadPoolExecutor.shutdown().
            # The SDK-maintained logical queue and in-flight gauges provide an
            # O(1), implementation-independent completion condition.
            executor_service.shutdown(wait=False)
            deadline = time.monotonic() + (max(0, timeout_ms) / 1000.0)
            while True:
                if self.stats_state.sender_tasks_pending() == 0:
                    break
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    self.memory_limiter.close()
                    raise TLSException(
                        error_code="ProducerError",
                        error_message="producer executor did not drain before timeout")
                time.sleep(min(remaining, 0.01))
        self.memory_limiter.close()
        if self.memory_limiter.used() != 0:
            raise TLSException(
                error_code="ProducerError",
                error_message="producer memory did not settle before close")

        self.LOG.info("producer executor service is closed")

        now_ms = time.time() * 1000
        return max(0, int(timeout_ms - (now_ms - start_ms)))

    def _close_mover_unbounded(self) -> None:
        self.dispatcher.close()
        self.retry_queue.close()
        mover_was_alive = self.mover.is_alive()
        self.mover.close()
        if mover_was_alive:
            self.mover.join()
        else:
            self.mover.drain_remaining()
        if self.mover.is_alive():
            raise RuntimeError("producer mover did not settle during close finalization")

    def _close_executor_service_unbounded(self) -> None:
        executor_service = self.dispatcher.executor_service
        if executor_service:
            executor_service.shutdown(wait=True)
        self.memory_limiter.close()
        if self.memory_limiter.used() != 0:
            raise RuntimeError("producer memory did not settle during close finalization")
