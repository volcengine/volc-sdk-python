# coding=utf-8
"""Internal mutable stats state for producer and consumer.

Snapshot lifecycle:
- Counters live in a flat list of ints guarded by a small ``_lock`` so compound
  cross-field reads (the snapshot) are consistent; we do NOT rely on the GIL to
  make ``x += 1`` atomic across implementations.
- Counter helpers update a fixed-size bank; they retain no per-event history.
- Lifecycle uses a single ``_lifecycle_lock`` plus a ``_frozen`` flag and a
  ``_final_snapshot`` cache. Once frozen, the same immutable snapshot is
  returned for every subsequent ``get_stats()`` call.
- ``snapshot_sequence`` increments on every live snapshot and stops advancing
  after freeze.
- All time uses the injected clock: monotonic for uptime/ages, wall for capture.

The state objects admit mutations through collection-generation gates. When
metrics are Off, business counter mutations are skipped. The state still
produces a valid Off snapshot with lifecycle information.
"""
from __future__ import absolute_import

import threading
from contextlib import contextmanager

from volcengine.tls._stats.clock import default_clock
from volcengine.tls._stats.histogram import FixedHistogram, FAST_BOUNDS_MS, SLOW_BOUNDS_MS
from volcengine.tls._stats.common import saturating_u64
from volcengine.tls.stats import constants as _c


class _CounterBank(object):
    """Fixed-size int counter bank with a dedicated lock.

    Indices are assigned by the owning state class. All mutations take the lock;
    the lock scope is a single arithmetic op, so contention is negligible and no
    business logic ever runs under it.
    """

    __slots__ = ("_values", "_lock")

    def __init__(self, size):
        self._values = [0] * size
        self._lock = threading.Lock()

    def add(self, idx, delta):
        with self._lock:
            self._values[idx] += delta

    def add_two(self, idx_a, delta_a, idx_b, delta_b):
        """Atomically adjust two related counters."""
        with self._lock:
            self._values[idx_a] += delta_a
            self._values[idx_b] += delta_b

    def inc(self, idx):
        with self._lock:
            self._values[idx] += 1

    def dec(self, idx):
        with self._lock:
            self._values[idx] -= 1

    def set_max(self, idx, value):
        with self._lock:
            if value > self._values[idx]:
                self._values[idx] = value

    def set(self, idx, value):
        with self._lock:
            self._values[idx] = value

    def inc_with_max(self, idx, max_idx):
        """Atomically ++value[idx] and bump value[max_idx] to the new high."""
        with self._lock:
            self._values[idx] += 1
            cur = self._values[idx]
            if cur > self._values[max_idx]:
                self._values[max_idx] = cur

    def add_with_max(self, idx, delta, max_idx):
        """Atomically value[idx] += delta and bump value[max_idx] to the new high."""
        with self._lock:
            self._values[idx] += delta
            cur = self._values[idx]
            if cur > self._values[max_idx]:
                self._values[max_idx] = cur

    def sub_nonneg(self, idx, delta):
        """Atomically subtract delta from value[idx], clamped at zero."""
        with self._lock:
            cur = self._values[idx]
            self._values[idx] = max(0, cur - delta)

    def get_two(self, idx_a, idx_b):
        """Atomically read two values under one lock (consistent pair)."""
        with self._lock:
            return self._values[idx_a], self._values[idx_b]

    def dec_nonneg(self, idx):
        """Atomically decrement but never below zero."""
        with self._lock:
            if self._values[idx] > 0:
                self._values[idx] -= 1

    def dec_two_nonneg(self, idx_a, idx_b):
        """Atomically decrement two related counters, clamped at zero."""
        with self._lock:
            if self._values[idx_a] > 0:
                self._values[idx_a] -= 1
            if self._values[idx_b] > 0:
                self._values[idx_b] -= 1

    def get(self, idx):
        with self._lock:
            return self._values[idx]

    def snapshot_values(self):
        with self._lock:
            return list(self._values)


class _BaseStatsState(object):
    """Shared lifecycle + sequence + freeze machinery."""

    __slots__ = (
        "metrics_level", "instance_id", "sdk_version",
        "_clock", "_start_mono_ns", "_lifecycle_lock", "_frozen",
        "_final_snapshot", "_seq", "_seq_lock", "_close_wall_ms",
        "_close_mono_ns", "_started", "_closing", "_closed", "_failed",
        "_state_lock", "_last_error_category", "_last_error_mono_ns",
        "collection_generation", "collection_started_at_unix_ms",
        "_detail_generation", "_histogram_names", "_hist",
    )

    def __init__(self, metrics_level, instance_id, sdk_version, clock=None):
        self.metrics_level = _c.normalize_metrics_level(metrics_level)
        self.instance_id = instance_id
        self.sdk_version = sdk_version
        self._clock = clock or default_clock
        self._start_mono_ns = self._clock.monotonic_ns()
        self._lifecycle_lock = threading.RLock()
        self._frozen = False
        self._final_snapshot = None
        self._seq = 0
        self._seq_lock = threading.Lock()
        self._close_wall_ms = None
        self._close_mono_ns = None
        # lifecycle flags
        self._state_lock = threading.Lock()
        self._started = False
        self._closing = False
        self._closed = False
        self._failed = False
        self._last_error_category = None
        self._last_error_mono_ns = None
        self.collection_generation = 1
        self.collection_started_at_unix_ms = self._clock.wall_ms() if self.enabled else 0
        self._detail_generation = 1
        self._histogram_names = ()
        self._hist = {}

    @property
    def enabled(self):
        """True when any business counter should be maintained."""
        return self.metrics_level != _c.METRICS_LEVEL_OFF and not self._frozen

    @property
    def latency_enabled(self):
        return self.metrics_level == _c.METRICS_LEVEL_DETAILED and not self._frozen

    def token(self):
        if not self.enabled:
            return 0
        with self._lifecycle_lock:
            return self.collection_generation if self.enabled else 0

    def detail_token(self):
        if not self.latency_enabled:
            return 0
        with self._lifecycle_lock:
            return self._detail_generation if self.latency_enabled else 0

    @contextmanager
    def event(self, token=None):
        """Serialize a bounded observation with collection changes and snapshots.

        The lock must never cover I/O, a user callback or admission waiting.
        A zero token denotes work that began while collection was disabled.
        """
        if not self.enabled:
            yield False
            return
        with self._lifecycle_lock:
            yield self.enabled and (token is None or token == self.collection_generation)

    @contextmanager
    def detail_event(self, token):
        if not self.latency_enabled:
            yield False
            return
        with self._lifecycle_lock:
            yield self.latency_enabled and token != 0 and token == self._detail_generation

    def _reset_collection(self):
        """Component hook: reset observed gauges/ages, never cumulative counters."""
        with self._state_lock:
            self._last_error_category = None
            self._last_error_mono_ns = None

    def set_metrics_level(self, level):
        if level is None:
            raise ValueError("metrics level must be off, core or detailed")
        level = _c.normalize_metrics_level(level)
        with self._lifecycle_lock:
            with self._state_lock:
                if not self._started or self._closing or self._closed or self._failed:
                    raise RuntimeError("metrics level change requires a running component")
            old = self.metrics_level
            if old == level:
                return
            if (old == _c.METRICS_LEVEL_DETAILED) != (level == _c.METRICS_LEVEL_DETAILED):
                self._detail_generation += 1
            if level == _c.METRICS_LEVEL_DETAILED:
                self._init_detailed_histograms()
            self.metrics_level = level
            if old == _c.METRICS_LEVEL_OFF or level == _c.METRICS_LEVEL_OFF:
                self.collection_generation += 1
                self.collection_started_at_unix_ms = self._clock.wall_ms() if self.enabled else 0
                self._reset_collection()

    def resume_for_start(self):
        """Resume only after the caller has joined every previous-generation task."""
        with self._lifecycle_lock:
            reset_collection = self._closed or self._frozen or self._failed
            self._frozen = False
            self._final_snapshot = None
            self._close_wall_ms = None
            self._close_mono_ns = None
            with self._state_lock:
                self._started = self._closing = self._closed = self._failed = False
            if reset_collection:
                self.collection_generation += 1
                self._detail_generation += 1
                self.collection_started_at_unix_ms = self._clock.wall_ms() if self.enabled else 0
                self._reset_collection()

    # ---- lifecycle transitions -------------------------------------------
    def mark_started(self):
        with self._lifecycle_lock:
            with self._state_lock:
                if not self._closed and not self._closing:
                    self._started = True

    def mark_closing(self):
        with self._lifecycle_lock:
            with self._state_lock:
                if not self._closed:
                    self._closing = True

    def mark_failed(self, category=None):
        with self._lifecycle_lock:
            with self._state_lock:
                self._failed = True
                if category is not None:
                    self._last_error_category = category
                    self._last_error_mono_ns = self._clock.monotonic_ns()

    def record_error(self, category):
        """Atomically record a bounded category and its monotonic instant."""
        with self.event() as active:
            if active:
                with self._state_lock:
                    self._last_error_category = category
                    self._last_error_mono_ns = self._clock.monotonic_ns()

    def _current_state(self):
        with self._state_lock:
            if self._closed:
                return _c.STATE_FAILED if self._failed else _c.STATE_CLOSED
            if self._failed:
                return _c.STATE_FAILED
            if self._closing:
                return _c.STATE_CLOSING
            if self._started:
                return _c.STATE_RUNNING
            return _c.STATE_NEW

    def freeze(self):
        """Freeze the final clock and set closed. Idempotent.

        Must be called after background work is settled so the final snapshot is
        stable. Sets close-time clock before marking closed so any concurrent
        get_stats observing closed also sees a valid frozen clock.
        """
        with self._lifecycle_lock:
            if self._frozen:
                return
        prepared = self._prepare_snapshot()
        with self._lifecycle_lock:
            if self._frozen:
                return
            self._close_wall_ms = self._clock.wall_ms()
            self._close_mono_ns = self._clock.monotonic_ns()
            with self._state_lock:
                self._closing = False
                self._closed = True
            # Build the final snapshot before disabling observation hooks.
            self._final_snapshot = self._build_prepared_snapshot(True, prepared)
            self._frozen = True

    def _next_seq(self):
        with self._seq_lock:
            self._seq += 1
            return self._seq

    def _uptime_ms(self):
        end = self._close_mono_ns if self._close_mono_ns is not None else self._clock.monotonic_ns()
        return max(0, (end - self._start_mono_ns) // 1_000_000)

    def _capture_ms(self):
        if self._close_wall_ms is not None:
            return self._close_wall_ms
        return self._clock.wall_ms()

    # ---- public snapshot entrypoint --------------------------------------
    def get_stats(self):
        # Even frozen reads use the lock: Consumer may resume the same state for
        # another lifecycle. A lock-free read could race thaw and return None.
        with self._lifecycle_lock:
            if self._frozen:
                return self._final_snapshot
        prepared = self._prepare_snapshot()
        with self._lifecycle_lock:
            if self._frozen:
                return self._final_snapshot
            return self._build_prepared_snapshot(False, prepared)

    def _prepare_snapshot(self):
        """Read external owners outside the collection lock."""
        return ()

    def _build_prepared_snapshot(self, is_final, prepared):
        del prepared
        return self._build_snapshot(is_final)

    def _build_snapshot(self, is_final):
        raise NotImplementedError

    def _base_kwargs(self, is_final, seq_override=None, include_error_time=False):
        # Lifecycle state and last-error fields form one logical observation.
        # Capture them under one lock so snapshots cannot publish a new category
        # with a stale or missing age instant.
        with self._state_lock:
            if self._closed:
                state = _c.STATE_FAILED if self._failed else _c.STATE_CLOSED
            elif self._failed:
                state = _c.STATE_FAILED
            elif self._closing:
                state = _c.STATE_CLOSING
            elif self._started:
                state = _c.STATE_RUNNING
            else:
                state = _c.STATE_NEW
            last_error_category = self._last_error_category
            last_error_mono_ns = self._last_error_mono_ns
        consistency = _c.CONSISTENCY_FINAL if (is_final or state == _c.STATE_CLOSED) \
            else _c.CONSISTENCY_NON_FINAL
        seq = seq_override if seq_override is not None else self._next_seq()
        result = dict(
            schema_version=_c.SCHEMA_VERSION,
            instance_id=self.instance_id,
            captured_at_unix_ms=self._capture_ms(),
            sdk_name=_c.SDK_NAME,
            sdk_language=_c.SDK_LANGUAGE,
            sdk_version=self.sdk_version,
            state=state,
            consistency=consistency,
            metrics_level=self.metrics_level,
            metrics_disabled=self.metrics_level == _c.METRICS_LEVEL_OFF,
            uptime_ms=self._uptime_ms(),
            snapshot_sequence=seq,
            critical_flags=(),
            counter_saturated=False,
            collection_generation=self.collection_generation,
            collection_started_at_unix_ms=self.collection_started_at_unix_ms,
        )
        if last_error_category is not None:
            result["last_error_category"] = last_error_category
        if include_error_time:
            result["_last_error_mono_ns"] = last_error_mono_ns
        return result

    def _make_histograms(self, names):
        self._histogram_names = tuple(names)
        return self._create_histograms() if self.latency_enabled else {}

    def _create_histograms(self):
        slow = ("batch_delivery_duration", "callback_duration", "process_duration",
                "checkpoint_call_duration")
        return {name: FixedHistogram(SLOW_BOUNDS_MS if name in slow else FAST_BOUNDS_MS)
                for name in self._histogram_names}

    def _init_detailed_histograms(self):
        if not self._hist:
            self._hist = self._create_histograms()
