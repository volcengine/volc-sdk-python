# coding=utf-8
"""Monotonic + wall clocks for health stats.

Durations/ages use a monotonic source so wall-clock adjustments never produce
negative intervals; capture timestamps use wall time. Python 3.7 compatible:
``time.monotonic_ns`` exists since 3.7, but we degrade gracefully just in case
a stripped runtime lacks it.
"""
from __future__ import absolute_import

import time

__all__ = ["Clock", "SystemClock", "monotonic_ns", "wall_ms", "default_clock"]


def _has_monotonic_ns():
    return hasattr(time, "monotonic_ns")


if _has_monotonic_ns():
    def monotonic_ns():
        return time.monotonic_ns()
else:  # pragma: no cover - only on stripped 3.7 runtimes
    def monotonic_ns():
        return int(time.monotonic() * 1e9)


def wall_ms():
    return int(time.time() * 1000)


class Clock(object):
    """Clock interface. Durations in ns (monotonic), captures in ms (wall)."""

    __slots__ = ()

    def monotonic_ns(self):
        raise NotImplementedError

    def wall_ms(self):
        raise NotImplementedError

    def monotonic_ms(self):
        return self.monotonic_ns() // 1_000_000


class SystemClock(Clock):
    __slots__ = ()

    def monotonic_ns(self):
        return monotonic_ns()

    def wall_ms(self):
        return wall_ms()


# Module-level singleton reused by state objects to avoid per-record allocation.
default_clock = SystemClock()
