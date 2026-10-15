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

    _PHASES = ("ingress", "aggregate", "send", "retry")

    def __init__(self, capacity_bytes, payload_capacity_bytes=None):
        if payload_capacity_bytes is None:
            payload_capacity_bytes = capacity_bytes
        if capacity_bytes <= 0 or payload_capacity_bytes <= 0 or payload_capacity_bytes > capacity_bytes:
            raise ValueError("invalid memory limiter capacity")
        self._capacity_bytes = int(capacity_bytes)
        self._payload_capacity_bytes = int(payload_capacity_bytes)
        self._used_bytes = 0
        self._payload_used_bytes = 0
        # Collection-scoped high-watermark of total accounted bytes.
        self._used_high_watermark = 0
        self._closed = False
        self._payload_closed = False
        # Observability ledger.  It is deliberately fixed-size: no per-batch
        # or per-generation registry is kept here.  Allocations made while
        # collection is Off are aggregated as unknown until they release.
        self._metrics_generation = 0
        self._metrics_enabled = False
        self._phase_bytes = dict((phase, 0) for phase in self._PHASES)
        self._unknown_payload_bytes = 0
        self._unknown_temporary_bytes = 0
        self._payload_rejected_total = 0
        self._temporary_rejected_total = 0
        self._lock = threading.Condition()

    def acquire_payload(self, size, timeout_ms, generation=None, phase="aggregate"):
        return self._acquire(size, timeout_ms, payload=True,
                             generation=generation, phase=phase)

    def acquire_temporary(self, size, timeout_ms, generation=None):
        return self._acquire(size, timeout_ms, payload=False,
                             generation=generation, phase=None)

    def _acquire(self, size, timeout_ms, payload, generation=None, phase=None):
        size = int(size)
        if size <= 0:
            return True
        if size > self._capacity_bytes or (payload and size > self._payload_capacity_bytes):
            with self._lock:
                self._record_rejection_locked(payload, generation)
            return False
        deadline = None
        if timeout_ms is not None and timeout_ms > 0:
            deadline = time.monotonic() + (timeout_ms / 1000.0)
        with self._lock:
            while not self._is_closed_for(payload) and not self._has_capacity(size, payload):
                if timeout_ms == 0:
                    self._record_rejection_locked(payload, generation)
                    return False
                if timeout_ms is None or timeout_ms < 0:
                    self._lock.wait()
                    continue
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    self._record_rejection_locked(payload, generation)
                    return False
                self._lock.wait(remaining)
            if self._is_closed_for(payload):
                self._record_rejection_locked(payload, generation)
                return False
            self._used_bytes += size
            if payload:
                self._payload_used_bytes += size
            # Allocations made while collection is Off (or by an older token)
            # must not leak a high-watermark observation into a later window.
            if (self._tracks_generation_locked(generation) and
                    self._used_bytes > self._used_high_watermark):
                self._used_high_watermark = self._used_bytes
            self._ledger_acquire_locked(size, generation, phase, payload)
            return True

    def _record_rejection_locked(self, payload, generation=None):
        # Rejections are business observations. Only an explicit current
        # collection token may record one: an untagged or stale waiter might
        # have begun before an Off/On boundary.
        if not self._tracks_generation_locked(generation):
            return
        if payload:
            self._payload_rejected_total += 1
        else:
            self._temporary_rejected_total += 1

    def _tracks_generation_locked(self, generation):
        return (self._metrics_enabled and generation not in (None, 0) and
                int(generation) == self._metrics_generation)

    def _ledger_acquire_locked(self, size, generation, phase, payload):
        if not self._tracks_generation_locked(generation):
            if payload:
                self._unknown_payload_bytes += size
            else:
                self._unknown_temporary_bytes += size
            return
        if payload:
            if phase not in self._phase_bytes:
                phase = "aggregate"
            self._phase_bytes[phase] += size

    def _ledger_release_locked(self, size, generation, phase, payload):
        if self._tracks_generation_locked(generation):
            if payload:
                if phase in self._phase_bytes and self._phase_bytes[phase] >= size:
                    self._phase_bytes[phase] -= size
                else:
                    # Preserve a non-negative fixed ledger even if a legacy
                    # caller omitted/incorrectly tagged a phase.
                    remaining = size
                    for candidate in self._PHASES:
                        released = min(remaining, self._phase_bytes[candidate])
                        self._phase_bytes[candidate] -= released
                        remaining -= released
                        if remaining <= 0:
                            break
            return
        if payload:
            self._unknown_payload_bytes = max(0, self._unknown_payload_bytes - size)
        else:
            self._unknown_temporary_bytes = max(0, self._unknown_temporary_bytes - size)

    def move_payload(self, size, from_phase, to_phase, generation=None):
        size = int(size)
        if size <= 0 or from_phase == to_phase:
            return
        with self._lock:
            if not self._tracks_generation_locked(generation):
                return
            if from_phase not in self._phase_bytes:
                from_phase = "aggregate"
            if to_phase not in self._phase_bytes:
                to_phase = "aggregate"
            moved = min(size, self._phase_bytes[from_phase])
            self._phase_bytes[from_phase] -= moved
            self._phase_bytes[to_phase] += moved

    def set_metrics_generation(self, generation, enabled):
        """Switch the fixed ledger to a collection generation.

        Turning collection Off transfers currently attributable allocations to
        the fixed unknown bucket.  This makes a later Off->On snapshot partial
        without scanning business batches; releases still drain the bucket.
        """
        with self._lock:
            if not enabled:
                self._unknown_payload_bytes += sum(self._phase_bytes.values())
                self._unknown_temporary_bytes += max(0, self._used_bytes - self._payload_used_bytes - self._unknown_temporary_bytes)
                for phase in self._PHASES:
                    self._phase_bytes[phase] = 0
            else:
                # A later collection begins with no attributed memory. Existing
                # Off-era allocations remain in the unknown bucket until their
                # real release; do not seed HWM from them.
                self._used_high_watermark = 0
            self._metrics_generation = int(generation or 0)
            self._metrics_enabled = bool(enabled)

    def ownership_unknown(self):
        with self._lock:
            return (self._unknown_payload_bytes + self._unknown_temporary_bytes) > 0

    def _has_capacity(self, size, payload):
        return (self._used_bytes + size <= self._capacity_bytes and
                (not payload or self._payload_used_bytes + size <= self._payload_capacity_bytes))

    def _is_closed_for(self, payload):
        return self._closed or (payload and self._payload_closed)

    def release_payload(self, size, generation=None, phase=None):
        self._release(size, payload=True, generation=generation, phase=phase)

    def release_temporary(self, size, generation=None):
        self._release(size, payload=False, generation=generation, phase=None)

    def release(self, size):
        self.release_payload(size)

    def _release(self, size, payload, generation=None, phase=None):
        size = int(size)
        if size <= 0:
            return
        with self._lock:
            if size > self._used_bytes or (payload and size > self._payload_used_bytes):
                raise RuntimeError("release exceeds acquired bytes")
            self._used_bytes -= size
            if payload:
                self._payload_used_bytes -= size
            self._ledger_release_locked(size, generation, phase, payload)
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

    def payload_used(self):
        with self._lock:
            return self._payload_used_bytes

    def used_high_watermark(self):
        with self._lock:
            return self._used_high_watermark

    def available_permits(self):
        with self._lock:
            return self._payload_capacity_bytes - self._payload_used_bytes

    def capacity(self):
        return self._capacity_bytes

    def payload_capacity(self):
        return self._payload_capacity_bytes

    def stats_snapshot(self):
        """Return one internally consistent health snapshot under one lock."""
        with self._lock:
            return {
                "accounted_limit_bytes": self._capacity_bytes,
                "accounted_used_bytes": self._used_bytes,
                "payload_bytes": self._payload_used_bytes,
                "temporary_bytes": self._used_bytes - self._payload_used_bytes,
                "high_watermark_bytes": self._used_high_watermark,
                "payload_admission_limit_bytes": self._payload_capacity_bytes,
                "bounded_runtime_buffer_bytes": self._used_bytes - self._payload_used_bytes,
                "payload_admission_rejected_total": self._payload_rejected_total,
                "runtime_buffer_rejected_total": self._temporary_rejected_total,
                "accounting_rejected_total": self._payload_rejected_total + self._temporary_rejected_total,
                "ingress_owned_bytes": self._phase_bytes["ingress"],
                "aggregate_owned_bytes": self._phase_bytes["aggregate"],
                "send_owned_bytes": self._phase_bytes["send"],
                "retry_owned_bytes": self._phase_bytes["retry"],
                "ownership_unknown": (self._unknown_payload_bytes + self._unknown_temporary_bytes) > 0,
            }
