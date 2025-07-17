# coding=utf-8
import os
import time
import unittest
import uuid

from volcengine.tls import tls_requests
from volcengine.tls.consumer.consumer import LogProcessor, TLSConsumer
from volcengine.tls.consumer.consumer_model import ConsumerConfig
from volcengine.tls.log_pb2 import LogGroupList
from volcengine.tls.test.util_test import NewTLSService

class TestLogProcessor(LogProcessor):
    def process(self, topic_id: str, shard_id: int, log_group_list: LogGroupList):
        print(topic_id + " --- " + str(shard_id))

        count = 0

        for log_group in log_group_list.log_groups:
            for log in log_group.logs:
                count += 1
                print("*** Count = {} ***".format(count))

                for content in log.contents:
                    print("{}: {}".format(content.key, content.value))
                print()


class TestTLSService(unittest.TestCase):

    cli = NewTLSService()

    project_id = ""
    project_name = "python-sdk-consumer-test-project" + uuid.uuid4().hex
    topic_id = ""
    topic_name = "python-sdk-consumer-test-topic" + uuid.uuid4().hex
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

        # 写入日志数据
        logs = tls_requests.PutLogsV2Logs(source="python-sdk-local", filename="test.log")
        for i in range(10):
            logs.add_log(
                contents={
                    "key": "key-" + str(i),
                    "value": "test-message" + str(i)
                },
                 log_time=int(time.time())
            )
        cls.cli.put_logs_v2(tls_requests.PutLogsV2Request(cls.topic_id, logs))

        time.sleep(10)

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

    def test_consumer(self):
        # 配置消费组的必填参数，ConsumerConfig构造函数设定了一些默认参数，您也可根据需要自定义配置
        consumer_config = ConsumerConfig(
            project_id=self.project_id,
            consumer_group_name="python-consumer-group",
            consumer_name="python-consumer",
            topic_id_list=[self.topic_id],
            consume_from=self.timestamp,
        )
        tls_consumer = TLSConsumer(consumer_config, self.cli, TestLogProcessor())

        # 调用start方法开始持续消费
        tls_consumer.start()

        # 可通过调用tls_consumer.stop()来结束消费组消费
        time.sleep(300)
        tls_consumer.stop()
