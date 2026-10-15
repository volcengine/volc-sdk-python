# coding=utf-8
"""Stable public constants for TLS SDK health stats.

Plain module-level string/int constants (Python 3.7 friendly, no Enum needed on
the hot path). Values are part of the cross-language schema and must stay in
sync with the Go/Java/C++ SDKs.
"""
from __future__ import absolute_import

__all__ = [
    "SCHEMA_VERSION",
    "SDK_NAME", "SDK_LANGUAGE",
    "COMPONENT_PRODUCER", "COMPONENT_CONSUMER",
    "METRICS_LEVEL_OFF", "METRICS_LEVEL_CORE", "METRICS_LEVEL_DETAILED",
    "METRICS_LEVELS",
    "STATE_NEW", "STATE_RUNNING", "STATE_CLOSING", "STATE_CLOSED", "STATE_FAILED",
    "CONSISTENCY_NON_FINAL", "CONSISTENCY_FINAL",
    "normalize_metrics_level",
]

SCHEMA_VERSION = 2

SDK_NAME = "volc-sdk-python"
SDK_LANGUAGE = "python"

# component_type
COMPONENT_PRODUCER = "producer"
COMPONENT_CONSUMER = "consumer"

# metrics_level
METRICS_LEVEL_OFF = "off"
METRICS_LEVEL_CORE = "core"
METRICS_LEVEL_DETAILED = "detailed"
METRICS_LEVELS = (METRICS_LEVEL_OFF, METRICS_LEVEL_CORE, METRICS_LEVEL_DETAILED)

# lifecycle state
STATE_NEW = "new"
STATE_RUNNING = "running"
STATE_CLOSING = "closing"
STATE_CLOSED = "closed"
STATE_FAILED = "failed"

# consistency
CONSISTENCY_NON_FINAL = "weak"
CONSISTENCY_FINAL = "final"


def normalize_metrics_level(value):
    """Default None to off; normalize known levels and reject unknown values."""
    if value is None:
        return METRICS_LEVEL_OFF
    v = str(value).strip().lower()
    if v in METRICS_LEVELS:
        return v
    raise ValueError(
        "invalid metrics_level {!r}; expected one of {}".format(value, METRICS_LEVELS)
    )
