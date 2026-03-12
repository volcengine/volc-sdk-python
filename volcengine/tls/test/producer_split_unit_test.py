import threading
import unittest

from volcengine.tls.producer.producer import TLSProducer
from volcengine.tls.producer.producer_model import BatchLog
from volcengine.tls.producer.producer_model import ProducerConfig
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import PutLogsV2LogContent
from volcengine.tls.log_pb2 import LogGroup, Log


class _CaptureDispatcher:
    def __init__(self):
        self.lock = threading.Lock()
        self.groups = []

    def add_batch(self, hash_key, topic_id, source, filename, log_group, callback):
        with self.lock:
            self.groups.append(log_group)


class ProducerSplitUnitTest(unittest.TestCase):
    def _new_producer(self):
        config = ProducerConfig("endpoint", "region", "ak", "sk", None)
        producer = TLSProducer(config)
        producer.dispatcher = _CaptureDispatcher()
        return producer

    def test_split_by_count(self):
        producer = self._new_producer()
        logs = [PutLogsV2LogContent(time=1, log_dict={"k": "v"}) for _ in range(25000)]
        producer.send_logs_v2(None, "topic", None, None, logs, None)

        groups = producer.dispatcher.groups
        self.assertEqual(3, len(groups))
        self.assertEqual(10000, len(groups[0].logs))
        self.assertEqual(10000, len(groups[1].logs))
        self.assertEqual(5000, len(groups[2].logs))
        for g in groups:
            self.assertLessEqual(len(g.logs), ProducerConfig.MAX_LOG_GROUP_COUNT)
            self.assertLessEqual(len(g.SerializeToString()), ProducerConfig.MAX_BATCH_SIZE)

    def test_split_by_size(self):
        producer = self._new_producer()
        value = "a" * (2 * 1024 * 1024)
        logs = [PutLogsV2LogContent(time=1, log_dict={"k": value}) for _ in range(10)]
        producer.send_logs_v2(None, "topic", None, None, logs, None)
        groups = producer.dispatcher.groups
        self.assertGreater(len(groups), 1)
        for g in groups:
            self.assertLessEqual(len(g.SerializeToString()), ProducerConfig.MAX_BATCH_SIZE)

    def test_concurrent_produce_never_exceeds_max_size(self):
        producer = self._new_producer()

        def worker():
            for _ in range(200):
                producer.send_log_v2(None, "topic", None, None, PutLogsV2LogContent(time=1, log_dict={"k": "v"}), None)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        groups = producer.dispatcher.groups
        self.assertGreater(len(groups), 0)
        for g in groups:
            self.assertLessEqual(len(g.SerializeToString()), ProducerConfig.MAX_BATCH_SIZE)

    def test_single_log_exceeds_max_size_raises(self):
        producer = self._new_producer()
        value = "a" * (ProducerConfig.MAX_BATCH_SIZE + 1024)
        with self.assertRaises(TLSException):
            producer.send_log_v2(None, "topic", None, None, PutLogsV2LogContent(time=1, log_dict={"k": value}), None)

    def test_batch_log_group_list_count_never_exceeds_32768(self):
        config = ProducerConfig("endpoint", "region", "ak", "sk", None)
        config.max_batch_count = ProducerConfig.MAX_BATCH_COUNT
        config.max_batch_size_bytes = ProducerConfig.MAX_BATCH_SIZE

        key = BatchLog.BatchKey("", "topic", "", "")
        groups = []
        for _ in range(6):
            g = LogGroup()
            for _ in range(10000):
                g.logs.append(Log())
            groups.append(g)

        batches = []
        current = BatchLog(key, config)
        for g in groups:
            added = current.try_add(g, len(g.SerializeToString()), None)
            if not added:
                self.assertLessEqual(current.current_batch_count, ProducerConfig.MAX_BATCH_COUNT)
                batches.append(current)
                current = BatchLog(key, config)
                self.assertTrue(current.try_add(g, len(g.SerializeToString()), None))
        batches.append(current)

        self.assertGreater(len(batches), 1)
        total = 0
        for b in batches:
            self.assertLessEqual(b.current_batch_count, ProducerConfig.MAX_BATCH_COUNT)
            total += b.current_batch_count
        self.assertEqual(60000, total)


if __name__ == "__main__":
    unittest.main()
