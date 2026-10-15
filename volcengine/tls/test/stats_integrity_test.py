# coding=utf-8
"""Producer and consumer stats integrity, histogram, queue, and lifecycle tests."""
from __future__ import absolute_import

import threading
import unittest

from volcengine.tls.producer.producer_model import ProducerConfig
from volcengine.tls.consumer.consumer_model import ConsumerConfig
from volcengine.tls._stats.producer_state import ProducerStatsState
from volcengine.tls._stats.consumer_state import ConsumerStatsState
from volcengine.tls._stats.common import QueueStats, UINT64_MAX


class HistogramBoundariesTest(unittest.TestCase):
    """Required histograms record both direct measurements and SDK flow boundaries."""

    def test_invalid_credential_reset_does_not_echo_credentials(self):
        from volcengine.tls.producer.producer import TLSProducer
        from volcengine.tls.tls_exception import TLSException
        producer = TLSProducer.__new__(TLSProducer)
        producer.name = "test-producer"
        for access, secret in (("", "secret-sentinel"), ("access-sentinel", "")):
            with self.assertRaises(TLSException) as caught:
                producer.reset_access_key_token(access, secret, "token-sentinel")
            text = str(caught.exception)
            for value in (access, secret, "token-sentinel"):
                if value:
                    self.assertNotIn(value, text)

    def test_producer_batch_queue_delay_recordable(self):
        st = ProducerStatsState("detailed", "p", "v")
        st.observe_ms("batch_queue_delay", 3)
        snap = st.get_stats()
        h = snap.get("batch_queue_delay_ms")
        self.assertIsNotNone(h)
        self.assertEqual(h.count, 1)

    def test_consumer_checkpoint_call_duration_recordable(self):
        st = ConsumerStatsState("detailed", "c", "v")
        st.observe_ms("checkpoint_call_duration", 7)
        snap = st.get_stats()
        h = snap.get("checkpoint_call_duration_ms")
        self.assertIsNotNone(h)
        self.assertEqual(h.count, 1)

    def test_producer_all_four_histograms_present_in_dict(self):
        st = ProducerStatsState("detailed", "p", "v")
        for name in ("batch_queue_delay", "send_call_duration",
                     "batch_delivery_duration", "callback_duration"):
            st.observe_ms(name, 1)
        d = st.get_stats().to_dict()
        for key in ("batch_queue_delay_ms", "send_call_duration_ms",
                    "batch_delivery_duration_ms", "callback_duration_ms"):
            self.assertIn(key, d)

    def test_consumer_all_four_histograms_present_in_dict(self):
        st = ConsumerStatsState("detailed", "c", "v")
        for name in ("fetch_call_duration", "dispatch_delay",
                     "process_duration", "checkpoint_call_duration"):
            st.observe_ms(name, 1)
        d = st.get_stats().to_dict()
        for key in ("fetch_call_duration_ms", "dispatch_delay_ms",
                    "process_duration_ms", "checkpoint_call_duration_ms"):
            self.assertIn(key, d)

    def test_checkpoint_call_duration_recorded_through_flow(self):
        # Exercise checkpoint duration through the actual upload path.
        from volcengine.tls.consumer.consumer_model import ConsumerConfig, CheckpointInfo
        from volcengine.tls.consumer.checkpoint_manager import CheckpointManager
        from volcengine.tls.data import ConsumeShard
        import logging

        class _Svc:
            def __init__(self):
                self.modify_calls = 0

            def modify_checkpoint(self, _req):
                self.modify_calls += 1

        class _Consumer:
            def __init__(self):
                self.consumer_config = ConsumerConfig(
                    "proj", "grp", ["topic"], "cn",
                    metrics_level="detailed")
                self.consumer_config.validate()
                self.logger = logging.getLogger("test-ckpt")
                self.tls_service = _Svc()
                self.stats_state = ConsumerStatsState(
                    "detailed", "c", "v")

        cons = _Consumer()
        cm = CheckpointManager(cons)
        cm.add_checkpoint(CheckpointInfo("cur1", ConsumeShard("topic", 0)))
        cm.upload_checkpoint()
        snap = cons.stats_state.get_stats()
        h = snap.get("checkpoint_call_duration_ms")
        self.assertIsNotNone(h)
        self.assertGreaterEqual(h.count, 1)
        self.assertIn("checkpoint_call_duration_ms", snap.to_dict())
        self.assertEqual(snap.checkpoint_calls, 1)

    def test_producer_batch_queue_delay_recorded_through_flow(self):
        # Exercise batch-ready to sender-start timing through SendBatchTask.run().
        from volcengine.tls.producer.batch_semaphore import MemoryLimiter
        from volcengine.tls._stats.producer_state import ProducerStatsState
        from volcengine.tls.log_pb2 import LogGroup
        from volcengine.tls.producer.producer_model import BatchLog
        from volcengine.tls.producer.retry_queue import RetryQueue
        from volcengine.tls.producer.send_batch_task import SendBatchTask

        class _Resp:
            request_id = "r"

        class _Client:
            def put_logs(self, _req):
                return _Resp()

            def set_retry_policy(self, _p):
                pass

        cfg = ProducerConfig("ep", "region", "akid", "seckey", None,
                            metrics_level="detailed")
        cfg.max_block_ms = 0
        cfg.valid_config()
        cfg.memory_limiter = MemoryLimiter(cfg.max_producer_memory_bytes,
                                           cfg.total_size_in_bytes)
        cfg.stats_state = ProducerStatsState(
            "detailed", "p", "v",
            memory_limiter=cfg.memory_limiter, max_sender_count=cfg.max_thread_count)
        group = LogGroup()
        log = group.logs.add()  # pylint: disable=no-member
        log.time = 1
        c = log.contents.add()
        c.key, c.value = "k", "v"
        batch = BatchLog(BatchLog.BatchKey(None, "topic", None, None), cfg)
        batch.try_add(group, 64, None)
        task = SendBatchTask(batch, cfg, cfg.memory_limiter, _Client(),
                             RetryQueue(), None)
        task.run()
        snap = cfg.stats_state.get_stats()
        h = snap.get("batch_queue_delay_ms")
        self.assertIsNotNone(h)
        self.assertGreaterEqual(h.count, 1)
        self.assertIn("batch_queue_delay_ms", snap.to_dict())


class ShardWorkerRoleTest(unittest.TestCase):
    """Item 5: consumer must report a shard_worker role and roll back
    submitted/in-flight on thread-start failure (plan §8.4, §11.2)."""

    def test_shard_worker_role_present(self):
        st = ConsumerStatsState("core", "c", "v")
        roles = {r.role for r in st.get_stats().worker_roles}
        self.assertIn("shard_worker", roles)
        self.assertEqual(roles, {"main_loop", "heartbeat", "checkpoint", "shard_worker"})

    def test_shard_worker_expected_tracks_assigned(self):
        st = ConsumerStatsState("core", "c", "v")
        st.set_assigned_shards(3)
        sw = [r for r in st.get_stats().worker_roles if r.role == "shard_worker"][0]
        self.assertEqual(sw.expected, 3)

    def test_shard_task_in_flight_gauge(self):
        st = ConsumerStatsState("core", "c", "v")
        st.on_shard_task_submitted()
        st.on_shard_task_submitted()
        st.on_shard_task_started()
        st.on_shard_task_started()
        sw = [r for r in st.get_stats().worker_roles if r.role == "shard_worker"][0]
        self.assertEqual(sw.in_flight, 2)
        self.assertEqual(sw.running, 2)
        st.on_shard_task_done()
        sw = [r for r in st.get_stats().worker_roles if r.role == "shard_worker"][0]
        self.assertEqual(sw.in_flight, 1)

    def test_shard_task_start_failure_rollback(self):
        st = ConsumerStatsState("core", "c", "v")
        st.on_shard_task_submitted()
        # Thread failed to start: roll back.
        st.on_shard_task_start_failed()
        c = st.get_stats().to_dict()
        self.assertEqual(c["shard_tasks_in_flight"], 0)
        self.assertEqual(c["shard_tasks_submitted"], 0)
        self.assertEqual(c["shard_tasks_started"], 0)
        self.assertEqual(c["shard_tasks_completed"], 0)
        self.assertEqual(c["shard_task_errors"], 1)

    def test_shard_task_never_negative_under_extra_done(self):
        st = ConsumerStatsState("core", "c", "v")
        st.on_shard_task_done()  # spurious
        sw = [r for r in st.get_stats().worker_roles if r.role == "shard_worker"][0]
        self.assertEqual(sw.in_flight, 0)

    def test_logconsumer_thread_start_failure_rolls_back(self):
        # When threading.Thread.start raises, LogConsumer._spawn must roll back
        # the shard-task gauges and not leave in_flight incremented (plan §11.2).
        import logging
        from volcengine.tls.consumer.consumer_model import ConsumerConfig, ConsumerStatus
        from volcengine.tls.consumer.log_consumer import LogConsumer
        from volcengine.tls.data import ConsumeShard
        import volcengine.tls.consumer.log_consumer as lc_mod

        class _Consumer:
            def __init__(self):
                self.consumer_config = ConsumerConfig(
                    "proj", "grp", ["topic"], "cn", metrics_level="core")
                self.consumer_config.validate()
                self.logger = logging.getLogger("test-spawn")
                self.tls_service = object()
                self.log_processor = object()
                self.checkpoint_manager = None
                self.stats_state = ConsumerStatsState("core", "c", "v")

        cons = _Consumer()
        lc = LogConsumer(cons, ConsumeShard("topic", 0))

        class _BoomThread:
            def __init__(self, *a, **k):
                pass

            def start(self):
                raise RuntimeError("cannot start thread")

        orig = lc_mod.threading.Thread
        lc_mod.threading.Thread = _BoomThread
        try:
            with self.assertRaises(RuntimeError):
                lc.run()  # PENDING -> spawns init thread, which fails to start
        finally:
            lc_mod.threading.Thread = orig
        c = cons.stats_state.get_stats().to_dict()
        self.assertEqual(c["shard_tasks_in_flight"], 0)
        self.assertEqual(c["shard_tasks_submitted"], 0)
        self.assertEqual(c["shard_tasks_started"], 0)
        self.assertEqual(c["shard_tasks_completed"], 0)
        self.assertEqual(c["shard_task_errors"], 1)
        self.assertFalse(lc.thread_running_status)


class ProducerQueuesTest(unittest.TestCase):
    """Item 6: producer must expose ingress and send queues with real O(1)
    gauges and truthful aggregate_batches (plan §8.3, §11.1)."""

    def test_ingress_and_send_queues_present(self):
        st = ProducerStatsState("core", "p", "v")
        snap = st.get_stats()
        self.assertIsNotNone(snap.ingress_queue)
        self.assertIsNotNone(snap.send_queue)

    def test_ingress_gauge_add_release(self):
        st = ProducerStatsState("core", "p", "v")
        st.on_ingress_add(3)
        self.assertEqual(st.get_stats().ingress_queue.current_items, 3)
        self.assertEqual(st.get_stats().ingress_queue.high_watermark_items, 3)
        st.on_ingress_release(2)
        self.assertEqual(st.get_stats().ingress_queue.current_items, 1)
        # high watermark does not decrease
        self.assertEqual(st.get_stats().ingress_queue.high_watermark_items, 3)

    def test_ingress_release_never_negative(self):
        st = ProducerStatsState("core", "p", "v")
        st.on_ingress_add(1)
        st.on_ingress_release(5)
        self.assertEqual(st.get_stats().ingress_queue.current_items, 0)

    def test_send_queue_enqueue_dequeue(self):
        st = ProducerStatsState("core", "p", "v")
        st.on_send_enqueue()
        st.on_send_enqueue()
        self.assertEqual(st.get_stats().send_queue.current_items, 2)
        st.on_send_dequeue()
        self.assertEqual(st.get_stats().send_queue.current_items, 1)
        self.assertEqual(st.get_stats().send_queue.high_watermark_items, 2)

    def test_aggregate_batches_truthful_through_flow(self):
        # Accepting logs and creating a batch must increment aggregate_batches.
        from volcengine.tls.producer.producer import TLSProducer
        from volcengine.tls.tls_requests import PutLogsV2LogContent
        cfg = ProducerConfig("ep", "region", "akid", "seckey", None,
                            metrics_level="core")
        p = TLSProducer(cfg)
        logs = [PutLogsV2LogContent(time=1, log_dict={"k": "v"}) for _ in range(3)]
        p.send_logs_v2(None, "topic", None, None, logs, None)
        snap = p.stats_state.get_stats()
        self.assertGreaterEqual(snap.aggregate_batches, 1)
        # ingress backlog reflects the owned-but-unsent group.
        self.assertGreaterEqual(snap.ingress_queue.current_items, 1)


class QueueStatsSchemaTest(unittest.TestCase):
    """Item 7: QueueStats JSON keys are high_watermark_items/bytes (plan §8.2),
    NOT lifetime_high_watermark_*."""

    def test_to_dict_uses_plan_names(self):
        q = QueueStats(current_items=5, bounded=True, high_watermark_items=9,
                       high_watermark_bytes=1024)
        d = q.to_dict()
        self.assertIn("high_watermark_items", d)
        self.assertIn("high_watermark_bytes", d)
        self.assertNotIn("lifetime_high_watermark_items", d)
        self.assertNotIn("lifetime_high_watermark_bytes", d)
        self.assertEqual(d["high_watermark_items"], 9)
        self.assertEqual(d["high_watermark_bytes"], 1024)


class LevelLatencyEndToEndTest(unittest.TestCase):
    """Only Detailed collects latency histograms."""

    def _producer_config(self, metrics_level):
        from volcengine.tls.producer.batch_semaphore import MemoryLimiter
        from volcengine.tls._stats.producer_state import ProducerStatsState
        cfg = ProducerConfig("endpoint", "region", "akid", "seckey", None,
                            metrics_level=metrics_level)
        cfg.max_block_ms = 0
        cfg.valid_config()
        cfg.memory_limiter = MemoryLimiter(cfg.max_producer_memory_bytes,
                                           cfg.total_size_in_bytes)
        cfg.stats_state = ProducerStatsState(
            metrics_level=cfg.metrics_level,
            instance_id="p-off-lat", sdk_version="v",
            memory_limiter=cfg.memory_limiter, max_sender_count=cfg.max_thread_count)
        return cfg

    def _run_producer_task(self, metrics_level):
        from volcengine.tls.log_pb2 import LogGroup
        from volcengine.tls.producer.producer_model import BatchLog
        from volcengine.tls.producer.retry_queue import RetryQueue
        from volcengine.tls.producer.send_batch_task import SendBatchTask

        class _Resp:
            request_id = "r"

        class _Client:
            def put_logs(self, _req):
                return _Resp()

            def set_retry_policy(self, _p):
                pass

        cfg = self._producer_config(metrics_level)
        group = LogGroup()
        log = group.logs.add()  # pylint: disable=no-member
        log.time = 1
        c = log.contents.add()
        c.key, c.value = "k", "v"
        batch = BatchLog(BatchLog.BatchKey(None, "topic", None, None), cfg)
        batch.try_add(group, 64, None)
        task = SendBatchTask(batch, cfg, cfg.memory_limiter, _Client(),
                             RetryQueue(), None)
        task.run()
        return cfg.stats_state.get_stats()

    def test_producer_off_omits_latency_and_business(self):
        snap = self._run_producer_task("off")
        d = snap.to_dict()
        self.assertNotIn("send_call_duration_ms", d)
        self.assertNotIn("accepted_logs", d)
        self.assertNotIn("accepted_logs", snap)
        self.assertTrue(d["metrics_disabled"])

    def test_producer_detailed_records_fixed_latency(self):
        snap = self._run_producer_task("detailed")
        d = snap.to_dict()
        self.assertIn("send_call_duration_ms", d)
        self.assertIn("batch_delivery_duration_ms", d)
        self.assertGreaterEqual(snap.get("send_call_duration_ms").count, 1)
        self.assertIn("accepted_logs", snap)
        self.assertFalse(d["metrics_disabled"])

    def test_consumer_off_omits_latency_and_business(self):
        st = ConsumerStatsState("off", "c", "v")
        st.observe_ms("fetch_call_duration", 5)
        st.observe_ms("process_duration", 8)
        st.observe_ms("checkpoint_call_duration", 2)
        snap = st.get_stats()
        d = snap.to_dict()
        self.assertNotIn("fetch_call_duration_ms", d)
        self.assertNotIn("checkpoint_call_duration_ms", d)
        self.assertNotIn("fetch_calls", snap)
        self.assertTrue(d["metrics_disabled"])


class LifecycleAndSaturationTest(unittest.TestCase):
    """Item 8: lifecycle contracts + u64 saturation of derived owned counters."""

    def test_get_stats_before_start(self):
        st = ProducerStatsState("core", "p", "v")
        snap = st.get_stats()
        self.assertEqual(snap.state, "new")
        self.assertEqual(snap.consistency, "weak")
        st = ProducerStatsState("core", "p", "v")
        st.mark_started()
        st.freeze()
        a = st.get_stats()
        st.freeze()  # repeated
        b = st.get_stats()
        self.assertIs(a, b)
        self.assertEqual(a.consistency, "final")
        self.assertEqual(a.state, "closed")

    def test_final_snapshot_identical_across_reads(self):
        st = ConsumerStatsState("core", "c", "v")
        st.mark_started()
        st.freeze()
        self.assertEqual(st.get_stats().to_dict(), st.get_stats().to_dict())

    def test_latency_only_freeze(self):
        st = ProducerStatsState("detailed", "p", "v")
        st.observe_ms("send_call_duration", 4)
        st.mark_started()
        st.freeze()
        d = st.get_stats().to_dict()
        self.assertEqual(d["consistency"], "final")
        self.assertIn("send_call_duration_ms", d)
        self.assertFalse(d["metrics_disabled"])

    def test_owned_derived_saturates_u64(self):
        st = ProducerStatsState("core", "p", "v")
        # accepted beyond u64 max, no terminals -> owned should saturate and flag.
        st.on_accepted(UINT64_MAX + 100, 5)
        snap = st.get_stats()
        self.assertEqual(snap.owned_logs, UINT64_MAX)
        self.assertTrue(snap.counter_saturated)


class QueueGaugeConcurrencyTest(unittest.TestCase):
    """Barrier-controlled race over the new ingress/send gauges: exact final
    values and never-negative under concurrent add/release + reads."""

    def test_ingress_send_gauges_race(self):
        st = ProducerStatsState("core", "p", "v", max_sender_count=8)
        st.mark_started()
        n, per = 8, 4000
        # workers + reader + main coordinator
        start = threading.Barrier(n + 2)
        errors = []

        def worker():
            start.wait()
            try:
                for _ in range(per):
                    st.on_ingress_add(1)
                    st.on_send_enqueue()
                    st.on_send_dequeue()
                    st.on_ingress_release(1)
            except Exception as e:  # pragma: no cover
                errors.append(e)

        def reader():
            start.wait()
            for _ in range(3000):
                snap = st.get_stats()
                # gauges must never read negative
                if snap.ingress_queue.current_items < 0 or snap.send_queue.current_items < 0:
                    errors.append(AssertionError("negative gauge"))
                    return

        threads = [threading.Thread(target=worker) for _ in range(n)]
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
        # equal adds and releases -> back to zero, high watermark >= 1
        self.assertEqual(snap.ingress_queue.current_items, 0)
        self.assertEqual(snap.send_queue.current_items, 0)
        self.assertGreaterEqual(snap.ingress_queue.high_watermark_items, 1)

    def test_shard_task_gauge_race(self):
        st = ConsumerStatsState("core", "c", "v")
        st.mark_started()
        n, per = 6, 3000
        start = threading.Barrier(n + 1)

        def worker():
            start.wait()
            for _ in range(per):
                st.on_shard_task_submitted()
                st.on_shard_task_started()
                st.on_shard_task_done()

        threads = [threading.Thread(target=worker) for _ in range(n)]
        for t in threads:
            t.start()
        start.wait()
        for t in threads:
            t.join()
        c = st.get_stats().to_dict()
        self.assertEqual(c["shard_tasks_in_flight"], 0)
        self.assertEqual(c["shard_tasks_submitted"], n * per)
        self.assertEqual(c["shard_tasks_started"], n * per)
        self.assertEqual(c["shard_tasks_completed"], n * per)


if __name__ == "__main__":
    unittest.main()
