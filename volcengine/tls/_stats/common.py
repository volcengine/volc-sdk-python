# coding=utf-8
"""Private immutable queue, worker and memory measurements.

These internal values are Python 3.7 plain classes with ``__slots__``,
read-only properties, tuple/None outputs, and a ``to_dict()`` that returns fresh
containers and omits absent (None) optional fields.
"""
from __future__ import absolute_import

from volcengine.tls.stats._immutable import _ImmutableSnapshot

__all__ = [
    "UINT64_MAX", "saturating_u64",
    "QueueStats", "WorkerRoleStats", "MemoryStats",
]

# Public cumulative counters saturate at unsigned 64-bit for cross-language
# schema stability, even though Python ints are unbounded (plan §8.6).
UINT64_MAX = (1 << 64) - 1


def saturating_u64(value):
    """Clamp an int into [0, UINT64_MAX]. Returns (clamped, saturated_bool)."""
    if value is None:
        return None, False
    if value < 0:
        return 0, False
    if value > UINT64_MAX:
        return UINT64_MAX, True
    return value, False


class QueueStats(_ImmutableSnapshot):
    __slots__ = (
        "_current_items", "_capacity_items", "_current_bytes", "_capacity_bytes",
        "_oldest_age_ms", "_high_watermark_items", "_high_watermark_bytes", "_bounded",
    )

    def __init__(self, current_items, bounded, high_watermark_items=0,
                 capacity_items=None, current_bytes=None, capacity_bytes=None,
                 oldest_age_ms=None, high_watermark_bytes=None):
        self._current_items = int(current_items)
        self._bounded = bool(bounded)
        self._high_watermark_items = int(high_watermark_items)
        self._capacity_items = capacity_items
        self._current_bytes = current_bytes
        self._capacity_bytes = capacity_bytes
        self._oldest_age_ms = oldest_age_ms
        self._high_watermark_bytes = high_watermark_bytes

    @property
    def current_items(self):
        return self._current_items

    @property
    def capacity_items(self):
        return self._capacity_items

    @property
    def current_bytes(self):
        return self._current_bytes

    @property
    def capacity_bytes(self):
        return self._capacity_bytes

    @property
    def oldest_age_ms(self):
        return self._oldest_age_ms

    @property
    def high_watermark_items(self):
        return self._high_watermark_items

    @property
    def high_watermark_bytes(self):
        return self._high_watermark_bytes

    @property
    def bounded(self):
        return self._bounded

    def to_dict(self):
        d = {
            "current_items": self._current_items,
            "high_watermark_items": self._high_watermark_items,
            "bounded": self._bounded,
        }
        if self._capacity_items is not None:
            d["capacity_items"] = self._capacity_items
        if self._current_bytes is not None:
            d["current_bytes"] = self._current_bytes
        if self._capacity_bytes is not None:
            d["capacity_bytes"] = self._capacity_bytes
        if self._oldest_age_ms is not None:
            d["oldest_age_ms"] = self._oldest_age_ms
        if self._high_watermark_bytes is not None:
            d["high_watermark_bytes"] = self._high_watermark_bytes
        return d

    def __repr__(self):
        # No business identifiers; safe fields only.
        return "QueueStats(current_items={}, bounded={})".format(
            self._current_items, self._bounded)


class WorkerRoleStats(_ImmutableSnapshot):
    __slots__ = ("_role", "_expected", "_running", "_in_flight")

    def __init__(self, role, expected, running, in_flight):
        self._role = role
        self._expected = int(expected)
        self._running = int(running)
        self._in_flight = int(in_flight)

    @property
    def role(self):
        return self._role

    @property
    def expected(self):
        return self._expected

    @property
    def running(self):
        return self._running

    @property
    def in_flight(self):
        return self._in_flight

    def to_dict(self):
        return {
            "role": self._role,
            "expected": self._expected,
            "running": self._running,
            "in_flight": self._in_flight,
        }

    def __repr__(self):
        return "WorkerRoleStats(role={!r}, expected={}, running={}, in_flight={})".format(
            self._role, self._expected, self._running, self._in_flight)


class MemoryStats(_ImmutableSnapshot):
    __slots__ = (
        "_accounted_limit_bytes", "_accounted_used_bytes", "_payload_bytes",
        "_temporary_bytes", "_rejected_total", "_high_watermark_bytes",
        "_payload_admission_limit_bytes", "_bounded_runtime_buffer_bytes",
        "_payload_admission_rejected_total", "_runtime_buffer_rejected_total",
        "_ingress_owned_bytes", "_aggregate_owned_bytes", "_send_owned_bytes",
        "_retry_owned_bytes",
    )

    def __init__(self, accounted_limit_bytes, accounted_used_bytes, rejected_total,
                 high_watermark_bytes, payload_bytes=None, temporary_bytes=None,
                 payload_admission_limit_bytes=None,
                 bounded_runtime_buffer_bytes=None,
                 payload_admission_rejected_total=None,
                 runtime_buffer_rejected_total=None,
                 ingress_owned_bytes=None, aggregate_owned_bytes=None,
                 send_owned_bytes=None, retry_owned_bytes=None):
        self._accounted_limit_bytes = int(accounted_limit_bytes)
        self._accounted_used_bytes = int(accounted_used_bytes)
        self._rejected_total = int(rejected_total)
        self._high_watermark_bytes = int(high_watermark_bytes)
        self._payload_bytes = payload_bytes
        self._temporary_bytes = temporary_bytes
        self._payload_admission_limit_bytes = payload_admission_limit_bytes
        self._bounded_runtime_buffer_bytes = bounded_runtime_buffer_bytes
        self._payload_admission_rejected_total = payload_admission_rejected_total
        self._runtime_buffer_rejected_total = runtime_buffer_rejected_total
        self._ingress_owned_bytes = ingress_owned_bytes
        self._aggregate_owned_bytes = aggregate_owned_bytes
        self._send_owned_bytes = send_owned_bytes
        self._retry_owned_bytes = retry_owned_bytes

    @property
    def accounted_limit_bytes(self):
        return self._accounted_limit_bytes

    @property
    def accounted_used_bytes(self):
        return self._accounted_used_bytes

    @property
    def payload_bytes(self):
        return self._payload_bytes

    @property
    def temporary_bytes(self):
        return self._temporary_bytes

    @property
    def payload_admission_limit_bytes(self):
        return self._payload_admission_limit_bytes

    @property
    def bounded_runtime_buffer_bytes(self):
        return self._bounded_runtime_buffer_bytes

    @property
    def payload_admission_rejected_total(self):
        return self._payload_admission_rejected_total

    @property
    def runtime_buffer_rejected_total(self):
        return self._runtime_buffer_rejected_total

    @property
    def ingress_owned_bytes(self):
        return self._ingress_owned_bytes

    @property
    def aggregate_owned_bytes(self):
        return self._aggregate_owned_bytes

    @property
    def send_owned_bytes(self):
        return self._send_owned_bytes

    @property
    def retry_owned_bytes(self):
        return self._retry_owned_bytes

    @property
    def rejected_total(self):
        return self._rejected_total

    @property
    def high_watermark_bytes(self):
        return self._high_watermark_bytes

    def to_dict(self):
        d = {
            "accounted_limit_bytes": self._accounted_limit_bytes,
            "accounted_used_bytes": self._accounted_used_bytes,
            "rejected_total": self._rejected_total,
            "high_watermark_bytes": self._high_watermark_bytes,
        }
        if self._payload_bytes is not None:
            d["payload_bytes"] = self._payload_bytes
        if self._temporary_bytes is not None:
            d["temporary_bytes"] = self._temporary_bytes
        optional = (
            ("payload_admission_limit_bytes", self._payload_admission_limit_bytes),
            ("bounded_runtime_buffer_bytes", self._bounded_runtime_buffer_bytes),
            ("payload_admission_rejected_total", self._payload_admission_rejected_total),
            ("runtime_buffer_rejected_total", self._runtime_buffer_rejected_total),
            ("ingress_owned_bytes", self._ingress_owned_bytes),
            ("aggregate_owned_bytes", self._aggregate_owned_bytes),
            ("send_owned_bytes", self._send_owned_bytes),
            ("retry_owned_bytes", self._retry_owned_bytes),
        )
        for key, value in optional:
            if value is not None:
                d[key] = value
        return d

    def __repr__(self):
        return "MemoryStats(limit={}, used={})".format(
            self._accounted_limit_bytes, self._accounted_used_bytes)
