# coding=utf-8
"""Consumer lifecycle, generation, and public observability tests."""
from __future__ import absolute_import

import threading
import time
import unittest
from unittest import mock

from volcengine.tls.consumer.consumer import LogProcessor, TLSConsumer
from volcengine.tls.consumer.consumer_model import CheckpointInfo, ConsumerConfig, ConsumerStatus
from volcengine.tls.consumer.log_consumer import LogConsumer
from volcengine.tls._stats.consumer_state import ConsumerStatsState
from volcengine.tls.data import ConsumeShard
from volcengine.tls.log_pb2 import LogGroupList
from volcengine.tls.tls_exception import TLSException

try:
    from volcengine.tls.stats import StatsOptions
except ImportError:  # The shared projection is intentionally landed by owner.
    StatsOptions = None


class _Groups(object):
    def __init__(self, names=()):
        self.consumer_groups = [type("Group", (), {"consumer_group_name": n})()
                                for n in names]


class _ConsumeResponse(object):
    def __init__(self, log_group_list=None, cursor="cursor-next"):
        self._log_group_list = log_group_list or LogGroupList()
        self._cursor = cursor

    def get_pb_message(self):
        return self._log_group_list

    def get_x_tls_cursor(self):
        return self._cursor


def _log_groups(groups=1, logs_per_group=1):
    result = LogGroupList()
    for _ in range(groups):
        # Protobuf repeated fields are generated dynamically; pylint cannot infer them.
        group = result.log_groups.add()  # pylint: disable=no-member
        for _ in range(logs_per_group):
            log = group.logs.add()
            log.time = 1
            content = log.contents.add()
            content.key = "k"
            content.value = "v"
    return result


class _ControlledService(object):
    def __init__(self):
        self.describe_calls = 0
        self.fail_describe = 0
        self.describe_error = TLSException(error_code="InitFailed",
                                           error_message="init failed")
        self.init_entered = threading.Event()
        self.init_release = threading.Event()
        self.block_describe = False
        self.heartbeat_shards = []
        self.heartbeat_calls = 0
        self.consume_entered = threading.Event()
        self.consume_release = threading.Event()
        self.block_consume = False
        self.consume_error = None
        self.consume_response = _ConsumeResponse(_log_groups(1, 2))
        self.modify_calls = 0
        self.modify_release = threading.Event()
        self.block_modify = False

    def describe_consumer_groups(self, _request):
        self.describe_calls += 1
        if self.block_describe:
            self.init_entered.set()
            self.init_release.wait(5)
        if self.fail_describe > 0:
            self.fail_describe -= 1
            raise self.describe_error
        return _Groups()

    def create_consumer_group(self, _request):
        return None

    def consumer_heartbeat(self, _request):
        self.heartbeat_calls += 1
        return type("Heartbeat", (), {"shards": list(self.heartbeat_shards)})()

    def describe_checkpoint(self, _request):
        return type("Checkpoint", (), {"checkpoint": ""})()

    def describe_cursor(self, _request):
        return type("Cursor", (), {"cursor": "cursor-start"})()

    def consume_logs(self, _request):
        self.consume_entered.set()
        if self.block_consume:
            self.consume_release.wait(5)
        if self.consume_error is not None:
            raise self.consume_error
        return self.consume_response

    def modify_checkpoint(self, _request):
        self.modify_calls += 1
        if self.block_modify:
            self.modify_release.wait(5)

    def reset_access_key_token(self, *_args):
        return None


class _Processor(LogProcessor):
    def __init__(self, error=None, entered=None, release=None):
        self.error = error
        self.entered = entered
        self.release = release
        self.calls = 0

    def process(self, topic_id, shard_id, log_group_list):
        del topic_id, shard_id, log_group_list
        self.calls += 1
        if self.entered is not None:
            self.entered.set()
        if self.release is not None:
            self.release.wait(5)
        if self.error is not None:
            raise self.error


def _wait(event, timeout=3):
    if not event.wait(timeout):
        raise AssertionError("event was not set within {}s".format(timeout))


def _wait_until(predicate, timeout=3):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if predicate():
            return
        time.sleep(0.01)
    raise AssertionError("condition was not met within {}s".format(timeout))


def _config(level="core", stop_timeout=1):
    return ConsumerConfig(
        "project", "group", ["topic"], "consumer",
        heartbeat_interval_in_second=1,
        data_fetch_interval_in_millisecond=10,
        flush_checkpoint_interval_in_second=1,
        stop_timeout=stop_timeout,
        metrics_level=level,
    )


class ConsumerLifecycleTest(unittest.TestCase):
    def test_role_failure_stops_sibling_roles_and_propagates(self):
        class _FailingConsumer(TLSConsumer):
            def run(self):
                raise RuntimeError("main role failed")

        consumer = _FailingConsumer(_config("core"), _ControlledService(), _Processor())
        consumer.stats_state.mark_started()
        consumer.working_flag = True
        consumer.heartbeat_runner.working_flag = True
        consumer.checkpoint_manager.working_flag = True
        try:
            with self.assertRaises(RuntimeError):
                consumer._role_wrapper(
                    consumer.run, consumer.stats_state.set_main_running)()

            snapshot = consumer.stats_state.get_stats()
            self.assertEqual(snapshot.state, "failed")
            self.assertEqual(snapshot.last_error_category, "lifecycle")
            self.assertFalse(consumer.working_flag)
            self.assertFalse(consumer.heartbeat_runner.working_flag)
            self.assertTrue(consumer.heartbeat_runner._stop_event.is_set())
            self.assertFalse(consumer.checkpoint_manager.working_flag)
            self.assertTrue(consumer.checkpoint_manager.force_stop)
            self.assertTrue(consumer.checkpoint_manager._stop_event.is_set())
        finally:
            consumer.stop()

    def test_started_role_failure_exits_siblings_and_restarts_fresh(self):
        class _FailOnceConsumer(TLSConsumer):
            def __init__(self, *args, **kwargs):
                super(_FailOnceConsumer, self).__init__(*args, **kwargs)
                self.fail_next = True
                self.role_started = threading.Event()
                self.role_errors = []

            def run(self):
                if self.fail_next:
                    self.fail_next = False
                    self.role_started.set()
                    raise RuntimeError("main role failed")
                return super(_FailOnceConsumer, self).run()

            def _role_wrapper(self, target, set_running):
                wrapped = super(_FailOnceConsumer, self)._role_wrapper(
                    target, set_running)

                def capture_expected_failure():
                    try:
                        wrapped()
                    except RuntimeError as error:
                        self.role_errors.append(error)

                return capture_expected_failure

        consumer = _FailOnceConsumer(_config("core"), _ControlledService(), _Processor())
        consumer.start()
        _wait(consumer.role_started)
        _wait_until(lambda: consumer.stats_state.get_stats().state == "failed")
        for thread in (consumer.run_thread, consumer.heartbeat_thread,
                       consumer.checkpoint_thread):
            thread.join(3)
            self.assertFalse(thread.is_alive())
        self.assertEqual([str(error) for error in consumer.role_errors],
                         ["main role failed"])
        failed_generation = consumer.stats_state.get_stats().collection_generation

        old_heartbeat = consumer.heartbeat_runner
        old_checkpoint = consumer.checkpoint_manager
        consumer.start()
        try:
            self.assertGreater(
                consumer.stats_state.get_stats().collection_generation,
                failed_generation)
            self.assertIsNot(consumer.heartbeat_runner, old_heartbeat)
            self.assertIsNot(consumer.checkpoint_manager, old_checkpoint)
        finally:
            consumer.stop()

    def test_public_metrics_level_switch_and_lifecycle_gates(self):
        consumer = TLSConsumer(_config("off"), _ControlledService(), _Processor())
        with self.assertRaises(RuntimeError):
            consumer.set_metrics_level("core")
        consumer.start()
        try:
            consumer.set_metrics_level("core")
            core = consumer.get_stats(StatsOptions("operational"))
            self.assertEqual(core.collected_level, "core")
            consumer.set_metrics_level("detailed")
            detailed = consumer.get_stats(StatsOptions("debug"))
            self.assertEqual(detailed.collection_generation, core.collection_generation)
            self.assertIsNotNone(detailed.latency_histograms)
            consumer.set_metrics_level("off")
            off = consumer.get_stats(StatsOptions("health"))
            self.assertTrue(off.metrics_disabled)
            self.assertGreater(off.collection_generation, core.collection_generation)
            consumer.stats_state.mark_closing()
            with self.assertRaises(RuntimeError):
                consumer.set_metrics_level("core")
        finally:
            consumer.stop()
        with self.assertRaises(RuntimeError):
            consumer.set_metrics_level("core")
        failed = TLSConsumer(_config("core"), _ControlledService(), _Processor())
        failed.stats_state.mark_failed("lifecycle")
        with self.assertRaises(RuntimeError):
            failed.set_metrics_level("detailed")
        failed.stop()

    def test_get_stats_requires_explicit_stats_options(self):
        self.assertIsNotNone(StatsOptions)
        service = _ControlledService()
        consumer = TLSConsumer(_config("core"), service, _Processor())
        self.assertRaises(TypeError, consumer.get_stats)
        snapshot = consumer.get_stats(StatsOptions("health"))
        self.assertEqual(snapshot.component_type, "consumer")

    def test_transient_init_failure_can_be_retried(self):
        service = _ControlledService()
        service.fail_describe = 1
        consumer = TLSConsumer(_config("core"), service, _Processor())
        with self.assertRaises(TLSException):
            consumer.start()
        self.assertEqual(consumer.stats_state.get_stats().state, "failed")

        consumer.start()
        self.assertEqual(consumer.stats_state.get_stats().state, "running")
        consumer.stop()
        self.assertEqual(consumer.stats_state.get_stats().consistency, "final")

    def test_failed_frozen_restart_uses_fresh_role_managers(self):
        consumer = TLSConsumer(_config("core"), _ControlledService(), _Processor())
        old_heartbeat = consumer.heartbeat_runner
        old_checkpoint = consumer.checkpoint_manager
        consumer.stats_state.mark_failed("lifecycle")
        consumer.stop()
        self.assertEqual(consumer.stats_state.get_stats().state, "failed")

        consumer.start()
        try:
            self.assertIsNot(consumer.heartbeat_runner, old_heartbeat)
            self.assertIsNot(consumer.checkpoint_manager, old_checkpoint)
        finally:
            consumer.stop()

    def test_checkpoint_failure_after_stop_deadline_can_exit_and_restart(self):
        service = _ControlledService()
        consumer = TLSConsumer(_config("core"), service, _Processor())
        manager = consumer.checkpoint_manager
        manager.add_checkpoint(CheckpointInfo("checkpoint", ConsumeShard("topic", 0)))

        def fail_modify(_request):
            service.modify_calls += 1
            raise RuntimeError("checkpoint failed")

        service.modify_checkpoint = fail_modify
        old_manager = consumer.checkpoint_manager
        consumer.start()
        try:
            _wait_until(lambda: service.modify_calls > 0)
            consumer.stop()
            self.assertTrue(old_manager.force_stop)
            _wait_until(lambda: consumer.stats_state.get_stats().state == "closed")
            _wait_until(lambda: not consumer._thread_alive(consumer.checkpoint_thread))

            consumer.start()
            self.assertIsNot(consumer.checkpoint_manager, old_manager)
        finally:
            old_manager.force_stop = True
            old_manager.working_flag = False
            old_manager._stop_event.set()
            if consumer.checkpoint_thread is not None:
                consumer.checkpoint_thread.join(3)
            if consumer.stats_state.get_stats().state in ("running", "closing"):
                consumer.stop()

    def test_stop_wins_init_race_without_starting_closed_generation(self):
        service = _ControlledService()
        service.block_describe = True
        consumer = TLSConsumer(_config("core"), service, _Processor())
        start_errors = []
        start_thread = threading.Thread(
            target=lambda: _capture(consumer.start, start_errors))
        start_thread.start()
        _wait(service.init_entered)

        stop_thread = threading.Thread(target=consumer.stop)
        stop_thread.start()
        time.sleep(0.05)
        service.init_release.set()
        start_thread.join(3)
        stop_thread.join(3)
        self.assertFalse(start_thread.is_alive())
        self.assertFalse(stop_thread.is_alive())
        self.assertEqual(start_errors, [])
        self.assertIsNone(consumer.run_thread)
        self.assertEqual(consumer.stats_state.get_stats().state, "closed")

    def test_stop_timeout_during_init_stays_weak_until_init_exits(self):
        service = _ControlledService()
        service.block_describe = True
        consumer = TLSConsumer(_config("core", stop_timeout=1), service, _Processor())
        start_errors = []
        starter = threading.Thread(target=lambda: _capture(consumer.start, start_errors))
        starter.start()
        _wait(service.init_entered)
        try:
            consumer.stop()
            settling = consumer.stats_state.get_stats()
            self.assertEqual(settling.state, "closing")
            self.assertEqual(settling.consistency, "weak")
            self.assertTrue(starter.is_alive())
            self.assertIsNone(consumer.run_thread)
        finally:
            service.init_release.set()
        starter.join(3)
        self.assertFalse(starter.is_alive())
        self.assertEqual(start_errors, [])
        _wait_until(lambda: consumer.stats_state.get_stats().state == "closed")
        self.assertEqual(consumer.stats_state.get_stats().consistency, "final")
        self.assertIsNone(consumer.run_thread)

    def test_restart_resumes_new_collection_generation_and_same_instance(self):
        service = _ControlledService()
        consumer = TLSConsumer(_config("core"), service, _Processor())
        consumer.start()
        first = consumer.stats_state.get_stats()
        first_generation = first.collection_generation
        instance_id = first.instance_id
        consumer.stop()

        consumer.start()
        second = consumer.stats_state.get_stats()
        self.assertGreater(second.collection_generation, first_generation)
        self.assertEqual(second.instance_id, instance_id)
        consumer.stop()

    def test_timeout_stop_stays_closing_until_revoked_inflight_worker_exits(self):
        service = _ControlledService()
        service.block_consume = True
        service.heartbeat_shards = [ConsumeShard("topic", 0)]
        consumer = TLSConsumer(_config("core", stop_timeout=1), service, _Processor())
        consumer.start()
        _wait(service.consume_entered)

        consumer.handle_shards([])
        stop_thread = threading.Thread(target=consumer.stop)
        stop_thread.start()
        stop_thread.join(3)
        self.assertFalse(stop_thread.is_alive())
        closing = consumer.stats_state.get_stats()
        self.assertEqual(closing.state, "closing")
        self.assertEqual(closing.consistency, "weak")

        service.consume_release.set()
        _wait_until(lambda: consumer.stats_state.get_stats().state == "closed")
        final = consumer.stats_state.get_stats()
        self.assertEqual(final.consistency, "final")

    def test_off_generation_does_not_accept_old_fetch_completion(self):
        service = _ControlledService()
        service.block_consume = True
        consumer = TLSConsumer(_config("core"), service, _Processor())
        consumer.stats_state.mark_started()
        worker = LogConsumer(consumer, ConsumeShard("topic", 0))
        fetch_thread = threading.Thread(target=worker.fetch_data)
        fetch_thread.start()
        _wait(service.consume_entered)

        consumer.stats_state.set_metrics_level("off")
        service.consume_release.set()
        fetch_thread.join(3)
        self.assertFalse(fetch_thread.is_alive())
        self.assertNotIn("fetch_calls", consumer.stats_state.get_stats())

        consumer.stats_state.set_metrics_level("core")
        service.block_consume = False
        worker.fetch_data()
        raw = consumer.stats_state.get_stats()
        self.assertEqual(raw.fetch_calls, 1)

    def test_revoke_during_blocked_fetch_never_publishes_held_batch(self):
        service = _ControlledService()
        service.block_consume = True
        consumer = TLSConsumer(_config("core"), service, _Processor())
        consumer.stats_state.mark_started()
        worker = LogConsumer(consumer, ConsumeShard("topic", 0))
        worker.set_status(ConsumerStatus.READY_TO_FETCH)
        consumer.worker_map["topic0"] = worker
        worker.run()
        _wait(service.consume_entered)
        try:
            consumer.handle_shards([])
            self.assertNotIn("topic0", consumer.worker_map)
            self.assertIsNone(worker._held_token)
            service.consume_release.set()
            worker.thread.join(3)
            self.assertFalse(worker.thread.is_alive())
            snapshot = consumer.stats_state.get_stats()
            self.assertEqual(snapshot.held_batch_references, 0)
            self.assertEqual(snapshot.ready_to_process, 0)
            self.assertIsNone(worker.curr_log_group_list)
        finally:
            service.consume_release.set()
            consumer.stop()

    def test_wait_for_restart_replacement_releases_held_once(self):
        consumer = TLSConsumer(_config("core"), _ControlledService(), _Processor())
        consumer.stats_state.mark_started()
        shard = ConsumeShard("topic", 0)
        old_worker = LogConsumer(consumer, shard)
        old_worker.set_status(ConsumerStatus.WAIT_FOR_RESTART)
        old_worker._held_token = consumer.stats_state.acquire_held(
            logs=1, groups=1, token=consumer.stats_state.token())
        release_calls = []
        original_release = old_worker.release_held_on_revoke

        def release_once():
            release_calls.append(1)
            original_release()

        old_worker.release_held_on_revoke = release_once
        consumer.worker_map["topic0"] = old_worker
        with mock.patch.object(LogConsumer, "run", return_value=None):
            consumer.handle_shards([shard])

        self.assertIsNot(consumer.worker_map["topic0"], old_worker)
        self.assertEqual(release_calls, [1])
        self.assertIsNone(old_worker._held_token)
        self.assertEqual(consumer.stats_state.get_stats().held_batch_references, 0)
        consumer.stop()

    def test_checkpoint_calls_refresh_generation_per_transport_call(self):
        service = _ControlledService()
        consumer = TLSConsumer(_config("core"), service, _Processor())
        state = consumer.stats_state
        state.mark_started()
        manager = consumer.checkpoint_manager
        manager.add_checkpoint(CheckpointInfo("a", ConsumeShard("topic-a", 0)))
        manager.add_checkpoint(CheckpointInfo("b", ConsumeShard("topic-b", 0)))
        calls = []

        def modify(_request):
            calls.append(state.collection_generation)
            if len(calls) == 1:
                state.set_metrics_level("off")
                state.set_metrics_level("detailed")

        service.modify_checkpoint = modify
        manager.upload_checkpoint()
        snapshot = state.get_stats()
        self.assertEqual(calls, [1, snapshot.collection_generation])
        self.assertEqual(snapshot.checkpoint_calls, 1)
        self.assertEqual(snapshot.checkpoint_failures, 0)
        self.assertEqual(manager.checkpoint_info_map, {})
        self.assertEqual(snapshot.checkpoint_pending.current_items, 0)
        self.assertEqual(snapshot.get("checkpoint_call_duration_ms").count, 1)


    def test_old_generation_shard_completion_cannot_leave_ghost_running_role(self):
        state = ConsumerStatsState("core", "consumer", "test")
        state.mark_started()
        old_generation = state.token()
        state.on_shard_task_submitted(token=old_generation)
        state.on_shard_task_started(token=old_generation)

        state.set_metrics_level("off")
        state.set_metrics_level("core")
        state.on_shard_task_done(token=old_generation)

        snapshot = state.get_stats()
        shard = [role for role in snapshot.worker_roles
                 if role.role == "shard_worker"][0]
        self.assertEqual(snapshot.shard_tasks_started, 1)
        self.assertEqual(snapshot.shard_tasks_completed, 0)
        self.assertEqual(shard.running, 0)
        self.assertEqual(shard.in_flight, 0)
        state.freeze()
        final_shard = [role for role in state.get_stats().worker_roles
                       if role.role == "shard_worker"][0]
        self.assertEqual(final_shard.running, 0)

    def test_fetch_process_failures_success_payload_and_ages(self):
        service = _ControlledService()
        service.consume_response = _ConsumeResponse(_log_groups(2, 2))
        processor = _Processor(error=RuntimeError("callback failed"))
        consumer = TLSConsumer(_config("core"), service, processor)
        consumer.stats_state.mark_started()
        worker = LogConsumer(consumer, ConsumeShard("topic", 0))
        worker.fetch_data()
        with self.assertRaises(RuntimeError):
            worker.consume()
        raw = consumer.stats_state.get_stats()
        self.assertEqual(raw.fetch_calls, 1)
        self.assertEqual(raw.fetch_failures, 0)
        self.assertEqual(raw.fetched_log_groups, 2)
        self.assertEqual(raw.fetched_logs, 4)
        self.assertEqual(raw.process_attempts, 1)
        self.assertEqual(raw.process_failures, 1)
        self.assertEqual(raw.processed_success_logs, 0)
        self.assertIsNotNone(raw.last_error_age_ms)

        processor.error = None
        worker.consume()
        raw = consumer.stats_state.get_stats()
        self.assertEqual(raw.process_attempts, 2)
        self.assertEqual(raw.processed_success_logs, 4)
        self.assertEqual(raw.processed_success_groups, 2)
        self.assertIsNotNone(raw.last_success_age_ms)


def _capture(func, errors):
    try:
        func()
    except Exception as exc:  # pragma: no cover - only for race diagnostics
        errors.append(exc)


if __name__ == "__main__":
    unittest.main()
