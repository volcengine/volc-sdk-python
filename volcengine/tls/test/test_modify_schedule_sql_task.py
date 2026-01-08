# coding=utf-8
import os
import unittest
import uuid

from volcengine.tls.tls_requests import (
    CreateProjectRequest, CreateTopicRequest, DeleteTopicRequest,
    DeleteProjectRequest, ModifyScheduleSqlTaskRequest
)
from volcengine.tls.data import RequestCycle
from volcengine.tls.test.util_test import NewTLSService


class TestModifyScheduleSqlTask(unittest.TestCase):
    """测试ModifyScheduleSqlTask功能"""

    @classmethod
    def setUpClass(cls):
        """创建测试所需的资源"""
        cls.tls_service = NewTLSService()
        cls.region = os.environ["VOLCENGINE_REGION"]

        # 创建测试项目
        cls.project_name = f"tls-python-sdk-test-schedule-project-{uuid.uuid4().hex[:16]}"
        create_project_request = CreateProjectRequest(
            project_name=cls.project_name,
            region=cls.region
        )
        create_project_response = cls.tls_service.create_project(create_project_request)
        cls.project_id = create_project_response.get_project_id()

        # 创建测试主题
        cls.topic_name = f"tls-python-sdk-test-schedule-topic-{uuid.uuid4().hex[:16]}"
        create_topic_request = CreateTopicRequest(
            project_id=cls.project_id,
            topic_name=cls.topic_name,
            shard_count=1,
            ttl=1
        )
        create_topic_response = cls.tls_service.create_topic(create_topic_request)
        cls.topic_id = create_topic_response.get_topic_id()

    @classmethod
    def tearDownClass(cls):
        """清理测试资源"""
        # 删除测试主题
        delete_topic_request = DeleteTopicRequest(topic_id=cls.topic_id)
        cls.tls_service.delete_topic(delete_topic_request)

        # 删除测试项目
        delete_project_request = DeleteProjectRequest(project_id=cls.project_id)
        cls.tls_service.delete_project(delete_project_request)

    def test_modify_schedule_sql_task(self):
        """测试修改定时SQL任务"""
        # 测试数据
        task_id = f"test-schedule-task-{uuid.uuid4().hex}"
        task_name = f"test-schedule-task-name-{uuid.uuid4().hex}"

        # 创建调度周期配置
        request_cycle = RequestCycle(
            cycle_type="Period",
            time=1
        )

        # 创建修改请求
        modify_request = ModifyScheduleSqlTaskRequest(
            task_id=task_id,
            task_name=task_name,
            description="This is a test schedule sql task",
            dest_region=self.region,
            dest_topic_id=self.topic_id,
            status=0,
            process_sql_delay=60,
            process_time_window="@m-15m,@m",
            query="* | select *",
            request_cycle=request_cycle
        )

        # 验证请求参数
        self.assertTrue(modify_request.check_validation())

        # 验证API输入格式
        api_input = modify_request.get_api_input()
        self.assertEqual(api_input["TaskId"], task_id)
        self.assertEqual(api_input["TaskName"], task_name)
        self.assertEqual(api_input["Description"], "This is a test schedule sql task")
        self.assertEqual(api_input["DestRegion"], self.region)
        self.assertEqual(api_input["DestTopicID"], self.topic_id)
        self.assertEqual(api_input["Status"], 0)
        self.assertEqual(api_input["ProcessSqlDelay"], 60)
        self.assertEqual(api_input["ProcessTimeWindow"], "@m-15m,@m")
        self.assertEqual(api_input["Query"], "* | select *")
        self.assertIn("RequestCycle", api_input)
        self.assertEqual(api_input["RequestCycle"]["Type"], "Period")
        self.assertEqual(api_input["RequestCycle"]["Time"], 1)

    def test_modify_schedule_sql_task_with_cron(self):
        """测试使用Cron表达式的定时SQL任务"""
        task_id = f"test-schedule-task-cron-{uuid.uuid4().hex}"

        # 创建带有时区的调度周期配置
        request_cycle = RequestCycle(
            cycle_type="Cron",
            time=0,
            cron_tab="0 18 * * *",
            cron_time_zone="Asia/Shanghai"
        )

        modify_request = ModifyScheduleSqlTaskRequest(
            task_id=task_id,
            task_name="test-cron-task",
            request_cycle=request_cycle,
            query="* | select count(*) as count"
        )

        # 验证请求参数
        self.assertTrue(modify_request.check_validation())

        # 验证API输入格式
        api_input = modify_request.get_api_input()
        self.assertEqual(api_input["TaskId"], task_id)
        self.assertIn("RequestCycle", api_input)
        self.assertEqual(api_input["RequestCycle"]["Type"], "Cron")
        self.assertEqual(api_input["RequestCycle"]["Time"], 0)
        self.assertEqual(api_input["RequestCycle"]["CronTab"], "0 18 * * *")
        self.assertEqual(api_input["RequestCycle"]["CronTimeZone"], "Asia/Shanghai")

    def test_modify_schedule_sql_task_validation(self):
        """测试参数验证"""
        # 测试缺少必需的task_id
        modify_request = ModifyScheduleSqlTaskRequest(task_id=None)
        self.assertFalse(modify_request.check_validation())

        # 测试正常的task_id
        modify_request = ModifyScheduleSqlTaskRequest(task_id="test-task-id")
        self.assertTrue(modify_request.check_validation())

    def test_request_cycle_model(self):
        """测试RequestCycle模型"""
        # 测试基本功能
        request_cycle = RequestCycle(
            cycle_type="Fixed",
            time=720,
            cron_tab=None,
            cron_time_zone=None
        )

        self.assertEqual(request_cycle.get_cycle_type(), "Fixed")
        self.assertEqual(request_cycle.get_time(), 720)
        self.assertIsNone(request_cycle.get_cron_tab())
        self.assertIsNone(request_cycle.get_cron_time_zone())

        # 测试JSON序列化
        json_data = request_cycle.json()
        self.assertEqual(json_data["Type"], "Fixed")
        self.assertEqual(json_data["Time"], 720)
        self.assertIsNone(json_data.get("CronTab"))
        # 为None时不应该出现在JSON中
        self.assertNotIn("CronTimeZone", json_data)

        # 测试带时区的Cron类型
        request_cycle_cron = RequestCycle(
            cycle_type="Cron",
            time=0,
            cron_tab="0 18 * * *",
            cron_time_zone="Asia/Shanghai"
        )

        json_data_cron = request_cycle_cron.json()
        self.assertEqual(json_data_cron["Type"], "Cron")
        self.assertEqual(json_data_cron["Time"], 0)
        self.assertEqual(json_data_cron["CronTab"], "0 18 * * *")
        self.assertEqual(json_data_cron["CronTimeZone"], "Asia/Shanghai")


if __name__ == '__main__':
    unittest.main()
