# coding=utf-8
import os
import time
import unittest
import uuid

from volcengine.tls import tls_requests
from volcengine.tls.test.util_test import NewTLSService
from volcengine.tls.tls_responses import PutLogsResponse, DescribeCursorResponse, ConsumeLogsResponse

class TestPutLogs(unittest.TestCase):

    cli = NewTLSService()

    project_id = ""
    project_name = "python-sdk-consumer-test-project" + uuid.uuid4().hex
    topic_id = ""
    topic_name = "python-sdk-consumer-test-topic" + uuid.uuid4().hex

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

    def test_put_logs_v2(self):

        num = 100
        time_start = int(time.time())

        logGroup = tls_requests.PutLogsV2Logs(source="python-sdk-local", filename="test.log")
        for i in range(num):
            logGroup.add_log(
                contents={
                    "key": "key-" + str(i),
                    "value": "test-message" + str(i)
                },
                log_time=time_start + i
            )

        logGroup.add_log(
            contents={
                "key": "key-" + str(num),
                "value": "test-message" + str(num),
            },
            log_time=0
        )

        response: PutLogsResponse = self.cli.put_logs_v2(tls_requests.PutLogsV2Request(self.topic_id, logGroup))
        self.assertIsNotNone(response.get_request_id())

        describe_cursor_response: DescribeCursorResponse = self.cli.describe_cursor(tls_requests.DescribeCursorRequest(
            topic_id=self.topic_id,
            shard_id=0,
            from_time="begin",
        ))
        self.assertIsNotNone(response.get_request_id())

        consume_logs_response: ConsumeLogsResponse = self.cli.consume_logs(tls_requests.ConsumeLogsRequest(
            self.topic_id,
            shard_id=0,
            cursor=describe_cursor_response.get_cursor(),
        ))

        self.assertEqual(1, consume_logs_response.get_x_tls_count())

        log_group_list = consume_logs_response.get_pb_message()

        count = 0

        for log_group in log_group_list.log_groups:
            for log in log_group.logs:

                if log.time < int(1e10):
                    self.assertLessEqual(time_start, log.time)
                    self.assertGreaterEqual(time_start+num-1, log.time)
                else:
                    self.assertLessEqual(time_start * 1000, log.time)
                    self.assertGreaterEqual((time_start+num-1) * 1000, log.time)

                count += 1

        self.assertEqual(num+1, count)

