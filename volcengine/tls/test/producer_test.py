# coding=utf-8
import os
import random
import string
import time
import unittest
import uuid

from volcengine.tls import tls_requests
from volcengine.tls.consumer.consumer import LogProcessor, TLSConsumer
from volcengine.tls.consumer.consumer_model import ConsumerConfig
from volcengine.tls.log_pb2 import LogGroupList
from volcengine.tls.producer.producer import TLSProducer
from volcengine.tls.producer.producer_model import ProducerConfig, CallBack
from volcengine.tls.test.util_test import NewTLSService
from volcengine.tls.tls_requests import PutLogsV2LogContent

consume_count = 0
produce_success_count = 0
produce_failed_count = 0


class TestLogProcessor(LogProcessor):
    def process(self, topic_id: str, shard_id: int, log_group_list: LogGroupList):
        print(topic_id + " --- " + str(shard_id))
        global consume_count
        for log_group in log_group_list.log_groups:
            for log in log_group.logs:
                consume_count += 1
        print("*** Count = {} ***".format(consume_count))


class MyCallBack(CallBack):
    def __init__(self, logs: list[PutLogsV2LogContent]):
        self.logs = logs

    def on_complete(self, result: 'Result'):
        global produce_success_count
        global produce_failed_count
        if result.success:
            produce_success_count += len(self.logs)
        else:
            produce_failed_count += len(self.logs)


class TestTLSProducerService(unittest.TestCase):
    cli = NewTLSService()

    project_id = ""
    project_name = "python-sdk-producer-test-project" + uuid.uuid4().hex
    topic_id = ""
    topic_name = "python-sdk-producer-test-topic" + uuid.uuid4().hex
    timestamp = str(int(time.time()) - 1)

    @classmethod
    def setUpClass(cls):
        # 创建project
        create_project_request = tls_requests.CreateProjectRequest(
            project_name=cls.project_name,
            region=os.environ["VOLCENGINE_REGION"],
        )
        create_project_response = cls.cli.create_project(create_project_request)
        cls.assertTrue(create_project_response.project_id, "create project failed")
        cls.project_id = create_project_response.project_id

        # 创建topic
        create_topic_request = tls_requests.CreateTopicRequest(
            project_id=cls.project_id,
            topic_name=cls.topic_name,
            ttl=1,
            shard_count=1,
        )
        create_topic_response = cls.cli.create_topic(create_topic_request)
        cls.assertTrue(create_topic_response.topic_id, "create topic failed")
        cls.topic_id = create_topic_response.topic_id
        pass

    @classmethod
    def tearDownClass(cls):
        # 删除topic
        delete_topic_request = tls_requests.DeleteTopicRequest(topic_id=cls.topic_id)
        delete_topic_response = cls.cli.delete_topic(delete_topic_request)
        cls.assertTrue(delete_topic_response.request_id, "delete topic failed")

        # 删除project
        delete_project_request = tls_requests.DeleteProjectRequest(project_id=cls.project_id)
        delete_project_response = cls.cli.delete_project(delete_project_request)
        cls.assertTrue(delete_project_response.request_id, "delete project failed")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_producer_and_consumer(self):
        # 创建producer
        producer_config = ProducerConfig(
            endpoint=os.environ["VOLCENGINE_ENDPOINT"],
            access_key=os.environ["VOLCENGINE_ACCESS_KEY_ID"],
            access_secret=os.environ["VOLCENGINE_ACCESS_KEY_SECRET"],
            region=os.environ["VOLCENGINE_REGION"],
        )
        producer_config.total_size_in_bytes = 10 * 1024 * 1024
        tls_producer = TLSProducer(producer_config)
        tls_producer.start()

        size = 5 * 1024
        large_string = ''.join(random.choices(string.ascii_letters + string.digits, k=size))

        for i in range(100):
            logs = [tls_requests.PutLogsV2LogContent(
                log_dict={
                    "key": "key-" + str(i),
                    "value": large_string + str(i)
                },
                time=int(time.time()) - 300
            ), tls_requests.PutLogsV2LogContent(
                log_dict={
                    "key": "key1-" + str(i),
                    "value": large_string + str(i)
                },
                time=int(time.time()) - 300
            )]
            callback = MyCallBack(logs)
            tls_producer.send_logs_v2("", self.topic_id, "python-sdk-local", "test.log",
                                      logs, callback)
        tls_producer.close()
        tls_producer.close()
        print("*****produce success count: " + str(produce_success_count))
        print("*****produce failed count: " + str(produce_failed_count))

        # 配置消费组的必填参数，ConsumerConfig构造函数设定了一些默认参数，您也可根据需要自定义配置
        consumer_config = ConsumerConfig(
            project_id=self.project_id,
            consumer_group_name="python-consumer-group-1",
            consumer_name="python-consumer-1",
            topic_id_list=[self.topic_id],
            consume_from=self.timestamp,
        )
        tls_consumer = TLSConsumer(consumer_config, self.cli, TestLogProcessor())

        # 调用start方法开始持续消费
        tls_consumer.start()

        # 可通过调用tls_consumer.stop()来结束消费组消费
        time.sleep(60)
        tls_consumer.stop()
        print("consume count: " + str(consume_count))
