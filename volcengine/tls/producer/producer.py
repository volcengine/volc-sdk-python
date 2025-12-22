import threading
import time
from typing import Optional

from volcengine.tls.log_pb2 import LogGroup
from volcengine.tls.producer.batch_semaphore import BatchSemaphore
from volcengine.tls.producer.log_dispatcher import LogDispatcher
from volcengine.tls.producer.mover import Mover
from volcengine.tls.producer.producer_model import ProducerConfig, CallBack
from volcengine.tls.producer.retry_queue import RetryQueue
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import PutLogsV2LogContent
from volcengine.tls.util import get_logger


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

        self.memory_lock = BatchSemaphore(producer_config.total_size_in_bytes)

        # 初始化组件
        self.retry_queue = RetryQueue()
        self.dispatcher = LogDispatcher(producer_config, self.name, self.memory_lock, self.retry_queue)
        self.mover = Mover(f"{self.name}-mover", producer_config, self.dispatcher, self.retry_queue)
        self.LOG = get_logger(__name__)

    @staticmethod
    def default_producer(endpoint: str, region: str, access_key: str,
                         access_secret: str, token: Optional[str] = None) -> 'TLSProducer':
        """创建默认的Producer实例"""
        config = ProducerConfig(endpoint, region, access_key, access_secret, token)
        return TLSProducer(config)

    def send_log_v2(self, hash_key: Optional[str], topic_id: str, source: Optional[str],
                    filename: Optional[str], log: PutLogsV2LogContent, callback: Optional[CallBack]) -> None:
        """发送单条日志（新版本）"""
        self.send_logs_v2(hash_key, topic_id, source, filename, [log], callback)

    def send_logs_v2(self, hash_key: Optional[str], topic_id: str, source: Optional[str],
                     filename: Optional[str], logs: [PutLogsV2LogContent], callback: Optional[CallBack]) -> None:
        """发送多条日志（新版本）"""
        # 检查参数
        if not topic_id or not logs:
            raise TLSException(error_code="InvalidArgument", error_message=f"topic id: {topic_id}, log group: {logs}")

        # 检查批次大小
        if len(logs) > ProducerConfig.MAX_LOG_GROUP_COUNT:
            raise TLSException(
                error_code="InvalidArgument",
                error_message=f"log list size {len(logs)} is greater than threshold {ProducerConfig.MAX_LOG_GROUP_COUNT}"
            )

        # 转换为日志组并添加到分发器
        log_group = LogGroup()
        if source is not None:
            log_group.source = source
        if filename is not None:
            log_group.filename = filename
        for v in logs:
            new_log = log_group.logs.add()  # pylint: disable=no-member
            new_log.time = v.time
            for key in v.log_dict.keys():
                log_content = new_log.contents.add()
                log_content.key = str(key)
                log_content.value = str(v.log_dict[key])

        self.dispatcher.add_batch(hash_key, topic_id, source, filename, log_group, callback)

    def reset_access_key_token(self, access_key: str, secret_key: str, security_token: Optional[str]) -> None:
        """重置访问密钥和令牌"""
        if not access_key or not secret_key:
            raise TLSException(
                error_code="InvalidArgument",
                error_message=f"reset producer {self.name} access key failed, accessKey is {access_key}, "
                              f"secretKey is {secret_key}, token is {security_token}"
            )
        self.dispatcher.reset_access_key_token(access_key, secret_key, security_token)

    def start(self) -> None:
        """启动Producer"""
        self.dispatcher.start()
        self.mover.start()
        self.LOG.info(f"producer {self.name} started")

    def close(self, timeout_ms: int = 30000) -> None:
        """关闭Producer"""
        feedback_exception = None

        try:
            timeout_ms = self._close_mover(timeout_ms)
        except TLSException as e:
            feedback_exception = e

        try:
            timeout_ms = self._close_executor_service(timeout_ms)
        except TLSException as e:
            if feedback_exception is None:
                feedback_exception = e

        if feedback_exception:
            raise feedback_exception

        self.LOG.info(f"producer {self.name} closed")

    def _close_mover(self, timeout_ms: int) -> int:
        start_ms = time.time() * 1000

        self.dispatcher.close()
        self.retry_queue.closed = True
        self.mover.close()
        self.mover.join(timeout_ms / 1000)  # 转换为秒

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
            executor_service.shutdown()

        self.LOG.info("producer executor service is closed")

        now_ms = time.time() * 1000
        return max(0, int(timeout_ms - (now_ms - start_ms)))
