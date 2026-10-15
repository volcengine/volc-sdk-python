# coding=utf-8
"""Pure counter delta and rate adapter for health-stat snapshots.

The adapter keeps one copied baseline and has no I/O or background work.  It
uses only cumulative counters and the snapshot header fields defined by the
observability contract; gauges are deliberately not compared here.
"""
from __future__ import absolute_import

import threading
from numbers import Integral
from types import MappingProxyType

from volcengine.tls.stats._immutable import _ImmutableSnapshot

__all__ = [
    "CounterSample", "DeltaResult", "DeltaAdapter", "compute_delta",
    "DELTA_INITIAL_BASELINE", "DELTA_METRICS_UNAVAILABLE",
    "DELTA_INSTANCE_CHANGED", "DELTA_COLLECTION_CHANGED",
    "DELTA_SEQUENCE_REGRESSED", "DELTA_UPTIME_REGRESSED",
    "DELTA_CLOCK_REGRESSED", "DELTA_COUNTER_REGRESSED",
    "DELTA_COUNTER_SET_CHANGED",
]


DELTA_INITIAL_BASELINE = "initial_baseline"
DELTA_METRICS_UNAVAILABLE = "metrics_unavailable"
DELTA_INSTANCE_CHANGED = "instance_changed"
DELTA_COLLECTION_CHANGED = "collection_changed"
DELTA_SEQUENCE_REGRESSED = "sequence_not_increasing"
DELTA_UPTIME_REGRESSED = "uptime_regressed"
DELTA_CLOCK_REGRESSED = "capture_time_not_increasing"
DELTA_COUNTER_REGRESSED = "counter_regressed"
DELTA_COUNTER_SET_CHANGED = "counter_set_changed"
_UINT64_MAX = (1 << 64) - 1


def _copy_mapping(value):
    if value is None:
        return None
    return dict(value)


def _as_int(value, default=0):
    if value is None:
        return default
    return int(value)


def _valid_counter_value(value):
    """Return whether a counter is a supported cumulative uint64 value."""
    return (isinstance(value, Integral) and not isinstance(value, bool)
            and 0 <= value <= _UINT64_MAX)


def _counters_available(counters):
    """Validate counter values without coercing invalid values to zero."""
    if counters is None:
        return False
    try:
        return all(_valid_counter_value(value) for value in counters.values())
    except (AttributeError, TypeError, ValueError):
        return False


class CounterSample(_ImmutableSnapshot):
    """An immutable copy of a cumulative counter sample.

    ``header`` and ``counters`` are exposed as read-only mappings so a caller
    cannot mutate a sample after it has been used as an adapter baseline.
    ``counters=None`` represents an unavailable counter section; an empty
    mapping remains an available, empty counter set as in the Go contract.
    """

    __slots__ = ("_header", "_counters")

    def __init__(self, header, counters):
        if header is None:
            header = {}
        self._header = MappingProxyType(dict(header))
        copied = _copy_mapping(counters)
        self._counters = MappingProxyType(copied) if copied is not None else None

    @property
    def header(self):
        return self._header

    @property
    def counters(self):
        return self._counters


class DeltaResult(_ImmutableSnapshot):
    """Immutable result for one counter interval.

    Invalid intervals retain the Go zero-value shape: ``interval_ms`` is 0
    and delta/rate mappings are absent (``None``).  A valid interval always
    has read-only mappings, including when the counter set is empty.
    """

    __slots__ = (
        "_valid", "_reset_reason", "_interval_ms", "_deltas",
        "_rates_per_second",
    )

    def __init__(self, valid=False, reset_reason=None, interval_ms=0,
                 deltas=None, rates_per_second=None):
        self._valid = bool(valid)
        self._reset_reason = reset_reason
        self._interval_ms = int(interval_ms)
        self._deltas = (MappingProxyType(dict(deltas))
                        if deltas is not None else None)
        self._rates_per_second = (MappingProxyType(dict(rates_per_second))
                                  if rates_per_second is not None else None)

    @property
    def valid(self):
        return self._valid

    @property
    def reset_reason(self):
        return self._reset_reason

    @property
    def interval_ms(self):
        return self._interval_ms

    @property
    def deltas(self):
        return self._deltas

    @property
    def rates_per_second(self):
        return self._rates_per_second

    def to_dict(self):
        """Return a fresh JSON-shaped dictionary with copied mappings."""
        result = {"valid": self._valid}
        if self._reset_reason:
            result["reset_reason"] = self._reset_reason
        if self._interval_ms:
            result["interval_ms"] = self._interval_ms
        if self._deltas is not None:
            result["deltas"] = dict(self._deltas)
        if self._rates_per_second is not None:
            result["rates_per_second"] = dict(self._rates_per_second)
        return result

    def __repr__(self):
        return ("DeltaResult(valid={!r}, reset_reason={!r}, interval_ms={!r})"
                .format(self._valid, self._reset_reason, self._interval_ms))


def _copy_sample(sample):
    if not isinstance(sample, CounterSample):
        try:
            return CounterSample(sample.header, sample.counters)
        except AttributeError:
            raise TypeError("sample must be a CounterSample")
    return CounterSample(sample.header, sample.counters)


def _header(sample, name, default=None):
    return sample.header.get(name, default)


def compute_delta(previous, current):
    """Compute a stateless Go-contract delta between two samples."""
    previous = _copy_sample(previous)
    current = _copy_sample(current)

    if (_header(current, "metrics_disabled", False) or
            _header(previous, "metrics_disabled", False) or
            not _counters_available(current.counters) or
            not _counters_available(previous.counters)):
        return DeltaResult(reset_reason=DELTA_METRICS_UNAVAILABLE)

    previous_instance = _header(previous, "instance_id", "") or ""
    current_instance = _header(current, "instance_id", "") or ""
    if not previous_instance or previous_instance != current_instance:
        return DeltaResult(reset_reason=DELTA_INSTANCE_CHANGED)

    if (_as_int(_header(previous, "collection_generation")) !=
            _as_int(_header(current, "collection_generation"))):
        return DeltaResult(reset_reason=DELTA_COLLECTION_CHANGED)

    if (_as_int(_header(current, "snapshot_sequence")) <=
            _as_int(_header(previous, "snapshot_sequence"))):
        return DeltaResult(reset_reason=DELTA_SEQUENCE_REGRESSED)

    if (_as_int(_header(current, "uptime_ms")) <
            _as_int(_header(previous, "uptime_ms"))):
        return DeltaResult(reset_reason=DELTA_UPTIME_REGRESSED)

    interval_ms = (_as_int(_header(current, "captured_at_unix_ms")) -
                   _as_int(_header(previous, "captured_at_unix_ms")))
    if interval_ms <= 0:
        return DeltaResult(reset_reason=DELTA_CLOCK_REGRESSED)

    if len(current.counters) != len(previous.counters):
        return DeltaResult(reset_reason=DELTA_COUNTER_SET_CHANGED)

    deltas = {}
    rates = {}
    for name, current_value in current.counters.items():
        if name not in previous.counters:
            return DeltaResult(reset_reason=DELTA_COUNTER_SET_CHANGED)
        previous_value = previous.counters[name]
        if current_value < previous_value:
            return DeltaResult(reset_reason=DELTA_COUNTER_REGRESSED)
        delta = current_value - previous_value
        deltas[name] = delta
        rates[name] = float(delta) * 1000.0 / float(interval_ms)

    return DeltaResult(valid=True, interval_ms=interval_ms,
                       deltas=deltas, rates_per_second=rates)


class DeltaAdapter(object):
    """Retain one bounded copied baseline for sequential observations."""

    def __init__(self):
        self._lock = threading.Lock()
        self._previous = None

    def observe(self, current):
        """Compute against the previous baseline and always replace it."""
        current = _copy_sample(current)
        with self._lock:
            if (_header(current, "metrics_disabled", False) or
                    not _counters_available(current.counters)):
                self._previous = current
                return DeltaResult(reset_reason=DELTA_METRICS_UNAVAILABLE)
            if self._previous is None:
                self._previous = current
                return DeltaResult(reset_reason=DELTA_INITIAL_BASELINE)

            result = compute_delta(self._previous, current)
            self._previous = current
            return result

    def reset(self):
        """Discard the current baseline."""
        with self._lock:
            self._previous = None
