import unittest

from volcengine.tls.producer.batch_manager import BatchManager
from volcengine.tls.producer.producer_model import ProducerConfig, BatchLog


class _FakeExecutor:
    def __init__(self):
        self.submitted = None

    def submit(self, fn, *args, **kwargs):
        self.submitted = (fn, args, kwargs)


class _FakeClient:
    def __init__(self):
        self.called = False

    def put_logs(self, _req):
        self.called = True
        raise RuntimeError("boom")


class _FakeMemoryLock:
    def __init__(self):
        self.released = []

    def release(self, size):
        self.released.append(size)


class _FakeRetryQueue:
    def __init__(self):
        self.closed = False

    def add_to_retry_queue(self, _batch_log):
        raise RuntimeError("should not retry in this test")


class TestProducerBatchManager(unittest.TestCase):
    def test_add_now_submits_callable_without_executing(self):
        config = ProducerConfig(endpoint="example.com", region="cn-beijing", access_key="ak", access_secret="sk")
        batch_key = BatchLog.BatchKey(shard_hash="0", topic_id="t", source="s", file_name="f")
        batch_log = BatchLog(batch_key, config)

        manager = BatchManager()
        manager.batch_log = batch_log

        executor = _FakeExecutor()
        client = _FakeClient()
        memory_lock = _FakeMemoryLock()
        retry_queue = _FakeRetryQueue()

        manager.add_now(config=config, executor_service=executor, client=client, memory_lock=memory_lock, retry_queue=retry_queue)

        self.assertFalse(client.called)
        self.assertIsNotNone(executor.submitted)
        fn, args, kwargs = executor.submitted
        self.assertTrue(callable(fn))
        self.assertEqual(args, ())
        self.assertEqual(kwargs, {})
        self.assertIsNone(manager.batch_log)


if __name__ == "__main__":
    unittest.main()

