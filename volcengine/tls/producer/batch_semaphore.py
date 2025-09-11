import threading
import time


class BatchSemaphore:
    """支持一次性申请多个配额的信号量"""

    def __init__(self, value=1):
        if value < 0:
            raise ValueError("Semaphore initial value must be >= 0")
        self._value = value
        self._lock = threading.Condition()

    def acquire(self, permits=1, blocking=True, timeout=None):
        """申请一个或多个配额"""
        if permits < 1:
            raise ValueError("Permits must be positive")

        with self._lock:
            # 非阻塞模式立即返回
            if not blocking:
                if self._value < permits:
                    return False
                else:
                    self._value -= permits
                    return True

            # 处理超时
            endtime = None
            if timeout is not None:
                endtime = time.time() + timeout

            # 等待直到有足够的配额
            while self._value < permits:
                if timeout is not None:
                    remaining = endtime - time.time()
                    if remaining <= 0.0:
                        return False
                    self._lock.wait(remaining)
                else:
                    self._lock.wait()

            # 获取配额
            self._value -= permits
            return True

    def release(self, permits=1):
        """释放一个或多个配额"""
        if permits < 1:
            raise ValueError("Permits must be positive")

        with self._lock:
            self._value += permits
            self._lock.notify_all()  # 通知所有等待的线程

    def available_permits(self):
        """返回当前可用的配额数量"""
        with self._lock:
            return self._value

    def try_acquire(self, permits=1):
        """尝试获取配额，不阻塞立即返回"""
        return self.acquire(permits, blocking=False)