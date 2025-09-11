import threading

from volcengine.tls.producer.producer_model import ProducerConfig, BatchLog
from volcengine.tls.producer.send_batch_task import SendBatchTask


class BatchManager:
    """批次管理器，用于管理批次的发送和生命周期"""

    def __init__(self):
        self.batch_log = None
        self.lock = threading.Lock()

    def full_and_send_batch_request(self) -> bool:
        if self.batch_log is not None:
            return self.batch_log.full_and_send_batch_request()
        return False

    def add_now(self, config: ProducerConfig, executor_service, client, memory_lock, retry_queue) -> None:
        if self.batch_log is not None:
            task = SendBatchTask(
                self.batch_log, config, memory_lock, client, retry_queue)
            executor_service.submit(task.run())
            self.batch_log = None

    def remove_batch(self, batch_logs: ['BatchLog']) -> None:
        if self.batch_log is not None:
            batch_logs.append(self.batch_log)
            self.batch_log = None
