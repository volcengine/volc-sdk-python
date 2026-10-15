# coding=utf-8
"""Producer local health stats wiring and conservation semantics.

Uses an offline fake transport so no network is required. Drives SendBatchTask
directly (as the executor would) to validate accept/terminal/retry/callback
accounting and the accepted = terminal + owned conservation identity.
"""
from __future__ import absolute_import

import unittest
import inspect
import threading

from volcengine.tls.log_pb2 import LogGroup
from volcengine.tls._stats.counters import PRODUCER_COUNTER_KEYS
from volcengine.tls._stats.state import _CounterBank
from volcengine.tls.producer.batch_semaphore import MemoryLimiter
from volcengine.tls.producer.log_dispatcher import LogDispatcher
from volcengine.tls.producer.producer import TLSProducer
from volcengine.tls.producer.producer_model import BatchLog, ProducerConfig
from volcengine.tls.producer.retry_queue import RetryQueue
from volcengine.tls.producer.send_batch_task import SendBatchTask
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import PutLogsV2LogContent


class _FakeResponse:
    request_id = "request-id"


class _FakeClient:
    def __init__(self, exception=None):
        self.calls = 0
        self.exception = exception
        self.retry_policy = None

    def put_logs(self, _request):
        self.calls += 1
        if self.exception is not None:
            raise self.exception
        return _FakeResponse()

    def set_retry_policy(self, policy):
        self.retry_policy = policy


class _RecordingCallback:
    def __init__(self, raise_exc=False):
        self.results = []
        self.raise_exc = raise_exc

    def on_complete(self, result):
        self.results.append(result)
        if self.raise_exc:
            raise RuntimeError("callback boom")


class _BlockingCounterBank(_CounterBank):
    """Pause the first counter update to test the collection lock boundary."""

    def __init__(self, size):
        super(_BlockingCounterBank, self).__init__(size)
        self.entered = threading.Event()
        self.release = threading.Event()

    def add(self, idx, delta):
        self.entered.set()
        if not self.release.wait(2):
            raise AssertionError("counter update was not released")
        return super(_BlockingCounterBank, self).add(idx, delta)


def _cfg(metrics_level="core"):
    config = ProducerConfig(
        "endpoint", "region", "akid", "seckey", None,
        metrics_level=metrics_level)
    config.max_block_ms = 0
    config.valid_config()
    return config


def _cfg_with_state(metrics_level="core"):
    """Standalone config + memory limiter + stats_state, as TLSProducer wires."""
    from volcengine.tls._stats.producer_state import ProducerStatsState
    config = _cfg(metrics_level)
    config.memory_limiter = MemoryLimiter(config.max_producer_memory_bytes,
                                          config.total_size_in_bytes)
    config.stats_state = ProducerStatsState(
        metrics_level=config.metrics_level,
        instance_id="producer-test-1", sdk_version="test",
        memory_limiter=config.memory_limiter, max_sender_count=config.max_thread_count)
    return config


def _log_group(n=1, value="v"):
    group = LogGroup()
    for _ in range(n):
        log = getattr(group, "logs").add()
        log.time = 1
        content = log.contents.add()
        content.key = "k"
        content.value = value
    return group


def _tls_exception(http_code):
    e = TLSException(error_code="E", error_message="failed")
    e.http_code = http_code
    e.request_id = "request-id"
    return e


def _assert_conservation(test, snap):
    d = snap.to_dict()
    test.assertEqual(
        d["accepted_logs"],
        d["terminal_success_logs"] + d["terminal_failure_logs"]
        + d["terminal_dropped_logs"] + d["owned_logs"])
    test.assertEqual(
        d["accepted_groups"],
        d["terminal_success_groups"] + d["terminal_failure_groups"]
        + d["terminal_dropped_groups"] + d["owned_groups"])


class ProducerConfigTest(unittest.TestCase):
    def test_defaults_off(self):
        c = ProducerConfig("e", "r", "akid", "seckey")
        c.valid_config()
        self.assertEqual(c.metrics_level, "off")

    def test_positional_arguments(self):
        c = ProducerConfig("e", "r", "akid", "seckey", None, None)
        c.valid_config()
        self.assertEqual(c.client_config.endpoint, "e")
        detailed = ProducerConfig("e", "r", "akid", "seckey", None, None, "detailed")
        detailed.valid_config()
        self.assertEqual(detailed.metrics_level, "detailed")

    def test_invalid_level_raises(self):
        with self.assertRaises(ValueError):
            ProducerConfig(
                "e", "r", "akid", "seckey", metrics_level="loud")

    def test_collection_argument_follows_credentials(self):
        params = inspect.signature(ProducerConfig.__init__).parameters
        self.assertEqual(list(params)[-3:], ["token", "api_key", "metrics_level"])
        self.assertEqual(params["metrics_level"].default, "off")

    def test_health_switches_normalized_and_frozen_at_construction(self):
        c = ProducerConfig(
            "e", "r", "akid", "seckey",
            metrics_level="CORE")
        self.assertEqual(c.metrics_level, "core")
        with self.assertRaises(AttributeError):
            c.metrics_level = "off"


class ProducerDispatcherStatsTest(unittest.TestCase):
    def test_do_add_off_does_not_fetch_stats_token(self):
        class _OffStats:
            enabled = False

            def __init__(self):
                self.token_calls = 0

            def token(self):
                self.token_calls += 1
                return 99

        stats = _OffStats()
        dispatcher = LogDispatcher.__new__(LogDispatcher)
        dispatcher.stats_state = stats
        dispatcher.closed = True

        with self.assertRaises(TLSException):
            dispatcher.do_add(None, "topic", None, None, _log_group(), None)
        self.assertEqual(stats.token_calls, 0)


class ProducerStatsEventTest(unittest.TestCase):
    def test_group_accept_combines_new_batch_and_callback_updates(self):
        config = _cfg_with_state()
        stats = config.stats_state
        token = stats.token()

        stats.on_group_accepted(2, new_batch=True, has_callback=True, token=token)
        stats.on_group_accepted(3, new_batch=False, has_callback=False, token=token)

        d = stats.get_stats().to_dict()
        self.assertEqual(d["accepted_logs"], 5)
        self.assertEqual(d["accepted_groups"], 2)
        self.assertEqual(d["owned_logs"], 5)
        self.assertEqual(d["owned_groups"], 2)
        self.assertEqual(d["aggregate_batches"], 1)
        self.assertEqual(d["aggregate_groups"], 2)
        self.assertEqual(d["callbacks_pending"], 1)
        self.assertEqual(d["ingress_queue"]["current_items"], 2)
        self.assertEqual(d["ingress_queue"]["high_watermark_items"], 2)
        self.assertEqual(d["aggregate_queue"]["current_items"], 1)
        self.assertEqual(d["aggregate_queue"]["high_watermark_items"], 1)
        self.assertEqual(d["callback_queue"]["current_items"], 1)
        self.assertEqual(d["callback_queue"]["high_watermark_items"], 1)

    def test_group_accept_is_one_atomic_observation(self):
        config = _cfg_with_state()
        stats = config.stats_state
        bank = _BlockingCounterBank(len(PRODUCER_COUNTER_KEYS))
        stats._bank = bank
        accepted = threading.Thread(
            target=lambda: stats.on_group_accepted(
                2, new_batch=True, has_callback=True, token=stats.token()))
        accepted.start()
        self.assertTrue(bank.entered.wait(1))

        snapshot_done = threading.Event()
        snapshots = []

        def read_snapshot():
            snapshots.append(stats.get_stats().to_dict())
            snapshot_done.set()

        reader = threading.Thread(target=read_snapshot)
        reader.start()
        self.assertFalse(snapshot_done.wait(0.1))

        bank.release.set()
        accepted.join(2)
        reader.join(2)
        self.assertFalse(accepted.is_alive())
        self.assertTrue(snapshot_done.is_set())
        d = snapshots[0]
        self.assertEqual(d["accepted_logs"], 2)
        self.assertEqual(d["accepted_groups"], 1)
        self.assertEqual(d["aggregate_batches"], 1)
        self.assertEqual(d["aggregate_groups"], 1)
        self.assertEqual(d["owned_logs"], 2)
        self.assertEqual(d["owned_groups"], 1)
        self.assertEqual(d["callbacks_pending"], 1)
        self.assertEqual(d["ingress_queue"]["current_items"], 1)
        self.assertEqual(d["aggregate_queue"]["current_items"], 1)
        self.assertEqual(d["callback_queue"]["current_items"], 1)

    def test_group_accept_rejects_stale_token_atomically(self):
        config = _cfg_with_state()
        stats = config.stats_state
        stats.mark_started()
        stale_token = stats.token()
        stats.set_metrics_level("off")
        stats.set_metrics_level("core")
        self.assertNotEqual(stats.token(), stale_token)

        stats.on_group_accepted(
            4, new_batch=True, has_callback=True, token=stale_token)

        d = stats.get_stats().to_dict()
        for key in (
                "accepted_logs", "accepted_groups", "owned_logs", "owned_groups",
                "aggregate_batches", "aggregate_groups", "callbacks_pending"):
            self.assertEqual(d[key], 0)
        for queue in ("ingress_queue", "aggregate_queue", "callback_queue"):
            self.assertEqual(d[queue]["current_items"], 0)
        self.assertEqual(d["ingress_queue"]["high_watermark_items"], 0)
        self.assertEqual(d["aggregate_queue"]["high_watermark_items"], 0)
        self.assertEqual(d["callback_queue"]["high_watermark_items"], 0)


class ProducerGetStatsLifecycleTest(unittest.TestCase):
    def test_get_stats_before_start(self):
        p = TLSProducer(_cfg())
        snap = p.stats_state.get_stats()
        self.assertEqual(snap.component_type, "producer")
        self.assertEqual(snap.state, "new")
        self.assertEqual(snap.metrics_level, "core")

    def test_off_producer_snapshot_valid(self):
        p = TLSProducer(_cfg(metrics_level="off"))
        d = p.stats_state.get_stats().to_dict()
        self.assertTrue(d["metrics_disabled"])
        self.assertNotIn("accepted_logs", d)


class ProducerAcceptTest(unittest.TestCase):
    def test_accept_counts_logs_and_groups(self):
        p = TLSProducer(_cfg())
        logs = [PutLogsV2LogContent(time=1, log_dict={"k": "v"}) for _ in range(5)]
        p.send_logs_v2(None, "topic", None, None, logs, None)
        snap = p.stats_state.get_stats()
        self.assertEqual(snap.accepted_logs, 5)
        self.assertEqual(snap.accepted_groups, 1)
        self.assertEqual(snap.owned_logs, 5)  # nothing sent yet
        _assert_conservation(self, snap)

    def test_reject_invalid_not_accepted(self):
        p = TLSProducer(_cfg())
        big = "a" * (ProducerConfig.MAX_BATCH_SIZE + 4096)
        with self.assertRaises(TLSException):
            p.send_log_v2(None, "topic", None, None,
                          PutLogsV2LogContent(time=1, log_dict={"k": big}), None)
        snap = p.stats_state.get_stats()
        self.assertEqual(snap.accepted_logs, 0)
        self.assertEqual(snap.rejected_invalid, 1)


class ProducerTerminalTest(unittest.TestCase):
    def _run_task(self, config, callback=None, client=None):
        limiter = config.memory_limiter
        batch = BatchLog(BatchLog.BatchKey(None, "topic", None, None), config)
        batch.try_add(_log_group(3), 64, callback)
        # simulate accept accounting the dispatcher would have done
        config.stats_state.on_accepted(logs=3, groups=1)
        task = SendBatchTask(batch, config, limiter, client or _FakeClient(),
                             RetryQueue(), None)
        task.run()
        return batch

    def test_success_terminal(self):
        config = _cfg_with_state(metrics_level="detailed")
        cb = _RecordingCallback()
        self._run_task(config, cb)
        snap = config.stats_state.get_stats()
        self.assertEqual(snap.terminal_success_logs, 3)
        self.assertEqual(snap.terminal_success_groups, 1)
        self.assertEqual(snap.terminal_success_batches, 1)
        self.assertEqual(snap.send_calls_success, 1)
        self.assertEqual(snap.owned_logs, 0)
        self.assertEqual(snap.callbacks_success, 1)
        _assert_conservation(self, snap)
        # histogram observed
        self.assertGreaterEqual(snap.get("send_call_duration_ms").count, 1)
        self.assertGreaterEqual(snap.get("batch_delivery_duration_ms").count, 1)

    def test_nonretriable_failure_terminal(self):
        config = _cfg_with_state()
        client = _FakeClient(exception=_tls_exception(400))  # permanent
        cb = _RecordingCallback()
        self._run_task(config, cb, client=client)
        snap = config.stats_state.get_stats()
        self.assertEqual(snap.terminal_failure_logs, 3)
        self.assertEqual(snap.send_calls_failure, 1)
        self.assertEqual(snap.owned_logs, 0)
        _assert_conservation(self, snap)

    def test_retriable_then_scheduled(self):
        config = _cfg_with_state()
        client = _FakeClient(exception=_tls_exception(500))  # server -> retry
        limiter = config.memory_limiter
        batch = BatchLog(BatchLog.BatchKey(None, "topic", None, None), config)
        batch.try_add(_log_group(3), 64, None)
        config.stats_state.on_accepted(logs=3, groups=1)
        rq = RetryQueue()
        task = SendBatchTask(batch, config, limiter, client, rq, None)
        task.run()
        snap = config.stats_state.get_stats()
        # retriable failure schedules a retry; not yet terminal
        self.assertEqual(snap.retries_scheduled, 1)
        self.assertEqual(snap.terminal_failure_logs, 0)
        self.assertEqual(snap.owned_logs, 3)
        _assert_conservation(self, snap)

    def test_callback_exception_still_terminal(self):
        config = _cfg_with_state()
        cb = _RecordingCallback(raise_exc=True)
        # callback raising must not corrupt terminal accounting
        try:
            self._run_task(config, cb)
        except Exception:
            pass
        snap = config.stats_state.get_stats()
        self.assertEqual(snap.terminal_success_logs, 3)
        self.assertEqual(snap.owned_logs, 0)
        _assert_conservation(self, snap)


class ProducerCloseTest(unittest.TestCase):
    def test_close_settles_owned_to_zero_and_freezes(self):
        # Inject a succeeding fake client so close drains pending batches to
        # terminal success; owned must reach 0 and the snapshot freezes final.
        p = TLSProducer(_cfg())
        p.dispatcher.client = _FakeClient()
        p.mover.client = _FakeClient()
        logs = [PutLogsV2LogContent(time=1, log_dict={"k": "v"}) for _ in range(4)]
        p.send_logs_v2(None, "topic", None, None, logs, None)
        p.start()
        p.close(timeout_ms=3000)
        snap = p.stats_state.get_stats()
        self.assertEqual(snap.state, "closed")
        self.assertEqual(snap.consistency, "final")
        self.assertEqual(snap.owned_logs, 0)
        _assert_conservation(self, snap)

    def test_settle_owned_on_close_attributes_force_close(self):
        # Directly exercise the residual-owned settlement path: accepted with no
        # terminal -> close settles the residual as dropped(force_close).
        config = _cfg_with_state()
        st = config.stats_state
        st.on_accepted(logs=4, groups=1)
        # emulate what TLSProducer.close does after workers stop
        st.mark_closing()
        snap0 = st.get_stats()
        owned_logs, owned_groups = snap0.owned_logs, snap0.owned_groups
        st.on_terminal("dropped", owned_logs, owned_groups)
        st.on_dropped_reason("force_close", owned_logs, owned_groups)
        st.freeze()
        snap = st.get_stats()
        self.assertEqual(snap.owned_logs, 0)
        self.assertEqual(snap.terminal_dropped_logs, 4)
        self.assertEqual(snap.dropped_force_close_logs, 4)
        _assert_conservation(self, snap)

    def test_final_snapshot_identical(self):
        p = TLSProducer(_cfg())
        p.dispatcher.client = _FakeClient()
        p.mover.client = _FakeClient()
        p.start()
        p.close(timeout_ms=3000)
        s1 = p.stats_state.get_stats()
        s2 = p.stats_state.get_stats()
        self.assertIs(s1, s2)


class ProducerMemoryAndRolesTest(unittest.TestCase):
    def test_memory_payload_and_high_watermark_accurate(self):
        # Review fix (M2): payload_bytes is payload-only used, and
        # high_watermark_bytes is a true lifetime peak (not the instantaneous
        # value). Acquire then release; HWM must retain the peak.
        config = _cfg_with_state()
        ml = config.memory_limiter
        st = config.stats_state
        ml.acquire_payload(5000, 0, generation=st.token())
        peak_used = st.get_stats().memory.accounted_used_bytes
        self.assertGreaterEqual(peak_used, 5000)
        ml.release_payload(5000, generation=st.token())
        snap = st.get_stats().memory
        # after release, used drops but HWM keeps the peak
        self.assertLess(snap.accounted_used_bytes, peak_used)
        self.assertGreaterEqual(snap.high_watermark_bytes, 5000)
        # payload_bytes reflects payload-only used (0 after full release)
        self.assertEqual(snap.payload_bytes, snap.accounted_used_bytes)

    def test_sender_role_running_not_false_underprovisioned(self):
        # Review fix (M3): sender.running must not be a 0/1 dispatcher flag
        # against expected=max_sender_count. Idle pool => running 0; while a
        # send is in-flight => running == in_flight (<= expected).
        config = _cfg_with_state()
        st = config.stats_state
        st.mark_started()
        roles = {r.role: r for r in st.get_stats().worker_roles}
        self.assertIn("sender", roles)
        self.assertNotIn("dispatcher", roles)  # no fake dispatcher thread
        sender = roles["sender"]
        self.assertEqual(sender.running, 0)   # idle pool, honest 0
        self.assertLessEqual(sender.running, sender.expected)
        # with an executing sender task, running tracks SDK task wrappers
        st.on_sender_task_submitted()
        st.on_sender_task_start()
        roles2 = {r.role: r for r in st.get_stats().worker_roles}
        self.assertEqual(roles2["sender"].running, 1)
        self.assertEqual(roles2["sender"].in_flight, 1)
        self.assertGreaterEqual(roles2["sender"].in_flight, 1)
        st.on_sender_task_end()
        st.on_sender_task_done()


if __name__ == "__main__":
    unittest.main()
