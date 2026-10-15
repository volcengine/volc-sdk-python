import heapq
import time
import threading
from typing import List, Optional

from volcengine.tls.producer.producer_model import BatchLog


def get_time_ms(nano_seconds: int) -> int:
    """将纳秒转换为毫秒"""
    return nano_seconds // 1_000_000


class RetryQueue:
    def __init__(self):
        self.batch: List[BatchLog] = []
        self.mutex = threading.Lock()
        self.closed = False
        self._high_watermark = 0
        # 初始化堆
        heapq.heapify(self.batch)

    def add_to_retry_queue(self, batch: Optional[BatchLog]) -> bool:
        """Atomically reject enqueue after close; otherwise add the batch."""
        with self.mutex:
            if self.closed or batch is None:
                return False
            heapq.heappush(self.batch, batch)
            if len(self.batch) > self._high_watermark:
                self._high_watermark = len(self.batch)
            return True

    def close(self) -> None:
        """Close the enqueue side under the same lock used by add()."""
        with self.mutex:
            self.closed = True

    def get_retry_batch(self, stop_flag: bool) -> List[BatchLog]:
        """获取可以重试的批次列表"""
        producer_batch_list: List[BatchLog] = []

        with self.mutex:
            if not stop_flag:
                # 非停止状态，只获取已到重试时间的批次
                while self.__len__() > 0:
                    # 查看堆顶元素但不弹出
                    peek_batch = self.batch[0]
                    current_ms = get_time_ms(time.time_ns())

                    if peek_batch.next_retry_ms < current_ms:
                        # 已到重试时间，弹出并加入结果列表
                        producer_batch = heapq.heappop(self.batch)
                        producer_batch_list.append(producer_batch)
                    else:
                        # 未到重试时间，停止检查
                        break
            else:
                # 停止状态，获取所有批次
                while self.__len__() > 0:
                    producer_batch = heapq.heappop(self.batch)
                    producer_batch_list.append(producer_batch)

        return producer_batch_list

    def __len__(self) -> int:
        """返回队列长度"""
        return len(self.batch)

    def stats_snapshot(self):
        """Return current depth and lifetime high-watermark atomically."""
        with self.mutex:
            return {
                "current_items": len(self.batch),
                "high_watermark_items": self._high_watermark,
            }
