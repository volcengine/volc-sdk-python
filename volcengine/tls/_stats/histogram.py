# coding=utf-8
"""Fixed-bucket latency histogram for health stats.

Bucket semantics:
- fast / slow finite bounds in ms; an implicit +Inf bucket is appended.
- Bounds are inclusive on the upper edge (value <= bound falls in that bucket).
- Internal storage is a fixed-length non-cumulative count array plus a running
  sum in milliseconds. Recording never allocates a list/dict.
- A snapshot copies the fixed array under a short lock and computes cumulative
  counts outside the lock. Invariants the snapshot must satisfy:
      count == cumulative_counts[-1]
      count == sum(internal_counts)
      cumulative_counts monotonically non-decreasing
      sum_ms >= 0
- Durations are recorded from a monotonic source (see clock.py); we accept a
  value already expressed in milliseconds (float or int).

Python 3.7 compatible. No dependency on GIL atomicity: a small lock guards the
compound (bucket bump + sum add) so cross-field reads stay consistent.
"""
from __future__ import absolute_import

import math
import threading

from volcengine.tls.stats._immutable import _ImmutableSnapshot

__all__ = [
    "FAST_BOUNDS_MS",
    "SLOW_BOUNDS_MS",
    "FixedHistogram",
    "HistogramSnapshot",
]

# Finite upper bounds in milliseconds; +Inf is implicit (one extra bucket).
FAST_BOUNDS_MS = (1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000)
SLOW_BOUNDS_MS = (
    10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000,
    20000, 50000, 100000, 200000, 300000,
)


def _bucket_index(bounds, value_ms):
    """Index of the first bound >= value_ms (inclusive), else the +Inf bucket.

    Linear scan is fine: bounds have <= 15 entries, and record() is on the hot
    path so we avoid bisect import overhead and keep it allocation-free.
    """
    n = len(bounds)
    i = 0
    while i < n:
        if value_ms <= bounds[i]:
            return i
        i += 1
    return n  # +Inf bucket


class HistogramSnapshot(_ImmutableSnapshot):
    """Immutable point-in-time view of a histogram."""

    __slots__ = ("_bounds", "_cumulative", "_count", "_sum_ms")

    def __init__(self, bounds, cumulative_counts, count, sum_ms):
        self._bounds = bounds
        self._cumulative = cumulative_counts
        self._count = count
        self._sum_ms = sum_ms

    @property
    def bounds_ms(self):
        return self._bounds

    @property
    def cumulative_counts(self):
        return self._cumulative

    @property
    def count(self):
        return self._count

    @property
    def sum_ms(self):
        return self._sum_ms

    def to_dict(self):
        # Fresh containers each call; caller mutation cannot affect the source.
        return {
            "bounds_ms": list(self._bounds),
            "cumulative_counts": list(self._cumulative),
            "count": self._count,
            "sum_ms": self._sum_ms,
        }


class FixedHistogram(object):
    """Fixed-bucket histogram with a dedicated lock.

    One instance per (component, boundary). Lock scope is tiny: bump one bucket
    and add to the sum. Business logic must never run under this lock.
    """

    __slots__ = ("_bounds", "_counts", "_sum_ms", "_count", "_lock")

    def __init__(self, bounds):
        self._bounds = tuple(bounds)
        # len(bounds) finite buckets + 1 implicit +Inf bucket.
        self._counts = [0] * (len(self._bounds) + 1)
        self._sum_ms = 0.0
        self._count = 0
        self._lock = threading.Lock()

    def record_ms(self, value_ms):
        """Record one observation expressed in milliseconds."""
        if value_ms is None:
            return
        try:
            value_ms = float(value_ms)
        except OverflowError:
            # An integer outside float's range can still be classified by
            # sign; preserve the existing negative-value clamp in that case.
            try:
                if value_ms < 0:
                    value_ms = 0.0
                else:
                    return
            except (TypeError, ValueError):
                return
        except (TypeError, ValueError):
            return
        if not math.isfinite(value_ms):
            return
        if value_ms < 0:
            # Clock skew guard: a monotonic source should never yield this, but
            # never let a negative sneak into sum_ms.
            value_ms = 0.0
        idx = _bucket_index(self._bounds, value_ms)
        with self._lock:
            new_sum_ms = self._sum_ms + value_ms
            if not math.isfinite(new_sum_ms):
                return
            self._counts[idx] += 1
            self._sum_ms = new_sum_ms
            self._count += 1

    def record_ns(self, value_ns):
        """Convenience: record a nanosecond duration as milliseconds."""
        if value_ns is None:
            return
        try:
            value_ms = value_ns / 1_000_000.0
        except OverflowError:
            try:
                if value_ns < 0:
                    value_ms = 0.0
                else:
                    return
            except (TypeError, ValueError):
                return
        except (TypeError, ValueError):
            return
        self.record_ms(value_ms)

    def snapshot(self):
        with self._lock:
            counts_copy = list(self._counts)
            count = self._count
            sum_ms = self._sum_ms
        # Compute cumulative outside the lock.
        cumulative = []
        running = 0
        for c in counts_copy:
            running += c
            cumulative.append(running)
        return HistogramSnapshot(self._bounds, tuple(cumulative), count, sum_ms)
