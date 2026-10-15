# coding=utf-8
"""Concurrency, stability, thread-leak, and exception-isolation tests.

Barrier-driven races, high-frequency repetition, and final-snapshot stability.
Python has no built-in race detector, so we use Event/Barrier to align timing,
repeat hot cases many times, and assert invariants + no leaked non-daemon
threads. All offline.
"""
from __future__ import absolute_import

import json
import threading
import unittest

from volcengine.tls._stats.producer_state import ProducerStatsState
from volcengine.tls._stats.consumer_state import ConsumerStatsState
from volcengine.tls._stats.histogram import FixedHistogram, FAST_BOUNDS_MS


def _internal_from_cumulative(cum):
    if not cum:
        return []
    out = [cum[0]]
    for i in range(1, len(cum)):
        out.append(cum[i] - cum[i - 1])
    return out


class ConcurrentGetStatsTest(unittest.TestCase):
    def test_disabled_tokens_do_not_acquire_collection_lock(self):
        class UnexpectedLock(object):
            def __enter__(self):
                raise AssertionError("disabled token acquired collection lock")

            def __exit__(self, *_args):
                return False

        for state in (ConsumerStatsState("off", "c", "test"),
                      ProducerStatsState("off", "p", "test", max_sender_count=1)):
            state._lifecycle_lock = UnexpectedLock()
            self.assertEqual(state.token(), 0)
            self.assertEqual(state.detail_token(), 0)

    def test_slow_checkpoint_provider_does_not_hold_observation_lock(self):
        for operation in ("get_stats", "freeze", "checkpoint_add", "checkpoint_clear"):
            with self.subTest(operation=operation):
                st = ConsumerStatsState("core", "c", "test")
                st.mark_started()
                entered, release, updated = (threading.Event() for _ in range(3))

                def provider():
                    entered.set()
                    release.wait(3)
                    return 7

                st.bind_checkpoint_provider(provider)
                reader = threading.Thread(target=getattr(st, operation))
                writer = threading.Thread(target=lambda: (st.on_heartbeat(True), updated.set()))
                reader.start()
                try:
                    self.assertTrue(entered.wait(1))
                    writer.start()
                    self.assertTrue(updated.wait(1), "provider held observation lock")
                finally:
                    release.set()
                    reader.join(3)
                    if writer.ident is not None:
                        writer.join(3)
                self.assertFalse(reader.is_alive())

    def test_snapshot_provider_is_read_only_and_discards_old_generation(self):
        st = ConsumerStatsState("core", "c", "test")
        st.mark_started()
        st.bind_checkpoint_provider(lambda: 7)
        self.assertEqual(st.get_stats().checkpoint_pending.current_items, 7)
        self.assertEqual(st._checkpoint_count, 0)
        entered, release = threading.Event(), threading.Event()
        results = []

        def provider():
            entered.set()
            release.wait(3)
            return 9

        st.bind_checkpoint_provider(provider)
        reader = threading.Thread(target=lambda: results.append(st.get_stats()))
        reader.start()
        try:
            self.assertTrue(entered.wait(1))
            st.set_metrics_level("off")
            st.set_metrics_level("core")
        finally:
            release.set()
            reader.join(4)
        self.assertFalse(reader.is_alive())
        self.assertEqual(results[0].checkpoint_pending.current_items, 0)

    def test_concurrent_business_and_get_stats(self):
        st = ProducerStatsState("detailed", "p", "test", max_sender_count=8)
        st.mark_started()
        n_workers = 8
        per = 3000
        # parties = workers + reader + main coordinator
        start = threading.Barrier(n_workers + 2)
        errors = []

        def worker():
            start.wait()
            try:
                for i in range(per):
                    st.on_accepted(1, 1)
                    st.on_send_start()
                    st.on_send_end(success=True, payload_logs=1, payload_groups=1)
                    st.on_terminal("success", 1, 1)
                    if i % 10 == 0:
                        st.observe_ms("send_call_duration", i % 50)
            except Exception as e:  # pragma: no cover
                errors.append(e)

        def reader():
            start.wait()
            for _ in range(2000):
                snap = st.get_stats()
                d = snap.to_dict()
                # conservation must hold at every observation point
                if d["accepted_logs"] != (d["terminal_success_logs"]
                                          + d["terminal_failure_logs"]
                                          + d["terminal_dropped_logs"]
                                          + d["owned_logs"]):
                    errors.append(AssertionError("conservation broke: %r" % d))
                    return

        threads = [threading.Thread(target=worker) for _ in range(n_workers)]
        rt = threading.Thread(target=reader)
        for t in threads:
            t.start()
        rt.start()
        start.wait()
        for t in threads:
            t.join()
        rt.join()
        self.assertEqual(errors, [])
        snap = st.get_stats()
        self.assertEqual(snap.accepted_logs, n_workers * per)
        self.assertEqual(snap.terminal_success_logs, n_workers * per)
        self.assertEqual(snap.owned_logs, 0)


class HistogramRaceTest(unittest.TestCase):
    def test_record_snapshot_race_repeated(self):
        for _ in range(20):
            h = FixedHistogram(FAST_BOUNDS_MS)
            n, per = 8, 2000
            barrier = threading.Barrier(n + 1)

            def worker():
                barrier.wait()
                for i in range(per):
                    h.record_ms(i % 100)

            threads = [threading.Thread(target=worker) for _ in range(n)]
            for t in threads:
                t.start()
            barrier.wait()
            for t in threads:
                t.join()
            snap = h.snapshot()
            self.assertEqual(snap.count, n * per)
            self.assertEqual(snap.count, snap.cumulative_counts[-1])
            self.assertEqual(snap.count, sum(_internal_from_cumulative(list(snap.cumulative_counts))))


class FinalFreezeStabilityTest(unittest.TestCase):
    def test_final_snapshot_hash_stable_under_concurrent_reads(self):
        st = ProducerStatsState("core", "p", "test", max_sender_count=4)
        st.mark_started()
        for _ in range(100):
            st.on_accepted(1, 1)
            st.on_terminal("success", 1, 1)
        st.freeze()

        hashes = []
        lock = threading.Lock()

        def reader():
            for _ in range(500):
                d = st.get_stats().to_dict()
                # captured_at/uptime are frozen; whole dict must be identical
                s = json.dumps(d, sort_keys=True)
                with lock:
                    hashes.append(hash(s))

        threads = [threading.Thread(target=reader) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(len(set(hashes)), 1, "final snapshot must be byte-identical")

    def test_repeated_close_race_100x(self):
        race_errors = []
        for _ in range(100):
            st = ConsumerStatsState("core", "c", "test")
            st.mark_started()
            st.on_fetch_start(); st.on_fetch_end(1, 5)
            # concurrent freeze() + get_stats(); readers MUST never see None
            # The lifecycle lock serializes publication with these reads;
            # this verifies that the locking invariant remains intact.
            def freezer():
                st.freeze()

            def reader():
                for _ in range(50):
                    snap = st.get_stats()
                    if snap is None:
                        race_errors.append("get_stats returned None during freeze")
                        return
            ts = [threading.Thread(target=freezer) for _ in range(3)] + \
                 [threading.Thread(target=reader) for _ in range(3)]
            for t in ts:
                t.start()
            for t in ts:
                t.join()
            s1 = st.get_stats()
            s2 = st.get_stats()
            self.assertIs(s1, s2)
            self.assertEqual(s1.state, "closed")
        self.assertEqual(race_errors, [])


class ThreadLeakTest(unittest.TestCase):
    def test_stats_state_creates_no_threads(self):
        before = threading.active_count()
        states = []
        for _ in range(50):
            st = ProducerStatsState("detailed", "p", "test", max_sender_count=4)
            st.mark_started()
            st.on_accepted(10, 1)
            st.get_stats()
            st.freeze()
            states.append(st)
        after = threading.active_count()
        # No background/sampling threads should be spawned by the stats layer.
        self.assertEqual(before, after)

    def test_producer_lifecycle_leaves_no_threads(self):
        import logging
        import time as _time
        from volcengine.tls.producer.producer import TLSProducer
        from volcengine.tls.producer.producer_model import ProducerConfig
        from volcengine.tls.tls_requests import PutLogsV2LogContent

        logging.disable(logging.CRITICAL)
        try:
            class _Resp:
                request_id = "r"

            class _Client:
                def put_logs(self, _):
                    return _Resp()

                def set_retry_policy(self, _p):
                    pass

            before = threading.active_count()
            for _ in range(10):
                c = ProducerConfig(
                    "e", "cn-beijing", "akid", "seckey",
                    metrics_level="core")
                c.max_block_ms = 0
                c.linger_ms = 100
                p = TLSProducer(c)
                p.dispatcher.client = _Client()
                p.mover.client = _Client()
                p.start()
                for _ in range(20):
                    p.send_logs_v2(None, "topic", None, None,
                                   [PutLogsV2LogContent(time=1, log_dict={"k": "v"})], None)
                p.close(timeout_ms=3000)
            _time.sleep(0.5)
            after = threading.active_count()
            self.assertLessEqual(after, before,
                                 "producer lifecycle leaked threads: before=%d after=%d" % (before, after))
        finally:
            logging.disable(logging.NOTSET)


class ExceptionIsolationTest(unittest.TestCase):
    def test_stats_never_raises_on_bad_input(self):
        st = ProducerStatsState("core", "p", "test")
        # Extra decrements, odd values -> must clamp/no-op, never raise.
        st.on_send_end(success=True)         # no matching start
        st.on_callback_end(success=True)     # no matching start
        st.observe_ms("nonexistent_hist", 5)  # unknown histogram -> no-op
        st.observe_ns("send_call_duration", None)  # None ignored
        snap = st.get_stats()
        self.assertGreaterEqual(snap.send_calls_in_flight, 0)
        self.assertGreaterEqual(snap.callbacks_in_flight, 0)

    def test_consumer_release_without_acquire_noop(self):
        st = ConsumerStatsState("core", "c", "test")
        st.release_held(None)  # no token -> no-op
        self.assertEqual(st.get_stats().held_batch_references, 0)


if __name__ == "__main__":
    unittest.main()
