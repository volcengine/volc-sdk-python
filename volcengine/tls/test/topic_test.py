# coding=utf-8

import os
import unittest
import uuid

from volcengine.tls import tls_requests
from volcengine.tls.const import ENABLE_ENCRYPT_CONF, ENCRYPT_TYPE
from volcengine.tls.data import EncryptConf
from volcengine.tls.test.util_test import NewTLSService


class TestTopic(unittest.TestCase):

    cli = NewTLSService()

    project_id = ""
    project_name = "python-sdk-topic-test-project" + uuid.uuid4().hex

    topic_ids = []

    @classmethod
    def setUpClass(cls):
        # 创建project
        create_project_request = tls_requests.CreateProjectRequest(
            project_name=cls.project_name,
            region=os.environ["VOLCENGINE_REGION"],
        )
        create_project_response = cls.cli.create_project(
            create_project_request)
        cls.assertTrue(create_project_response.project_id,
                       "create project failed")
        cls.project_id = create_project_response.project_id

    @classmethod
    def tearDownClass(cls):
        for topic_id in cls.topic_ids:
            # 删除topic
            delete_topic_request = tls_requests.DeleteTopicRequest(topic_id)
            delete_topic_response = cls.cli.delete_topic(delete_topic_request)
            cls.assertTrue(delete_topic_response.request_id,
                           "delete topic failed")

        # 删除project
        delete_project_request = tls_requests.DeleteProjectRequest(
            project_id=cls.project_id)
        delete_project_response = cls.cli.delete_project(
            delete_project_request)
        cls.assertTrue(delete_project_response.request_id,
                       "delete project failed")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_topic_with_kms(self):
        # 创建
        create_topic_request = tls_requests.CreateTopicRequest(
            project_id=self.project_id,
            topic_name="python-sdk-topic-test-topic" + uuid.uuid4().hex,
            ttl=1,
            shard_count=1,
            encrypt_conf=EncryptConf(
                enable=True,
                encrypt_type="default",
            ).json(),
        )
        create_topic_response = self.cli.create_topic(create_topic_request)
        self.assertTrue(create_topic_response.topic_id)
        self.topic_ids.append(create_topic_response.topic_id)

        # 查询
        describe_topic_request = tls_requests.DescribeTopicRequest(
            topic_id=create_topic_response.topic_id,
        )
        describe_topic_response = self.cli.describe_topic(
            describe_topic_request)
        self.assertTrue(describe_topic_response.get_request_id())
        self.assertEqual(create_topic_request.encrypt_conf.get(
            ENCRYPT_TYPE), describe_topic_response.topic.encrypt_conf.get(ENCRYPT_TYPE))

        # 修改
        modifyTopicRequest = tls_requests.ModifyTopicRequest(
            topic_id=create_topic_response.topic_id,
            encrypt_conf=EncryptConf(
                enable=False,
            ).json(),
        )
        modify_topic_response = self.cli.modify_topic(modifyTopicRequest)
        self.assertTrue(modify_topic_response.get_request_id())

       # 查询
        describe_topic_request = tls_requests.DescribeTopicRequest(
            topic_id=create_topic_response.topic_id,
        )
        describe_topic_response = self.cli.describe_topic(
            describe_topic_request)
        self.assertTrue(describe_topic_response.get_request_id())
        self.assertFalse(
            describe_topic_response.topic.encrypt_conf.get(ENABLE_ENCRYPT_CONF))


if __name__ == '__main__':
    unittest.main()
