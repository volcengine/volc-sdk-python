import os
import unittest
import random
from unittest.mock import Mock, patch

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import DeleteScheduleSqlTaskRequest
from volcengine.tls.tls_responses import DeleteScheduleSqlTaskResponse


class TestDeleteScheduleSqlTask(unittest.TestCase):
    """DeleteScheduleSqlTask 功能测试类"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = os.environ.get("VOLCENGINE_ENDPOINT", "https://tls-cn-beijing.ivolces.com")
        self.region = os.environ.get("VOLCENGINE_REGION", "cn-beijing")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "test-ak")
        self.access_key_secret = os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET", "test-sk")

    def test_delete_schedule_sql_task_request_validation(self):
        """测试 DeleteScheduleSqlTaskRequest 参数验证"""
        # 测试有效的请求
        request = DeleteScheduleSqlTaskRequest(task_id="test-task-id")
        self.assertTrue(request.check_validation())

        # 测试无效的请求
        request_invalid = DeleteScheduleSqlTaskRequest(task_id=None)
        self.assertFalse(request_invalid.check_validation())

    def test_delete_schedule_sql_task_request_api_input(self):
        """测试 DeleteScheduleSqlTaskRequest 的 API 输入转换"""
        task_id = "test-schedule-sql-task-123"
        request = DeleteScheduleSqlTaskRequest(task_id=task_id)

        api_input = request.get_api_input()
        self.assertEqual(api_input["TaskId"], task_id)

    @patch('volcengine.tls.TLSService.TLSService._TLSService__request')
    def test_delete_schedule_sql_task_service_call(self, mock_request):
        """测试 TLSService.delete_schedule_sql_task 方法调用"""
        # 设置 mock 响应
        mock_response = Mock()
        mock_response.headers = {
            'X-Tls-Requestid': 'test-request-id',
            'Content-Type': 'application/json',
        }
        mock_response.text = '{}'
        mock_request.return_value = mock_response

        # 创建 TLS 服务实例
        tls_service = TLSService(
            self.endpoint,
            self.access_key_id,
            self.access_key_secret,
            self.region
        )

        # 创建请求
        task_id = f"test-schedule-sql-task-{str(int(__import__('time').time()))}"
        request = DeleteScheduleSqlTaskRequest(task_id=task_id)

        # 调用方法
        response = tls_service.delete_schedule_sql_task(request)

        # 验证响应类型
        self.assertIsInstance(response, DeleteScheduleSqlTaskResponse)

        # 验证 mock 调用
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        self.assertEqual(call_args[1]['api'], '/DeleteScheduleSqlTask')
        self.assertEqual(call_args[1]['body']['TaskId'], task_id)

    @patch('volcengine.tls.TLSService.TLSService._TLSService__request')
    def test_delete_schedule_sql_task_with_invalid_request(self, mock_request):
        """测试使用无效请求调用 delete_schedule_sql_task"""
        # 创建 TLS 服务实例
        tls_service = TLSService(
            self.endpoint,
            self.access_key_id,
            self.access_key_secret,
            self.region
        )

        # 创建无效请求（task_id 为 None）
        invalid_request = DeleteScheduleSqlTaskRequest(task_id=None)

        # 验证抛出异常
        with self.assertRaises(Exception) as context:
            tls_service.delete_schedule_sql_task(invalid_request)

        # 验证异常信息
        self.assertIn("InvalidArgument", str(context.exception))

        # 验证 mock 没有被调用
        mock_request.assert_not_called()

    def test_delete_schedule_sql_task_integration_pattern(self):
        """测试与 Node.js 示例类似的集成模式"""
        # 模拟 Node.js 测试中的随机任务ID生成
        task_id = f"test-schedule-sql-task-{str(random.random()).replace('.', '')}"

        request = DeleteScheduleSqlTaskRequest(task_id=task_id)

        # 验证请求对象创建成功
        self.assertIsNotNone(request)
        self.assertEqual(request.task_id, task_id)
        self.assertTrue(request.check_validation())


if __name__ == '__main__':
    unittest.main()