import threading
import time
from typing import List

from volcengine.tls.producer.log_dispatcher import LogDispatcher
from volcengine.tls.producer.producer_model import ProducerConfig, BatchLog
from volcengine.tls.producer.retry_queue import RetryQueue
from volcengine.tls.producer.send_batch_task import SendBatchTask
from volcengine.tls.util import get_logger


class Mover(threading.Thread):
    def __init__(self, name: str, producer_config: ProducerConfig,
                 dispatcher: LogDispatcher, retry_manager: RetryQueue):
        super().__init__(name=name)
        self.name = name
        self.producer_config = producer_config
        self.retry_queue = retry_manager
        self.executor_service = dispatcher.executor_service
        self.client = dispatcher.client
        self.batches = dispatcher.batches
        self.batches_mutex = dispatcher.batches_mutex
        self.memory_lock = dispatcher.memory_lock
        self.closed = False
        self.LOG = get_logger(__name__)

    def run(self) -> None:
        """线程主执行方法"""
        self.handle_timeout()

        # 处理剩余的重试批次
        self.handle_remaining_batch()
        remaining_retry_batches = self.retry_queue.get_retry_batch(True)
        for log in remaining_retry_batches:
            self.executor_service.submit(
                SendBatchTask(
                    log, self.producer_config, self.memory_lock, self.client, self.retry_queue
                ).run()
            )
        self.LOG.info(f"Mover {self.name} has stopped")

    def handle_timeout(self) -> None:
        """处理超时批次的循环"""
        while not self.closed:
            try:
                self.handle_timeout_batch()
                self.handle_retry_batch()
                time.sleep(1)
            except Exception as e:
                self.LOG.error(f"Mover {self.name} error in handle_timeout: {str(e)}")



    def handle_retry_batch(self) -> None:
        """处理需要重试的批次"""
        batch_logs = self.retry_queue.get_retry_batch(False)
        for log in batch_logs:
            self.executor_service.submit(
                SendBatchTask(
                    log, self.producer_config, self.memory_lock, self.client, self.retry_queue
                ).run()
            )

    def handle_timeout_batch(self) -> int:
        """处理超时的批次并返回剩余时间"""
        self.LOG.debug(f"mover {self.name} handle timeout batch")
        now = int(time.time() * 1000)  # 当前时间（毫秒）
        batch_logs: List[BatchLog] = []
        remains = self.producer_config.linger_ms

        # 遍历所有批次检查超时
        with self.batches_mutex:
            for entry in self.batches.values():
                batch_manager = entry
                with batch_manager.lock:
                    batch_log = batch_manager.batch_log
                    if batch_log is None:
                        continue

                # 计算剩余时间
                cur_remains = self.producer_config.linger_ms + batch_log.create_ms - now
                if cur_remains <= 0:
                    # 批次超时，加入处理列表并移除
                    batch_manager.remove_batch(batch_logs)
                else:
                    # 更新最小剩余时间
                    remains = min(remains, cur_remains)

        # 提交所有超时批次的发送任务
        for log in batch_logs:
            self.executor_service.submit(
                SendBatchTask(log, self.producer_config, self.memory_lock, self.client, self.retry_queue).run()
            )

        return remains

    def handle_remaining_batch(self) -> None:
        """处理剩余的所有批次"""
        self.LOG.debug(f"mover {self.name} handle remaining batch")
        batch_logs: List[BatchLog] = []

        # 遍历所有批次检查超时
        with self.batches_mutex:
            for entry in self.batches.values():
                batch_manager = entry
                with batch_manager.lock:  # 同步处理
                    batch_log = batch_manager.batch_log
                    if batch_log is None:
                        continue
                    batch_manager.remove_batch(batch_logs)

        # 提交所有剩余批次的发送任务
        for log in batch_logs:
            self.executor_service.submit(
                SendBatchTask(
                    log, self.producer_config, self.memory_lock, self.client, self.retry_queue
                ).run()
            )

    def close(self) -> None:
        self.LOG.info(f"Mover {self.name} closed")
        self.closed = True
