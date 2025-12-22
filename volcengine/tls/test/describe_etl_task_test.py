import os
import unittest
from unittest.mock import Mock, patch

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import DescribeETLTaskRequest
from volcengine.tls.tls_responses import DescribeETLTaskResponse


class TestDescribeETLTask(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = os.environ.get("VOLCENGINE_ENDPOINT", "https://tls-cn-beijing.ivolces.com")
        self.region = os.environ.get("VOLCENGINE_REGION", "cn-beijing")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "test-ak")
        self.access_key_secret = os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET", "test-sk")

    def test_describe_etl_task_request_validation(self):
        """测试 DescribeETLTaskRequest 参数验证"""
        # 测试正常情况
        request = DescribeETLTaskRequest(task_id="test-task-id")
        self.assertTrue(request.check_validation())

        # 测试 task_id 为 None 的情况
        request = DescribeETLTaskRequest(task_id=None)
        self.assertFalse(request.check_validation())

    @patch('volcengine.tls.TLSService.TLSService._TLSService__request')
    def test_describe_etl_task_success(self, mock_request):
        """测试 DescribeETLTask 成功场景"""
        # 模拟响应数据
        mock_response = Mock()
        mock_response.headers = {'X-Tls-Requestid': 'test-request-id', 'Content-Type': 'application/json'}
        mock_response.text = '''{
            "CreateTime": "2023-12-01T12:00:00Z",
            "DSLType": "NORMAL",
            "Description": "Test ETL Task",
            "ETLStatus": "RUNNING",
            "Enable": true,
            "FromTime": 1701432000,
            "LastEnableTime": "2023-12-01T12:00:00Z",
            "ModifyTime": "2023-12-01T12:00:00Z",
            "Name": "test-etl-task",
            "ProjectId": "test-project-id",
            "ProjectName": "test-project",
            "Script": "test script content",
            "SourceTopicId": "test-source-topic-id",
            "SourceTopicName": "test-source-topic",
            "TargetResources": [
                {
                    "Alias": "target1",
                    "TopicId": "test-target-topic-id",
                    "ProjectId": "test-target-project-id",
                    "ProjectName": "test-target-project",
                    "Region": "cn-beijing",
                    "TopicName": "test-target-topic",
                    "RoleTrn": "test-role-trn"
                }
            ],
            "TaskId": "test-task-id",
            "TaskType": "Resident",
            "ToTime": 1701518400
        }'''

        mock_request.return_value = mock_response

        # 创建 TLS 服务实例
        tls_service = TLSService(
            self.endpoint,
            self.access_key_id,
            self.access_key_secret,
            self.region
        )

        # 创建请求
        request = DescribeETLTaskRequest(task_id="test-task-id")

        # 执行请求
        response = tls_service.describe_etl_task(request)

        # 验证响应
        self.assertIsInstance(response, DescribeETLTaskResponse)
        self.assertEqual(response.get_create_time(), "2023-12-01T12:00:00Z")
        self.assertEqual(response.get_dsl_type(), "NORMAL")
        self.assertEqual(response.get_description(), "Test ETL Task")
        self.assertEqual(response.get_etl_status(), "RUNNING")
        self.assertEqual(response.get_enable(), True)
        self.assertEqual(response.get_from_time(), 1701432000)
        self.assertEqual(response.get_last_enable_time(), "2023-12-01T12:00:00Z")
        self.assertEqual(response.get_modify_time(), "2023-12-01T12:00:00Z")
        self.assertEqual(response.get_name(), "test-etl-task")
        self.assertEqual(response.get_project_id(), "test-project-id")
        self.assertEqual(response.get_project_name(), "test-project")
        self.assertEqual(response.get_script(), "test script content")
        self.assertEqual(response.get_source_topic_id(), "test-source-topic-id")
        self.assertEqual(response.get_source_topic_name(), "test-source-topic")
        self.assertEqual(response.get_task_id(), "test-task-id")
        self.assertEqual(response.get_task_type(), "Resident")
        self.assertEqual(response.get_to_time(), 1701518400)

        # 验证目标资源
        target_resources = response.get_target_resources()
        self.assertEqual(len(target_resources), 1)
        target_resource = target_resources[0]
        self.assertEqual(target_resource.get_alias(), "target1")
        self.assertEqual(target_resource.get_topic_id(), "test-target-topic-id")
        self.assertEqual(target_resource.get_project_id(), "test-target-project-id")
        self.assertEqual(target_resource.get_project_name(), "test-target-project")
        self.assertEqual(target_resource.get_region(), "cn-beijing")
        self.assertEqual(target_resource.get_topic_name(), "test-target-topic")
        self.assertEqual(target_resource.get_role_trn(), "test-role-trn")

    def test_describe_etl_task_invalid_request(self):
        """测试 DescribeETLTask 无效请求"""
        tls_service = TLSService(
            self.endpoint,
            self.access_key_id,
            self.access_key_secret,
            self.region
        )

        # 创建无效请求（task_id 为 None）
        request = DescribeETLTaskRequest(task_id=None)

        # 验证请求无效
        self.assertFalse(request.check_validation())

        # 执行请求应该抛出异常
        with self.assertRaises(Exception) as context:
            tls_service.describe_etl_task(request)

        self.assertIn("InvalidArgument", str(context.exception))

    @patch('volcengine.tls.TLSService.TLSService._TLSService__request')
    def test_describe_etl_task_empty_target_resources(self, mock_request):
        """测试 DescribeETLTask 空目标资源场景"""
        # 模拟响应数据（空目标资源）
        mock_response = Mock()
        mock_response.headers = {'X-Tls-Requestid': 'test-request-id', 'Content-Type': 'application/json'}
        mock_response.text = '''{
            "CreateTime": "2023-12-01T12:00:00Z",
            "DSLType": "NORMAL",
            "Description": "Test ETL Task",
            "ETLStatus": "RUNNING",
            "Enable": true,
            "FromTime": 1701432000,
            "LastEnableTime": "2023-12-01T12:00:00Z",
            "ModifyTime": "2023-12-01T12:00:00Z",
            "Name": "test-etl-task",
            "ProjectId": "test-project-id",
            "ProjectName": "test-project",
            "Script": "test script content",
            "SourceTopicId": "test-source-topic-id",
            "SourceTopicName": "test-source-topic",
            "TargetResources": [],
            "TaskId": "test-task-id",
            "TaskType": "Resident",
            "ToTime": 1701518400
        }'''

        mock_request.return_value = mock_response

        # 创建 TLS 服务实例
        tls_service = TLSService(
            self.endpoint,
            self.access_key_id,
            self.access_key_secret,
            self.region
        )

        # 创建请求
        request = DescribeETLTaskRequest(task_id="test-task-id")

        # 执行请求
        response = tls_service.describe_etl_task(request)

        # 验证响应
        self.assertIsInstance(response, DescribeETLTaskResponse)
        target_resources = response.get_target_resources()
        self.assertEqual(len(target_resources), 0)


if __name__ == '__main__':
    unittest.main()