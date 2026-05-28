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
                endtime = time.monotonic() + timeout

            # 等待直到有足够的配额
            while self._value < permits:
                if timeout is not None:
                    remaining = endtime - time.monotonic()
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


class MemoryLimiter:
    """Producer lifecycle memory limiter with payload and temporary reservations."""

    def __init__(self, capacity_bytes, payload_capacity_bytes=None):
        if payload_capacity_bytes is None:
            payload_capacity_bytes = capacity_bytes
        if capacity_bytes <= 0 or payload_capacity_bytes <= 0 or payload_capacity_bytes > capacity_bytes:
            raise ValueError("invalid memory limiter capacity")
        self._capacity_bytes = int(capacity_bytes)
        self._payload_capacity_bytes = int(payload_capacity_bytes)
        self._used_bytes = 0
        self._payload_used_bytes = 0
        self._closed = False
        self._payload_closed = False
        self._lock = threading.Condition()

    def acquire_payload(self, size, timeout_ms):
        return self._acquire(size, timeout_ms, payload=True)

    def acquire_temporary(self, size, timeout_ms):
        return self._acquire(size, timeout_ms, payload=False)

    def _acquire(self, size, timeout_ms, payload):
        size = int(size)
        if size <= 0:
            return True
        if size > self._capacity_bytes or (payload and size > self._payload_capacity_bytes):
            return False
        deadline = None
        if timeout_ms is not None and timeout_ms > 0:
            deadline = time.monotonic() + (timeout_ms / 1000.0)
        with self._lock:
            while not self._is_closed_for(payload) and not self._has_capacity(size, payload):
                if timeout_ms == 0:
                    return False
                if timeout_ms is None or timeout_ms < 0:
                    self._lock.wait()
                    continue
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    return False
                self._lock.wait(remaining)
            if self._is_closed_for(payload):
                return False
            self._used_bytes += size
            if payload:
                self._payload_used_bytes += size
            return True

    def _has_capacity(self, size, payload):
        return (self._used_bytes + size <= self._capacity_bytes and
                (not payload or self._payload_used_bytes + size <= self._payload_capacity_bytes))

    def _is_closed_for(self, payload):
        return self._closed or (payload and self._payload_closed)

    def release_payload(self, size):
        self._release(size, payload=True)

    def release_temporary(self, size):
        self._release(size, payload=False)

    def release(self, size):
        self.release_payload(size)

    def _release(self, size, payload):
        size = int(size)
        if size <= 0:
            return
        with self._lock:
            if size > self._used_bytes or (payload and size > self._payload_used_bytes):
                raise RuntimeError("release exceeds acquired bytes")
            self._used_bytes -= size
            if payload:
                self._payload_used_bytes -= size
            self._lock.notify_all()

    def close_payload(self):
        with self._lock:
            self._payload_closed = True
            self._lock.notify_all()

    def close(self):
        with self._lock:
            self._closed = True
            self._payload_closed = True
            self._lock.notify_all()

    def used(self):
        with self._lock:
            return self._used_bytes

    def available_permits(self):
        with self._lock:
            return self._payload_capacity_bytes - self._payload_used_bytes

    def capacity(self):
        return self._capacity_bytes

    def payload_capacity(self):
        return self._payload_capacity_bytes
