# coding=utf-8
"""Consumer local health stats wiring and accounting semantics.

Fully offline: fake TLSService + LogConsumer driven directly through its state
machine. Validates fetch/held/process/checkpoint accounting, once-release under
success/exception/revoke, distinct-shard checkpoint pending, and freeze.
"""
from __future__ import absolute_import

import inspect
import unittest

from volcengine.tls.log_pb2 import LogGroupList, LogGroup
from volcengine.tls.data import ConsumeShard
from volcengine.tls.consumer.consumer_model import ConsumerConfig, CheckpointInfo
from volcengine.tls.consumer.log_consumer import LogConsumer
from volcengine.tls.consumer.checkpoint_manager import CheckpointManager
from volcengine.tls._stats.consumer_state import ConsumerStatsState
from volcengine.tls.tls_exception import TLSException


class _FakeConsumeResp:
    def __init__(self, log_group_list, cursor):
        self._lgl = log_group_list
        self._cursor = cursor

    def get_pb_message(self):
        return self._lgl

    def get_x_tls_cursor(self):
        return self._cursor


class _FakeService:
    def __init__(self, resp=None, exc=None):
        self.resp = resp
        self.exc = exc
        self.modify_calls = 0
        self.modify_exc = None

    def consume_logs(self, _req):
        if self.exc is not None:
            raise self.exc
        return self.resp

    def modify_checkpoint(self, _req):
        self.modify_calls += 1
        if self.modify_exc is not None:
            raise self.modify_exc


class _Processor:
    def __init__(self, raise_exc=False):
        self.calls = 0
        self.raise_exc = raise_exc

    def process(self, topic_id, shard_id, log_group_list):
        self.calls += 1
        if self.raise_exc:
            raise RuntimeError("process boom")


class _FakeConsumer:
    """Minimal holder exposing the attributes LogConsumer/CheckpointManager read."""

    def __init__(self, metrics_level="core", processor=None,
                 service=None):
        self.consumer_config = ConsumerConfig(
            "proj", "grp", ["topic"], "consumer-1",
            metrics_level=metrics_level)
        self.consumer_config.validate()
        import logging
        self.logger = logging.getLogger("test-consumer")
        self.tls_service = service or _FakeService()
        self.log_processor = processor or _Processor()
        self.stats_state = ConsumerStatsState(
            metrics_level=self.consumer_config.metrics_level,
            instance_id="consumer-test-1", sdk_version="test")
        self.checkpoint_manager = CheckpointManager(self)


def _lgl(num_groups=1, logs_per_group=3):
    lgl = LogGroupList()
    for _ in range(num_groups):
        g = lgl.log_groups.add()  # pylint: disable=no-member
        for _ in range(logs_per_group):
            log = g.logs.add()
            log.time = 1
            c = log.contents.add()
            c.key = "k"
            c.value = "v"
    return lgl


class ConsumerConfigTest(unittest.TestCase):
    def test_off_fetch_and_process_do_not_scan_logs_for_statistics(self):
        class Group(object):
            @property
            def logs(self):
                raise AssertionError("Off collection scanned payload logs")

        payload = type("Payload", (), {"log_groups": [Group()]})()
        service = _FakeService(resp=_FakeConsumeResp(payload, "next"))
        consumer = _FakeConsumer(metrics_level="off", service=service)
        worker = LogConsumer(consumer, ConsumeShard("topic", 0))
        worker.fetch_data()
        worker.consume()
        self.assertEqual(consumer.log_processor.calls, 1)

    def test_defaults_off(self):
        c = ConsumerConfig("p", "g", ["t"], "n")
        c.validate()
        self.assertEqual(c.metrics_level, "off")

    def test_positional_arguments(self):
        c = ConsumerConfig("p", "g", ["t"], "n", "begin", 20, 200, 5, 100, False, 15)
        c.validate()
        self.assertEqual(c.consumer_name, "n")

    def test_invalid_level_raises(self):
        with self.assertRaises(ValueError):
            ConsumerConfig(
                "p", "g", ["t"], "n", metrics_level="loud")

    def test_metrics_level_normalized_and_frozen_at_construction(self):
        params = inspect.signature(ConsumerConfig.__init__).parameters
        self.assertEqual(list(params)[-2:], ["compression", "metrics_level"])
        c = ConsumerConfig(
            "p", "g", ["t"], "n",
            metrics_level="CORE")
        self.assertEqual(c.metrics_level, "core")
        with self.assertRaises(AttributeError):
            c.metrics_level = "off"

class ConsumerFetchProcessTest(unittest.TestCase):
    def test_fetch_counts_and_held_release_on_success(self):
        svc = _FakeService(resp=_FakeConsumeResp(_lgl(2, 3), "cursor-1"))
        consumer = _FakeConsumer(metrics_level="detailed", service=svc)
        lc = LogConsumer(consumer, ConsumeShard("topic", 0))
        lc.fetch_data()
        st = consumer.stats_state.get_stats()
        self.assertEqual(st.fetch_calls, 1)
        self.assertEqual(st.fetched_log_groups, 2)
        self.assertEqual(st.fetched_logs, 6)
        self.assertEqual(st.held_batch_references, 1)  # held after fetch
        # process
        lc.consume()
        st2 = consumer.stats_state.get_stats()
        self.assertEqual(st2.process_attempts, 1)
        self.assertEqual(st2.processed_success_groups, 2)
        self.assertEqual(st2.processed_success_logs, 6)
        self.assertEqual(st2.held_batch_references, 0)  # released after consume
        self.assertEqual(st2.ready_to_process, 0)
        # histograms observed
        self.assertGreaterEqual(st2.get("fetch_call_duration_ms").count, 1)
        self.assertGreaterEqual(st2.get("process_duration_ms").count, 1)
        self.assertGreaterEqual(st2.get("dispatch_delay_ms").count, 1)

    def test_empty_fetch_no_held_leak(self):
        svc = _FakeService(resp=_FakeConsumeResp(_lgl(0, 0), "cursor-1"))
        consumer = _FakeConsumer(service=svc)
        lc = LogConsumer(consumer, ConsumeShard("topic", 0))
        lc.fetch_data()
        lc.consume()
        st = consumer.stats_state.get_stats()
        self.assertEqual(st.fetch_calls, 1)
        self.assertEqual(st.held_batch_references, 0)
        self.assertEqual(st.process_attempts, 0)  # empty -> no process

    def test_process_exception_keeps_held_for_retry_and_counts_attempt(self):
        svc = _FakeService(resp=_FakeConsumeResp(_lgl(1, 2), "cursor-1"))
        consumer = _FakeConsumer(service=svc, processor=_Processor(raise_exc=True))
        lc = LogConsumer(consumer, ConsumeShard("topic", 0))
        lc.fetch_data()
        with self.assertRaises(RuntimeError):
            lc.consume()
        st = consumer.stats_state.get_stats()
        self.assertEqual(st.process_attempts, 1)
        self.assertEqual(st.processed_success_logs, 0)  # failed
        # The worker returns to READY_TO_CONSUME and retries this same batch, so
        # ownership remains held until success or explicit revoke/stop.
        self.assertEqual(st.held_batch_references, 1)
        lc.release_held_on_revoke()
        self.assertEqual(
            consumer.stats_state.get_stats().held_batch_references, 0)

    def test_fetch_exception_counts_call_and_no_held(self):
        svc = _FakeService(exc=TLSException(error_code="E", error_message="x"))
        consumer = _FakeConsumer(service=svc)
        lc = LogConsumer(consumer, ConsumeShard("topic", 0))
        with self.assertRaises(TLSException):
            lc.fetch_data()
        st = consumer.stats_state.get_stats()
        self.assertEqual(st.fetch_calls, 1)
        self.assertEqual(st.held_batch_references, 0)

    def test_revoke_releases_held(self):
        svc = _FakeService(resp=_FakeConsumeResp(_lgl(1, 2), "cursor-1"))
        consumer = _FakeConsumer(service=svc)
        lc = LogConsumer(consumer, ConsumeShard("topic", 0))
        lc.fetch_data()
        self.assertEqual(consumer.stats_state.get_stats().held_batch_references, 1)
        lc.release_held_on_revoke()
        lc.release_held_on_revoke()  # idempotent
        self.assertEqual(consumer.stats_state.get_stats().held_batch_references, 0)


class ConsumerCheckpointTest(unittest.TestCase):
    def test_checkpoint_pending_distinct_shards_and_clear(self):
        consumer = _FakeConsumer()
        cm = consumer.checkpoint_manager
        cm.add_checkpoint(CheckpointInfo("c1", ConsumeShard("topic", 0)))
        cm.add_checkpoint(CheckpointInfo("c1b", ConsumeShard("topic", 0)))  # same shard
        cm.add_checkpoint(CheckpointInfo("c2", ConsumeShard("topic", 1)))
        cp = consumer.stats_state.get_stats().checkpoint_pending
        self.assertEqual(cp.current_items, 2)  # distinct shards
        self.assertEqual(cp.high_watermark_items, 2)
        self.assertIsNone(cp.get("oldest_age_ms"))
        # upload clears
        cm.upload_checkpoint()
        cp2 = consumer.stats_state.get_stats().checkpoint_pending
        self.assertEqual(cp2.current_items, 0)
        self.assertEqual(cp2.high_watermark_items, 2)
        self.assertIsNone(cp2.get("oldest_age_ms"))
        self.assertEqual(consumer.tls_service.modify_calls, 2)
        # checkpoint calls counted
        st = consumer.stats_state.get_stats()
        self.assertEqual(st.checkpoint_calls, 2)
        self.assertEqual(st.checkpoint_failures, 0)

    def test_checkpoint_failure_counted(self):
        consumer = _FakeConsumer()
        consumer.tls_service.modify_exc = TLSException(error_code="E", error_message="x")
        cm = consumer.checkpoint_manager
        cm.add_checkpoint(CheckpointInfo("c1", ConsumeShard("topic", 0)))
        with self.assertRaises(TLSException):
            cm.upload_checkpoint()
        st = consumer.stats_state.get_stats()
        self.assertEqual(st.checkpoint_failures, 1)
        # failed upload keeps the shard pending
        self.assertEqual(st.checkpoint_pending.current_items, 1)
        self.assertIsNone(
            st.checkpoint_pending.get("oldest_age_ms"))

    def test_checkpoint_manager_readd_preserves_pending_and_hwm(self):
        consumer = _FakeConsumer()
        cm = consumer.checkpoint_manager
        cm.add_checkpoint(CheckpointInfo("c0", ConsumeShard("topic", 0)))
        cm.add_checkpoint(CheckpointInfo("c0-new", ConsumeShard("topic", 0)))
        cm.add_checkpoint(CheckpointInfo("c1", ConsumeShard("topic", 1)))
        self.assertEqual(cm.checkpoint_info_map["topic0"].checkpoint, "c0-new")

        pending = consumer.stats_state.get_stats().checkpoint_pending
        self.assertEqual(pending.current_items, 2)
        self.assertEqual(pending.high_watermark_items, 2)
        self.assertIsNone(pending.get("oldest_age_ms"))

        consumer.tls_service.modify_exc = TLSException(
            error_code="E", error_message="x")
        with self.assertRaises(TLSException):
            cm.upload_checkpoint()
        failed = consumer.stats_state.get_stats().checkpoint_pending
        self.assertEqual(len(cm.checkpoint_info_map), 2)
        self.assertEqual(failed.current_items, 2)
        self.assertEqual(failed.high_watermark_items, 2)
        self.assertIsNone(failed.get("oldest_age_ms"))

        consumer.tls_service.modify_exc = None
        cm.upload_checkpoint()
        cleared = consumer.stats_state.get_stats().checkpoint_pending
        self.assertEqual(cm.checkpoint_info_map, {})
        self.assertEqual(cleared.current_items, 0)
        self.assertEqual(cleared.high_watermark_items, 2)
        self.assertIsNone(cleared.get("oldest_age_ms"))

        cm.add_checkpoint(CheckpointInfo("c0-final", ConsumeShard("topic", 0)))
        readded = consumer.stats_state.get_stats().checkpoint_pending
        self.assertEqual(readded.current_items, 1)
        self.assertEqual(readded.high_watermark_items, 2)
        self.assertIsNone(readded.get("oldest_age_ms"))
        cm.upload_checkpoint()
        self.assertEqual(cm.checkpoint_info_map, {})

    def test_private_checkpoint_state_has_no_synthetic_oldest_age(self):
        # The private state does not own the business checkpoint map. It may
        # maintain bounded count/HWM facts but must not invent an oldest age.
        st = ConsumerStatsState("core", "c", "test")
        for i in range(100):
            st.checkpoint_add("shard-%d" % i)
        snap = st.get_stats()
        self.assertEqual(snap.checkpoint_pending.current_items, 100)
        self.assertEqual(snap.checkpoint_pending.high_watermark_items, 100)
        self.assertIsNone(
            snap.checkpoint_pending.get("oldest_age_ms"))


class ConsumerInstanceIdTest(unittest.TestCase):
    def test_instance_id_has_no_business_name(self):
        # Review fix (spec): consumer instance_id must NOT embed consumer_name.
        from volcengine.tls.consumer.consumer import TLSConsumer, LogProcessor

        class _P(LogProcessor):
            def process(self, topic_id, shard_id, log_group_list):
                pass

        cfg = ConsumerConfig("proj", "grp", ["topic"], "my-secret-consumer-name",
                             metrics_level="core")
        consumer = TLSConsumer(cfg, _FakeService(), _P())
        iid = consumer.stats_state.get_stats().instance_id
        self.assertNotIn("my-secret-consumer-name", iid)
        self.assertTrue(iid.startswith("consumer-"))


class ConsumerLifecycleTest(unittest.TestCase):
    def test_get_stats_before_start(self):
        consumer = _FakeConsumer()
        snap = consumer.stats_state.get_stats()
        self.assertEqual(snap.component_type, "consumer")
        self.assertEqual(snap.state, "new")

    def test_off_consumer_snapshot(self):
        consumer = _FakeConsumer(metrics_level="off")
        d = consumer.stats_state.get_stats().to_dict()
        self.assertTrue(d["metrics_disabled"])
        self.assertNotIn("fetch_calls", d)

    def test_freeze_final(self):
        consumer = _FakeConsumer()
        consumer.stats_state.mark_started()
        consumer.stats_state.freeze()
        s1 = consumer.stats_state.get_stats()
        s2 = consumer.stats_state.get_stats()
        self.assertIs(s1, s2)
        self.assertEqual(s1.state, "closed")
        self.assertEqual(s1.consistency, "final")


if __name__ == "__main__":
    unittest.main()
