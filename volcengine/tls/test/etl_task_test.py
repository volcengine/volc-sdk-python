"""ETL Task Test Module

This module contains unit tests for ETL task functionality.
"""
import os
import unittest
import random
import string
from unittest.mock import Mock, patch

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import ModifyETLTaskRequest, DescribeETLTasksRequest
from volcengine.tls.tls_responses import DescribeETLTasksResponse
from volcengine.tls.data import TargetResource


class TestETLTask(unittest.TestCase):
    """Test class for ETL task functionality."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = os.environ.get("VOLCENGINE_ENDPOINT", "tls-cn-beijing.ivolces.com")
        self.region = os.environ.get("VOLCENGINE_REGION", "cn-beijing")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "test-ak")
        self.access_key_secret = os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET", "test-sk")

    def generate_random_string(self, length=10):
        """Generate a random string for testing."""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def test_modify_etl_task_request_validation(self):
        """测试 ModifyETLTaskRequest 参数验证"""
        # 测试 task_id 为 None 的情况
        request = ModifyETLTaskRequest(task_id=None)
        self.assertFalse(request.check_validation())

        # 测试 task_id 不为 None 的情况
        request = ModifyETLTaskRequest(task_id="test-task-id")
        self.assertTrue(request.check_validation())

    def test_modify_etl_task_request_with_target_resources(self):
        """测试 ModifyETLTaskRequest 包含 TargetResource 的情况"""
        target_resources = [
            TargetResource(
                alias="test",
                topic_id="test-topic-id",
                region="cn-beijing",
                role_trn="trn:iam::2100000001:role/TLSETLAccessForUserA"
            )
        ]

        request = ModifyETLTaskRequest(
            task_id="test-task-id",
            name="test-etl-task-name",
            description="This is a test ETL task",
            script='f_set("key","value")',
            target_resources=target_resources
        )

        # 验证参数
        self.assertTrue(request.check_validation())
        self.assertEqual(request.task_id, "test-task-id")
        self.assertEqual(request.name, "test-etl-task-name")
        self.assertEqual(request.description, "This is a test ETL task")
        self.assertEqual(request.script, 'f_set("key","value")')
        self.assertEqual(len(request.target_resources), 1)

        # 验证 API 输入格式
        api_input = request.get_api_input()
        self.assertIn("TaskId", api_input)
        self.assertIn("Name", api_input)
        self.assertIn("Description", api_input)
        self.assertIn("Script", api_input)
        self.assertIn("TargetResources", api_input)

        target_resource = api_input["TargetResources"][0]
        self.assertEqual(target_resource["Alias"], "test")
        self.assertEqual(target_resource["TopicId"], "test-topic-id")
        self.assertEqual(target_resource["Region"], "cn-beijing")
        self.assertEqual(target_resource["RoleTrn"], "trn:iam::2100000001:role/TLSETLAccessForUserA")

    def test_target_resource_data_class(self):
        """测试 TargetResource 数据类"""
        target_resource = TargetResource(
            alias="test-alias",
            topic_id="test-topic",
            region="cn-shanghai",
            role_trn="trn:iam::123456789:role/TestRole"
        )

        # 测试 json 方法
        json_data = target_resource.json()
        self.assertEqual(json_data["Alias"], "test-alias")
        self.assertEqual(json_data["TopicId"], "test-topic")
        self.assertEqual(json_data["Region"], "cn-shanghai")
        self.assertEqual(json_data["RoleTrn"], "trn:iam::123456789:role/TestRole")

    def test_modify_etl_task_integration(self):
        """测试 ModifyETLTask 方法的集成测试（模拟）"""
        # 生成随机任务ID和名称
        task_id = f"test-etl-task-{self.generate_random_string()}"
        task_name = f"test-etl-task-name-{self.generate_random_string()}"

        # 创建请求
        target_resources = [
            TargetResource(
                alias="test",
                topic_id="test-topic-id",
                region="cn-beijing",
                role_trn="trn:iam::2100000001:role/TLSETLAccessForUserA"
            )
        ]

        modify_request = ModifyETLTaskRequest(
            task_id=task_id,
            name=task_name,
            description="This is a test ETL task",
            script='f_set("key","value")',
            target_resources=target_resources
        )

        # 验证请求参数
        self.assertTrue(modify_request.check_validation())

        # 验证 API 输入格式
        api_input = modify_request.get_api_input()
        self.assertEqual(api_input["TaskId"], task_id)
        self.assertEqual(api_input["Name"], task_name)
        self.assertEqual(api_input["Description"], "This is a test ETL task")
        self.assertEqual(api_input["Script"], 'f_set("key","value")')

    def test_create_etl_task_request_body_fields(self):
        """测试 CreateETLTaskRequest 的请求体字段与 TargetResources 序列化"""
        from volcengine.tls import tls_requests

        request = tls_requests.CreateETLTaskRequest(
            dsl_type="NORMAL",
            name="python-sdk-etl-test-task-body",
            source_topic_id="source-topic-id",
            script='f_set("key","value")',
            target_resources=[
                {
                    "alias": "dict-alias",
                    "topic_id": "dict-topic-id",
                    "region": "cn-beijing",
                    "role_trn": "trn:iam::2100000001:role/DictRole",
                },
                TargetResource(
                    alias="obj-alias",
                    topic_id="obj-topic-id",
                    region="cn-shanghai",
                    role_trn="trn:iam::2100000001:role/ObjRole",
                ),
            ],
        )

        body = request.get_api_input()
        # 顶层字段命名
        self.assertEqual(body["DSLType"], "NORMAL")
        self.assertEqual(body["Name"], "python-sdk-etl-test-task-body")
        self.assertEqual(body["SourceTopicId"], "source-topic-id")
        self.assertEqual(body["Script"], 'f_set("key","value")')

        # TargetResources 序列化结果
        self.assertIn("TargetResources", body)
        self.assertEqual(len(body["TargetResources"]), 2)

        first = body["TargetResources"][0]
        self.assertEqual(first["Alias"], "dict-alias")
        self.assertEqual(first["TopicId"], "dict-topic-id")
        self.assertEqual(first["Region"], "cn-beijing")
        self.assertEqual(first["RoleTrn"], "trn:iam::2100000001:role/DictRole")

        second = body["TargetResources"][1]
        self.assertEqual(second["Alias"], "obj-alias")
        self.assertEqual(second["TopicId"], "obj-topic-id")
        self.assertEqual(second["Region"], "cn-shanghai")
        self.assertEqual(second["RoleTrn"], "trn:iam::2100000001:role/ObjRole")

    def test_describe_etl_tasks_request_body_fields(self):
        """测试 DescribeETLTasksRequest 的查询参数序列化。"""
        request = DescribeETLTasksRequest(
            project_id="project-1",
            project_name="project-name",
            source_topic_id="source-topic-1",
            source_topic_name="source-topic-name",
            task_id="etl-task-1",
            task_name="etl-task-name",
            status="RUNNING",
            iam_project_name="default",
            page_number=2,
            page_size=50,
        )

        params = request.get_api_input()
        self.assertEqual(params["ProjectId"], "project-1")
        self.assertEqual(params["ProjectName"], "project-name")
        self.assertEqual(params["SourceTopicId"], "source-topic-1")
        self.assertEqual(params["SourceTopicName"], "source-topic-name")
        self.assertEqual(params["TaskId"], "etl-task-1")
        self.assertEqual(params["TaskName"], "etl-task-name")
        self.assertEqual(params["Status"], "RUNNING")
        self.assertEqual(params["IamProjectName"], "default")
        self.assertEqual(params["PageNumber"], 2)
        self.assertEqual(params["PageSize"], 50)

    @patch("volcengine.tls.TLSService.TLSService._TLSService__request")
    def test_describe_etl_tasks_service_call(self, mock_request):
        """测试 TLSService.describe_etl_tasks 调用路径与响应解析。"""
        tls_service = TLSService(
            self.endpoint,
            self.access_key_id,
            self.access_key_secret,
            self.region,
        )

        mock_response = Mock()
        mock_response.headers = {
            "X-Tls-Requestid": "test-request-id",
            "Content-Type": "application/json",
        }
        mock_response.text = (
            '{"Total": 1, "Tasks": ['
            '{"TaskId": "etl-task-1", "Name": "etl-task-name", '
            '"ProjectId": "project-1", "SourceTopicId": "topic-1", "TargetResources": []}'
            ']}'
        )
        mock_request.return_value = mock_response

        request = DescribeETLTasksRequest(project_id="project-1", page_number=1, page_size=20)
        response = tls_service.describe_etl_tasks(request)

        expected_params = request.get_api_input()
        mock_request.assert_called_once_with(
            api="/DescribeETLTasks",
            params=expected_params,
        )
        self.assertIsInstance(response, DescribeETLTasksResponse)
        self.assertEqual(response.get_total(), 1)
        tasks = response.get_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].task_id, "etl-task-1")


if __name__ == '__main__':
    unittest.main()
