# coding=utf-8
"""Producer lifecycle, generation, memory, and retry observability tests.

These tests deliberately use an in-process client. They cover lifecycle and
admission boundaries owned by the Producer implementation.
"""
from __future__ import absolute_import

import threading
import time
import unittest

from volcengine.tls.log_pb2 import LogGroup
from volcengine.tls.producer.producer import TLSProducer
from volcengine.tls.producer.producer_model import BatchLog, ProducerConfig
from volcengine.tls.producer.send_batch_task import SendBatchTask
from volcengine.tls.producer.retry_queue import RetryQueue
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import PutLogsV2LogContent


class _Response(object):
    request_id = "v2-request"


class _GateClient(object):
    def __init__(self, gate=None):
        self.gate = gate
        self.started = threading.Event()
        self.calls = 0

    def put_logs(self, _request):
        self.calls += 1
        self.started.set()
        if self.gate is not None:
            self.gate.wait(5)
        return _Response()

    def set_retry_policy(self, _policy):
        pass


class _SequenceClient(object):
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = 0

    def put_logs(self, _request):
        self.calls += 1
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    def set_retry_policy(self, _policy):
        pass


def _retryable_exception():
    error = TLSException(error_code="E", error_message="retry")
    error.http_code = 429
    error.request_id = "retry-request"
    return error


class _CloseInCallback(object):
    def __init__(self, producer):
        self.producer = producer
        self.called = threading.Event()
        self.error = None

    def on_complete(self, _result):
        try:
            self.producer.close(timeout_ms=50)
        except Exception as exc:  # a timeout is allowed; deadlock is not
            self.error = exc
        finally:
            self.called.set()


class _CountingCallback(object):
    def __init__(self):
        self.results = []

    def on_complete(self, result):
        self.results.append(result)


def _config(level="core", total=4096, memory=None):
    config = ProducerConfig("endpoint", "region", "ak", "sk", metrics_level=level)
    config.total_size_in_bytes = total
    config.max_batch_size_bytes = total
    config.max_batch_count = 1
    config.max_block_ms = 0
    if memory is not None:
        config.max_producer_memory_bytes = memory
    config.valid_config()
    return config


def _log_group(value="v"):
    group = LogGroup()
    # Protobuf repeated fields are generated dynamically; pylint cannot infer them.
    log = group.logs.add()  # pylint: disable=no-member
    log.time = 1
    content = log.contents.add()
    content.key = "k"
    content.value = value
    return group


class ProducerConfigTest(unittest.TestCase):
    def test_batch_key_isolated_by_collection_generation(self):
        first = BatchLog.BatchKey(None, "topic", None, None, 1)
        second = BatchLog.BatchKey(None, "topic", None, None, 2)
        self.assertNotEqual(first, second)
        self.assertNotEqual(hash(first), hash(second))


class ProducerLifecycleTest(unittest.TestCase):
    def test_set_metrics_level_requires_running_and_off_boundary_resets_generation(self):
        producer = TLSProducer(_config("off"))
        with self.assertRaises(RuntimeError):
            producer.set_metrics_level("core")
        producer.start()
        try:
            before = producer.stats_state.collection_generation
            producer.set_metrics_level("core")
            self.assertGreater(producer.stats_state.collection_generation, before)
            generation = producer.stats_state.collection_generation
            producer.set_metrics_level("detailed")
            self.assertEqual(producer.stats_state.collection_generation, generation)
            producer.set_metrics_level("core")
            self.assertEqual(producer.stats_state.collection_generation, generation)
            producer.set_metrics_level("off")
            self.assertGreater(producer.stats_state.collection_generation, generation)
        finally:
            producer.close(timeout_ms=3000)

    def test_timeout_close_stays_weak_until_sender_and_memory_settle(self):
        gate = threading.Event()
        producer = TLSProducer(_config("core"))
        client = _GateClient(gate)
        producer.dispatcher.client = client
        producer.mover.client = client
        producer.start()
        producer.send_log_v2(None, "topic", None, None,
                             PutLogsV2LogContent(time=1, log_dict={"k": "v"}), None)
        self.assertTrue(client.started.wait(2))
        with self.assertRaises(TLSException):
            producer.close(timeout_ms=10)
        weak = producer.stats_state.get_stats()
        self.assertEqual(weak.state, "closing")
        self.assertEqual(weak.consistency, "weak")
        gate.set()
        deadline = time.time() + 3
        while producer.stats_state.get_stats().state != "closed" and time.time() < deadline:
            time.sleep(0.01)
        final = producer.stats_state.get_stats()
        self.assertEqual(final.state, "closed")
        self.assertEqual(final.consistency, "final")
        self.assertEqual(producer.memory_limiter.used(), 0)

    def test_off_on_resets_current_gauges_without_reattributing_old_work(self):
        producer = TLSProducer(_config("core"))
        producer.start()
        try:
            state = producer.stats_state
            old_token = state.token()
            state.on_accepted(1, 1, token=old_token)
            state.on_aggregate(1, 1, token=old_token)
            state.on_send_start(token=old_token)
            state.on_callback_pending(1, token=old_token)

            producer.set_metrics_level("off")
            producer.set_metrics_level("core")
            state.on_send_end(True, 1, 1, token=old_token)
            state.on_terminal("success", 1, 1, token=old_token)

            current = state.get_stats()
            self.assertEqual(current.send_calls_in_flight, 0)
            self.assertEqual(current.callbacks_pending, 0)
            self.assertEqual(current.callbacks_in_flight, 0)
            self.assertEqual(current.aggregate_batches, 0)
            self.assertEqual(current.aggregate_groups, 0)
            self.assertEqual(current.owned_logs, 0)
            self.assertEqual(current.owned_groups, 0)
            self.assertEqual(current.send_calls_success, 0)
            self.assertEqual(current.terminal_success_logs, 0)
        finally:
            producer.close(timeout_ms=3000)

    def test_close_from_callback_does_not_self_deadlock(self):
        producer = TLSProducer(_config("core"))
        client = _GateClient()
        producer.dispatcher.client = client
        producer.mover.client = client
        callback = _CloseInCallback(producer)
        producer.start()
        producer.send_log_v2(None, "topic", None, None,
                             PutLogsV2LogContent(time=1, log_dict={"k": "v"}), callback)
        self.assertTrue(callback.called.wait(3))
        producer.close(timeout_ms=3000)
        self.assertEqual(producer.stats_state.get_stats().state, "closed")

    def test_callback_close_racing_timeout_finalizer_does_not_wait_on_close_lock(self):
        gate = threading.Event()
        producer = TLSProducer(_config("core"))
        client = _GateClient(gate)
        producer.dispatcher.client = client
        producer.mover.client = client
        callback = _CloseInCallback(producer)
        producer.start()
        producer.send_log_v2(None, "topic", None, None,
                              PutLogsV2LogContent(time=1, log_dict={"k": "v"}), callback)
        self.assertTrue(client.started.wait(2))

        close_errors = []

        def close_from_owner_thread():
            try:
                producer.close(timeout_ms=10)
            except TLSException as exc:
                close_errors.append(exc)

        closer = threading.Thread(target=close_from_owner_thread)
        closer.start()
        closer.join(2)
        self.assertFalse(closer.is_alive())
        self.assertEqual(len(close_errors), 1)

        gate.set()
        self.assertTrue(callback.called.wait(3))
        self.assertIsInstance(callback.error, TLSException)
        deadline = time.time() + 3
        while producer.stats_state.get_stats().state != "closed" and time.time() < deadline:
            time.sleep(0.01)
        final = producer.stats_state.get_stats()
        self.assertEqual(final.state, "closed")
        self.assertEqual(final.consistency, "final")

    def test_unexpected_close_error_clears_in_progress_and_finalizes(self):
        producer = TLSProducer(_config("core"))
        original_close_mover = producer._close_mover

        def raise_unexpected(_timeout_ms):
            raise ValueError("test close failure")

        producer._close_mover = raise_unexpected
        try:
            with self.assertRaises(ValueError):
                producer.close(timeout_ms=1)
            self.assertFalse(producer._close_in_progress)
            deadline = time.time() + 3
            while producer.stats_state.get_stats().state != "closed" and time.time() < deadline:
                time.sleep(0.01)
            self.assertEqual(producer.stats_state.get_stats().state, "closed")
        finally:
            producer._close_mover = original_close_mover


class ProducerMemoryTest(unittest.TestCase):
    def test_memory_raw_fields_conserve_payload_and_temporary(self):
        producer = TLSProducer(_config("core", total=128, memory=256))
        limiter = producer.memory_limiter
        self.assertTrue(limiter.acquire_payload(64, 0, generation=producer.stats_state.token(), phase="aggregate"))
        self.assertTrue(limiter.acquire_temporary(32, 0, generation=producer.stats_state.token()))
        memory = producer.stats_state.get_stats().memory.to_dict()
        self.assertEqual(memory["accounted_used_bytes"],
                         memory["payload_bytes"] + memory["temporary_bytes"])
        self.assertEqual(memory["payload_admission_limit_bytes"], 128)
        self.assertEqual(memory["bounded_runtime_buffer_bytes"], 32)
        limiter.release_temporary(32, generation=producer.stats_state.token())
        limiter.release_payload(64, generation=producer.stats_state.token(), phase="aggregate")

    def test_off_allocation_is_unknown_until_released_after_reenable(self):
        producer = TLSProducer(_config("off"))
        producer.start()
        try:
            self.assertTrue(producer.memory_limiter.acquire_payload(16, 0, generation=0, phase="aggregate"))
            producer.set_metrics_level("core")
            self.assertIsNone(producer.stats_state.get_stats().get("memory"))
            producer.memory_limiter.release_payload(16, generation=0, phase="aggregate")
            self.assertIsNotNone(
                producer.stats_state.get_stats().get("memory"))
        finally:
            producer.close(timeout_ms=3000)

    def test_off_allocation_does_not_leak_high_watermark_into_new_collection(self):
        producer = TLSProducer(_config("core", total=128, memory=256))
        producer.start()
        try:
            state = producer.stats_state
            old_token = state.token()
            self.assertTrue(producer.memory_limiter.acquire_payload(
                64, 0, generation=old_token, phase="aggregate"))
            self.assertEqual(state.get_stats().memory.high_watermark_bytes, 64)

            producer.set_metrics_level("off")
            producer.set_metrics_level("core")
            self.assertIsNone(state.get_stats().get("memory"))
            producer.memory_limiter.release_payload(
                64, generation=old_token, phase="aggregate")
            memory = state.get_stats().memory
            self.assertEqual(memory.high_watermark_bytes, 0)
            current_token = state.token()
            self.assertTrue(producer.memory_limiter.acquire_payload(
                16, 0, generation=current_token, phase="aggregate"))
            self.assertEqual(state.get_stats().memory.high_watermark_bytes, 16)
            producer.memory_limiter.release_payload(
                16, generation=current_token, phase="aggregate")
        finally:
            producer.close(timeout_ms=3000)

    def test_rejections_require_an_explicit_current_collection_token(self):
        producer = TLSProducer(_config("core", total=64, memory=128))
        producer.start()
        try:
            limiter = producer.memory_limiter
            state = producer.stats_state
            stale_token = state.token()
            producer.set_metrics_level("off")
            producer.set_metrics_level("core")
            current_token = state.token()

            self.assertFalse(limiter.acquire_payload(65, 0))
            self.assertFalse(limiter.acquire_payload(65, 0, generation=0))
            self.assertFalse(limiter.acquire_payload(
                65, 0, generation=stale_token))
            self.assertFalse(limiter.acquire_payload(
                65, 0, generation=current_token))

            memory = state.get_stats().memory
            self.assertEqual(memory.payload_admission_rejected_total, 1)
            self.assertEqual(memory.runtime_buffer_rejected_total, 0)
        finally:
            producer.close(timeout_ms=3000)

    def test_cross_off_wait_rejection_does_not_count_in_new_collection(self):
        producer = TLSProducer(_config("core", total=64, memory=128))
        producer.start()
        try:
            limiter = producer.memory_limiter
            state = producer.stats_state
            old_token = state.token()
            self.assertTrue(limiter.acquire_payload(
                64, 0, generation=old_token, phase="aggregate"))

            entered_wait = threading.Event()
            original_has_capacity = limiter._has_capacity

            def mark_wait(size, payload):
                entered_wait.set()
                return original_has_capacity(size, payload)

            limiter._has_capacity = mark_wait
            result = {}

            def wait_for_payload():
                result["acquired"] = limiter.acquire_payload(
                    1, 100, generation=old_token, phase="aggregate")

            waiter = threading.Thread(target=wait_for_payload)
            waiter.start()
            self.assertTrue(entered_wait.wait(1))
            time.sleep(0.01)
            producer.set_metrics_level("off")
            producer.set_metrics_level("core")
            waiter.join(1)
            self.assertFalse(waiter.is_alive())
            self.assertFalse(result["acquired"])

            limiter.release_payload(
                64, generation=old_token, phase="aggregate")
            memory = state.get_stats().memory
            self.assertEqual(memory.payload_admission_rejected_total, 0)
        finally:
            limiter._has_capacity = original_has_capacity
            producer.close(timeout_ms=3000)


class ProducerRetryTest(unittest.TestCase):
    def test_off_admission_before_batch_creation_is_not_reassigned(self):
        producer = TLSProducer(_config("off"))
        producer.start()
        try:
            state = producer.stats_state
            key = BatchLog.BatchKey(None, "topic", None, None, state.token())
            producer.set_metrics_level("detailed")
            batch = BatchLog(key, producer.producer_config)
            self.assertEqual(batch.stats_generation, 0)
            self.assertTrue(batch.try_add(_log_group(), 32, None))
            state.on_accepted(1, 1, token=batch.stats_generation)
            self.assertTrue(producer.memory_limiter.ownership_unknown())
            SendBatchTask(batch, producer.producer_config,
                          producer.memory_limiter, _GateClient(), RetryQueue()).send_request()
            current = state.get_stats()
            self.assertEqual(current.accepted_logs, 0)
            self.assertEqual(current.terminal_success_logs, 0)
            self.assertEqual(current.send_calls_success, 1)
            self.assertEqual(current.get("batch_delivery_duration_ms").count, 0)
            self.assertFalse(producer.memory_limiter.ownership_unknown())
        finally:
            producer.close(timeout_ms=3000)

    def test_terminal_settlement_is_once_only(self):
        config = _config("core")
        producer = TLSProducer(config)
        batch = BatchLog(BatchLog.BatchKey(None, "topic", None, None), config)
        self.assertTrue(batch.try_add(_log_group(), 32, None))
        config.stats_state.on_accepted(1, 1, token=batch.stats_generation)
        task = SendBatchTask(batch, config, config.memory_limiter,
                             _GateClient(), RetryQueue())
        task.send_request()
        task.handle_success(_Response())
        snap = config.stats_state.get_stats()
        self.assertEqual(snap.terminal_success_batches, 1)
        self.assertEqual(snap.owned_logs, 0)

    def test_old_batch_records_new_generation_transport_only(self):
        producer = TLSProducer(_config("core"))
        producer.start()
        try:
            config = producer.producer_config
            state = producer.stats_state
            old_token = state.token()
            batch = BatchLog(BatchLog.BatchKey(None, "topic", None, None, old_token), config)
            self.assertTrue(batch.try_add(_log_group(), 32, None))
            state.on_accepted(1, 1, token=old_token)

            producer.set_metrics_level("off")
            producer.set_metrics_level("core")
            client = _GateClient()
            task = SendBatchTask(batch, config, config.memory_limiter, client, RetryQueue())
            task.send_request()

            current = state.get_stats()
            self.assertEqual(client.calls, 1)
            self.assertEqual(current.send_calls_success, 1)
            self.assertEqual(current.send_calls_failure, 0)
            self.assertEqual(current.terminal_success_logs, 0)
            self.assertEqual(current.owned_logs, 0)
        finally:
            producer.close(timeout_ms=3000)

    def test_old_batch_uses_current_detailed_transport_and_callback_timing(self):
        producer = TLSProducer(_config("core"))
        producer.start()
        try:
            config = producer.producer_config
            state = producer.stats_state
            old_token = state.token()
            callback = _CountingCallback()
            batch = BatchLog(BatchLog.BatchKey(None, "topic", None, None, old_token), config)
            self.assertTrue(batch.try_add(_log_group(), 32, callback))
            state.on_accepted(1, 1, token=old_token)

            producer.set_metrics_level("off")
            producer.set_metrics_level("detailed")
            task = SendBatchTask(
                batch, config, config.memory_limiter, _GateClient(), RetryQueue())
            task.send_request()

            current = state.get_stats()
            self.assertEqual(len(callback.results), 1)
            self.assertEqual(current.send_calls_success, 1)
            self.assertEqual(current.terminal_success_logs, 0)
            self.assertEqual(current.get("send_call_duration_ms").count, 1)
            self.assertEqual(current.get("callback_duration_ms").count, 1)
        finally:
            producer.close(timeout_ms=3000)

    def test_local_temporary_rejection_is_a_delivery_not_send_call(self):
        producer = TLSProducer(_config("detailed", total=64, memory=64))
        producer.start()
        try:
            config = producer.producer_config
            state = producer.stats_state
            batch = BatchLog(BatchLog.BatchKey(None, "topic", None, None), config)
            self.assertTrue(batch.try_add(_log_group(), 16, None))
            state.on_accepted(1, 1, token=batch.stats_generation)
            client = _GateClient()
            task = SendBatchTask(batch, config, config.memory_limiter, client, RetryQueue())
            task.send_request()

            current = state.get_stats()
            self.assertEqual(client.calls, 0)
            self.assertEqual(current.send_calls_failure, 0)
            self.assertEqual(current.terminal_failure_batches, 1)
            self.assertIsNotNone(batch.first_send_attempt_mono_ns)
            self.assertEqual(current.get("batch_delivery_duration_ms").count, 1)
        finally:
            producer.close(timeout_ms=3000)

    def test_core_admission_detailed_ready_records_batch_timing(self):
        producer = TLSProducer(_config("core"))
        producer.start()
        try:
            config = producer.producer_config
            state = producer.stats_state
            batch = BatchLog(BatchLog.BatchKey(
                None, "topic", None, None, state.token()), config)
            self.assertTrue(batch.try_add(_log_group(), 32, None))
            state.on_accepted(1, 1, token=batch.stats_generation)

            producer.set_metrics_level("detailed")
            client = _GateClient()
            SendBatchTask(batch, config, config.memory_limiter,
                          client, RetryQueue()).run()

            current = state.get_stats()
            self.assertEqual(client.calls, 1)
            self.assertEqual(current.get("batch_queue_delay_ms").count, 1)
            self.assertEqual(
                current.get("batch_delivery_duration_ms").count, 1)
            self.assertEqual(current.get("send_call_duration_ms").count, 1)
        finally:
            producer.close(timeout_ms=3000)

    def test_detailed_retry_records_one_batch_queue_and_delivery_sample(self):
        producer = TLSProducer(_config("detailed"))
        producer.start()
        try:
            config = producer.producer_config
            config.retry_count = 2
            state = producer.stats_state
            batch = BatchLog(BatchLog.BatchKey(
                None, "topic", None, None, state.token()), config)
            self.assertTrue(batch.try_add(_log_group(), 32, None))
            state.on_accepted(1, 1, token=batch.stats_generation)
            client = _SequenceClient(
                [_retryable_exception(), _retryable_exception(), _Response()])
            retry_queue = RetryQueue()

            for attempt in range(3):
                SendBatchTask(batch, config, config.memory_limiter,
                              client, retry_queue).run()
                if attempt < 2:
                    batch = retry_queue.get_retry_batch(True)[0]

            current = state.get_stats()
            self.assertEqual(client.calls, 3)
            self.assertEqual(current.get("batch_queue_delay_ms").count, 1)
            self.assertEqual(
                current.get("batch_delivery_duration_ms").count, 1)
            self.assertEqual(current.get("send_call_duration_ms").count, 3)
        finally:
            producer.close(timeout_ms=3000)


if __name__ == "__main__":
    unittest.main()
