# coding=utf-8
"""Contract tests for component-neutral delta and health adapters."""
from __future__ import absolute_import

import unittest

from volcengine.tls.stats.delta import (
    CounterSample,
    DeltaAdapter,
    DELTA_METRICS_UNAVAILABLE,
    compute_delta,
)
from volcengine.tls.stats.health import HealthPolicy, evaluate_health


def _counter_sample(instance="one", generation=1, sequence=1,
                    uptime=1000, captured=1000, value=10,
                    metrics_disabled=False, counters=None):
    header = {
        "instance_id": instance,
        "collection_generation": generation,
        "snapshot_sequence": sequence,
        "uptime_ms": uptime,
        "captured_at_unix_ms": captured,
        "metrics_disabled": metrics_disabled,
    }
    if counters is None:
        counters = {"requests_total": value}
    return CounterSample(header, counters)


class ObservabilityDeltaTest(unittest.TestCase):

    def test_valid_delta_rate_and_input_result_isolation(self):
        adapter = DeltaAdapter()
        header = {
            "instance_id": "one",
            "collection_generation": 1,
            "snapshot_sequence": 1,
            "uptime_ms": 1000,
            "captured_at_unix_ms": 1000,
            "metrics_disabled": False,
        }
        counters = {"requests_total": 10}
        self.assertEqual(adapter.observe(CounterSample(header, counters)).reset_reason,
                         "initial_baseline")

        header["snapshot_sequence"] = 999
        counters["requests_total"] = 999
        result = adapter.observe(_counter_sample(sequence=2, captured=3000,
                                                 uptime=3000, value=16))
        self.assertTrue(result.valid)
        self.assertEqual(result.interval_ms, 2000)
        self.assertEqual(dict(result.deltas), {"requests_total": 6})
        self.assertEqual(dict(result.rates_per_second), {"requests_total": 3.0})
        with self.assertRaises(TypeError):
            result.deltas["requests_total"] = 1
        output = result.to_dict()
        output["deltas"]["requests_total"] = 999
        self.assertEqual(result.deltas["requests_total"], 6)

    def test_invalid_intervals_rebaseline_with_go_reasons(self):
        cases = (
            ("instance", _counter_sample(instance="two", sequence=2,
                                           captured=2000, uptime=2000, value=11),
             "instance_changed"),
            ("generation", _counter_sample(generation=2, sequence=2,
                                            captured=2000, uptime=2000, value=11),
             "collection_changed"),
            ("sequence", _counter_sample(sequence=1, captured=2000,
                                          uptime=2000, value=11),
             "sequence_not_increasing"),
            ("uptime", _counter_sample(sequence=2, captured=2000,
                                        uptime=500, value=11),
             "uptime_regressed"),
            ("wall_time", _counter_sample(sequence=2, captured=1000,
                                           uptime=2000, value=11),
             "capture_time_not_increasing"),
            ("counter", _counter_sample(sequence=2, captured=2000,
                                         uptime=2000, value=9),
             "counter_regressed"),
        )
        for name, current, reason in cases:
            with self.subTest(name=name):
                adapter = DeltaAdapter()
                adapter.observe(_counter_sample())
                result = adapter.observe(current)
                self.assertFalse(result.valid)
                self.assertEqual(result.reset_reason, reason)
                # Every invalid sample is the next baseline.
                next_sample = _counter_sample(sequence=3, captured=3000,
                                              uptime=3000, value=12)
                if name == "instance":
                    next_sample = _counter_sample(instance="two", sequence=3,
                                                  captured=3000, uptime=3000,
                                                  value=12)
                elif name == "generation":
                    next_sample = _counter_sample(generation=2, sequence=3,
                                                  captured=3000, uptime=3000,
                                                  value=12)
                self.assertTrue(adapter.observe(next_sample).valid)

    def test_off_none_counter_and_counter_set_changes_rebaseline(self):
        adapter = DeltaAdapter()
        off = _counter_sample(metrics_disabled=True, counters=None)
        self.assertEqual(adapter.observe(off).reset_reason,
                         "metrics_unavailable")

        none_adapter = DeltaAdapter()
        none_adapter.observe(_counter_sample())
        none_counter = CounterSample({
            "instance_id": "one",
            "collection_generation": 1,
            "snapshot_sequence": 2,
            "uptime_ms": 2000,
            "captured_at_unix_ms": 2000,
            "metrics_disabled": False,
        }, None)
        self.assertEqual(none_adapter.observe(none_counter).reset_reason,
                         "metrics_unavailable")

        enabled = _counter_sample(generation=2, sequence=2, captured=2000,
                                  uptime=2000, value=10)
        self.assertEqual(adapter.observe(enabled).reset_reason,
                         "metrics_unavailable")
        changed = _counter_sample(generation=2, sequence=3, captured=3000,
                                  uptime=3000,
                                  counters={"requests_total": 12,
                                            "new_total": 1})
        self.assertEqual(adapter.observe(changed).reset_reason,
                         "counter_set_changed")
        stable = _counter_sample(generation=2, sequence=4, captured=4000,
                                 uptime=4000,
                                 counters={"requests_total": 13,
                                           "new_total": 2})
        self.assertTrue(adapter.observe(stable).valid)

    def test_reset_discards_baseline(self):
        adapter = DeltaAdapter()
        adapter.observe(_counter_sample())
        adapter.observe(_counter_sample(sequence=2, captured=2000,
                                        uptime=2000, value=11))
        adapter.reset()
        result = adapter.observe(_counter_sample(sequence=3, captured=3000,
                                                 uptime=3000, value=12))
        self.assertFalse(result.valid)
        self.assertEqual(result.reset_reason, "initial_baseline")

    def test_invalid_counter_values_are_metrics_unavailable(self):
        previous = _counter_sample(value=10)
        for invalid in (None, 1.5, "11", -1, True, 1 << 64, 10 ** 400):
            with self.subTest(invalid=invalid):
                current = _counter_sample(sequence=2, captured=2000,
                                          uptime=2000,
                                          counters={"requests_total": invalid})
                result = compute_delta(previous, current)
                self.assertFalse(result.valid)
                self.assertEqual(result.reset_reason,
                                 DELTA_METRICS_UNAVAILABLE)

        previous_invalid = _counter_sample(
            counters={"requests_total": None})
        result = compute_delta(
            previous_invalid,
            _counter_sample(sequence=2, captured=2000, uptime=2000, value=11))
        self.assertFalse(result.valid)
        self.assertEqual(result.reset_reason, DELTA_METRICS_UNAVAILABLE)

        max_value = (1 << 64) - 1
        result = compute_delta(
            _counter_sample(value=max_value - 1),
            _counter_sample(sequence=2, captured=2000, uptime=2000,
                            value=max_value))
        self.assertTrue(result.valid)
        self.assertEqual(dict(result.deltas), {"requests_total": 1})


def _health_snapshot(**kwargs):
    header = {
        "instance_id": "instance",
        "collection_generation": 1,
        "captured_at_unix_ms": 20,
        "lifecycle_state": "running",
        "metrics_disabled": False,
    }
    header.update(kwargs.pop("header", {}))
    signals = {
        "critical_flags": [],
        "worker_summary": {"missing_critical_roles": 0},
    }
    signals.update(kwargs.pop("signals", {}))
    header.update(kwargs)
    snapshot = dict(header)
    snapshot["health"] = {"signals": signals}
    return snapshot


class _SnapshotObject(object):
    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return self.value


class ObservabilityHealthTest(unittest.TestCase):

    def test_first_off_closed_instance_and_generation_are_unknown(self):
        current = _health_snapshot()
        result = evaluate_health(None, current)
        self.assertEqual(result.status, "unknown")
        self.assertEqual(result.reason_codes, ("insufficient_data",))
        self.assertTrue(result.insufficient_data)

        previous = _health_snapshot()
        for name, changed, reason in (
                ("off", {"metrics_disabled": True}, "metrics_disabled"),
                ("closed", {"lifecycle_state": "closed"},
                 "lifecycle_not_running"),
                ("new", {"lifecycle_state": "new"},
                 "lifecycle_not_running"),
                ("closing", {"lifecycle_state": "closing"},
                 "lifecycle_not_running"),
                ("instance", {"instance_id": "other"}, "instance_changed"),
                ("generation", {"collection_generation": 2},
                 "collection_changed")):
            with self.subTest(name=name):
                now = _health_snapshot(header=changed)
                result = evaluate_health(previous, now)
                self.assertEqual(result.status, "unknown")
                self.assertEqual(result.reason_codes, (reason,))
                self.assertTrue(result.insufficient_data)

    def test_previous_and_signal_gaps_have_exact_unknown_reasons(self):
        current = _health_snapshot()
        cases = (
            ("previous_instance", _health_snapshot(instance_id=""),
             "insufficient_data"),
            ("previous_disabled", _health_snapshot(metrics_disabled=True),
             "metrics_disabled"),
        )
        for name, previous, reason in cases:
            with self.subTest(name=name):
                result = evaluate_health(previous, current)
                self.assertEqual(result.status, "unknown")
                self.assertEqual(result.reason_codes, (reason,))
                self.assertTrue(result.insufficient_data)

        invalid_lifecycle = _health_snapshot(lifecycle_state="paused")
        result = evaluate_health(_health_snapshot(), invalid_lifecycle)
        self.assertEqual(result.status, "unknown")
        self.assertEqual(result.reason_codes, ("lifecycle_not_running",))
        self.assertTrue(result.insufficient_data)

        missing_signals = _health_snapshot()
        missing_signals["health"]["signals"] = None
        result = evaluate_health(_health_snapshot(), missing_signals)
        self.assertEqual(result.status, "unknown")
        self.assertEqual(result.reason_codes, ("insufficient_data",))
        self.assertTrue(result.insufficient_data)

    def test_failed_critical_worker_pressure_and_idle_rules(self):
        previous = _health_snapshot()
        cases = (
            ({"lifecycle_state": "failed"}, "unhealthy", ("lifecycle_failed",)),
            ({"signals": {"critical_flags": ["x"]}}, "unhealthy",
             ("critical_flag",)),
            ({"signals": {"worker_summary": {"missing_critical_roles": 1}}},
             "unhealthy", ("worker_missing",)),
            ({"signals": {"queue_pressure": 0.8}}, "degraded",
             ("queue_pressure",)),
            ({"signals": {"memory_pressure": 0.8}}, "degraded",
             ("memory_pressure",)),
            ({}, "healthy", ()),
        )
        for values, status, reasons in cases:
            with self.subTest(status=status, reasons=reasons):
                now = _health_snapshot(**values)
                result = evaluate_health(previous, now)
                self.assertEqual(result.status, status)
                self.assertEqual(result.reason_codes, reasons)
                self.assertFalse(result.insufficient_data)

    def test_effective_memory_pressure_wins_and_policy_applies(self):
        previous = _health_snapshot()
        now = _health_snapshot(signals={"memory_pressure": 0.9})
        result = evaluate_health(previous, _SnapshotObject(now),
                                 HealthPolicy(queue_pressure_degraded=0.95,
                                              memory_pressure_degraded=0.85))
        self.assertEqual(result.status, "degraded")
        self.assertEqual(result.reason_codes, ("memory_pressure",))
        self.assertEqual(result.evaluated_at_unix_ms, 20)

        idle = evaluate_health(previous, _health_snapshot(signals={
            "queue_pressure": 0.0, "memory_pressure": 0.0,
        }))
        self.assertEqual(idle.status, "healthy")

    def test_none_and_nan_policy_thresholds_fallback_to_point_eight(self):
        previous = _health_snapshot()
        cases = (
            (HealthPolicy(queue_pressure_degraded=None,
                          memory_pressure_degraded=1.0),
             {"queue_pressure": 0.8}, "queue_pressure"),
            (HealthPolicy(queue_pressure_degraded=1.0,
                          memory_pressure_degraded=None),
             {"memory_pressure": 0.8}, "memory_pressure"),
            (HealthPolicy(queue_pressure_degraded=float("nan"),
                          memory_pressure_degraded=1.0),
             {"queue_pressure": 0.8}, "queue_pressure"),
            (HealthPolicy(queue_pressure_degraded=1.0,
                          memory_pressure_degraded=float("nan")),
             {"memory_pressure": 0.8}, "memory_pressure"),
        )
        for policy, signals, reason in cases:
            with self.subTest(reason=reason, signals=signals):
                result = evaluate_health(previous,
                                         _health_snapshot(signals=signals),
                                         policy)
                self.assertEqual(result.status, "degraded")
                self.assertEqual(result.reason_codes, (reason,))

    def test_health_result_is_immutable_and_to_dict_is_fresh(self):
        result = evaluate_health(_health_snapshot(), _health_snapshot(
            signals={"critical_flags": ["broken"]}))
        with self.assertRaises(AttributeError):
            result.status = "healthy"
        with self.assertRaises(AttributeError):
            result.reason_codes += ("x",)
        output = result.to_dict()
        output["reason_codes"].append("changed")
        self.assertEqual(result.reason_codes, ("critical_flag",))


if __name__ == "__main__":
    unittest.main()
