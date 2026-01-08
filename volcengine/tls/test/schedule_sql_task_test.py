# coding=utf-8
import os
import time
import unittest
import uuid

from volcengine.tls import tls_requests
from volcengine.tls.test.util_test import NewTLSService


class TestScheduleSqlTask(unittest.TestCase):

    cli = NewTLSService()

    project_id = ""
    project_name = "python-sdk-schedule-sql-test-project" + uuid.uuid4().hex[:16]
    source_topic_id = ""
    source_topic_name = "python-sdk-schedule-sql-source-topic" + uuid.uuid4().hex[:16]
    dest_topic_id = ""
    dest_topic_name = "python-sdk-schedule-sql-dest-topic" + uuid.uuid4().hex[:16]

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
        create_project_response = cls.cli.create_project(create_project_request)
        cls.assertTrue(create_project_response.project_id, "create project failed")
        cls.project_id = create_project_response.project_id

        # 创建源topic
        create_source_topic_request = tls_requests.CreateTopicRequest(
            project_id=cls.project_id,
            topic_name=cls.source_topic_name,
            ttl=1,
            shard_count=1,
        )
        create_source_topic_response = cls.cli.create_topic(create_source_topic_request)
        cls.assertTrue(create_source_topic_response.topic_id, "create source topic failed")
        cls.source_topic_id = create_source_topic_response.topic_id

        # 创建目标topic
        create_dest_topic_request = tls_requests.CreateTopicRequest(
            project_id=cls.project_id,
            topic_name=cls.dest_topic_name,
            ttl=1,
            shard_count=1,
        )
        create_dest_topic_response = cls.cli.create_topic(create_dest_topic_request)
        cls.assertTrue(create_dest_topic_response.topic_id, "create dest topic failed")
        cls.dest_topic_id = create_dest_topic_response.topic_id

        # 为源主题创建索引
        create_index_request = tls_requests.CreateIndexRequest(
            topic_id=cls.source_topic_id,
            full_text=tls_requests.FullTextInfo(
                delimiter=",; ",
                case_sensitive=False,
                include_chinese=False,
            ),
        )
        create_index_response = cls.cli.create_index(create_index_request)
        cls.assertTrue(create_index_response.request_id, "create index failed")

    @classmethod
    def tearDownClass(cls):
        # 删除目标topic
        delete_dest_topic_request = tls_requests.DeleteTopicRequest(topic_id=cls.dest_topic_id)
        delete_dest_topic_response = cls.cli.delete_topic(delete_dest_topic_request)
        cls.assertTrue(delete_dest_topic_response.request_id, "delete dest topic failed")

        # 删除源topic
        delete_source_topic_request = tls_requests.DeleteTopicRequest(topic_id=cls.source_topic_id)
        delete_source_topic_response = cls.cli.delete_topic(delete_source_topic_request)
        cls.assertTrue(delete_source_topic_response.request_id, "delete source topic failed")

        # 删除project
        delete_project_request = tls_requests.DeleteProjectRequest(project_id=cls.project_id)
        delete_project_response = cls.cli.delete_project(delete_project_request)
        cls.assertTrue(delete_project_response.request_id, "delete project failed")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_schedule_sql_task(self):
        # 创建定时SQL任务
        current_time = int(time.time())
        task_name = f"python-sdk-test-schedule-task-{uuid.uuid4().hex}"
        create_schedule_sql_task_request = tls_requests.CreateScheduleSqlTaskRequest(
            task_name=task_name,
            topic_id=self.source_topic_id,
            dest_topic_id=self.dest_topic_id,
            process_start_time=current_time + 3600,  # 1小时后开始
            process_time_window="@m-15m,@m",
            query="* | select count(*) as count",
            request_cycle=tls_requests.RequestCycle(
                cycle_type="Period",
                time=60,  # 每60分钟执行一次
            ),
            status=0,  # 关闭任务，后续需手动启动
            description="测试定时SQL任务",
            process_sql_delay=60,
        )

        create_schedule_sql_task_response = self.cli.create_schedule_sql_task(
            create_schedule_sql_task_request)
        self.assertIsNotNone(create_schedule_sql_task_response.get_task_id(),
                              "create schedule sql task failed")
        self.assertTrue(create_schedule_sql_task_response.get_task_id(),
                        "task_id should not be empty")

    def test_create_schedule_sql_task_request_body(self):
        """验证 CreateScheduleSqlTaskRequest.get_api_input 的字段结构"""
        current_time = int(time.time())
        task_name = f"python-sdk-test-schedule-body-{uuid.uuid4().hex}"
        request_cycle = tls_requests.RequestCycle(
            cycle_type="Period",
            time=5,
        )

        request = tls_requests.CreateScheduleSqlTaskRequest(
            task_name=task_name,
            topic_id="4a9bd4bd-53f1-43ff-b88a-64ee1be5****",
            dest_topic_id="2a9bd4bd-53f1-43ff-b88a-64ee1be5****",
            process_start_time=current_time,
            process_time_window="@m-15m,@m",
            query="* | select count(*) as count",
            request_cycle=request_cycle,
            status=1,
        )

        self.assertTrue(request.check_validation())

        body = request.get_api_input()

        # 顶层字段键名与服务端 JSON tag 对齐
        self.assertEqual(body["TaskName"], task_name)
        self.assertIn("TopicID", body)
        self.assertIn("DestTopicID", body)
        self.assertEqual(body["Status"], 1)
        self.assertEqual(body["ProcessStartTime"], current_time)
        self.assertEqual(body["ProcessTimeWindow"], "@m-15m,@m")
        self.assertEqual(body["Query"], "* | select count(*) as count")

        # RequestCycle 嵌套结构校验
        self.assertIn("RequestCycle", body)
        request_cycle_body = body["RequestCycle"]
        self.assertEqual(request_cycle_body["Type"], "Period")
        self.assertEqual(request_cycle_body["Time"], 5)
        self.assertNotIn("CronTab", request_cycle_body)
        self.assertNotIn("CronTimeZone", request_cycle_body)


if __name__ == '__main__':
    unittest.main()
