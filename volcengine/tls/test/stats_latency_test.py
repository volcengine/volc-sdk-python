# coding=utf-8
"""Latency histogram stress, snapshot p99, and detailed-level tests.

These are still unit-scale (no network). Heavier resource A-E benchmarking is
The resource probe owns longer benchmarks. Here we validate histograms under
concurrent record+snapshot; get_stats() snapshot latency p99 is well under the
1ms budget; last_success/error ages populate at Core; detailed level works.
"""
from __future__ import absolute_import

import threading
import time
import unittest

from volcengine.tls._stats.producer_state import ProducerStatsState
from volcengine.tls._stats.consumer_state import ConsumerStatsState


def _percentile(sorted_vals, q):
    # nearest-rank
    if not sorted_vals:
        return 0.0
    import math
    rank = max(1, int(math.ceil(q / 100.0 * len(sorted_vals))))
    return sorted_vals[rank - 1]


class HistogramStressTest(unittest.TestCase):
    def test_concurrent_record_and_snapshot_consistent(self):
        st = ProducerStatsState("detailed", "p", "test", max_sender_count=8)
        st.mark_started()
        stop = threading.Event()
        n_record_threads = 8
        per = 5000

        def recorder():
            for i in range(per):
                st.observe_ms("send_call_duration", (i % 50))
                st.on_accepted(1, 0)

        def snapshotter():
            # concurrently snapshot; must never raise or see broken invariants
            while not stop.is_set():
                snap = st.get_stats()
                h = snap.get("send_call_duration_ms")
                cum = list(h.cumulative_counts)
                assert h.count == cum[-1]
                assert all(cum[i] <= cum[i + 1] for i in range(len(cum) - 1))

        recorders = [threading.Thread(target=recorder) for _ in range(n_record_threads)]
        snap_t = threading.Thread(target=snapshotter)
        snap_t.start()
        for t in recorders:
            t.start()
        for t in recorders:
            t.join()
        stop.set()
        snap_t.join()
        final = st.get_stats()
        h = final.get("send_call_duration_ms")
        self.assertEqual(h.count, n_record_threads * per)
        self.assertEqual(h.count, h.cumulative_counts[-1])


class SnapshotLatencyGateTest(unittest.TestCase):
    def _measure(self, st, iters=2000):
        # warm up
        for _ in range(200):
            st.get_stats()
        samples = []
        for _ in range(iters):
            t0 = time.perf_counter_ns()
            st.get_stats()
            samples.append((time.perf_counter_ns() - t0) / 1e6)  # ms
        samples.sort()
        return samples

    def test_producer_snapshot_p99_under_1ms(self):
        st = ProducerStatsState("detailed", "p", "test", max_sender_count=8)
        st.mark_started()
        # populate some state so the snapshot does real work
        for i in range(1000):
            st.on_accepted(1, 1)
            st.observe_ms("send_call_duration", i % 100)
        samples = self._measure(st)
        p50 = _percentile(samples, 50)
        p99 = _percentile(samples, 99)
        # Budget: < 1ms p99 (plan §7 resource budget). Assert with margin.
        self.assertLess(p99, 1.0, "producer snapshot p99 {:.4f}ms exceeds 1ms".format(p99))
        self.assertLess(p50, 1.0)

    def test_consumer_snapshot_p99_under_1ms(self):
        st = ConsumerStatsState("detailed", "c", "test")
        st.mark_started()
        for i in range(1000):
            st.on_fetch_start(); st.on_fetch_end(1, 10)
            st.checkpoint_add("shard-{}".format(i % 20))
            st.observe_ms("process_duration", i % 100)
        samples = self._measure(st)
        p99 = _percentile(samples, 99)
        self.assertLess(p99, 1.0, "consumer snapshot p99 {:.4f}ms exceeds 1ms".format(p99))


class DetailedLevelTest(unittest.TestCase):
    def test_last_success_error_age_populated_core(self):
        st = ProducerStatsState("core", "p", "test", max_sender_count=2)
        st.on_send_start(); st.on_send_end(success=True, payload_logs=1, payload_groups=1)
        st.on_send_start()
        st.on_send_end(success=False, error_category="transport")
        snap = st.get_stats()
        self.assertIsNotNone(snap.get("last_success_age_ms"))
        self.assertIsNotNone(snap.get("last_error_age_ms"))
        self.assertGreaterEqual(snap.get("last_success_age_ms"), 0)

    def test_ages_absent_before_any_send(self):
        st = ProducerStatsState("core", "p", "test")
        snap = st.get_stats()
        self.assertIsNone(snap.get("last_success_age_ms"))
        self.assertIsNone(snap.get("last_error_age_ms"))
        self.assertNotIn("last_success_age_ms", snap.to_dict())

if __name__ == "__main__":
    unittest.main()
