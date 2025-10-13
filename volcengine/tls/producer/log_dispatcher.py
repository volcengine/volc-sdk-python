import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

from volcengine.tls.TLSService import TLSService
from volcengine.tls.log_pb2 import LogGroup
from volcengine.tls.producer.batch_manager import BatchManager
from volcengine.tls.producer.batch_semaphore import BatchSemaphore
from volcengine.tls.producer.producer_model import ProducerConfig, BatchLog, CallBack
from volcengine.tls.producer.retry_queue import RetryQueue
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.util import get_logger


class LogDispatcher:
    TLS_THREAD_POOL_FORMAT = "dispatcher-thread-%d"

    def __init__(self, producer_config: ProducerConfig, producer_name: str, memory_lock: BatchSemaphore,
                 retry_queue: RetryQueue):
        self.producer_config = producer_config
        self.producer_name = producer_name
        self.memory_lock = memory_lock
        self.retry_queue = retry_queue
        self.closed = False

        # 初始化批次映射（用普通dict配合锁实现线程安全）
        self.batches: Dict[BatchLog.BatchKey, BatchManager] = {}
        self.batches_mutex = threading.Lock()

        # 初始化线程池
        self.executor_service = self._create_thread_pool()
        self.LOG = get_logger(__name__)

        # 初始化TLS客户端
        try:
            client_config = self.producer_config.client_config
            self.client = TLSService(client_config.endpoint, client_config.access_key_id,
                                     client_config.access_key_secret, client_config.region, client_config.token)
        except Exception as e:
            self.LOG.error("Failed to create TLS client", exc_info=e)
            raise TLSException(error_code="Initialization Error", error_message="Failed to create TLS client")

    def _create_thread_pool(self) -> ThreadPoolExecutor:
        """创建线程池"""
        thread_count = self.producer_config.max_thread_count
        thread_name_prefix = f"{self.producer_name}-dispatcher-thread-"

        # 创建线程池
        return ThreadPoolExecutor(
            max_workers=thread_count,
            thread_name_prefix=thread_name_prefix
        )

    def start(self) -> None:
        self.closed = False
        self.LOG.info(f"log dispatcher {self.producer_name} started and client init success")

    def close(self) -> None:
        self.LOG.info(f"log dispatcher {self.producer_name} closed")
        self.closed = True

    def close_now(self) -> None:
        self.LOG.info(f"log dispatcher {self.producer_name} close now")
        self.closed = True
        self.executor_service.shutdown(False)

    def get_or_create_batch_manager(self, batch_key: BatchLog.BatchKey) -> BatchManager:
        """获取或创建批次管理器，线程安全实现"""
        with self.batches_mutex:
            # 先检查是否已存在
            batch_manager = self.batches.get(batch_key)
            if batch_manager is not None:
                return batch_manager

            # 不存在则创建新的并添加
            batch_manager = BatchManager()
            # 检查是否有其他线程已添加（双重检查）
            existing = self.batches.get(batch_key)
            if existing is not None:
                return existing
            self.batches[batch_key] = batch_manager
            return batch_manager

    def reset_access_key_token(self, access_key: str, secret_key: str, security_token: str) -> None:
        """重置访问密钥信息"""
        client_config = self.producer_config.client_config
        client_config.reset_access_key_token(access_key, secret_key, security_token)
        self.client.reset_access_key_token(access_key, secret_key, security_token)
        self.LOG.info(f"log dispatcher {self.producer_name} update client config {client_config} success")

    def add_batch(self, hash_key: str, topic_id: str, source: str, filename: str,
                  log_group: LogGroup, callback: CallBack) -> None:
        """添加批次日志的公开接口"""
        try:
            self.do_add(hash_key, topic_id, source, filename, log_group, callback)
        except Exception as e:
            raise TLSException(error_code="AddBatch Error", error_message=str(e))

    def do_add(self, hash_key: str, topic_id: str, source: str, filename: str,
               log_group: LogGroup, callback: CallBack) -> None:
        """添加批次日志的内部实现"""
        # 检查是否已关闭
        if self.closed:
            raise TLSException(error_code="AddBatch Error",
                               error_message="closed LogDispatcher cannot receive logs anymore")

        # 计算批次大小
        batch_size = len(log_group.SerializeToString())
        self.producer_config.check_batch_size(batch_size)

        # 获取内存锁
        max_block_ms = self.producer_config.max_block_ms
        self.LOG.debug(f"dispatcher {self.producer_name} try acquire memory lock")

        if max_block_ms == 0:
            self.memory_lock.acquire(batch_size)
        else:
            # 尝试在指定时间内获取锁
            acquired = self.memory_lock.acquire(
                batch_size,
                timeout=max_block_ms / 1000  # 转换为秒
            )
            if not acquired:
                available = self.memory_lock.available_permits()  # 获取当前可用许可数
                self.LOG.warn(
                    f"Failed to acquire memory within the configured max blocking time {max_block_ms} ms, "
                    f"requiredSizeInBytes={batch_size}, availableSizeInBytes={available}"
                )
                raise TLSException(
                    error_code="AddBatch Error",
                    error_message=f"dispatcher {self.producer_name} try acquire memory lock failed"
                )

        # 添加到批次
        try:
            batch_key = BatchLog.BatchKey(hash_key, topic_id, source, filename)
            batch_manager = self.get_or_create_batch_manager(batch_key)

            # 同步操作
            with batch_manager.lock:
                self.add_to_batch_manager(batch_key, log_group, callback, batch_size, batch_manager)
        except Exception as e:
            # 发生异常时释放内存锁
            self.memory_lock.release(batch_size)
            raise TLSException(error_code="Add Batch Error", error_message="dispatcher add batch concurrent error")

    def add_to_batch_manager(self, batch_key: BatchLog.BatchKey, log_group: LogGroup,
                             callback: CallBack, batch_size: int, batch_manager: BatchManager) -> None:
        """将日志添加到批次管理器"""
        # 尝试添加到现有批次
        batch_log = batch_manager.batch_log
        if batch_log is not None:
            success = batch_log.try_add(log_group, batch_size, callback)
            if success:
                # 检查是否已满需要发送
                if batch_manager.full_and_send_batch_request():
                    batch_manager.add_now(
                        self.producer_config,
                        self.executor_service,
                        self.client,
                        self.memory_lock,
                        self.retry_queue
                    )
                return
            else:
                # 现有批次已满，立即发送
                batch_manager.add_now(
                    self.producer_config,
                    self.executor_service,
                    self.client,
                    self.memory_lock,
                    self.retry_queue
                )

        # 创建新批次并添加
        batch_log = BatchLog(batch_key, self.producer_config)
        batch_manager.batch_log = batch_log

        success = batch_log.try_add(log_group, batch_size, callback)
        if not success:
            self.LOG.error(
                f"tryAdd batchLog failed, batchKey = {str(batch_key)}, batchSize = {batch_size}, "
                f"batchCount = {log_group.get_logs_count()}"
            )
            raise TLSException(error_code="Producer Error", error_message="tryAdd batchLog failed")

        # 检查新批次是否已满需要发送
        if batch_manager.full_and_send_batch_request():
            batch_manager.add_now(
                self.producer_config,
                self.executor_service,
                self.client,
                self.memory_lock,
                self.retry_queue
            )
