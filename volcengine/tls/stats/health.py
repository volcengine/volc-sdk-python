# coding=utf-8
"""Pure health evaluator for component-neutral observability snapshots."""
from __future__ import absolute_import

import math
from collections.abc import Mapping

from volcengine.tls.stats import constants as _c
from volcengine.tls.stats._immutable import _ImmutableSnapshot

__all__ = [
    "HealthPolicy", "HealthResult", "evaluate_health",
    "HEALTH_UNKNOWN", "HEALTH_HEALTHY", "HEALTH_DEGRADED",
    "HEALTH_UNHEALTHY",
]


HEALTH_UNKNOWN = "unknown"
HEALTH_HEALTHY = "healthy"
HEALTH_DEGRADED = "degraded"
HEALTH_UNHEALTHY = "unhealthy"


def _normalize_threshold(value, fallback=0.80):
    if value is None:
        return fallback
    try:
        value = float(value)
    except (TypeError, ValueError, OverflowError):
        return fallback
    if not math.isfinite(value) or value <= 0.0 or value > 1.0:
        return fallback
    return value


class HealthPolicy(_ImmutableSnapshot):
    """Thresholds used by :func:`evaluate_health`.

    The evaluator applies the same fallback rule as Go for non-positive or
    greater-than-one values.  Keeping the supplied values here makes the
    policy object a transparent, immutable configuration value.
    """

    __slots__ = ("_queue_pressure_degraded", "_memory_pressure_degraded")

    def __init__(self, queue_pressure_degraded=0.80,
                 memory_pressure_degraded=0.80):
        self._queue_pressure_degraded = (
            None if queue_pressure_degraded is None
            else float(queue_pressure_degraded))
        self._memory_pressure_degraded = (
            None if memory_pressure_degraded is None
            else float(memory_pressure_degraded))

    @property
    def queue_pressure_degraded(self):
        return self._queue_pressure_degraded

    @property
    def memory_pressure_degraded(self):
        return self._memory_pressure_degraded


class HealthResult(_ImmutableSnapshot):
    """Immutable health verdict and its contract reason codes."""

    __slots__ = (
        "_status", "_reason_codes", "_evaluated_at_unix_ms",
        "_insufficient_data",
    )

    def __init__(self, status, reason_codes=(), evaluated_at_unix_ms=0,
                 insufficient_data=False):
        self._status = status
        self._reason_codes = tuple(reason_codes)
        self._evaluated_at_unix_ms = int(evaluated_at_unix_ms)
        self._insufficient_data = bool(insufficient_data)

    @property
    def status(self):
        return self._status

    @property
    def reason_codes(self):
        return self._reason_codes

    @property
    def evaluated_at_unix_ms(self):
        return self._evaluated_at_unix_ms

    @property
    def insufficient_data(self):
        return self._insufficient_data

    def to_dict(self):
        return {
            "status": self._status,
            "reason_codes": list(self._reason_codes),
            "evaluated_at_unix_ms": self._evaluated_at_unix_ms,
            "insufficient_data": self._insufficient_data,
        }

    def __repr__(self):
        return ("HealthResult(status={!r}, reason_codes={!r}, "
                "insufficient_data={!r})".format(
                    self._status, self._reason_codes,
                    self._insufficient_data))


def _snapshot_dict(snapshot):
    if snapshot is None:
        return None
    if isinstance(snapshot, Mapping):
        return dict(snapshot)
    to_dict = getattr(snapshot, "to_dict", None)
    if to_dict is None or not callable(to_dict):
        raise TypeError("snapshot must be a mapping or expose to_dict()")
    value = to_dict()
    if not isinstance(value, Mapping):
        raise TypeError("snapshot.to_dict() must return a mapping")
    return dict(value)


def _header(data):
    nested = data.get("header")
    if isinstance(nested, Mapping):
        # The Go JSON shape embeds header fields at the top level, while a
        # caller may keep a nested header.  Top-level fields take precedence.
        result = dict(nested)
        result.update(data)
        return result
    return data


def _value(data, key, default=None, aliases=()):
    if key in data:
        return data[key]
    for alias in aliases:
        if alias in data:
            return data[alias]
    return default


def _int_value(value, default=0):
    if value is None:
        return default
    return int(value)


def _signals(data):
    health = data.get("health")
    if not isinstance(health, Mapping):
        return None
    signals = health.get("signals")
    return signals if isinstance(signals, Mapping) else None


def _unknown(evaluated_at, reason):
    return HealthResult(HEALTH_UNKNOWN, (reason,), evaluated_at, True)


def evaluate_health(previous, current, policy=None):
    """Evaluate one current snapshot against the preceding snapshot.

    The order and reason precedence intentionally mirror Go's
    ``EvaluateHealth``.  No lifecycle or pressure inference is made when the
    required baseline/signals are unavailable.
    """
    current_data = _snapshot_dict(current)
    if current_data is None:
        raise TypeError("current snapshot is required")
    current_header = _header(current_data)
    evaluated_at = _int_value(
        _value(current_header, "captured_at_unix_ms"), 0)

    current_disabled = bool(_value(current_header, "metrics_disabled", False))
    lifecycle = _value(current_header, "lifecycle_state", None,
                       aliases=("state",))
    if current_disabled:
        return _unknown(evaluated_at, "metrics_disabled")
    if lifecycle in (_c.STATE_NEW, _c.STATE_CLOSING, _c.STATE_CLOSED):
        return _unknown(evaluated_at, "lifecycle_not_running")

    previous_data = _snapshot_dict(previous)
    if previous_data is None:
        return _unknown(evaluated_at, "insufficient_data")
    previous_header = _header(previous_data)

    previous_instance = _value(previous_header, "instance_id", "") or ""
    current_instance = _value(current_header, "instance_id", "") or ""
    if not previous_instance:
        return _unknown(evaluated_at, "insufficient_data")
    if bool(_value(previous_header, "metrics_disabled", False)):
        return _unknown(evaluated_at, "metrics_disabled")
    if previous_instance != current_instance:
        return _unknown(evaluated_at, "instance_changed")
    if (_int_value(_value(previous_header, "collection_generation"), 0) !=
            _int_value(_value(current_header, "collection_generation"), 0)):
        return _unknown(evaluated_at, "collection_changed")

    if lifecycle == _c.STATE_FAILED:
        return HealthResult(HEALTH_UNHEALTHY, ("lifecycle_failed",),
                            evaluated_at, False)
    if lifecycle != _c.STATE_RUNNING:
        return _unknown(evaluated_at, "lifecycle_not_running")

    signals = _signals(current_data)
    if signals is None:
        return _unknown(evaluated_at, "insufficient_data")

    critical_flags = signals.get("critical_flags") or ()
    if len(critical_flags) > 0:
        return HealthResult(HEALTH_UNHEALTHY, ("critical_flag",),
                            evaluated_at, False)

    worker_summary = signals.get("worker_summary")
    if not isinstance(worker_summary, Mapping):
        worker_summary = {}
    if _int_value(worker_summary.get("missing_critical_roles"), 0) > 0:
        return HealthResult(HEALTH_UNHEALTHY, ("worker_missing",),
                            evaluated_at, False)

    policy = policy if policy is not None else HealthPolicy()
    queue_threshold = _normalize_threshold(policy.queue_pressure_degraded)
    memory_threshold = _normalize_threshold(policy.memory_pressure_degraded)
    reasons = []
    status = HEALTH_HEALTHY

    queue_pressure = signals.get("queue_pressure")
    if (queue_pressure is not None and
            float(queue_pressure) >= queue_threshold):
        status = HEALTH_DEGRADED
        reasons.append("queue_pressure")

    # The snapshot supplies effective pressure across the enforced memory limits.
    memory_pressure = signals.get("memory_pressure")
    if (memory_pressure is not None and
            float(memory_pressure) >= memory_threshold):
        status = HEALTH_DEGRADED
        reasons.append("memory_pressure")

    return HealthResult(status, tuple(reasons), evaluated_at, False)
