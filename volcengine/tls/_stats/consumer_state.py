# coding=utf-8
"""Private, bounded Consumer health state.

The state deliberately keeps no per-shard checkpoint map.  The checkpoint
manager owns that map and binds a small provider which supplies its current
size and oldest age.  Every observation carries the collection generation it
started in, so a completion from an old generation cannot update the new
snapshot after an Off switch or restart.
"""
from __future__ import absolute_import

import threading

from volcengine.tls._stats.common import QueueStats, WorkerRoleStats, saturating_u64
from volcengine.tls._stats.counters import CONSUMER_COUNTER_KEYS
from volcengine.tls._stats.state import _BaseStatsState, _CounterBank
from volcengine.tls.stats import constants as _c
from volcengine.tls.stats.snapshot import SnapshotValue


_IDX = {key: index for index, key in enumerate(CONSUMER_COUNTER_KEYS)}
_N = len(CONSUMER_COUNTER_KEYS)
_HISTS = ("fetch_call_duration", "dispatch_delay", "process_duration",
          "checkpoint_call_duration")


class _HeldToken(object):
    """Once-release guard carrying the generation which acquired the batch."""

    __slots__ = ("_released", "_held", "_ready", "_lock", "_generation",
                 "logs", "groups")

    def __init__(self, generation, logs=0, groups=0):
        self._released = False
        self._held = True
        self._ready = True
        self._lock = threading.Lock()
        self._generation = int(generation or 0)
        self.logs = int(logs or 0)
        self.groups = int(groups or 0)


class ConsumerStatsState(_BaseStatsState):
    __slots__ = (
        "_bank", "_main_running",
        "_heartbeat_running", "_checkpoint_running", "_shard_tasks_running",
        "_role_lock",
        "_checkpoint_provider", "_assignment_provider", "_checkpoint_count",
        "_checkpoint_oldest_age_ms", "_checkpoint_hwm", "_last_success_mono_ns",
        "_age_lock",
    )

    def __init__(self, metrics_level, instance_id, sdk_version,
                 clock=None):
        super(ConsumerStatsState, self).__init__(
            metrics_level, instance_id, sdk_version, clock)
        self._bank = _CounterBank(_N)
        self._hist = self._make_histograms(_HISTS)
        self._main_running = 0
        self._heartbeat_running = 0
        self._checkpoint_running = 0
        self._shard_tasks_running = 0
        self._role_lock = threading.Lock()
        self._checkpoint_provider = None
        self._assignment_provider = None
        self._checkpoint_count = 0
        self._checkpoint_oldest_age_ms = None
        self._checkpoint_hwm = 0
        self._last_success_mono_ns = None
        self._age_lock = threading.Lock()

    # ---- generation helpers ---------------------------------------------
    @staticmethod
    def _token_generation(token):
        if isinstance(token, _HeldToken):
            return token._generation
        if token is None:
            return None
        try:
            return int(token)
        except (TypeError, ValueError):
            return 0

    def _event_generation(self, token):
        generation = self._token_generation(token)
        return self.token() if generation is None else generation

    # ---- collection reset / providers ----------------------------------
    def _reset_collection(self):
        super(ConsumerStatsState, self)._reset_collection()
        # Cumulative counters intentionally survive a level boundary.  Gauges
        # and lifetime watermarks describe only the newly enabled collection.
        for key in (
                "assigned_shards", "held_batch_references", "ready_to_process",
                "fetch_in_flight", "process_in_flight",
                "checkpoint_flush_in_flight", "shard_tasks_in_flight",
                "shard_tasks_in_flight_max"):
            self._bank.set(_IDX[key], 0)
        with self._role_lock:
            self._shard_tasks_running = 0
        with self._age_lock:
            self._last_success_mono_ns = None
        self._checkpoint_count = 0
        self._checkpoint_oldest_age_ms = None
        self._checkpoint_hwm = 0

    def bind_checkpoint_provider(self, provider=None, assignment_provider=None):
        """Bind real checkpoint/assignment owners without copying their maps.

        ``provider`` may return an integer count, ``(count, oldest_age_ms)``,
        or a QueueStats value.  The callback is invoked only during a bounded
        snapshot or boundary update outside the collection lock; it must not
        perform network I/O. Its values have weak consistency with counters.
        """
        self._checkpoint_provider = provider
        self._assignment_provider = assignment_provider

    # A plural alias makes the intentionally small integration hook explicit.
    bind_checkpoint_providers = bind_checkpoint_provider

    def _checkpoint_value(self):
        provider = self._checkpoint_provider
        if provider is None:
            return self._checkpoint_count, self._checkpoint_oldest_age_ms
        try:
            value = provider()
            if isinstance(value, QueueStats):
                return value.current_items, value.oldest_age_ms
            if isinstance(value, (tuple, list)):
                if not value:
                    return 0, None
                return max(0, int(value[0] or 0)), value[1] if len(value) > 1 else None
            if isinstance(value, dict):
                return max(0, int(value.get("current_items", 0) or 0)), value.get("oldest_age_ms")
            return max(0, int(value or 0)), None
        except Exception:
            return self._checkpoint_count, self._checkpoint_oldest_age_ms

    def _assignment_count(self, fallback):
        provider = self._assignment_provider
        if provider is None:
            return max(0, int(fallback))
        try:
            return max(0, int(provider() or 0))
        except Exception:
            return max(0, int(fallback))

    # ---- generic bounded counter helpers -------------------------------
    def add(self, key, delta, token=None):
        with self.event(self._event_generation(token)) as active:
            if active:
                self._bank.add(_IDX[key], delta)

    def inc(self, key, token=None):
        with self.event(self._event_generation(token)) as active:
            if active:
                self._bank.inc(_IDX[key])

    def set_assigned_shards(self, n, token=None):
        with self.event(self._event_generation(token)) as active:
            if active:
                self._bank.set(_IDX["assigned_shards"], max(0, int(n)))

    def on_rebalance(self, token=None):
        self.inc("rebalance_events", token=token)

    def on_backoff(self, token=None):
        self.inc("backoff_events", token=token)

    # ---- fetch ----------------------------------------------------------
    def on_fetch_start(self, token=None):
        with self.event(self._event_generation(token)) as active:
            if active:
                self._bank.inc(_IDX["fetch_in_flight"])
        return active

    def on_fetch_end(self, success=True, log_groups=0, logs=0, token=None):
        with self.event(self._event_generation(token)) as active:
            if not active:
                return False
            self._bank.dec_nonneg(_IDX["fetch_in_flight"])
            self._bank.inc(_IDX["fetch_calls"])
            if not success:
                self._bank.inc(_IDX["fetch_failures"])
            if log_groups:
                self._bank.add(_IDX["fetched_log_groups"], log_groups)
            if logs:
                self._bank.add(_IDX["fetched_logs"], logs)
            if success:
                self._mark_success_locked()
            return True

    # ---- held batch / process ------------------------------------------
    def acquire_held(self, logs=0, groups=0, token=None):
        generation = self._event_generation(token)
        with self.event(generation) as active:
            if not active:
                return None
            self._bank.add_two(
                _IDX["held_batch_references"], 1,
                _IDX["ready_to_process"], 1)
            return _HeldToken(generation, logs=logs, groups=groups)

    def release_held(self, token):
        if token is None:
            return
        generation = self._event_generation(token)
        # Match on_process_start/end lock ordering: lifecycle event first,
        # then the once-release token.  This prevents revoke/process races
        # from taking the two locks in opposite order.
        with self.event(generation) as active:
            with token._lock:
                if token._released:
                    return
                token._released = True
                if active and token._held:
                    if token._ready:
                        self._bank.dec_two_nonneg(
                            _IDX["held_batch_references"],
                            _IDX["ready_to_process"])
                    else:
                        self._bank.dec_nonneg(_IDX["held_batch_references"])
                token._held = False
                token._ready = False

    def on_process_start(self, token=None, generation=None):
        held = token if isinstance(token, _HeldToken) else None
        event_generation = self._event_generation(
            generation if generation is not None else held)
        with self.event(event_generation) as active:
            if not active:
                return False
            if held is not None:
                with held._lock:
                    if not held._released:
                        # A callback owns the batch while it is in flight;
                        # it is neither held nor ready until completion.  A
                        # retry re-acquires both counters in on_process_end.
                        if held._held:
                            if held._ready:
                                self._bank.dec_two_nonneg(
                                    _IDX["held_batch_references"],
                                    _IDX["ready_to_process"])
                            else:
                                self._bank.dec_nonneg(
                                    _IDX["held_batch_references"])
                        held._held = False
                        held._ready = False
                        # A batch can cross an Off -> Core boundary.  Once a
                        # new generation admits its callback, make the token
                        # releasable by that generation.
                        held._generation = event_generation
            self._bank.inc(_IDX["process_in_flight"])
            return True

    def on_process_end(self, success, token=None, generation=None,
                       logs=None, groups=None):
        held = token if isinstance(token, _HeldToken) else None
        event_generation = self._event_generation(
            generation if generation is not None else held)
        with self.event(event_generation) as active:
            if not active:
                return False
            self._bank.dec_nonneg(_IDX["process_in_flight"])
            # ``process_attempts`` is the completed-call denominator used by
            # the public projection (success = attempts - failures).  The
            # in-flight gauge carries the start-side fact, so an admitted but
            # unfinished callback cannot be reported as a success.
            self._bank.inc(_IDX["process_attempts"])
            if success:
                if logs is None:
                    logs = held.logs if held is not None else 0
                if groups is None:
                    groups = held.groups if held is not None else 0
                self._bank.add(_IDX["processed_success_logs"], int(logs or 0))
                self._bank.add(_IDX["processed_success_groups"], int(groups or 0))
                self._mark_success_locked()
            else:
                self._bank.inc(_IDX["process_failures"])
                if held is not None:
                    with held._lock:
                        if not held._released and not held._held:
                            held._held = True
                            held._ready = True
                            self._bank.add_two(
                                _IDX["held_batch_references"], 1,
                                _IDX["ready_to_process"], 1)
            return True

    # ---- shard task lifecycle ------------------------------------------
    def on_shard_task_submitted(self, token=None):
        with self.event(self._event_generation(token)) as active:
            if active:
                self._bank.inc(_IDX["shard_tasks_submitted"])
                self._bank.inc_with_max(_IDX["shard_tasks_in_flight"],
                                        _IDX["shard_tasks_in_flight_max"])

    def on_shard_task_started(self, token=None):
        with self.event(self._event_generation(token)) as active:
            if active:
                self._bank.inc(_IDX["shard_tasks_started"])
                with self._role_lock:
                    self._shard_tasks_running += 1

    def on_shard_task_done(self, token=None):
        with self.event(self._event_generation(token)) as active:
            if active:
                self._bank.dec_nonneg(_IDX["shard_tasks_in_flight"])
                self._bank.inc(_IDX["shard_tasks_completed"])
                with self._role_lock:
                    if self._shard_tasks_running > 0:
                        self._shard_tasks_running -= 1

    def on_shard_task_start_failed(self, token=None):
        with self.event(self._event_generation(token)) as active:
            if active:
                self._bank.dec_nonneg(_IDX["shard_tasks_submitted"])
                self._bank.dec_nonneg(_IDX["shard_tasks_in_flight"])
                self._bank.inc(_IDX["shard_task_errors"])

    # ---- heartbeat / checkpoint ----------------------------------------
    def on_heartbeat(self, success, token=None):
        with self.event(self._event_generation(token)) as active:
            if not active:
                return False
            self._bank.inc(_IDX["heartbeat_calls"])
            if not success:
                self._bank.inc(_IDX["heartbeat_failures"])
            else:
                self._mark_success_locked()
            return True

    def on_checkpoint_call(self, success, token=None):
        with self.event(self._event_generation(token)) as active:
            if not active:
                return False
            self._bank.inc(_IDX["checkpoint_calls"])
            if not success:
                self._bank.inc(_IDX["checkpoint_failures"])
            else:
                self._mark_success_locked()
            return True

    def on_checkpoint_flush_start(self, token=None):
        with self.event(self._event_generation(token)) as active:
            if active:
                self._bank.inc(_IDX["checkpoint_flush_in_flight"])
        return active

    def on_checkpoint_flush_end(self, token=None):
        with self.event(self._event_generation(token)) as active:
            if active:
                self._bank.dec_nonneg(_IDX["checkpoint_flush_in_flight"])
        return active

    def checkpoint_add(self, _shard_key=None, token=None):
        generation = self._event_generation(token)
        if not self.enabled:
            return
        current, oldest = self._checkpoint_value()
        with self.event(generation) as active:
            if not active:
                return
            if self._checkpoint_provider is None:
                current = max(self._checkpoint_count + 1, current)
            self._checkpoint_count = current
            self._checkpoint_oldest_age_ms = oldest
            if current > self._checkpoint_hwm:
                self._checkpoint_hwm = current

    def checkpoint_clear(self, _shard_key=None, token=None):
        generation = self._event_generation(token)
        if not self.enabled:
            return
        value = self._checkpoint_value()
        with self.event(generation) as active:
            if active:
                self._checkpoint_count, self._checkpoint_oldest_age_ms = value

    # ---- errors / ages --------------------------------------------------
    def _mark_success_locked(self):
        # Called while the collection event is admitted.  The age lock keeps
        # this scalar independent from the fixed counter-bank lock.
        with self._age_lock:
            self._last_success_mono_ns = self._clock.monotonic_ns()

    def record_error(self, category, token=None):
        """Record a low-cardinality error, including when counters are Off.

        A zero token is the current disabled collection; a nonzero token must
        still match the active generation so late old work is ignored.
        """
        generation = self._event_generation(token)
        with self.event(generation) as active:
            if not active:
                return False
            with self._state_lock:
                self._last_error_category = category
                self._last_error_mono_ns = self._clock.monotonic_ns()
            return True

    # ---- checkpoint/worker roles ---------------------------------------
    def _checkpoint_snapshot(self, value):
        current, oldest_age_ms = value
        if oldest_age_ms is None:
            oldest_age_ms = self._checkpoint_oldest_age_ms
        hwm = max(self._checkpoint_hwm, current)
        return QueueStats(current_items=current, bounded=False,
                          high_watermark_items=hwm,
                          oldest_age_ms=oldest_age_ms), oldest_age_ms

    def set_main_running(self, n):
        with self._role_lock:
            self._main_running = max(0, int(n))

    def set_heartbeat_running(self, n):
        with self._role_lock:
            self._heartbeat_running = max(0, int(n))

    def set_checkpoint_running(self, n):
        with self._role_lock:
            self._checkpoint_running = max(0, int(n))

    # ---- histograms -----------------------------------------------------
    def observe_ns(self, name, value_ns, detail_token=None):
        if detail_token is None:
            detail_token = self.detail_token()
        with self.detail_event(detail_token) as active:
            if active:
                histogram = self._hist.get(name)
                if histogram is not None:
                    histogram.record_ns(value_ns)

    def observe_ms(self, name, value_ms, detail_token=None):
        if detail_token is None:
            detail_token = self.detail_token()
        with self.detail_event(detail_token) as active:
            if active:
                histogram = self._hist.get(name)
                if histogram is not None:
                    histogram.record_ms(value_ms)

    # ---- snapshot -------------------------------------------------------
    def _prepare_snapshot(self):
        generation = self.collection_generation
        checkpoint = (self._checkpoint_value() if self.enabled else
                      (self._checkpoint_count, self._checkpoint_oldest_age_ms))
        assigned = self._assignment_count(self._bank.get(_IDX["assigned_shards"]))
        return generation, checkpoint, assigned

    def _build_prepared_snapshot(self, is_final, prepared):
        if prepared[0] != self.collection_generation:
            prepared = None
        return self._build_snapshot(is_final, prepared)

    def _build_snapshot(self, is_final, prepared=None):
        base = self._base_kwargs(is_final, include_error_time=True)
        base["component_type"] = _c.COMPONENT_CONSUMER
        last_error_mono_ns = base.pop("_last_error_mono_ns")
        if self.metrics_level == _c.METRICS_LEVEL_OFF:
            counters = None
            checkpoint_pending = checkpoint_oldest = None
            saturated = False
            last_success_age = last_error_age = None
        else:
            values = self._bank.snapshot_values()
            counters, saturated = self._derive_counters(values)
            checkpoint_value = (prepared[1] if prepared is not None else
                                (self._checkpoint_count, self._checkpoint_oldest_age_ms))
            checkpoint_pending, checkpoint_oldest = self._checkpoint_snapshot(checkpoint_value)
            end = (self._close_mono_ns if self._close_mono_ns is not None
                    else self._clock.monotonic_ns())
            with self._age_lock:
                success_ns = self._last_success_mono_ns
            last_success_age = (max(0, (end - success_ns) // 1_000_000)
                                if success_ns is not None else None)
            last_error_age = (max(0, (end - last_error_mono_ns) // 1_000_000)
                              if last_error_mono_ns is not None else None)
        base["counter_saturated"] = saturated
        # Lifecycle roles are cheap, bounded facts and remain available while
        # counters are Off; projection can still omit operational sections.
        roles = self._worker_roles_snapshot(
            self._bank.snapshot_values() if self.metrics_level != _c.METRICS_LEVEL_OFF else None,
            prepared[2] if prepared is not None else None)
        histograms = ({name: histogram.snapshot() for name, histogram in self._hist.items()}
                      if self.latency_enabled else {})
        if counters is not None:
            base.update(counters)
            if checkpoint_pending is not None:
                base["checkpoint_pending"] = checkpoint_pending.to_dict()
            if checkpoint_oldest is not None:
                base["checkpoint_oldest_age_ms"] = checkpoint_oldest
            if last_success_age is not None:
                base["last_success_age_ms"] = last_success_age
            if last_error_age is not None:
                base["last_error_age_ms"] = last_error_age
        if roles:
            base["worker_roles"] = [role.to_dict() for role in roles]
        for name, histogram in histograms.items():
            base[name + "_ms"] = histogram.to_dict()
        return SnapshotValue(base)

    def _derive_counters(self, values):
        result = {}
        saturated = False
        for key in CONSUMER_COUNTER_KEYS:
            value = max(0, values[_IDX[key]])
            result[key], was_saturated = saturating_u64(value)
            saturated = saturated or was_saturated
        return result, saturated

    def _worker_roles_snapshot(self, values, assigned=None):
        with self._role_lock:
            main, heartbeat, checkpoint, shard_running = (
                self._main_running, self._heartbeat_running,
                self._checkpoint_running, self._shard_tasks_running)
        if assigned is None:
            assigned = values[_IDX["assigned_shards"]] if values is not None else 0
        if values is None:
            shard_running = shard_in_flight = 0
        else:
            shard_in_flight = max(0, values[_IDX["shard_tasks_in_flight"]])
        return (
            WorkerRoleStats("main_loop", expected=1, running=main, in_flight=0),
            WorkerRoleStats("heartbeat", expected=1, running=heartbeat, in_flight=0),
            WorkerRoleStats("checkpoint", expected=1, running=checkpoint, in_flight=0),
            WorkerRoleStats("shard_worker", expected=assigned,
                            running=shard_running, in_flight=shard_in_flight),
        )
