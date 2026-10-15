# coding=utf-8
"""Internal mutable Producer measurements.

Instrumentation methods are called from TLSProducer's hot/terminal paths. Each
mutation is a single locked arithmetic op on a fixed counter bank. Counters
remain cumulative across a Core/Detailed change, while owned work and the
operational gauges belong to the active collection generation. This prevents an
old asynchronous completion from being attributed to a later Off -> On window.
"""
from __future__ import absolute_import

import threading

from volcengine.tls._stats.state import _BaseStatsState, _CounterBank
from volcengine.tls._stats.common import (
    MemoryStats, QueueStats, WorkerRoleStats, saturating_u64,
)
from volcengine.tls._stats.counters import PRODUCER_COUNTER_KEYS
from volcengine.tls.stats import constants as _c
from volcengine.tls.stats.snapshot import SnapshotValue

# Fixed indexes for the internal counter bank.
_IDX = {k: i for i, k in enumerate(PRODUCER_COUNTER_KEYS)}
_N = len(PRODUCER_COUNTER_KEYS)

_HISTS = ("batch_queue_delay", "send_call_duration", "batch_delivery_duration",
          "callback_duration")

# Reason -> counter-key maps hoisted to module scope (no per-call dict alloc).
_REJECT_KEY = {
    "invalid": "rejected_invalid", "memory": "rejected_memory",
    "closed": "rejected_closed", "circuit": "rejected_circuit",
    "internal": "rejected_internal",
}
_DROP_KEY = {
    "force_close": ("dropped_force_close_logs", "dropped_force_close_groups"),
    "memory_evict": ("dropped_memory_evict_logs", "dropped_memory_evict_groups"),
    "ttl": ("dropped_ttl_expired_logs", "dropped_ttl_expired_groups"),
    "internal": ("dropped_internal_logs", "dropped_internal_groups"),
}


class ProducerStatsState(_BaseStatsState):
    __slots__ = ("_bank", "_owned", "_memory_limiter", "_max_sender_count",
                 "_dispatcher_running", "_mover_running",
                 "_role_lock", "_send_queue_provider", "_retry_queue_provider",
                 "_ingress_queue_provider", "_last_success_mono_ns",
                 "_age_lock", "_qgauge", "_pending_lock", "_pending_tasks")

    def __init__(self, metrics_level, instance_id, sdk_version,
                 memory_limiter=None, max_sender_count=0, clock=None):
        super(ProducerStatsState, self).__init__(
            metrics_level, instance_id, sdk_version, clock)
        self._bank = _CounterBank(_N)
        # Accepted work is cumulative, but the public owned gauge is scoped to
        # one collection generation. A terminal from an older cohort must not
        # reduce or fabricate ownership in a newer one.
        self._owned = _CounterBank(2)  # logs, groups
        self._hist = self._make_histograms(_HISTS)
        self._memory_limiter = memory_limiter
        self._max_sender_count = int(max_sender_count or 0)
        # worker running gauges (tracked even when metrics off is fine; cheap)
        self._dispatcher_running = 0
        self._mover_running = 0
        self._role_lock = threading.Lock()
        # Dedicated O(1) depth gauges for ingress and send logical queues, plus
        # their lifetime high-watermarks. These are SDK-maintained logical task
        # gauges (submit/start), NOT reads of ThreadPoolExecutor internals
        # (plan §5, §11.1). Indices: 0 ingress cur, 1 ingress hwm, 2 send cur,
        # 3 send hwm, 4 submitted task cur, 5 task hwm, 6 running task cur,
        # 7 running task hwm, 8 aggregate batches cur, 9 aggregate hwm,
        # 10 callback pending cur, 11 callback pending hwm.
        self._qgauge = _CounterBank(12)
        self._send_queue_provider = None
        self._retry_queue_provider = None
        self._ingress_queue_provider = None
        # last success/error monotonic instants for age fields (Core+).
        self._last_success_mono_ns = None
        self._age_lock = threading.Lock()
        self._pending_lock = threading.Lock()
        self._pending_tasks = 0
        if self._memory_limiter is not None:
            try:
                self._memory_limiter.set_metrics_generation(
                    self.collection_generation, self.enabled)
            except Exception:
                pass

    def _reset_collection(self):
        super(ProducerStatsState, self)._reset_collection()
        # These fields describe work currently resident in the producer, not
        # lifetime activity. The lifecycle lock held by set_metrics_level keeps
        # an old token from racing this reset into the new collection.
        for key in (
                "aggregate_batches", "aggregate_groups",
                "send_calls_in_flight", "send_calls_in_flight_max",
                "callbacks_pending", "callbacks_in_flight"):
            self._bank.set(_IDX[key], 0)
        self._owned = _CounterBank(2)
        self._qgauge = _CounterBank(12)
        with self._age_lock:
            self._last_success_mono_ns = None
        if self._memory_limiter is not None:
            try:
                self._memory_limiter.set_metrics_generation(
                    self.collection_generation, self.enabled)
            except Exception:
                pass

    def bind_queue_providers(self, send=None, retry=None, ingress=None):
        self._send_queue_provider = send
        self._retry_queue_provider = retry
        self._ingress_queue_provider = ingress

    def record_error(self, category, token=None):
        with self.event(token) as active:
            if active:
                with self._state_lock:
                    self._last_error_category = category
                    self._last_error_mono_ns = self._clock.monotonic_ns()

    # ---- ingress / send logical queue gauges (O(1), SDK-maintained) ------
    # _qgauge indices: 0=ingress current, 1=ingress hwm, 2=send current, 3=send hwm.
    def on_ingress_add(self, groups, token=None):
        """Groups accepted into the SDK, owned but not yet sealed into a send
        batch (plan §11.1 'ingress+')."""
        if groups:
            with self.event(token) as active:
                if active:
                    self._qgauge.add_with_max(0, groups, 1)

    def on_ingress_release(self, groups, token=None):
        """Groups leaving ingress as their batch is sealed for send ('ingress-')."""
        if groups:
            with self.event(token) as active:
                if active:
                    self._qgauge.sub_nonneg(0, groups)

    def on_send_enqueue(self, token=None):
        """A batch task was submitted to the sender pool (plan §11.1 'send queue+')."""
        with self.event(token) as active:
            if active:
                self._qgauge.inc_with_max(2, 3)

    def on_send_dequeue(self, token=None):
        """A sender started executing a batch task ('send queue-')."""
        with self.event(token) as active:
            if active:
                self._qgauge.dec_nonneg(2)

    def on_aggregate_queue_add(self, token=None):
        with self.event(token) as active:
            if active:
                self._qgauge.inc_with_max(8, 9)

    def on_aggregate_queue_release(self, groups=0, token=None):
        with self.event(token) as active:
            if active:
                self._qgauge.dec_nonneg(8)
                # aggregate_* is current sealed-batch ownership, not a
                # lifetime counter. One release corresponds to one batch;
                # group ownership is released with its complete batch.
                self._bank.dec_nonneg(_IDX["aggregate_batches"])
                if groups:
                    self._bank.sub_nonneg(_IDX["aggregate_groups"], groups)

    def on_sender_task_submitted(self, token=None):
        with self._pending_lock:
            self._pending_tasks += 1
        with self.event(token) as active:
            if active:
                self._qgauge.inc_with_max(4, 5)

    def on_sender_task_start(self, token=None):
        with self.event(token) as active:
            if active:
                self._qgauge.inc_with_max(6, 7)

    def on_sender_task_end(self, token=None):
        with self.event(token) as active:
            if active:
                self._qgauge.dec_nonneg(6)

    def on_sender_task_done(self, token=None):
        with self._pending_lock:
            if self._pending_tasks > 0:
                self._pending_tasks -= 1
        with self.event(token) as active:
            if active:
                self._qgauge.dec_nonneg(4)

    def sender_tasks_pending(self):
        with self._pending_lock:
            return self._pending_tasks

    # ---- counter mutators (called only when enabled) ---------------------
    def add(self, key, delta, token=None):
        with self.event(token) as active:
            if active:
                self._bank.add(_IDX[key], delta)

    def inc(self, key, token=None):
        with self.event(token) as active:
            if active:
                self._bank.inc(_IDX[key])

    def dec(self, key, token=None):
        with self.event(token) as active:
            if active:
                self._bank.dec(_IDX[key])

    # Accepted / ingress
    def on_accepted(self, logs, groups, token=None):
        with self.event(token) as active:
            if active:
                b = self._bank
                b.add(_IDX["accepted_logs"], logs)
                b.add(_IDX["accepted_groups"], groups)
                self._owned.add(0, logs)
                self._owned.add(1, groups)

    def on_group_accepted(self, logs, new_batch=False, has_callback=False,
                          token=None):
        """Atomically publish one accepted group and its resident ownership."""
        with self.event(token) as active:
            if active:
                b = self._bank
                b.add(_IDX["accepted_logs"], logs)
                b.add(_IDX["accepted_groups"], 1)
                self._owned.add(0, logs)
                self._owned.add(1, 1)
                if new_batch:
                    b.add(_IDX["aggregate_batches"], 1)
                    self._qgauge.inc_with_max(8, 9)
                b.add(_IDX["aggregate_groups"], 1)
                self._qgauge.inc_with_max(0, 1)
                if has_callback:
                    b.add(_IDX["callbacks_pending"], 1)
                    self._qgauge.inc_with_max(10, 11)

    def on_rejected(self, reason, token=None):
        with self.event(token) as active:
            if active:
                key = _REJECT_KEY.get(reason, "rejected_internal")
                self._bank.inc(_IDX[key])

    def on_aggregate(self, batches, groups, token=None):
        with self.event(token) as active:
            if active:
                self._bank.add(_IDX["aggregate_batches"], batches)
                self._bank.add(_IDX["aggregate_groups"], groups)

    # Send calls (in-flight gauge + max watermark)
    def on_send_start(self, token=None):
        with self.event(token) as active:
            if active:
                self._bank.inc_with_max(_IDX["send_calls_in_flight"], _IDX["send_calls_in_flight_max"])
        return active

    def on_send_end(self, success, payload_logs=0, payload_groups=0,
                    error_category=None, token=None):
        with self.event(token) as active:
            if not active:
                return False
            b = self._bank
            b.dec_nonneg(_IDX["send_calls_in_flight"])
            if success:
                b.inc(_IDX["send_calls_success"])
                now = self._clock.monotonic_ns()
                with self._age_lock:
                    self._last_success_mono_ns = now
            else:
                b.inc(_IDX["send_calls_failure"])
                if error_category is not None:
                    with self._state_lock:
                        self._last_error_category = error_category
                        self._last_error_mono_ns = self._clock.monotonic_ns()
            if payload_logs:
                b.add(_IDX["send_call_payload_logs"], payload_logs)
            if payload_groups:
                b.add(_IDX["send_call_payload_groups"], payload_groups)
            return True

    def on_retry_scheduled(self, token=None):
        with self.event(token) as active:
            if active:
                self._bank.inc(_IDX["retries_scheduled"])

    # Terminal batch/log/group settlement (once per batch)
    def on_terminal(self, outcome, logs, groups, token=None):
        with self.event(token) as active:
            if not active:
                return False
            b = self._bank
            if outcome == "success":
                b.add(_IDX["terminal_success_logs"], logs)
                b.add(_IDX["terminal_success_groups"], groups)
                b.inc(_IDX["terminal_success_batches"])
            elif outcome == "failure":
                b.add(_IDX["terminal_failure_logs"], logs)
                b.add(_IDX["terminal_failure_groups"], groups)
                b.inc(_IDX["terminal_failure_batches"])
            elif outcome == "dropped":
                b.add(_IDX["terminal_dropped_logs"], logs)
                b.add(_IDX["terminal_dropped_groups"], groups)
                b.inc(_IDX["terminal_dropped_batches"])
            else:
                return False
            self._owned.sub_nonneg(0, logs)
            self._owned.sub_nonneg(1, groups)
            return True

    def current_owned_counts(self):
        """Return active-collection owned logs/groups for close settlement."""
        return self._owned.get_two(0, 1)

    def on_dropped_reason(self, reason, logs, groups, token=None):
        """Attribute a dropped terminal to a specific reason (partition of
        terminal_dropped_*). Reason in force_close|memory_evict|ttl|internal."""
        with self.event(token) as active:
            if active:
                m = _DROP_KEY.get(reason, _DROP_KEY["internal"])
                self._bank.add(_IDX[m[0]], logs)
                self._bank.add(_IDX[m[1]], groups)

    # Callbacks
    def on_callback_pending(self, n=1, token=None):
        with self.event(token) as active:
            if active:
                self._bank.add(_IDX["callbacks_pending"], n)
                self._qgauge.add_with_max(10, n, 11)

    def on_callback_start(self, token=None):
        with self.event(token) as active:
            if active:
                b = self._bank
                b.dec_nonneg(_IDX["callbacks_pending"])
                b.inc(_IDX["callbacks_in_flight"])
                self._qgauge.dec_nonneg(10)

    def on_callback_cancelled(self, n=1, token=None):
        """Remove callbacks that will not run after an earlier callback error."""
        with self.event(token) as active:
            if active:
                self._bank.sub_nonneg(_IDX["callbacks_pending"], n)
                self._qgauge.sub_nonneg(10, n)

    def on_callback_end(self, success, token=None):
        with self.event(token) as active:
            if active:
                b = self._bank
                b.dec_nonneg(_IDX["callbacks_in_flight"])
                b.inc(_IDX["callbacks_success"] if success else _IDX["callbacks_failure"])

    # ---- worker role running ---------------------------------------------
    def set_dispatcher_running(self, n):
        with self._role_lock:
            self._dispatcher_running = n

    def set_mover_running(self, n):
        with self._role_lock:
            self._mover_running = n

    # ---- histograms ------------------------------------------------------
    def observe_ns(self, name, value_ns, detail_token=None):
        if detail_token is None:
            detail_token = self.detail_token()
        with self.detail_event(detail_token) as active:
            if active:
                h = self._hist.get(name)
                if h is not None:
                    h.record_ns(value_ns)

    def observe_ms(self, name, value_ms, detail_token=None):
        if detail_token is None:
            detail_token = self.detail_token()
        with self.detail_event(detail_token) as active:
            if active:
                h = self._hist.get(name)
                if h is not None:
                    h.record_ms(value_ms)

    # ---- snapshot --------------------------------------------------------
    def _build_snapshot(self, is_final):
        base = self._base_kwargs(is_final, include_error_time=True)
        base["component_type"] = _c.COMPONENT_PRODUCER
        last_error_mono_ns = base.pop("_last_error_mono_ns")
        last_success_age = last_error_age = None
        if self.metrics_level == _c.METRICS_LEVEL_OFF:
            counters = None
            memory = worker_roles = ingress = aggregate_q = send_q = retry_q = callback_q = None
        else:
            vals = self._bank.snapshot_values()
            counters, saturated = self._derive_counters(vals)
            base["counter_saturated"] = saturated
            memory = self._memory_snapshot()
            worker_roles = self._worker_roles_snapshot(vals)
            ingress = self._gauge_queue_snapshot(0, 1, bounded=False)
            aggregate_q = self._gauge_queue_snapshot(8, 9, bounded=False)
            # ThreadPoolExecutor's submission queue is unbounded; this logical
            # gauge must not claim a capacity the SDK does not enforce.
            send_q = self._gauge_queue_snapshot(2, 3, bounded=False)
            retry_q = self._queue_snapshot(self._retry_queue_provider, bounded=False)
            callback_q = self._gauge_queue_snapshot(10, 11, bounded=False)
            last_success_age, last_error_age = self._age_snapshot(
                last_error_mono_ns)
        # A retained Detailed histogram is still part of the final Detailed
        # snapshot, but raw histograms are absent at Core/Off.  Observations
        # themselves are token-gated by detail_event().
        histograms = ({name: h.snapshot() for name, h in self._hist.items()}
                      if self.metrics_level == _c.METRICS_LEVEL_DETAILED else {})
        if counters is not None:
            base.update(counters)
            if memory is not None:
                base["memory"] = memory.to_dict()
            if worker_roles:
                base["worker_roles"] = [role.to_dict() for role in worker_roles]
            for name, queue in (("ingress_queue", ingress),
                                ("aggregate_queue", aggregate_q),
                                ("send_queue", send_q),
                                ("retry_queue", retry_q),
                                ("callback_queue", callback_q)):
                if queue is not None:
                    base[name] = queue.to_dict()
            if last_success_age is not None:
                base["last_success_age_ms"] = last_success_age
            if last_error_age is not None:
                base["last_error_age_ms"] = last_error_age
        for name, histogram in histograms.items():
            base[name + "_ms"] = histogram.to_dict()
        return SnapshotValue(base)

    def _age_snapshot(self, error_mono_ns):
        # Use frozen close clock if closed, else live monotonic.
        end = self._close_mono_ns if self._close_mono_ns is not None else self._clock.monotonic_ns()
        with self._age_lock:
            s_ns = self._last_success_mono_ns
        s_age = max(0, (end - s_ns) // 1_000_000) if s_ns is not None else None
        e_age = (max(0, (end - error_mono_ns) // 1_000_000)
                 if error_mono_ns is not None else None)
        return s_age, e_age

    def _derive_counters(self, vals):
        out = {}
        saturated = False
        for k in PRODUCER_COUNTER_KEYS:
            v = vals[_IDX[k]]
            if v < 0:
                v = 0  # gauge underflow guard
            cv, sat = saturating_u64(v)
            out[k] = cv
            saturated = saturated or sat
        # Owned is an active-collection gauge. Cumulative accepted/terminal
        # counters intentionally survive an Off boundary, whereas an old batch
        # completion is ignored in the new collection.
        owned_logs, owned_groups = self._owned.get_two(0, 1)
        ol, ol_sat = saturating_u64(max(0, owned_logs))
        og, og_sat = saturating_u64(max(0, owned_groups))
        out["owned_logs"] = ol
        out["owned_groups"] = og
        saturated = saturated or ol_sat or og_sat
        return out, saturated

    def _memory_snapshot(self):
        ml = self._memory_limiter
        if ml is None:
            return None
        try:
            info = ml.stats_snapshot()
        except Exception:
            return None
        if info.get("ownership_unknown"):
            # A fixed summary tells the projection layer that an Off-era
            # allocation still exists.  Do not walk batch maps to guess its
            # owner; managed memory remains explicitly missing/partial until
            # the allocation releases.
            return None
        return MemoryStats(
            accounted_limit_bytes=info["accounted_limit_bytes"],
            accounted_used_bytes=info["accounted_used_bytes"],
            rejected_total=info.get(
                "accounting_rejected_total", self._bank.get(_IDX["rejected_memory"])),
            high_watermark_bytes=info["high_watermark_bytes"],
            payload_bytes=info["payload_bytes"],
            temporary_bytes=info.get("temporary_bytes"),
            payload_admission_limit_bytes=info.get("payload_admission_limit_bytes"),
            bounded_runtime_buffer_bytes=info.get("bounded_runtime_buffer_bytes"),
            payload_admission_rejected_total=info.get("payload_admission_rejected_total"),
            runtime_buffer_rejected_total=info.get("runtime_buffer_rejected_total"),
            ingress_owned_bytes=info.get("ingress_owned_bytes"),
            aggregate_owned_bytes=info.get("aggregate_owned_bytes"),
            send_owned_bytes=info.get("send_owned_bytes"),
            retry_owned_bytes=info.get("retry_owned_bytes"),
        )

    def _worker_roles_snapshot(self, vals):
        with self._role_lock:
            mover = self._mover_running
        submitted, _submitted_hwm = self._qgauge.get_two(4, 5)
        running, _running_hwm = self._qgauge.get_two(6, 7)
        # Python has no dedicated dispatcher thread (dispatch is inline on the
        # caller). We report the mover thread liveness and the sender pool. For
        # the sender pool we deliberately do NOT read ThreadPoolExecutor private
        # state; ``running`` is the count of senders actively executing a send
        # (== in_flight, always <= expected), and ``expected`` is the configured
        # pool capacity. An idle pool legitimately shows running=0.
        return (
            WorkerRoleStats("mover", expected=1, running=mover, in_flight=0),
            WorkerRoleStats("sender", expected=self._max_sender_count,
                            running=max(0, running),
                            in_flight=max(0, submitted)),
        )

    def _gauge_queue_snapshot(self, cur_idx, hwm_idx, bounded):
        """Build a QueueStats from the SDK-maintained O(1) depth gauges."""
        current, hwm = self._qgauge.get_two(cur_idx, hwm_idx)
        current = current if current > 0 else 0
        return QueueStats(current_items=current, bounded=bounded,
                          high_watermark_items=hwm)

    @staticmethod
    def _queue_snapshot(provider, bounded):
        if provider is None:
            return None
        try:
            info = provider()
        except Exception:
            return None
        if info is None:
            return None
        current = info.get("current_items", 0)
        return QueueStats(
            current_items=current,
            bounded=bounded,
            high_watermark_items=info.get("high_watermark_items", current),
            capacity_items=info.get("capacity_items"),
        )
