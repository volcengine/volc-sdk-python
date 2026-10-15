# coding=utf-8
"""Focused producer/consumer conservation, semantics, and freeze tests."""
from __future__ import absolute_import

import json
import logging
import unittest

from volcengine.tls import stats
from volcengine.tls.stats import constants as C
from volcengine.tls._stats.producer_state import ProducerStatsState
from volcengine.tls._stats.consumer_state import ConsumerStatsState
from volcengine.tls.consumer.checkpoint_manager import CheckpointManager
from volcengine.tls.consumer.consumer_model import CheckpointInfo, ConsumerConfig
from volcengine.tls.data import ConsumeShard


class ConstantsTest(unittest.TestCase):
    def test_sdk_identity(self):
        self.assertEqual(stats.SDK_NAME, "volc-sdk-python")
        self.assertEqual(stats.SDK_LANGUAGE, "python")

    def test_normalize(self):
        self.assertEqual(C.normalize_metrics_level("CORE"), "core")
        self.assertEqual(C.normalize_metrics_level(None), "off")
        with self.assertRaises(ValueError):
            C.normalize_metrics_level("bogus")


class ProducerConservationTest(unittest.TestCase):
    def test_accepted_equals_terminal_plus_owned(self):
        st = ProducerStatsState("core", "p", "test")
        st.on_accepted(logs=100, groups=10)
        st.on_terminal("success", 40, 4)
        st.on_terminal("failure", 20, 2)
        st.on_terminal("dropped", 10, 1)
        d = st.get_stats().to_dict()
        self.assertEqual(
            d["accepted_logs"],
            d["terminal_success_logs"] + d["terminal_failure_logs"]
            + d["terminal_dropped_logs"] + d["owned_logs"])
        self.assertEqual(d["owned_logs"], 30)
        self.assertEqual(
            d["accepted_groups"],
            d["terminal_success_groups"] + d["terminal_failure_groups"]
            + d["terminal_dropped_groups"] + d["owned_groups"])

    def test_dropped_reason_partitions_terminal_dropped(self):
        st = ProducerStatsState("core", "p", "test")
        st.on_accepted(50, 5)
        st.on_terminal("dropped", 50, 5)
        st.on_dropped_reason("force_close", 30, 3)
        st.on_dropped_reason("ttl", 20, 2)
        d = st.get_stats().to_dict()
        self.assertEqual(
            d["terminal_dropped_logs"],
            d["dropped_force_close_logs"] + d["dropped_ttl_expired_logs"])
        self.assertEqual(d["owned_logs"], 0)

    def test_gauges_never_negative(self):
        st = ProducerStatsState("core", None, "p", "test")
        # extra send_end / callback_end must not push gauge below zero
        st.on_send_end(success=True)
        st.on_callback_end(success=True)
        d = st.get_stats().to_dict()
        self.assertGreaterEqual(d["send_calls_in_flight"], 0)
        self.assertGreaterEqual(d["callbacks_in_flight"], 0)


class ConsumerSemanticsTest(unittest.TestCase):
    def test_once_release(self):
        st = ConsumerStatsState("core", "0", "test")
        tok = st.acquire_held(logs=10, groups=1)
        self.assertEqual(st.get_stats().held_batch_references, 1)
        st.release_held(tok)
        st.release_held(tok)  # second release is a no-op
        self.assertEqual(st.get_stats().held_batch_references, 0)
        self.assertEqual(st.get_stats().ready_to_process, 0)

    def test_checkpoint_pending_distinct_shards(self):
        class _Service(object):
            def __init__(self):
                self.calls = 0

            def modify_checkpoint(self, _request):
                self.calls += 1

        class _Consumer(object):
            pass

        consumer = _Consumer()
        consumer.consumer_config = ConsumerConfig(
            "project", "group", ["topic"], "consumer", metrics_level="core")
        consumer.consumer_config.validate()
        consumer.tls_service = _Service()
        consumer.logger = logging.getLogger("checkpoint-contract")
        consumer.stats_state = ConsumerStatsState("core", "0", "test")
        consumer.worker_map = {}
        manager = CheckpointManager(consumer)

        manager.add_checkpoint(CheckpointInfo("c0", ConsumeShard("topic", 0)))
        manager.add_checkpoint(CheckpointInfo("c0-new", ConsumeShard("topic", 0)))
        manager.add_checkpoint(CheckpointInfo("c1", ConsumeShard("topic", 1)))
        pending = consumer.stats_state.get_stats().checkpoint_pending
        self.assertEqual(manager.checkpoint_info_map["topic0"].checkpoint, "c0-new")
        self.assertEqual(pending.current_items, 2)
        self.assertEqual(pending.high_watermark_items, 2)
        self.assertIsNone(pending.get("oldest_age_ms"))

        manager.upload_checkpoint()
        cleared = consumer.stats_state.get_stats().checkpoint_pending
        self.assertEqual(manager.checkpoint_info_map, {})
        self.assertEqual(consumer.tls_service.calls, 2)
        self.assertEqual(cleared.current_items, 0)
        self.assertEqual(cleared.high_watermark_items, 2)
        self.assertIsNone(cleared.get("oldest_age_ms"))

    def test_process_attempt_vs_success(self):
        st = ConsumerStatsState("core", "0", "test")
        failed = st.acquire_held(logs=10, groups=1)
        st.on_process_start(failed)
        st.on_process_end(success=False, token=failed)
        succeeded = st.acquire_held(logs=10, groups=1)
        st.on_process_start(succeeded)
        st.on_process_end(success=True, token=succeeded)
        d = st.get_stats().to_dict()
        self.assertEqual(d["process_attempts"], 2)
        self.assertEqual(d["processed_success_groups"], 1)
        self.assertEqual(d["processed_success_logs"], 10)


class LifecycleFreezeTest(unittest.TestCase):
    def test_readable_before_start(self):
        st = ProducerStatsState("core", "p", "test")
        snap = st.get_stats()
        self.assertEqual(snap.state, "new")
        self.assertEqual(snap.consistency, "weak")

    def test_sequence_increments_then_freezes(self):
        st = ProducerStatsState("core", "p", "test")
        s1 = st.get_stats().snapshot_sequence
        s2 = st.get_stats().snapshot_sequence
        self.assertGreater(s2, s1)
        st.freeze()
        f1 = st.get_stats()
        f2 = st.get_stats()
        self.assertIs(f1, f2)
        self.assertEqual(f1.snapshot_sequence, f2.snapshot_sequence)

    def test_final_consistency_and_state(self):
        st = ConsumerStatsState("core", "0", "test")
        st.mark_started()
        st.freeze()
        snap = st.get_stats()
        self.assertEqual(snap.state, "closed")
        self.assertEqual(snap.consistency, "final")

    def test_final_dict_hash_stable(self):
        st = ProducerStatsState("core", "p", "test")
        st.on_accepted(10, 1)
        st.on_terminal("success", 10, 1)
        st.freeze()
        d1 = json.dumps(st.get_stats().to_dict(), sort_keys=True)
        d2 = json.dumps(st.get_stats().to_dict(), sort_keys=True)
        self.assertEqual(d1, d2)


if __name__ == "__main__":
    unittest.main()
