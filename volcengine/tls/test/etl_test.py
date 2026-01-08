# coding=utf-8

import os
import unittest
import uuid

from volcengine.tls import tls_requests
from volcengine.tls.test.util_test import NewTLSService


class TestETL(unittest.TestCase):

    cli = NewTLSService()

    project_id = ""
    project_name = "python-sdk-etl-test-project" + uuid.uuid4().hex
    source_topic_id = ""
    target_topic_id = ""

    @classmethod
    def setUpClass(cls):
        # 创建project
        region = os.environ.get("VOLCENGINE_REGION")
        if not region:
            raise unittest.SkipTest("Missing required environment variable VOLCENGINE_REGION")
        create_project_request = tls_requests.CreateProjectRequest(
            project_name=cls.project_name,
            region=region,
        )
        create_project_response = cls.cli.create_project(
            create_project_request)
        cls.assertTrue(create_project_response.project_id,
                       "create project failed")
        cls.project_id = create_project_response.project_id

        # 创建源topic
        create_source_topic_request = tls_requests.CreateTopicRequest(
            topic_name="python-sdk-etl-test-source-topic" + uuid.uuid4().hex,
            project_id=cls.project_id,
            ttl=1,
            shard_count=1
        )
        create_source_topic_response = cls.cli.create_topic(create_source_topic_request)
        cls.assertTrue(create_source_topic_response.topic_id,
                       "create source topic failed")
        cls.source_topic_id = create_source_topic_response.topic_id

        # 创建目标topic
        create_target_topic_request = tls_requests.CreateTopicRequest(
            topic_name="python-sdk-etl-test-target-topic" + uuid.uuid4().hex,
            project_id=cls.project_id,
            ttl=1,
            shard_count=1
        )
        create_target_topic_response = cls.cli.create_topic(create_target_topic_request)
        cls.assertTrue(create_target_topic_response.topic_id,
                       "create target topic failed")
        cls.target_topic_id = create_target_topic_response.topic_id

    @classmethod
    def tearDownClass(cls):
        # 删除topic
        delete_source_topic_request = tls_requests.DeleteTopicRequest(cls.source_topic_id)
        delete_source_topic_response = cls.cli.delete_topic(delete_source_topic_request)
        cls.assertTrue(delete_source_topic_response.request_id,
                       "delete source topic failed")

        delete_target_topic_request = tls_requests.DeleteTopicRequest(cls.target_topic_id)
        delete_target_topic_response = cls.cli.delete_topic(delete_target_topic_request)
        cls.assertTrue(delete_target_topic_response.request_id,
                       "delete target topic failed")

        # 删除project
        delete_project_request = tls_requests.DeleteProjectRequest(
            project_id=cls.project_id)
        delete_project_response = cls.cli.delete_project(
            delete_project_request)
        cls.assertTrue(delete_project_response.request_id,
                       "delete project failed")

    def test_create_etl_task(self):
        """测试创建ETL任务"""
        # 创建ETL任务
        create_etl_task_request = tls_requests.CreateETLTaskRequest(
            dsl_type="NORMAL",
            name="python-sdk-etl-test-task" + uuid.uuid4().hex,
            description="Test ETL task",
            enable=True,
            source_topic_id=self.source_topic_id,
            script='f_set("key", "value")',
            task_type="Resident",
            target_resources=[
                {
                    "alias": "test",
                    "topic_id": self.target_topic_id,
                    "region": os.environ["VOLCENGINE_REGION"]
                }
            ]
        )

        create_etl_task_response = self.cli.create_etl_task(create_etl_task_request)
        self.assertTrue(create_etl_task_response.task_id,
                       "create etl task failed")
        self.assertIsNotNone(create_etl_task_response.get_task_id(),
                           "get task id failed")


    def test_create_etl_task_validation(self):
        """测试ETL任务参数验证"""
        # 测试缺少必需参数
        with self.assertRaises(Exception):
            # 缺少dsl_type
            invalid_request = tls_requests.CreateETLTaskRequest(
                dsl_type=None,
                name="test-task",
                source_topic_id=self.source_topic_id,
                script='f_set("key", "value")',
                target_resources=[
                    {
                        "alias": "test",
                        "topic_id": self.target_topic_id,
                        "region": os.environ["VOLCENGINE_REGION"]
                    }
                ]
            )
            self.cli.create_etl_task(invalid_request)

        # 测试无效的target_resources格式
        with self.assertRaises(Exception):
            invalid_request = tls_requests.CreateETLTaskRequest(
                dsl_type="NORMAL",
                name="test-task",
                source_topic_id=self.source_topic_id,
                script='f_set("key", "value")',
                target_resources=[
                    {
                        "alias": "test",
                        # 缺少topic_id
                        "region": os.environ["VOLCENGINE_REGION"]
                    }
                ]
            )
            self.cli.create_etl_task(invalid_request)