import random
import sys
import time
from typing import Optional, List

from volcengine.tls.log_pb2 import LogGroupList, LogGroup
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.util import get_logger


class ClientConfig:
    """客户端配置类"""

    def __init__(self, endpoint: str, region: str, access_key: str, access_secret: str, token: Optional[str] = None):
        self.endpoint = endpoint
        self.region = region
        self.access_key_id = access_key
        self.access_key_secret = access_secret
        self.token = token

    def __str__(self) -> str:
        return (f"ClientConfig(endpoint={self.endpoint}, region={self.region}, "
                f"access_key_id={'***' if self.access_key_id else None}, "
                f"access_key_secret={'***' if self.access_key_secret else None}, "
                f"token={'***' if self.token else None})")


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


class ProducerConfig:
    """日志生产者配置类"""
    # 静态常量定义
    DEFAULT_TOTAL_SIZE_IN_BYTES = 100 * 1024 * 1024  # 100MB
    DEFAULT_MAX_THREAD_COUNT = 50
    DEFAULT_MAX_BATCH_SIZE = 512 * 1024  # 512KB
    MAX_BATCH_SIZE = 8 * 1024 * 1024  # 8MB
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

    def __init__(self, endpoint: str, region: str, access_key: str, access_secret: str, token: Optional[str] = None):
        """初始化生产者配置"""
        self.total_size_in_bytes = self.DEFAULT_TOTAL_SIZE_IN_BYTES
        self.max_thread_count = self.MAX_THREAD_COUNT
        self.max_batch_size_bytes = self.DEFAULT_MAX_BATCH_SIZE
        self.max_batch_count = self.DEFAULT_MAX_BATCH_COUNT
        self.linger_ms = self.DEFAULT_LINGER_MS
        self.max_block_ms = self.DEFAULT_BLOCK_MS
        self.retry_count = self.DEFAULT_RETRY_COUNT
        self.max_reserved_attempts = self.DEFAULT_RESERVED_ATTEMPTS
        self.client_config = ClientConfig(endpoint, region, access_key, access_secret, token)

    def __str__(self) -> str:
        return (f"ProducerConfig(total_size_in_bytes={self.total_size_in_bytes}, "
                f"max_thread_count={self.max_thread_count}, "
                f"max_batch_size_bytes={self.max_batch_size_bytes}, "
                f"max_batch_count={self.max_batch_count}, "
                f"linger_ms={self.linger_ms}, "
                f"max_block_ms={self.max_block_ms}, "
                f"retry_count={self.retry_count}, "
                f"max_reserved_attempts={self.max_reserved_attempts}, "
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

        # 验证客户端配置
        if (not self.client_config or
                not self.client_config.endpoint or
                not self.client_config.access_key_id or
                not self.client_config.access_key_secret or
                not self.client_config.region):
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
                not client_config.access_key_id or
                not client_config.access_key_secret or
                not client_config.region):
            raise TLSException(
                error_code="InvalidArgument",
                error_message=str(client_config)
            )
        self.client_config = client_config

    def set_max_block_ms(self, max_block_ms: int) -> None:
        if max_block_ms <= 0:
            raise TLSException(
                error_code="InvalidArgument",
                error_message=f"maxBlockMs must be greater than zero, actual: {max_block_ms}"
            )
        self.max_block_ms = max_block_ms

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
        self.LOG = get_logger(__name__)

    def try_add(self, log_group: LogGroup, batch_size: int, call_back: Optional[CallBack]) -> bool:
        """尝试添加日志组到批次中"""
        current_batch_count = self.current_batch_count
        current_batch_size = self.current_batch_size

        # 检查是否超过阈值
        if (len(log_group.logs) + current_batch_count > ProducerConfig.MAX_BATCH_COUNT or
                batch_size + current_batch_size > ProducerConfig.MAX_BATCH_SIZE):
            return False

        # 添加日志组
        self.log_group_list.log_groups.append(log_group)

        if call_back is not None:
            self.call_back_list.append(call_back)

        # 更新当前计数
        self.current_batch_count = current_batch_count + len(log_group.logs)
        self.current_batch_size = current_batch_size + batch_size

        return True

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

