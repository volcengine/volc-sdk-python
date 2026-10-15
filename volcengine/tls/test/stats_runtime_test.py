# coding=utf-8
"""Runtime lifecycle, publication, ownership, and callback regression tests."""
from __future__ import absolute_import

import threading
import time
import unittest
from unittest import mock

from volcengine.tls._stats.histogram import FixedHistogram, FAST_BOUNDS_MS
from volcengine.tls._stats.producer_state import ProducerStatsState
from volcengine.tls.consumer.consumer import TLSConsumer, LogProcessor
from volcengine.tls.consumer.consumer_model import ConsumerConfig
from volcengine.tls.consumer.log_consumer import LogConsumer
from volcengine.tls.data import ConsumeShard
from volcengine.tls.producer.batch_semaphore import MemoryLimiter
from volcengine.tls.producer.producer import TLSProducer
from volcengine.tls.producer.producer_model import (
    BatchLog,
    ProducerConfig,
)
from volcengine.tls.producer.retry_queue import RetryQueue
from volcengine.tls.producer.send_batch_task import SendBatchTask
from volcengine.tls._stats.common import QueueStats
from volcengine.tls.stats.health import evaluate_health
from volcengine.tls.stats.options import StatsOptions
from volcengine.tls.stats.snapshot import project_snapshot
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import PutLogsV2LogContent

from volcengine.tls.test.consumer_stats_test import (
    _FakeConsumeResp,
    _FakeConsumer,
    _FakeService,
    _Processor,
    _lgl,
)
from volcengine.tls.test.producer_stats_test import (
    _FakeClient,
    _RecordingCallback,
    _cfg,
    _cfg_with_state,
    _log_group,
)


class _NoopProcessor(LogProcessor):
    def process(self, topic_id, shard_id, log_group_list):
        pass


class _BlockingProcessor(LogProcessor):
    def __init__(self):
        self.entered = threading.Event()
        self.release = threading.Event()

    def process(self, topic_id, shard_id, log_group_list):
        self.entered.set()
        self.release.wait(2)


class _ImmediateExecutor(object):
    def submit(self, func):
        func()
        return object()


class _RejectingExecutor(object):
    def submit(self, _func):
        raise RuntimeError("executor rejected task")


class _BlockingClient(object):
    def __init__(self, entered, release):
        self.entered = entered
        self.release = release

    def put_logs(self, _request):
        self.entered.set()
        self.release.wait(2)
        return type("Response", (object,), {"request_id": "request-id"})()


class _AliveThread(object):
    def __init__(self):
        self._alive = True

    def join(self, timeout=None):
        pass

    def is_alive(self):
        return self._alive

    def stop(self):
        self._alive = False


class _AliveMover(_AliveThread):
    def close(self):
        pass


class _BlockingRetryQueue(RetryQueue):
    def __init__(self):
        super(_BlockingRetryQueue, self).__init__()
        self.add_entered = threading.Event()
        self.allow_add = threading.Event()
        self.close_called = threading.Event()

    def add_to_retry_queue(self, batch):
        self.add_entered.set()
        self.allow_add.wait(2)
        return super(_BlockingRetryQueue, self).add_to_retry_queue(batch)

    def close(self):
        super(_BlockingRetryQueue, self).close()
        self.close_called.set()


class _PausingBank(object):
    """Delegate counter bank that can pause exactly one increment."""
    def __init__(self, delegate):
        self._delegate = delegate
        self.pause_next_inc = False
        self.inc_entered = threading.Event()
        self.allow_inc = threading.Event()

    def __getattr__(self, name):
        return getattr(self._delegate, name)

    def inc(self, index):
        if self.pause_next_inc:
            self.pause_next_inc = False
            self.inc_entered.set()
            if not self.allow_inc.wait(2):
                raise RuntimeError("timed out waiting to resume counter increment")
        self._delegate.inc(index)


class _BlockingErrorClock(object):
    """Clock that pauses the first post-construction monotonic read."""
    def __init__(self):
        self.calls = 0
        self.error_clock_entered = threading.Event()
        self.allow_error_clock = threading.Event()

    def monotonic_ns(self):
        self.calls += 1
        if self.calls == 2:
            self.error_clock_entered.set()
            if not self.allow_error_clock.wait(2):
                raise RuntimeError("timed out waiting to resume error clock")
        return self.calls * 1000000

    def wall_ms(self):
        return 1


class _StartThread(object):
    starts = 0

    def __init__(self, *args, **kwargs):
        self.alive = False

    def start(self):
        type(self).starts += 1
        if type(self).starts == 2:
            raise RuntimeError("thread start failed")
        self.alive = True

    def join(self, timeout=None):
        self.alive = False

    def is_alive(self):
        return self.alive


def _tls_error(http_code):
    error = TLSException(error_code="E", error_message="failed")
    error.http_code = http_code
    return error


class PublicSnapshotImmutabilityTest(unittest.TestCase):
    def test_private_slots_cannot_be_reassigned_or_deleted(self):
        snap = ProducerStatsState("core", "p", "v").get_stats()
        queue = QueueStats(current_items=1, bounded=False)
        histogram = FixedHistogram(FAST_BOUNDS_MS).snapshot()
        for obj, attr, value in (
                (snap, "_state", "tampered"),
                (queue, "_current_items", 999),
                (histogram, "_count", 999)):
            with self.assertRaises(AttributeError):
                setattr(obj, attr, value)
            with self.assertRaises(AttributeError):
                delattr(obj, attr)

    def test_internal_snapshot_mappings_are_read_only(self):
        snap = ProducerStatsState("core", "p", "v").get_stats()
        with self.assertRaises(TypeError):
            snap._values["accepted_logs"] = 99
        detailed = ProducerStatsState("detailed", "p", "v").get_stats()
        with self.assertRaises(TypeError):
            detailed._values["send_call_duration_ms"] = None


class _BlockingSnapshotState(ProducerStatsState):
    def __init__(self):
        super(_BlockingSnapshotState, self).__init__(
            "core", "p", "v", max_sender_count=1)
        self.live_started = threading.Event()
        self.release_live = threading.Event()
        self.final_started = threading.Event()

    def _build_snapshot(self, is_final):
        if is_final:
            self.final_started.set()
        elif not self.live_started.is_set():
            self.live_started.set()
            self.release_live.wait(2)
        return super(_BlockingSnapshotState, self)._build_snapshot(is_final)


class FinalPublicationRaceTest(unittest.TestCase):
    def test_freeze_cannot_overtake_an_admitted_live_snapshot(self):
        state = _BlockingSnapshotState()
        state.mark_started()
        reader_result = []

        reader = threading.Thread(target=lambda: reader_result.append(state.get_stats()))
        freezer = threading.Thread(target=state.freeze)
        reader.start()
        self.assertTrue(state.live_started.wait(1))
        freezer.start()
        try:
            self.assertFalse(
                state.final_started.wait(0.2),
                "freeze published final while an admitted live snapshot was still building")
        finally:
            state.release_live.set()
        reader.join(2)
        freezer.join(2)
        self.assertFalse(reader.is_alive())
        self.assertFalse(freezer.is_alive())
        final = state.get_stats()
        if reader_result[0].consistency == "final":
            self.assertIs(reader_result[0], final)


class ProducerRuntimeTest(unittest.TestCase):
    def test_error_category_and_age_publish_as_one_observation(self):
        clock = _BlockingErrorClock()
        state = ProducerStatsState(
            "core", "off", "p", "v", max_sender_count=1, clock=clock)
        writer = threading.Thread(
            target=lambda: state.on_send_end(
                False, error_category="transport"))
        snapshots = []
        reader_done = threading.Event()

        def read():
            snapshots.append(state.get_stats())
            reader_done.set()

        writer.start()
        self.assertTrue(clock.error_clock_entered.wait(1))
        reader = threading.Thread(target=read)
        reader.start()
        try:
            self.assertFalse(
                reader_done.wait(0.2),
                "snapshot observed category before its error timestamp")
        finally:
            clock.allow_error_clock.set()
        writer.join(2)
        reader.join(2)
        self.assertFalse(writer.is_alive())
        self.assertFalse(reader.is_alive())
        self.assertEqual(snapshots[0].last_error_category, "transport")
        self.assertIsNotNone(snapshots[0].last_error_age_ms)

    def test_immediate_seal_does_not_leave_ingress_or_break_conservation(self):
        config = _cfg(metrics_level="core")
        config.max_batch_count = 1
        producer = TLSProducer(config)
        original_executor = producer.dispatcher.executor_service
        original_executor.shutdown(wait=False)
        producer.dispatcher.executor_service = _ImmediateExecutor()
        producer.dispatcher.client = _FakeClient()

        producer.send_logs_v2(
            None, "topic", None, None,
            [PutLogsV2LogContent(time=1, log_dict={"k": "v"})], None)
        snap = producer.stats_state.get_stats()
        self.assertEqual(snap.accepted_logs, 1)
        self.assertEqual(snap.terminal_success_logs, 1)
        self.assertEqual(snap.owned_logs, 0)
        self.assertEqual(snap.ingress_queue.current_items, 0)
        self.assertEqual(snap.send_queue.current_items, 0)

    def test_executor_rejection_settles_owned_batch_and_releases_memory(self):
        config = _cfg(metrics_level="core")
        config.max_batch_count = 1
        producer = TLSProducer(config)
        original_executor = producer.dispatcher.executor_service
        original_executor.shutdown(wait=False)
        producer.dispatcher.executor_service = _RejectingExecutor()
        with self.assertRaises(Exception):
            producer.send_logs_v2(
                None, "topic", None, None,
                [PutLogsV2LogContent(time=1, log_dict={"k": "v"})], None)

        snap = producer.stats_state.get_stats()
        self.assertEqual(snap.accepted_logs, 1)
        self.assertEqual(snap.terminal_failure_logs, 1)
        self.assertEqual(snap.owned_logs, 0)
        self.assertEqual(snap.rejected_internal, 0)
        self.assertEqual(snap.last_error_category, "local_resource")
        self.assertIsNotNone(snap.last_error_age_ms)
        self.assertEqual(snap.ingress_queue.current_items, 0)
        self.assertEqual(snap.aggregate_queue.current_items, 0)
        self.assertEqual(snap.send_queue.current_items, 0)
        self.assertEqual(snap.memory.accounted_used_bytes, 0)

    def test_first_memory_rejection_does_not_poison_next_aggregate(self):
        producer = TLSProducer(
            _cfg(metrics_level="core"))
        limiter = MemoryLimiter(64, 64)
        producer.memory_limiter = limiter
        producer.producer_config.memory_limiter = limiter
        producer.dispatcher.memory_limiter = limiter
        producer.dispatcher.memory_lock = limiter
        producer.dispatcher.client = _FakeClient()
        producer.mover.memory_lock = limiter
        producer.mover.client = producer.dispatcher.client
        self.assertTrue(limiter.acquire_payload(64, 0))

        with self.assertRaises(TLSException):
            producer.send_logs_v2(
                None, "topic", None, None,
                [PutLogsV2LogContent(time=1, log_dict={"k": "v"})], None)
        self.assertEqual(producer.stats_state.get_stats().aggregate_batches, 0)

        limiter.release_payload(64)
        producer.send_logs_v2(
            None, "topic", None, None,
            [PutLogsV2LogContent(time=1, log_dict={"k": "v"})], None)
        snap = producer.stats_state.get_stats()
        self.assertEqual(snap.aggregate_batches, 1)
        self.assertEqual(snap.aggregate_queue.current_items, 1)
        producer.close(timeout_ms=1000)

    def test_mover_settles_all_removed_batches_after_submit_rejection(self):
        producer = TLSProducer(
            _cfg(metrics_level="core"))
        producer.mover.executor_service = _RejectingExecutor()
        batches = []
        for index in range(2):
            batch = BatchLog(
                BatchLog.BatchKey(None, "topic-{}".format(index), None, None),
                producer.producer_config)
            batch.try_add(_log_group(1), 32, None)
            producer.stats_state.on_accepted(logs=1, groups=1)
            producer.stats_state.on_ingress_add(1)
            batches.append(batch)
        with self.assertRaises(Exception):
            producer.mover._submit_all(batches)
        snap = producer.stats_state.get_stats()
        self.assertEqual(snap.accepted_logs, 2)
        self.assertEqual(snap.terminal_failure_logs, 2)
        self.assertEqual(snap.owned_logs, 0)
        self.assertEqual(snap.memory.accounted_used_bytes, 0)

    def test_callback_exception_always_releases_payload_memory(self):
        config = _cfg_with_state(metrics_level="core")
        batch = BatchLog(BatchLog.BatchKey(None, "topic", None, None), config)
        batch.try_add(_log_group(1), 64, _RecordingCallback(raise_exc=True))
        config.stats_state.on_accepted(logs=1, groups=1)
        task = SendBatchTask(
            batch, config, config.memory_limiter, _FakeClient(), RetryQueue(), None)
        with self.assertRaises(RuntimeError):
            task.run()
        snap = config.stats_state.get_stats()
        self.assertEqual(snap.owned_logs, 0)
        self.assertEqual(snap.memory.accounted_used_bytes, 0)

    def test_callbacks_are_accounted_one_by_one(self):
        config = _cfg_with_state(
            metrics_level="detailed")
        good = _RecordingCallback()
        bad = _RecordingCallback(raise_exc=True)
        batch = BatchLog(BatchLog.BatchKey(None, "topic", None, None), config)
        batch.try_add(_log_group(1), 32, good)
        batch.try_add(_log_group(1), 32, bad)
        config.stats_state.on_accepted(logs=2, groups=2)
        config.stats_state.on_callback_pending(2)
        task = SendBatchTask(
            batch, config, config.memory_limiter, _FakeClient(), RetryQueue(), None)
        with self.assertRaises(RuntimeError):
            task.run()
        snap = config.stats_state.get_stats()
        self.assertEqual(snap.callbacks_pending, 0)
        self.assertEqual(snap.callbacks_in_flight, 0)
        self.assertEqual(snap.callbacks_success, 1)
        self.assertEqual(snap.callbacks_failure, 1)
        self.assertEqual(
            snap.get("callback_duration_ms").count, 2)

    def test_retry_queue_high_watermark_survives_drain(self):
        producer = TLSProducer(
            _cfg(metrics_level="core"))
        for index in range(2):
            batch = BatchLog(
                BatchLog.BatchKey(None, "topic-{}".format(index), None, None),
                producer.producer_config)
            producer.retry_queue.add_to_retry_queue(batch)
        producer.retry_queue.get_retry_batch(True)
        retry_stats = producer.stats_state.get_stats().retry_queue
        self.assertEqual(retry_stats.current_items, 0)
        self.assertEqual(retry_stats.high_watermark_items, 2)

    def test_memory_stats_snapshot_is_internally_consistent(self):
        limiter = MemoryLimiter(1000, 800)
        self.assertTrue(limiter.acquire_payload(300, 0))
        self.assertTrue(limiter.acquire_temporary(100, 0))
        snapshot = limiter.stats_snapshot()
        self.assertEqual(snapshot["accounted_used_bytes"], 400)
        self.assertEqual(snapshot["payload_bytes"], 300)
        self.assertGreaterEqual(
            snapshot["accounted_used_bytes"], snapshot["payload_bytes"])

    def test_close_before_start_freezes_new_to_closed(self):
        producer = TLSProducer(
            _cfg(metrics_level="core"))
        producer.close(timeout_ms=1000)
        first = producer.stats_state.get_stats()
        producer.close(timeout_ms=1000)
        self.assertEqual(first.state, "closed")
        self.assertEqual(first.consistency, "final")
        self.assertIs(first, producer.stats_state.get_stats())

    def test_close_before_start_drains_accepted_data_and_callback(self):
        producer = TLSProducer(
            _cfg(metrics_level="core"))
        producer.dispatcher.client = _FakeClient()
        producer.mover.client = producer.dispatcher.client
        callback = _RecordingCallback()
        producer.send_logs_v2(
            None, "topic", None, None,
            [PutLogsV2LogContent(time=1, log_dict={"k": "v"})],
            callback)
        pending = producer.stats_state.get_stats()
        self.assertEqual(pending.aggregate_queue.current_items, 1)
        self.assertEqual(pending.callback_queue.current_items, 1)
        producer.close(timeout_ms=1000)
        snap = producer.stats_state.get_stats()
        self.assertEqual(snap.state, "closed")
        self.assertEqual(snap.terminal_success_logs, 1)
        self.assertEqual(snap.owned_logs, 0)
        self.assertEqual(snap.callbacks_pending, 0)
        self.assertEqual(snap.callbacks_success, 1)
        self.assertEqual(snap.aggregate_queue.current_items, 0)
        self.assertEqual(snap.aggregate_queue.high_watermark_items, 1)
        self.assertEqual(snap.callback_queue.current_items, 0)
        self.assertEqual(snap.callback_queue.high_watermark_items, 1)
        self.assertEqual(snap.aggregate_batches, 0)
        self.assertEqual(snap.memory.accounted_used_bytes, 0)
        self.assertEqual(len(callback.results), 1)

    def test_close_timeout_publishes_closing_weak_until_resources_settle(self):
        config = _cfg(metrics_level="core")
        config.max_batch_count = 1
        producer = TLSProducer(config)
        entered = threading.Event()
        release = threading.Event()
        client = _BlockingClient(entered, release)
        producer.dispatcher.client = client
        producer.mover.client = client
        producer.start()
        producer.send_logs_v2(
            None, "topic", None, None,
            [PutLogsV2LogContent(time=1, log_dict={"k": "v"})], None)
        self.assertTrue(entered.wait(1))
        try:
            with self.assertRaises(TLSException):
                producer.close(timeout_ms=10)
            pending = producer.stats_state.get_stats()
            self.assertEqual(pending.state, "closing")
            self.assertEqual(pending.consistency, "weak")
            self.assertEqual(pending.owned_logs, 1)
            self.assertEqual(pending.terminal_dropped_logs, 0)
        finally:
            release.set()
        deadline = time.time() + 3
        while time.time() < deadline:
            if producer.stats_state.get_stats().state == "closed":
                break
            time.sleep(0.01)
        final = producer.stats_state.get_stats()
        self.assertEqual(final.state, "closed")
        self.assertEqual(final.consistency, "final")

    def test_mover_timeout_preserves_running_in_closing_weak(self):
        producer = TLSProducer(_cfg_with_state())
        producer.mover = _AliveMover()
        producer.stats_state.set_mover_running(1)

        with self.assertRaises(TLSException):
            producer.close(timeout_ms=0)

        snap = producer.stats_state.get_stats()
        mover = [role for role in snap.worker_roles
                 if role.role == "mover"][0]
        self.assertEqual(snap.state, "closing")
        self.assertEqual(snap.consistency, "weak")
        self.assertEqual(mover.running, 1)

    def test_close_racing_retry_enqueue_leaves_no_owned_payload(self):
        config = _cfg(metrics_level="core")
        config.max_batch_count = 1
        retry_queue = _BlockingRetryQueue()
        producer = TLSProducer(config)
        producer.retry_queue = retry_queue
        producer.dispatcher.retry_queue = retry_queue
        producer.mover.retry_queue = retry_queue
        client = _FakeClient(exception=_tls_error(429))
        producer.dispatcher.client = client
        producer.mover.client = client
        callback = _RecordingCallback()
        producer.start()
        producer.send_logs_v2(
            None, "topic", None, None,
            [PutLogsV2LogContent(time=1, log_dict={"k": "v"})], callback)
        self.assertTrue(retry_queue.add_entered.wait(1))

        close_errors = []

        def close():
            try:
                producer.close(timeout_ms=2000)
            except Exception as exc:  # pragma: no cover - asserted below
                close_errors.append(exc)

        closer = threading.Thread(target=close)
        closer.start()
        close_observed = retry_queue.close_called.wait(1)
        retry_queue.allow_add.set()
        closer.join(3)

        self.assertTrue(close_observed)
        self.assertFalse(closer.is_alive())
        self.assertEqual(close_errors, [])
        self.assertEqual(len(retry_queue), 0)
        snap = producer.stats_state.get_stats()
        self.assertEqual(snap.owned_logs, 0)
        self.assertEqual(snap.callbacks_pending, 0)
        self.assertEqual(snap.memory.accounted_used_bytes, 0)
        self.assertEqual(snap.terminal_failure_logs, 1)
        self.assertEqual(len(callback.results), 1)

    def test_off_mode_callback_failure_omits_error_category(self):
        config = _cfg_with_state(
            metrics_level="off")
        callback = _RecordingCallback(raise_exc=True)
        batch = BatchLog(
            BatchLog.BatchKey(None, "topic", None, None), config)
        batch.try_add(_log_group(1), 32, callback)
        task = SendBatchTask(
            batch, config, config.memory_limiter,
            _FakeClient(), RetryQueue(), None)

        with self.assertRaises(RuntimeError):
            task.run()

        self.assertEqual(len(callback.results), 1)
        snapshot = config.stats_state.get_stats()
        self.assertIsNone(snapshot.get("last_error_category"))
        self.assertIsNone(snapshot.get("last_error_age_ms"))


class ConsumerRuntimeTest(unittest.TestCase):
    def test_failed_process_restore_is_atomic_with_concurrent_release(self):
        consumer = _FakeConsumer()
        state = consumer.stats_state
        token = state.acquire_held(logs=1, groups=1)
        state.on_process_start(token)
        bank = _PausingBank(state._bank)
        state._bank = bank
        bank.pause_next_inc = True
        restore_errors = []
        release_errors = []
        release_done = threading.Event()

        def restore():
            try:
                state.on_process_end(False, token)
            except Exception as exc:  # pragma: no cover - asserted below
                restore_errors.append(exc)

        def release():
            try:
                state.release_held(token)
            except Exception as exc:  # pragma: no cover - asserted below
                release_errors.append(exc)
            finally:
                release_done.set()

        restorer = threading.Thread(target=restore)
        restorer.start()
        self.assertTrue(bank.inc_entered.wait(1))
        releaser = threading.Thread(target=release)
        releaser.start()
        try:
            self.assertFalse(
                release_done.wait(0.2),
                "release overtook the matching ready counter restoration")
        finally:
            bank.allow_inc.set()
        restorer.join(2)
        releaser.join(2)
        self.assertFalse(restorer.is_alive())
        self.assertFalse(releaser.is_alive())
        self.assertEqual(restore_errors, [])
        self.assertEqual(release_errors, [])
        snap = state.get_stats()
        self.assertEqual(snap.held_batch_references, 0)
        self.assertEqual(snap.ready_to_process, 0)
        self.assertEqual(snap.process_in_flight, 0)

    def test_process_exception_keeps_held_batch_for_retry(self):
        service = _FakeService(resp=_FakeConsumeResp(_lgl(1, 2), "cursor-1"))
        consumer = _FakeConsumer(
            service=service, processor=_Processor(raise_exc=True))
        from volcengine.tls.consumer.log_consumer import LogConsumer
        from volcengine.tls.data import ConsumeShard
        worker = LogConsumer(consumer, ConsumeShard("topic", 0))
        worker.fetch_data()
        with self.assertRaises(RuntimeError):
            worker.consume()
        snap = consumer.stats_state.get_stats()
        self.assertEqual(snap.held_batch_references, 1)
        self.assertEqual(snap.ready_to_process, 1)
        worker.release_held_on_revoke()
        self.assertEqual(
            consumer.stats_state.get_stats().held_batch_references, 0)

    def test_ready_backlog_excludes_callback_currently_processing(self):
        processor = _BlockingProcessor()
        service = _FakeService(resp=_FakeConsumeResp(_lgl(1, 2), "cursor-1"))
        consumer = _FakeConsumer(service=service, processor=processor)
        worker = LogConsumer(consumer, ConsumeShard("topic", 0))
        worker.fetch_data()
        process_thread = threading.Thread(target=worker.consume)
        process_thread.start()
        self.assertTrue(processor.entered.wait(1))

        during = consumer.stats_state.get_stats()
        self.assertEqual(during.held_batch_references, 0)
        self.assertEqual(during.ready_to_process, 0)
        self.assertEqual(during.process_in_flight, 1)

        processor.release.set()
        process_thread.join(2)
        self.assertFalse(process_thread.is_alive())
        final = consumer.stats_state.get_stats()
        self.assertEqual(final.held_batch_references, 0)
        self.assertEqual(final.ready_to_process, 0)
        self.assertEqual(final.process_in_flight, 0)

    def test_off_mode_process_failure_omits_error_category(self):
        service = _FakeService(resp=_FakeConsumeResp(_lgl(1, 1), "cursor-1"))
        consumer = _FakeConsumer(
            metrics_level="off",
            service=service, processor=_Processor(raise_exc=True))
        worker = LogConsumer(consumer, ConsumeShard("topic", 0))
        worker.fetch_data()

        with self.assertRaises(RuntimeError):
            worker.consume()

        self.assertEqual(consumer.log_processor.calls, 1)
        snapshot = consumer.stats_state.get_stats()
        self.assertIsNone(snapshot.get("last_error_category"))
        self.assertIsNone(snapshot.get("last_error_age_ms"))

    def test_stop_before_start_freezes_new_to_closed(self):
        config = ConsumerConfig(
            "proj", "grp", ["topic"], "consumer", stop_timeout=1,
            metrics_level="core")
        consumer = TLSConsumer(config, _FakeService(), _NoopProcessor())
        consumer.stop()
        first = consumer.stats_state.get_stats()
        consumer.stop()
        self.assertEqual(first.state, "closed")
        self.assertEqual(first.consistency, "final")
        self.assertIs(first, consumer.stats_state.get_stats())

    def test_live_thread_after_timeout_keeps_closing_weak(self):
        config = ConsumerConfig(
            "proj", "grp", ["topic"], "consumer", stop_timeout=1,
            metrics_level="core")
        consumer = TLSConsumer(config, _FakeService(), _NoopProcessor())
        threads = (_AliveThread(), _AliveThread(), _AliveThread())
        consumer.run_thread, consumer.checkpoint_thread, consumer.heartbeat_thread = threads
        try:
            consumer.stop()
            pending = consumer.stats_state.get_stats()
            self.assertEqual(pending.state, "closing")
            self.assertEqual(pending.consistency, "weak")
        finally:
            for thread in threads:
                thread.stop()
        deadline = time.time() + 2
        while time.time() < deadline:
            finalizer = consumer._finalizer_thread
            if (consumer.stats_state.get_stats().state == "closed" and
                    (finalizer is None or not finalizer.is_alive())):
                break
            time.sleep(0.01)
        finalizer = consumer._finalizer_thread
        if finalizer is not None:
            finalizer.join(1)
            self.assertFalse(finalizer.is_alive())
        final = consumer.stats_state.get_stats()
        self.assertEqual(final.state, "closed")
        self.assertEqual(final.consistency, "final")

    def test_partial_thread_start_failure_cleans_started_threads(self):
        class _Group(object):
            consumer_group_name = "grp"

        class _InitService(_FakeService):
            def describe_consumer_groups(self, _request):
                response = type("Response", (object,), {})()
                response.consumer_groups = [_Group()]
                return response

        config = ConsumerConfig(
            "proj", "grp", ["topic"], "consumer", stop_timeout=1,
            metrics_level="core")
        consumer = TLSConsumer(config, _InitService(), _NoopProcessor())
        _StartThread.starts = 0
        with mock.patch(
                "volcengine.tls.consumer.consumer.threading.Thread",
                _StartThread):
            with self.assertRaises(RuntimeError):
                consumer.start()
        self.assertEqual(consumer.stats_state.get_stats().state, "failed")
        self.assertFalse(consumer.working_flag)
        self.assertFalse(consumer.heartbeat_thread.is_alive())
        consumer.stop()
        self.assertEqual(consumer.stats_state.get_stats().state, "failed")
        self.assertEqual(consumer.stats_state.get_stats().consistency, "final")

    def test_generic_checkpoint_exception_is_counted(self):
        service = _FakeService()
        service.modify_exc = RuntimeError("checkpoint boom")
        consumer = _FakeConsumer(service=service)
        from volcengine.tls.consumer.consumer_model import CheckpointInfo
        consumer.checkpoint_manager.add_checkpoint(
            CheckpointInfo("c1", ConsumeShard("topic", 0)))
        with self.assertRaises(RuntimeError):
            consumer.checkpoint_manager.upload_checkpoint()
        snap = consumer.stats_state.get_stats()
        self.assertEqual(snap.checkpoint_calls, 1)
        self.assertEqual(snap.checkpoint_failures, 1)
        self.assertEqual(snap.last_error_category, "checkpoint")

    def test_concurrent_checkpoint_upload_of_same_key_is_idempotent(self):
        barrier = threading.Barrier(2)

        class _ConcurrentService(_FakeService):
            def modify_checkpoint(self, _request):
                barrier.wait()

        consumer = _FakeConsumer(service=_ConcurrentService())
        from volcengine.tls.consumer.consumer_model import CheckpointInfo
        consumer.checkpoint_manager.add_checkpoint(
            CheckpointInfo("c1", ConsumeShard("topic", 0)))
        errors = []

        def upload():
            try:
                consumer.checkpoint_manager.upload_checkpoint()
            except Exception as exc:  # pragma: no cover - asserted below
                errors.append(exc)

        threads = [threading.Thread(target=upload) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(2)

        self.assertEqual(errors, [])
        self.assertEqual(consumer.checkpoint_manager.checkpoint_info_map, {})
        self.assertEqual(
            consumer.stats_state.get_stats().checkpoint_pending.current_items, 0)

    def test_stop_drains_checkpoint_added_by_finishing_worker(self):
        from volcengine.tls.consumer.checkpoint_manager import CheckpointManager
        from volcengine.tls.consumer.consumer_model import CheckpointInfo

        class _ObservedCheckpointManager(CheckpointManager):
            def __init__(self, owner):
                super(_ObservedCheckpointManager, self).__init__(owner)
                self.started = threading.Event()
                self.exited = threading.Event()

            def run(self):
                self.started.set()
                try:
                    super(_ObservedCheckpointManager, self).run()
                finally:
                    self.exited.set()

        class _FinishingWorker(object):
            def __init__(self, manager):
                self.manager = manager
                self.stop_observed = threading.Event()
                self.allow_finish = threading.Event()
                self.finished = threading.Event()

            @property
            def thread_running_status(self):
                self.stop_observed.set()
                return not self.finished.is_set()

            def finish(self):
                self.allow_finish.wait(2)
                self.manager.add_checkpoint(
                    CheckpointInfo("last", ConsumeShard("topic", 0)))
                self.finished.set()

            def release_held_on_revoke(self):
                pass

        config = ConsumerConfig(
            "proj", "grp", ["topic"], "consumer",
            flush_checkpoint_interval_in_second=1,
            stop_timeout=3, metrics_level="core")
        service = _FakeService()
        consumer = TLSConsumer(config, service, _NoopProcessor())
        manager = _ObservedCheckpointManager(consumer)
        consumer.checkpoint_manager = manager
        worker = _FinishingWorker(manager)
        consumer.worker_map["topic0"] = worker
        consumer.checkpoint_thread = threading.Thread(target=manager.run)
        consumer.checkpoint_thread.start()
        self.assertTrue(manager.started.wait(1))
        finisher = threading.Thread(target=worker.finish)
        finisher.start()
        stop_errors = []

        def stop():
            try:
                consumer.stop()
            except Exception as exc:  # pragma: no cover - asserted below
                stop_errors.append(exc)

        stopper = threading.Thread(target=stop)
        stopper.start()
        self.assertTrue(worker.stop_observed.wait(1))
        exited_before_worker = manager.exited.wait(1.2)
        worker.allow_finish.set()
        finisher.join(2)
        stopper.join(4)

        self.assertFalse(exited_before_worker)
        self.assertFalse(stopper.is_alive())
        self.assertEqual(stop_errors, [])
        self.assertEqual(service.modify_calls, 1)
        self.assertEqual(manager.checkpoint_info_map, {})
        self.assertEqual(
            consumer.stats_state.get_stats().checkpoint_pending.current_items, 0)

    def test_backoff_and_assignment_changes_are_counted(self):
        service = _FakeService(exc=_tls_error(429))
        consumer = _FakeConsumer(service=service)
        worker = LogConsumer(consumer, ConsumeShard("topic", 0))
        worker.run_with_status(
            worker.fetch_data,
            worker.status,
            worker.status)
        self.assertEqual(
            consumer.stats_state.get_stats().backoff_events, 1)

        config = ConsumerConfig(
            "proj", "grp", ["topic"], "consumer", stop_timeout=1,
            metrics_level="core")
        top = TLSConsumer(config, _FakeService(), _NoopProcessor())
        top.handle_shards([ConsumeShard("topic", 0)])
        self.assertEqual(top.stats_state.get_stats().rebalance_events, 1)
        top.handle_shards([ConsumeShard("topic", 0)])
        self.assertEqual(top.stats_state.get_stats().rebalance_events, 1)
        top.handle_shards([
            ConsumeShard("topic", 0), ConsumeShard("topic", 1)])
        self.assertEqual(top.stats_state.get_stats().rebalance_events, 2)


class CapabilityTruthTest(unittest.TestCase):
    def test_unbounded_queues_and_tasks_are_disclosed(self):
        producer = ProducerStatsState(
            "core", "p", "v", max_sender_count=1).get_stats()
        self.assertFalse(producer.send_queue.bounded)

        consumer = _FakeConsumer(
            metrics_level="core")
        state = consumer.stats_state
        state.mark_started()
        state.set_main_running(1)
        state.set_heartbeat_running(1)
        state.set_checkpoint_running(1)
        previous = project_snapshot(state.get_stats(), StatsOptions("health"))
        current = project_snapshot(state.get_stats(), StatsOptions("health"))
        self.assertNotIn(
            "unbounded_shard_workers", current.health.signals.critical_flags)
        health = evaluate_health(previous, current)
        self.assertEqual(health.status, "healthy")
        self.assertEqual(health.reason_codes, ())

if __name__ == "__main__":
    unittest.main()
