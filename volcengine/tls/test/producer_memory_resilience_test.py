import unittest

from volcengine.tls.log_pb2 import LogGroup, LogGroupList
from volcengine.tls.producer.batch_manager import BatchManager
from volcengine.tls.producer.batch_semaphore import MemoryLimiter
from volcengine.tls.producer.producer import TLSProducer
from volcengine.tls.producer.producer_model import (
    BatchLog,
    CircuitBreakerConfig,
    FailureController,
    FailurePolicy,
    FailureType,
    ProducerConfig,
    RetryMode,
)
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

    def get_retry_policy(self):
        return self.retry_policy


class _RecordingCallback:
    def __init__(self):
        self.results = []

    def on_complete(self, result):
        self.results.append(result)


class _RecordingExecutor:
    def __init__(self):
        self.submitted = []

    def submit(self, callable_):
        self.submitted.append(callable_)


class _FailingExecutor:
    def submit(self, _callable):
        raise RuntimeError("submit failed")


class _TrackingBatchManager(BatchManager):
    def __init__(self):
        super(_TrackingBatchManager, self).__init__()
        self.remove_locked = None

    def remove_batch(self, batch_logs):
        self.remove_locked = self.lock.locked()
        super(_TrackingBatchManager, self).remove_batch(batch_logs)


def _config(total_size=4096, max_memory=None):
    config = ProducerConfig("endpoint", "region", "ak", "sk", None)
    config.total_size_in_bytes = total_size
    config.max_batch_size_bytes = total_size
    config.max_block_ms = 0
    if max_memory is not None:
        config.max_producer_memory_bytes = max_memory
    config.valid_config()
    config.memory_limiter = MemoryLimiter(config.max_producer_memory_bytes, config.total_size_in_bytes)
    return config


def _log_group(value="v"):
    group = LogGroup()
    log = getattr(group, "logs").add()
    log.time = 1
    content = log.contents.add()
    content.key = "k"
    content.value = value
    return group


def _batch(config, callback=None, estimated_size=32):
    batch = BatchLog(BatchLog.BatchKey(None, "topic", None, None), config)
    batch.try_add(_log_group(), estimated_size, callback)
    return batch


def _tls_exception(http_code):
    exception = TLSException(error_code="E", error_message="failed")
    exception.http_code = http_code
    exception.request_id = "request-id"
    return exception


class ProducerMemoryResilienceTest(unittest.TestCase):
    def test_default_max_producer_memory_covers_payload_and_temporary_reservation(self):
        config = ProducerConfig("endpoint", "region", "ak", "sk", None)
        config.total_size_in_bytes = 1234
        config.valid_config()

        self.assertEqual(3 * 1234 + 1024, config.max_producer_memory_bytes)

        limiter = MemoryLimiter(config.max_producer_memory_bytes, config.total_size_in_bytes)
        self.assertTrue(limiter.acquire_payload(config.total_size_in_bytes, 0))
        self.assertTrue(limiter.acquire_temporary(config.total_size_in_bytes * 2 + 1024, 0))

    def test_memory_limiter_immediate_failure_close_and_double_release(self):
        limiter = MemoryLimiter(10, 8)

        self.assertTrue(limiter.acquire_payload(8, 0))
        self.assertFalse(limiter.acquire_payload(1, 0))
        self.assertEqual(8, limiter.used())
        self.assertEqual(0, limiter.available_permits())
        limiter.release_payload(8)
        self.assertEqual(8, limiter.available_permits())
        with self.assertRaises(RuntimeError):
            limiter.release_payload(1)
        limiter.close()
        self.assertFalse(limiter.acquire_payload(1, 0))

    def test_success_releases_payload_reservation_once(self):
        config = _config()
        callback = _RecordingCallback()
        batch = _batch(config, callback)
        self.assertGreater(config.memory_limiter.used(), 0)

        SendBatchTask(batch, config, config.memory_limiter, _FakeClient(), RetryQueue()).send_request()

        self.assertEqual(0, config.memory_limiter.used())
        self.assertEqual(1, len(callback.results))
        self.assertTrue(callback.results[0].success)

    def test_retry_keeps_reservation_until_terminal_failure(self):
        config = _config()
        config.retry_count = 1
        callback = _RecordingCallback()
        batch = _batch(config, callback)
        retry_queue = RetryQueue()
        client = _FakeClient(_tls_exception(429))

        SendBatchTask(batch, config, config.memory_limiter, client, retry_queue).send_request()

        self.assertGreater(config.memory_limiter.used(), 0)
        self.assertEqual(batch.reserved_bytes, config.memory_limiter.used())
        retry_queue.closed = True
        retry_batch = retry_queue.get_retry_batch(True)[0]
        SendBatchTask(retry_batch, config, config.memory_limiter, client, retry_queue).send_request()
        self.assertEqual(0, config.memory_limiter.used())
        self.assertEqual(1, len(callback.results))
        self.assertFalse(callback.results[0].success)

    def test_scratch_reservation_failure_does_not_call_client(self):
        config = _config(total_size=64, max_memory=80)
        callback = _RecordingCallback()
        batch = _batch(config, callback, estimated_size=64)
        client = _FakeClient()

        SendBatchTask(batch, config, config.memory_limiter, client, RetryQueue()).send_request()

        self.assertEqual(0, client.calls)
        self.assertEqual(0, config.memory_limiter.used())
        self.assertEqual("MemoryLimitExceeded", callback.results[0].attempts[-1].error_code)

    def test_producer_managed_retry_disables_inner_client_retry(self):
        config = ProducerConfig("endpoint", "region", "ak", "sk", None)
        config.retry_mode = RetryMode.PRODUCER_MANAGED

        producer = TLSProducer(config)
        try:
            self.assertEqual(1, producer.dispatcher.client.get_retry_policy().max_attempts)
        finally:
            producer.dispatcher.executor_service.shutdown(False)

    def test_failfast_open_circuit_rejects_before_reservation(self):
        config = ProducerConfig("endpoint", "region", "ak", "sk", None)
        config.max_block_ms = 0
        config.failure_policy = FailurePolicy.FAIL_FAST
        config.circuit_breaker = CircuitBreakerConfig(enabled=True, consecutive_failures=1)
        producer = TLSProducer(config)
        try:
            producer.dispatcher.failure_controller.after_send(_tls_exception(429), success=False)
            with self.assertRaises(TLSException):
                producer.send_logs_v2(None, "topic", None, None, [object()], None)
            self.assertEqual(0, producer.memory_limiter.used())
        finally:
            producer.dispatcher.executor_service.shutdown(False)

    def test_drop_open_circuit_callbacks_without_reservation(self):
        config = ProducerConfig("endpoint", "region", "ak", "sk", None)
        config.max_block_ms = 0
        config.failure_policy = FailurePolicy.DROP_WITH_CALLBACK
        config.circuit_breaker = CircuitBreakerConfig(enabled=True, consecutive_failures=1)
        producer = TLSProducer(config)
        callback = _RecordingCallback()
        try:
            producer.dispatcher.failure_controller.after_send(_tls_exception(429), success=False)
            producer.send_logs_v2(None, "topic", None, None, [object()], callback)
            self.assertEqual(0, producer.memory_limiter.used())
            self.assertEqual(1, len(callback.results))
            self.assertEqual("CircuitOpenException", callback.results[0].attempts[-1].error_code)
        finally:
            producer.dispatcher.executor_service.shutdown(False)

    def test_retry_then_callback_does_not_reject_before_enqueue_when_circuit_open(self):
        config = ProducerConfig("endpoint", "region", "ak", "sk", None)
        config.max_block_ms = 0
        config.failure_policy = FailurePolicy.RETRY_THEN_CALLBACK
        config.circuit_breaker = CircuitBreakerConfig(enabled=True, consecutive_failures=1)
        producer = TLSProducer(config)
        try:
            producer.dispatcher.failure_controller.after_send(_tls_exception(429), success=False)
            producer.dispatcher.add_batch(None, "topic", None, None, _log_group(), _RecordingCallback())

            self.assertGreater(producer.memory_limiter.used(), 0)
        finally:
            producer.dispatcher.executor_service.shutdown(False)

    def test_half_open_requires_configured_successes_before_closing(self):
        controller = FailureController(CircuitBreakerConfig(
            enabled=True,
            consecutive_failures=1,
            open_duration_ms=0,
            half_open_max_requests=2,
        ))

        self.assertTrue(controller.before_send())
        controller.after_send(FailureType.THROTTLED, success=False)
        self.assertTrue(controller.before_send())
        controller.after_send(success=True)

        self.assertTrue(controller.before_send())
        self.assertTrue(controller.before_send())
        self.assertFalse(controller.before_send())

    def test_half_open_local_resource_failure_releases_permit_without_opening(self):
        controller = FailureController(CircuitBreakerConfig(
            enabled=True,
            consecutive_failures=1,
            open_duration_ms=0,
            half_open_max_requests=1,
        ))

        self.assertTrue(controller.before_send())
        controller.after_send(FailureType.THROTTLED, success=False)
        self.assertTrue(controller.before_send())
        controller.after_send(FailureType.LOCAL_RESOURCE, success=False)

        self.assertTrue(controller.before_send())

    def test_half_open_permit_is_not_consumed_by_enqueue(self):
        config = ProducerConfig("endpoint", "region", "ak", "sk", None)
        config.max_block_ms = 0
        config.failure_policy = FailurePolicy.FAIL_FAST
        config.circuit_breaker = CircuitBreakerConfig(
            enabled=True,
            consecutive_failures=1,
            open_duration_ms=0,
            half_open_max_requests=1,
        )
        producer = TLSProducer(config)
        try:
            controller = producer.dispatcher.failure_controller
            controller.after_send(_tls_exception(429), success=False)

            producer.dispatcher.add_batch(None, "topic", None, None, _log_group("a"), None)
            producer.dispatcher.add_batch(None, "topic", None, None, _log_group("b"), None)

            self.assertEqual(1, controller.acquire_permit())
            self.assertEqual(-1, controller.acquire_permit())
        finally:
            producer.dispatcher.executor_service.shutdown(False)

    def test_timeout_batch_remove_holds_batch_manager_lock(self):
        from volcengine.tls.producer.mover import Mover

        config = _config()
        manager = _TrackingBatchManager()
        manager.batch_log = _batch(config)
        manager.batch_log.create_ms = 0
        dispatcher = type("Dispatcher", (), {
            "executor_service": _RecordingExecutor(),
            "client": _FakeClient(),
            "batches": {manager.batch_log.batch_key: manager},
            "batches_mutex": __import__("threading").Lock(),
            "memory_limiter": config.memory_limiter,
            "failure_controller": FailureController(config.circuit_breaker),
        })()
        mover = Mover("mover", config, dispatcher, RetryQueue())

        mover.handle_timeout_batch()

        self.assertTrue(manager.remove_locked)

    def test_submit_failure_keeps_batch_owned_payload_reservation(self):
        from volcengine.tls.producer.log_dispatcher import LogDispatcher

        config = _config()
        config.max_batch_count = 1
        dispatcher = LogDispatcher(config, "test-producer", config.memory_limiter, RetryQueue())
        real_executor = dispatcher.executor_service
        dispatcher.executor_service = _FailingExecutor()
        dispatcher.client = _FakeClient()
        try:
            with self.assertRaises(TLSException):
                dispatcher.add_batch(None, "topic", None, None, _log_group(), None)

            batch_manager = list(dispatcher.batches.values())[0]
            self.assertIsNotNone(batch_manager.batch_log)
            self.assertEqual(batch_manager.batch_log.reserved_bytes, config.memory_limiter.used())
        finally:
            real_executor.shutdown(False)

    def test_batch_manager_submits_callable_without_inline_run(self):
        config = _config()
        batch_manager = BatchManager()
        batch_manager.batch_log = _batch(config)
        executor = _RecordingExecutor()

        batch_manager.add_now(config, executor, _FakeClient(), config.memory_limiter, RetryQueue())

        self.assertEqual(1, len(executor.submitted))
        self.assertTrue(callable(executor.submitted[0]))
        self.assertGreater(config.memory_limiter.used(), 0)


if __name__ == "__main__":
    unittest.main()
