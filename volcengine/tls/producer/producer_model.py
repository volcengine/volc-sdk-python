import random
import threading
import sys
import time
from enum import Enum
from typing import Optional, List

from volcengine.tls.log_pb2 import LogGroupList, LogGroup
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.util import get_logger


class ClientConfig:
    """客户端配置类"""

    def __init__(self, endpoint: str, region: str, access_key: str, access_secret: str, token: Optional[str] = None,
                 api_key: Optional[str] = None):
        self.endpoint = endpoint
        self.region = region
        self.access_key_id = access_key
        self.access_key_secret = access_secret
        self.token = token
        self.api_key = api_key

    def __str__(self) -> str:
        return (f"ClientConfig(endpoint={self.endpoint}, region={self.region}, "
                f"access_key_id={'***' if self.access_key_id else None}, "
                f"access_key_secret={'***' if self.access_key_secret else None}, "
                f"token={'***' if self.token else None}, "
                f"api_key={'***' if self.api_key else None})")

    def reset_api_key(self, api_key: str) -> None:
        self.api_key = api_key


def _valid_number(field: int, min_val: int, max_val: int, default_val: int) -> int:
    """验证数字是否在有效范围内，否则返回默认值"""
    try:
        field_val = int(field)
        min_val = int(min_val)
        max_val = int(max_val)
        default_val = int(default_val)

        if field_val < min_val or field_val > max_val:
            return default_val
        return field_val
    except (ValueError, TypeError):
        return default_val


class CallBack:
    """回调基类"""

    def on_complete(self, result: 'Result'):
        """请求完成回调"""
        raise NotImplementedError("Please implement the on_completion method.")


class Attempt:
    def __init__(self, success: bool, request_id: str = "", error_code: str = "", error_message: str = "",
                 http_code: int = -1):
        self.success = success
        self.request_id = request_id
        self.error_code = error_code
        self.error_message = error_message
        self.http_code = http_code


class Result:
    def __init__(self, success: bool, attempts: List['Attempt'], attempt_count: int):
        self.success = success
        self.attempts = attempts
        self.attempt_count = attempt_count


class RetryMode(Enum):
    LEGACY_DOUBLE_RETRY = "legacy_double_retry"
    PRODUCER_MANAGED = "producer_managed"


class FailurePolicy(Enum):
    RETRY_THEN_CALLBACK = "retry_then_callback"
    FAIL_FAST = "fail_fast"
    DROP_WITH_CALLBACK = "drop_with_callback"


class FailureType(Enum):
    PERMANENT = "permanent"
    THROTTLED = "throttled"
    SERVER = "server"
    NETWORK = "network"
    LOCAL_RESOURCE = "local_resource"
    CIRCUIT_OPEN = "circuit_open"


class FailureClassifier:
    @staticmethod
    def classify_exception(exception) -> FailureType:
        return FailureClassifier.classify_http_code(getattr(exception, "http_code", 0))

    @staticmethod
    def classify_http_code(http_code: int) -> FailureType:
        if http_code == ProducerConfig.TOO_MANY_REQUEST_ERROR:
            return FailureType.THROTTLED
        if http_code >= ProducerConfig.EXTERNAL_ERROR:
            return FailureType.SERVER
        if http_code == 0:
            return FailureType.NETWORK
        return FailureType.PERMANENT

    @staticmethod
    def should_retry(failure_type: FailureType) -> bool:
        return failure_type in (FailureType.THROTTLED, FailureType.SERVER, FailureType.NETWORK)

    @staticmethod
    def should_record_circuit_failure(failure_type: FailureType) -> bool:
        return FailureClassifier.should_retry(failure_type)


class CircuitBreakerConfig:
    def __init__(self, enabled=False, minimum_requests=100, failure_ratio=0.8,
                 consecutive_failures=20, open_duration_ms=30 * 1000, half_open_max_requests=5):
        self.enabled = enabled
        self.minimum_requests = minimum_requests
        self.failure_ratio = failure_ratio
        self.consecutive_failures = consecutive_failures
        self.open_duration_ms = open_duration_ms
        self.half_open_max_requests = half_open_max_requests


class CircuitBreaker:
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

    def __init__(self, config: Optional[CircuitBreakerConfig]):
        self.config = config or CircuitBreakerConfig()
        self._lock = threading.RLock()
        self.state = self.CLOSED
        self.total_requests = 0
        self.total_failures = 0
        self.consecutive_failures = 0
        self.half_open_in_flight = 0
        self.half_open_successes = 0
        self.opened_at_ms = 0

    def allow_request(self) -> bool:
        return self.acquire_permit() >= 0

    def acquire_permit(self) -> int:
        with self._lock:
            if not self.config.enabled:
                return 0
            now_ms = _monotonic_ms()
            if self.state == self.CLOSED:
                return 0
            if self.state == self.OPEN:
                if now_ms - self.opened_at_ms < self.config.open_duration_ms:
                    return -1
                self._to_half_open()
            if self.half_open_in_flight >= max(1, self.config.half_open_max_requests):
                return -1
            self.half_open_in_flight += 1
            return 1

    def reject_new_data(self) -> bool:
        with self._lock:
            if not self.config.enabled:
                return False
            now_ms = _monotonic_ms()
            if self.state == self.OPEN:
                if now_ms - self.opened_at_ms < self.config.open_duration_ms:
                    return True
                self._to_half_open()
                return False
            if self.state == self.HALF_OPEN:
                return self.half_open_in_flight >= max(1, self.config.half_open_max_requests)
            return False

    def record_success(self, permit_count: int = 1) -> None:
        with self._lock:
            if not self.config.enabled:
                return
            if self.state == self.HALF_OPEN:
                if permit_count <= 0:
                    return
                self._release_permits(permit_count)
                self.half_open_successes += permit_count
                if self.half_open_successes >= max(1, self.config.half_open_max_requests):
                    self._reset()
                return
            self.total_requests += 1
            self.consecutive_failures = 0

    def record_failure(self, failure_type: FailureType, permit_count: int = 1) -> None:
        with self._lock:
            if not self.config.enabled:
                return
            if self.state == self.HALF_OPEN:
                if permit_count > 0:
                    self._release_permits(permit_count)
                if FailureClassifier.should_record_circuit_failure(failure_type):
                    self._open()
                return
            if not FailureClassifier.should_record_circuit_failure(failure_type):
                return
            self.total_requests += 1
            self.total_failures += 1
            self.consecutive_failures += 1
            if self.consecutive_failures >= max(1, self.config.consecutive_failures):
                self._open()
                return
            if self.total_requests >= max(1, self.config.minimum_requests):
                if float(self.total_failures) / float(self.total_requests) >= self.config.failure_ratio:
                    self._open()

    def _open(self) -> None:
        self.state = self.OPEN
        self.opened_at_ms = _monotonic_ms()
        self.half_open_in_flight = 0
        self.half_open_successes = 0

    def _to_half_open(self) -> None:
        self.state = self.HALF_OPEN
        self.half_open_in_flight = 0
        self.half_open_successes = 0

    def release_permits(self, count: int) -> None:
        with self._lock:
            if not self.config.enabled:
                return
            self._release_permits(count)

    def _release_permits(self, count: int) -> None:
        if self.state == self.HALF_OPEN and count > 0:
            self.half_open_in_flight = max(0, self.half_open_in_flight - count)

    def _reset(self) -> None:
        self.state = self.CLOSED
        self.total_requests = 0
        self.total_failures = 0
        self.consecutive_failures = 0
        self.half_open_in_flight = 0
        self.half_open_successes = 0
        self.opened_at_ms = 0


def _monotonic_ms() -> float:
    return time.monotonic() * 1000


class FailureController:
    def __init__(self, config: Optional[CircuitBreakerConfig]):
        self.breaker = CircuitBreaker(config)

    def before_send(self) -> bool:
        return self.breaker.allow_request()

    def acquire_permit(self) -> int:
        return self.breaker.acquire_permit()

    def reject_new_data(self) -> bool:
        return self.breaker.reject_new_data()

    def release_permits(self, count: int) -> None:
        self.breaker.release_permits(count)

    def after_send(self, outcome=None, success=False, permit_count: int = 1) -> None:
        if success:
            self.breaker.record_success(permit_count)
            return
        if isinstance(outcome, FailureType):
            failure_type = outcome
        else:
            failure_type = FailureClassifier.classify_exception(outcome)
        self.breaker.record_failure(failure_type, permit_count)


class ProducerConfig:
    """日志生产者配置类"""
    # 静态常量定义
    DEFAULT_TOTAL_SIZE_IN_BYTES = 100 * 1024 * 1024  # 100MB
    DEFAULT_MAX_THREAD_COUNT = 50
    DEFAULT_MAX_BATCH_SIZE = 512 * 1024  # 512KB
    MAX_BATCH_SIZE = 9 * 1024 * 1024 + 512 * 1024
    DEFAULT_MAX_BATCH_COUNT = 4096
    MAX_BATCH_COUNT = 32768
    MAX_LOG_GROUP_COUNT = 10000
    DEFAULT_LINGER_MS = 2000  # 2秒
    TOO_MANY_REQUEST_ERROR = 429
    EXTERNAL_ERROR = 500
    MIN_WAIT_MS = 100
    DEFAULT_RETRY_COUNT = 4
    DEFAULT_RESERVED_ATTEMPTS = DEFAULT_RETRY_COUNT + 1
    MAX_RETRY_COUNT = 10
    MAX_RESERVED_ATTEMPTS = MAX_RETRY_COUNT + 1
    MAX_THREAD_COUNT = 10
    DEFAULT_BLOCK_MS = 60 * 1000  # 60秒
    TEMPORARY_RESERVATION_OVERHEAD_BYTES = 1024

    def __init__(self, endpoint: str, region: str, access_key: str, access_secret: str, token: Optional[str] = None,
                 api_key: Optional[str] = None):
        """初始化生产者配置"""
        self.total_size_in_bytes = self.DEFAULT_TOTAL_SIZE_IN_BYTES
        self.max_thread_count = self.MAX_THREAD_COUNT
        self.max_batch_size_bytes = self.DEFAULT_MAX_BATCH_SIZE
        self.max_batch_count = self.DEFAULT_MAX_BATCH_COUNT
        self.linger_ms = self.DEFAULT_LINGER_MS
        self.max_block_ms = self.DEFAULT_BLOCK_MS
        self.retry_count = self.DEFAULT_RETRY_COUNT
        self.max_reserved_attempts = self.DEFAULT_RESERVED_ATTEMPTS
        self.enable_nanosecond = False
        self.max_producer_memory_bytes = self._default_max_producer_memory_bytes(self.DEFAULT_TOTAL_SIZE_IN_BYTES)
        self._max_producer_memory_bytes_explicit = False
        self.retry_mode = RetryMode.LEGACY_DOUBLE_RETRY
        self.failure_policy = FailurePolicy.RETRY_THEN_CALLBACK
        self.circuit_breaker = CircuitBreakerConfig()
        self.memory_limiter = None
        self.client_config = ClientConfig(endpoint, region, access_key, access_secret, token, api_key)

    def __str__(self) -> str:
        return (f"ProducerConfig(total_size_in_bytes={self.total_size_in_bytes}, "
                f"max_thread_count={self.max_thread_count}, "
                f"max_batch_size_bytes={self.max_batch_size_bytes}, "
                f"max_batch_count={self.max_batch_count}, "
                f"linger_ms={self.linger_ms}, "
                f"max_block_ms={self.max_block_ms}, "
                f"retry_count={self.retry_count}, "
                f"max_reserved_attempts={self.max_reserved_attempts}, "
                f"max_producer_memory_bytes={self.max_producer_memory_bytes}, "
                f"retry_mode={self.retry_mode}, "
                f"failure_policy={self.failure_policy}, "
                f"enable_nanosecond={self.enable_nanosecond}, "
                f"client_config={self.client_config})")

    def valid_config(self) -> None:
        """验证并修正配置参数"""
        self.total_size_in_bytes = _valid_number(
            self.total_size_in_bytes, 1, sys.maxsize, self.DEFAULT_TOTAL_SIZE_IN_BYTES
        )
        self.max_thread_count = _valid_number(
            self.max_thread_count, 1, self.MAX_THREAD_COUNT, self.MAX_THREAD_COUNT
        )
        self.max_batch_size_bytes = _valid_number(
            self.max_batch_size_bytes, 1, self.MAX_BATCH_SIZE, self.DEFAULT_MAX_BATCH_SIZE
        )
        self.max_batch_count = _valid_number(
            self.max_batch_count, 1, self.MAX_BATCH_COUNT, self.DEFAULT_MAX_BATCH_COUNT
        )
        self.linger_ms = _valid_number(
            self.linger_ms, self.MIN_WAIT_MS, sys.maxsize, self.DEFAULT_LINGER_MS
        )
        self.max_block_ms = _valid_number(
            self.max_block_ms, 0, sys.maxsize, self.DEFAULT_BLOCK_MS
        )
        self.retry_count = _valid_number(
            self.retry_count, 1, self.MAX_RETRY_COUNT, self.DEFAULT_RETRY_COUNT
        )
        self.max_reserved_attempts = _valid_number(
            self.max_reserved_attempts, 2, self.MAX_RESERVED_ATTEMPTS, self.DEFAULT_RESERVED_ATTEMPTS
        )
        default_initial_values = (
            2 * self.DEFAULT_TOTAL_SIZE_IN_BYTES,
            self._default_max_producer_memory_bytes(self.DEFAULT_TOTAL_SIZE_IN_BYTES),
        )
        if not self._max_producer_memory_bytes_explicit and self.max_producer_memory_bytes in default_initial_values:
            self.max_producer_memory_bytes = self._default_max_producer_memory_bytes(self.total_size_in_bytes)
        else:
            try:
                max_producer_memory_bytes = int(self.max_producer_memory_bytes)
            except (ValueError, TypeError):
                max_producer_memory_bytes = self._default_max_producer_memory_bytes(self.total_size_in_bytes)
            if self._max_producer_memory_bytes_explicit and max_producer_memory_bytes < self.total_size_in_bytes:
                raise TLSException(
                    error_code="InvalidArgument",
                    error_message="maxProducerMemoryBytes must be greater or equal than totalSizeInBytes"
                )
            self.max_producer_memory_bytes = _valid_number(
                max_producer_memory_bytes, self.total_size_in_bytes, sys.maxsize,
                self._default_max_producer_memory_bytes(self.total_size_in_bytes)
            )
        if not isinstance(self.retry_mode, RetryMode):
            self.retry_mode = RetryMode(self.retry_mode or RetryMode.LEGACY_DOUBLE_RETRY.value)
        if not isinstance(self.failure_policy, FailurePolicy):
            self.failure_policy = FailurePolicy(self.failure_policy or FailurePolicy.RETRY_THEN_CALLBACK.value)
        if self.circuit_breaker is None:
            self.circuit_breaker = CircuitBreakerConfig()

        # 验证客户端配置
        if (not self.client_config or
                not self.client_config.endpoint or
                not self.client_config.region or
                not (self.client_config.api_key or
                     (self.client_config.access_key_id and self.client_config.access_key_secret))):
            raise TLSException(error_code="InvalidArgument", error_message=str(self.client_config))

    def set_total_size_in_bytes(self, total_size_in_bytes: int) -> None:
        if total_size_in_bytes <= 0:
            raise TLSException(
                error_code="InvalidArgument",
                error_message=f"totalSizeInBytes must be greater than zero, actual: {total_size_in_bytes}"
            )
        self.total_size_in_bytes = total_size_in_bytes

    def set_max_thread_count(self, max_thread_count: int) -> None:
        if max_thread_count <= 0 or max_thread_count > self.MAX_THREAD_COUNT:
            raise TLSException(
                error_code="InvalidArgument",
                error_message=f"maxThreadCount must be between 1 to {self.MAX_THREAD_COUNT}, actual: {max_thread_count}"
            )
        self.max_thread_count = max_thread_count

    def set_max_batch_size_bytes(self, max_batch_size_bytes: int) -> None:
        if max_batch_size_bytes <= 0 or max_batch_size_bytes > self.MAX_BATCH_SIZE:
            raise TLSException(
                error_code="InvalidArgument",
                error_message=f"maxBatchSizeBytes must be between 1 to {self.MAX_BATCH_SIZE}, actual: {max_batch_size_bytes}"
            )
        self.max_batch_size_bytes = max_batch_size_bytes

    def set_max_batch_count(self, max_batch_count: int) -> None:
        if max_batch_count <= 0 or max_batch_count > self.MAX_BATCH_COUNT:
            raise TLSException(
                error_code="InvalidArgument",
                error_message=f"maxBatchCount must be between 1 to {self.MAX_BATCH_COUNT}, actual: {max_batch_count}"
            )
        self.max_batch_count = max_batch_count

    def set_linger_ms(self, linger_ms: int) -> None:
        if linger_ms < self.MIN_WAIT_MS:
            raise TLSException(
                error_code="InvalidArgument",
                error_message=f"lingerMs must be greater than {self.MIN_WAIT_MS}, actual: {linger_ms}"
            )
        self.linger_ms = linger_ms

    def set_retry_count(self, retry_count: int) -> None:
        if retry_count <= 0 or retry_count > self.MAX_RETRY_COUNT:
            raise TLSException(
                error_code="InvalidArgument",
                error_message=f"retryCount must be between 1 to {self.MAX_RETRY_COUNT}, actual: {retry_count}"
            )
        self.retry_count = retry_count

    def set_max_reserved_attempts(self, max_reserved_attempts: int) -> None:
        if max_reserved_attempts < 2 or max_reserved_attempts > self.MAX_RESERVED_ATTEMPTS:
            raise TLSException(
                error_code="InvalidArgument",
                error_message=f"maxReservedAttempts must be between 2 to {self.MAX_RESERVED_ATTEMPTS}, actual: {max_reserved_attempts}"
            )
        self.max_reserved_attempts = max_reserved_attempts

    def set_client_config(self, client_config: ClientConfig) -> None:
        if (not client_config or
                not client_config.endpoint or
                not client_config.region or
                not (client_config.api_key or
                     (client_config.access_key_id and client_config.access_key_secret))):
            raise TLSException(
                error_code="InvalidArgument",
                error_message=str(client_config)
            )
        self.client_config = client_config

    def set_max_block_ms(self, max_block_ms: int) -> None:
        if max_block_ms < 0:
            raise TLSException(
                error_code="InvalidArgument",
                error_message=f"maxBlockMs must be greater or equal than zero, actual: {max_block_ms}"
            )
        self.max_block_ms = max_block_ms

    def set_max_producer_memory_bytes(self, max_producer_memory_bytes: int) -> None:
        if max_producer_memory_bytes <= 0:
            raise TLSException(
                error_code="InvalidArgument",
                error_message=f"maxProducerMemoryBytes must be greater than zero, actual: {max_producer_memory_bytes}"
            )
        self.max_producer_memory_bytes = max_producer_memory_bytes
        self._max_producer_memory_bytes_explicit = True

    @classmethod
    def _default_max_producer_memory_bytes(cls, total_size_in_bytes: int) -> int:
        return 3 * int(total_size_in_bytes) + cls.TEMPORARY_RESERVATION_OVERHEAD_BYTES

    def check_batch_size(self, batch_size: int) -> None:
        if batch_size > self.MAX_BATCH_SIZE:
            raise TLSException(
                error_code="InvalidArgument",
                error_message=f"log batch size {batch_size} is larger than MAX_BATCH_SIZE {self.MAX_BATCH_SIZE}"
            )
        if batch_size > self.total_size_in_bytes:
            raise TLSException(
                error_code="InvalidArgument",
                error_message=f"log batch size {batch_size} is larger than total_size_in_bytes {self.total_size_in_bytes}"
            )

    @classmethod
    def need_retry(cls, http_code):
        return http_code == cls.TOO_MANY_REQUEST_ERROR or http_code >= cls.EXTERNAL_ERROR or http_code == 0

class BatchLog:
    def __init__(self, batch_key: 'BatchLog.BatchKey', producer_config: ProducerConfig):
        self.batch_key = batch_key
        self.current_batch_size = 0
        self.current_batch_count = 0
        self.earliest_log_time = None
        self.latest_log_time = None
        self.call_back_list = []
        self.log_group_list = LogGroupList()
        self.producer_config = producer_config
        self.reserved_attempts = []
        self.attempt_count = 0
        self.create_ms = time.time() * 1000  # 转换为毫秒
        self.next_retry_ms = 0
        self.retry_backoff_ms = 0
        self.max_retry_backoff_ms = 10 * 1000  # 10秒
        self.base_retry_backoff_ms = 1000  # 1秒
        self.base_increase_backoff_ms = 1000  # 1秒
        self.reserved_bytes = 0
        self.circuit_permit_count = 0
        self.LOG = get_logger(__name__)

    def try_add(self, log_group: LogGroup, batch_size: int, call_back: Optional[CallBack],
                log_count: Optional[int] = None, earliest_log_time: Optional[int] = None,
                latest_log_time: Optional[int] = None) -> bool:
        """尝试添加日志组到批次中"""
        current_batch_count = self.current_batch_count
        current_batch_size = self.current_batch_size
        if log_count is None:
            log_count = len(log_group.logs)
            for log in log_group.logs:
                normalized_time = log.time
                if log.time < 1e10:
                    normalized_time = log.time * 1000
                elif log.time < 1e15:
                    normalized_time = log.time
                else:
                    normalized_time = log.time // int(1e6)
                if earliest_log_time is None or normalized_time < earliest_log_time:
                    earliest_log_time = normalized_time
                if latest_log_time is None or normalized_time > latest_log_time:
                    latest_log_time = normalized_time

        # 检查是否超过阈值
        if (log_count + current_batch_count > ProducerConfig.MAX_BATCH_COUNT or
                batch_size + current_batch_size > ProducerConfig.MAX_BATCH_SIZE):
            return False

        limiter = getattr(self.producer_config, "memory_limiter", None)
        acquired = False
        if limiter is not None:
            acquired = limiter.acquire_payload(batch_size, self.producer_config.max_block_ms)
            if not acquired:
                raise TLSException(error_code="MemoryLimitExceeded",
                                   error_message="failed to acquire producer payload memory")

        try:
            # 添加日志组
            self.log_group_list.log_groups.append(log_group)  # pylint: disable=no-member

            if call_back is not None:
                self.call_back_list.append(call_back)

            # 更新当前计数
            self.current_batch_count = current_batch_count + log_count
            self.current_batch_size = current_batch_size + batch_size
            self.reserved_bytes += batch_size
            if log_count > 0 and earliest_log_time is not None and latest_log_time is not None:
                if self.earliest_log_time is None or earliest_log_time < self.earliest_log_time:
                    self.earliest_log_time = earliest_log_time
                if self.latest_log_time is None or latest_log_time > self.latest_log_time:
                    self.latest_log_time = latest_log_time
        except Exception:
            if acquired:
                limiter.release_payload(batch_size)
            raise

        return True

    def add_circuit_permit_count(self, count: int) -> None:
        if count > 0:
            self.circuit_permit_count += count

    def take_circuit_permit_count(self) -> int:
        count = self.circuit_permit_count
        self.circuit_permit_count = 0
        return count

    def full_and_send_batch_request(self) -> bool:
        """检查批次是否已满，需要发送请求"""
        return (self.current_batch_count >= self.producer_config.max_batch_count or
                self.current_batch_size >= self.producer_config.max_batch_size_bytes)

    def add_attempt(self, attempt: Attempt) -> None:
        """添加尝试记录"""
        self.reserved_attempts.append(attempt)
        self.attempt_count += 1

    def fire_callbacks(self) -> None:
        """触发所有回调函数"""
        if len(self.reserved_attempts) == 0:
            self.LOG.error(f"batch log {self.batch_key} fire call back failed ")
            return

        attempt = self.reserved_attempts[-1]  # 取最后一个尝试结果
        result = Result(attempt.success, self.reserved_attempts, self.attempt_count)
        self._fire_callbacks(result)

    def handle_next_try(self) -> None:
        """处理下一次重试的退避时间"""
        if self.attempt_count == 1:
            self.retry_backoff_ms += self.base_retry_backoff_ms
        else:
            increase_backoff_ms = random.random() * self.base_increase_backoff_ms
            self.retry_backoff_ms += increase_backoff_ms

        self.retry_backoff_ms = min(self.retry_backoff_ms, self.max_retry_backoff_ms)
        self.next_retry_ms = time.time() * 1000 + self.retry_backoff_ms  # 转换为毫秒

    def _fire_callbacks(self, result: Result) -> None:
        """实际触发回调的私有方法"""
        for call_back in self.call_back_list:
            call_back.on_complete(result)

    def __lt__(self, other: 'BatchLog') -> bool:
        return self.next_retry_ms < other.next_retry_ms

    def __str__(self) -> str:
        return (f"BatchLog{{batchKey={self.batch_key}, currentBatchSize={self.current_batch_size}, "
                f"currentBatchCount={self.current_batch_count}, reservedAttempts={self.reserved_attempts}, "
                f"attemptCount={self.attempt_count}, createMs={self.create_ms}, nextRetryMs={self.next_retry_ms}, "
                f"retryBackoffMs={self.retry_backoff_ms}, maxRetryBackoffMs={self.max_retry_backoff_ms}, "
                f"baseRetryBackoffMs={self.base_retry_backoff_ms}, "
                f"baseIncreaseBackoffMs={self.base_increase_backoff_ms}}}")

    class BatchKey:
        """批次键，用于标识唯一批次"""

        def __init__(self, shard_hash: str, topic_id: str, source: str, file_name: str):
            self.shard_hash = shard_hash
            self.topic_id = topic_id
            self.source = source
            self.file_name = file_name

        def __eq__(self, other) -> bool:
            if not isinstance(other, BatchLog.BatchKey):
                return False
            return (self.shard_hash == other.shard_hash and
                    self.topic_id == other.topic_id and
                    self.source == other.source and
                    self.file_name == other.file_name)

        def __hash__(self) -> int:
            return hash((self.shard_hash, self.topic_id, self.source, self.file_name))

        def __str__(self) -> str:
            return (f"BatchKey{{shardHash={self.shard_hash}, topicId={self.topic_id}, "
                    f"source={self.source}, fileName={self.file_name}}}")
