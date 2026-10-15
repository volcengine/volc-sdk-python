"""Public snapshot views, collection boundaries, and immutable projections."""
import json
import threading
import unittest

from volcengine.tls._stats.producer_state import ProducerStatsState
from volcengine.tls._stats.consumer_state import ConsumerStatsState
from volcengine.tls.stats.options import StatsOptions
from volcengine.tls.stats.snapshot import project_snapshot


class SnapshotProjectionTest(unittest.TestCase):
    def test_view_level_matrix(self):
        for state_type in (ProducerStatsState, ConsumerStatsState):
            for level in ("off", "core", "detailed"):
                state = state_type(level, "fixture", "test")
                for view in ("health", "operational", "debug"):
                    with self.subTest(component=state_type.__name__, level=level, view=view):
                        s = project_snapshot(state.get_stats(), StatsOptions(view))
                        d = s.to_dict()
                        self.assertEqual(json.loads(json.dumps(d)), d)
                        self.assertEqual(d["schema_version"], 2)
                        self.assertEqual(
                            d["capabilities"],
                            255 if state_type is ProducerStatsState else 159)
                        self.assertEqual(d["collected_level"], level)
                        self.assertEqual(d["requested_view"], view)
                        self.assertEqual("health" in d, level != "off")
                        self.assertEqual("operational" in d, level != "off" and view != "health")
                        self.assertEqual("latency_histograms" in d, level == "detailed" and view == "debug")
                        if level == "off":
                            self.assertTrue(s.partial)
                            self.assertTrue(s.metrics_disabled)
                            self.assertIn("health", s.missing_sections)
                            if view != "health":
                                self.assertIn("operational", s.missing_sections)
                            self.assertIsNone(s.health)
                            self.assertIsNone(s.operational)
                            self.assertIsNone(s.counter_sample())
                        if state_type is ConsumerStatsState:
                            self.assertNotIn("managed_memory", s.missing_sections)
                            self.assertNotIn("memory_breakdown", s.missing_sections)

    def test_immutable_nested_copies(self):
        state = ConsumerStatsState("detailed", "fixture", "test")
        s = project_snapshot(state.get_stats(), StatsOptions("debug"))
        d = s.to_dict()
        with self.assertRaises(AttributeError):
            s.new_public_attribute = "blocked"
        with self.assertRaises(AttributeError):
            s.lifecycle_state = "hacked"
        self.assertIsInstance(s.health.signals.critical_flags, tuple)
        with self.assertRaises((AttributeError, TypeError)):
            s.health.signals.critical_flags += ("blocked",)

        d["worker_details"]["items"][0]["running"] = 999
        self.assertNotEqual(s.to_dict()["worker_details"]["items"][0]["running"], 999)
        d["operational"]["counters"]["fetch_calls_success_total"] = 999
        d["health"]["signals"]["critical_flags"].append("changed")
        self.assertEqual(s.operational.counters.fetch_calls_success_total, 0)
        self.assertEqual(s.health.signals.critical_flags, ())
        with self.assertRaises((AttributeError, TypeError)):
            s.health.signals.worker_summary.running = 99
        with self.assertRaises((AttributeError, TypeError)):
            s.health.signals["critical_flags"] = []

    def test_histogram_fields_and_checkpoint_slow_profile(self):
        state = ConsumerStatsState("detailed", "fixture", "test")
        state.observe_ms("checkpoint_call_duration", 6)
        snap = project_snapshot(state.get_stats(), StatsOptions("debug"))
        checkpoint = snap.latency_histograms.checkpoint_call_duration
        self.assertEqual(checkpoint.start, "checkpoint_call_start")
        self.assertTrue(checkpoint.includes_retry)
        histogram = checkpoint.histogram
        self.assertEqual(set(histogram), {
            "bucket_profile", "upper_bounds_ms", "cumulative_bucket_counts", "count", "sum_ms"})
        self.assertEqual(histogram.bucket_profile, "slow")
        self.assertEqual(histogram.upper_bounds_ms[0], 10)
        self.assertEqual(histogram.cumulative_bucket_counts[0], 1)
        self.assertEqual(histogram.cumulative_bucket_counts[-1], histogram.count)

    def test_process_inflight_is_not_reported_as_completed_success(self):
        state = ConsumerStatsState("core", "fixture", "test")
        state.mark_started()
        generation = state.token()
        held = state.acquire_held(logs=2, groups=1, token=generation)
        state.on_process_start(held, generation=generation)
        during = project_snapshot(state.get_stats(), StatsOptions("operational"))
        self.assertEqual(during.operational.counters.process_attempts_success_total, 0)
        self.assertEqual(during.operational.process_in_flight, 1)
        self.assertEqual(during.operational.held_batch_references, 0)
        self.assertEqual(during.operational.ready_to_process, 0)
        state.on_process_end(True, token=held, generation=generation)
        completed = project_snapshot(state.get_stats(), StatsOptions("operational"))
        self.assertEqual(completed.operational.counters.process_attempts_success_total, 1)
        self.assertEqual(completed.operational.counters.processed_success_logs_total, 2)
        self.assertEqual(completed.operational.process_in_flight, 0)

    def test_level_generation_and_tokens(self):
        s = ProducerStatsState("off", "fixture", "test")
        with self.assertRaises(RuntimeError):
            s.set_metrics_level("core")
        s.mark_started()
        off_token = s.token()
        s.set_metrics_level("core")
        generation = s.collection_generation
        token = s.token()
        with s.event(token) as active:
            self.assertTrue(active)
        with s.event(off_token) as active:
            self.assertFalse(active)
        s.set_metrics_level("detailed")
        self.assertEqual(s.collection_generation, generation)
        detail = s.detail_token()
        self.assertEqual(len(s._hist), 4)
        s.set_metrics_level("core")
        s.set_metrics_level("detailed")
        with s.detail_event(detail) as active:
            self.assertFalse(active)
        s.set_metrics_level("off")
        s.set_metrics_level("core")
        with s.event(token) as active:
            self.assertFalse(active)
        s.mark_closing()
        with self.assertRaises(RuntimeError):
            s.set_metrics_level("off")

    def test_view_required(self):
        self.assertRaises(TypeError, StatsOptions)
        with self.assertRaises(ValueError):
            StatsOptions("invalid")

    def test_frozen_history_survives_consumer_resume_with_concurrent_readers(self):
        state = ConsumerStatsState("core", "fixture", "test")
        state.mark_started()
        state.freeze()
        historical = project_snapshot(state.get_stats(), StatsOptions("operational"))
        before = historical.to_dict()
        failures = []
        barrier = threading.Barrier(3)

        def read():
            barrier.wait()
            for _ in range(100):
                try:
                    snap = project_snapshot(state.get_stats(), StatsOptions("operational"))
                    self.assertGreaterEqual(snap.snapshot_sequence, historical.snapshot_sequence)
                    self.assertEqual(snap.instance_id, historical.instance_id)
                except Exception as error:
                    failures.append(error)

        readers = [threading.Thread(target=read) for _ in range(2)]
        for reader in readers:
            reader.start()
        barrier.wait()
        for _ in range(20):
            state.resume_for_start()
            state.mark_started()
            state.freeze()
        for reader in readers:
            reader.join(3)
            self.assertFalse(reader.is_alive())
        self.assertFalse(failures, failures)
        self.assertEqual(historical.to_dict(), before)
        self.assertGreater(state.collection_generation, historical.collection_generation)


if __name__ == "__main__":
    unittest.main()
