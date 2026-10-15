# coding=utf-8
"""Contract tests for fixed histograms and clock primitives."""
from __future__ import absolute_import

import sys
import threading
import unittest

from volcengine.tls._stats.clock import Clock, SystemClock, monotonic_ns, wall_ms
from volcengine.tls._stats.histogram import (
    FAST_BOUNDS_MS,
    SLOW_BOUNDS_MS,
    FixedHistogram,
)


def _internal_from_cumulative(cum):
    if not cum:
        return []
    internal = [cum[0]]
    for i in range(1, len(cum)):
        internal.append(cum[i] - cum[i - 1])
    return internal


class HistogramContractTest(unittest.TestCase):
    def test_bounds_values(self):
        self.assertEqual(
            FAST_BOUNDS_MS,
            (1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000),
        )
        self.assertEqual(
            SLOW_BOUNDS_MS,
            (10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000,
             20000, 50000, 100000, 200000, 300000),
        )

    def test_bucket_count_is_finite_plus_inf(self):
        h = FixedHistogram(FAST_BOUNDS_MS)
        snap = h.snapshot()
        self.assertEqual(len(snap.cumulative_counts), len(FAST_BOUNDS_MS) + 1)

    def test_inclusive_upper_edge_and_inf(self):
        h = FixedHistogram((1, 2, 5))
        for v in (1, 2, 5, 6):
            h.record_ms(v)
        snap = h.snapshot()
        internal = _internal_from_cumulative(list(snap.cumulative_counts))
        # 1<=1 -> b0, 2<=2 -> b1, 5<=5 -> b2, 6 -> +Inf b3
        self.assertEqual(internal, [1, 1, 1, 1])

    def test_invariants(self):
        h = FixedHistogram(FAST_BOUNDS_MS)
        for v in (0.5, 1, 1.5, 2, 7, 123, 10000, 99999):
            h.record_ms(v)
        snap = h.snapshot()
        cum = list(snap.cumulative_counts)
        self.assertEqual(snap.count, cum[-1])
        self.assertEqual(snap.count, sum(_internal_from_cumulative(cum)))
        self.assertTrue(all(cum[i] <= cum[i + 1] for i in range(len(cum) - 1)))
        self.assertGreaterEqual(snap.sum_ms, 0)

    def test_negative_clamped(self):
        h = FixedHistogram((1, 2))
        h.record_ms(-5)
        snap = h.snapshot()
        self.assertEqual(snap.count, 1)
        self.assertGreaterEqual(snap.sum_ms, 0)

    def test_record_ns(self):
        h = FixedHistogram((1, 2, 5))
        h.record_ns(3_000_000)  # 3ms -> bucket <=5
        snap = h.snapshot()
        internal = _internal_from_cumulative(list(snap.cumulative_counts))
        self.assertEqual(internal, [0, 0, 1, 0])

    def test_none_ignored(self):
        h = FixedHistogram((1, 2))
        h.record_ms(None)
        h.record_ns(None)
        self.assertEqual(h.snapshot().count, 0)

    def test_nonfinite_and_overflow_values_are_ignored(self):
        h = FixedHistogram((1, 2))
        for value in (float("nan"), float("inf"), float("-inf"), 10 ** 400):
            h.record_ms(value)
            h.record_ns(value)
        snap = h.snapshot()
        self.assertEqual(snap.count, 0)
        self.assertEqual(snap.sum_ms, 0.0)

    def test_sum_overflow_does_not_modify_histogram(self):
        h = FixedHistogram((1, 2))
        h.record_ms(sys.float_info.max)
        before = h.snapshot()
        h.record_ms(sys.float_info.max)
        after = h.snapshot()
        self.assertEqual(after.count, before.count)
        self.assertEqual(after.sum_ms, before.sum_ms)

    def test_to_dict_isolation(self):
        h = FixedHistogram((1, 2))
        h.record_ms(1)
        snap = h.snapshot()
        d = snap.to_dict()
        d["cumulative_counts"][0] = 999
        d["bounds_ms"].append(9999)
        self.assertNotEqual(snap.cumulative_counts[0], 999)
        self.assertEqual(len(snap.bounds_ms), 2)

    def test_concurrent_record(self):
        h = FixedHistogram(FAST_BOUNDS_MS)
        n_threads, per = 16, 2000

        def worker():
            for _ in range(per):
                h.record_ms(7)

        threads = [threading.Thread(target=worker) for _ in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        snap = h.snapshot()
        self.assertEqual(snap.count, n_threads * per)
        self.assertEqual(snap.count, snap.cumulative_counts[-1])
        self.assertEqual(snap.count, sum(_internal_from_cumulative(list(snap.cumulative_counts))))


class ClockContractTest(unittest.TestCase):
    def test_system_clock(self):
        c = SystemClock()
        self.assertGreater(c.monotonic_ns(), 0)
        self.assertGreater(c.wall_ms(), 0)
        self.assertEqual(c.monotonic_ms(), c.monotonic_ns() // 1_000_000)

    def test_monotonic_non_decreasing(self):
        c = SystemClock()
        a = c.monotonic_ns()
        b = c.monotonic_ns()
        self.assertGreaterEqual(b, a)

    def test_module_helpers(self):
        self.assertGreater(monotonic_ns(), 0)
        self.assertGreater(wall_ms(), 0)

    def test_clock_is_abstract(self):
        with self.assertRaises(NotImplementedError):
            Clock().monotonic_ns()


if __name__ == "__main__":
    unittest.main()
