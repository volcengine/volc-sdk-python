# coding=utf-8
"""Unit tests for DeleteImportTask functionality."""
import unittest
from unittest.mock import Mock, patch

from volcengine.tls.TLSService import TLSService
from volcengine.tls.const import X_TLS_REQUEST_ID
from volcengine.tls.tls_requests import DeleteImportTaskRequest
from volcengine.tls.tls_responses import DeleteImportTaskResponse
from volcengine.tls.tls_exception import TLSException


class TestDeleteImportTask(unittest.TestCase):
    """Test class for DeleteImportTask functionality."""

    def setUp(self):
        self.endpoint = "https://tls-cn-beijing.ivolces.com"
        self.region = "cn-beijing"
        self.access_key_id = "test_ak"
        self.access_key_secret = "test_sk"
        self.tls_service = TLSService(
            self.endpoint,
            self.access_key_id,
            self.access_key_secret,
            self.region
        )

    def test_delete_import_task_request_validation_success(self):
        """测试 DeleteImportTaskRequest 参数验证成功的情况"""
        task_id = "test-import-task-123"
        request = DeleteImportTaskRequest(task_id)

        self.assertTrue(request.check_validation())
        self.assertEqual(request.task_id, task_id)

    def test_delete_import_task_request_validation_failed(self):
        """测试 DeleteImportTaskRequest 参数验证失败的情况"""
        # 测试 task_id 为 None
        request = DeleteImportTaskRequest(None)
        self.assertFalse(request.check_validation())

    def test_delete_import_task_api_call_success(self):
        """测试 DeleteImportTask API 调用成功的情况"""
        task_id = "test-import-task-123"
        request = DeleteImportTaskRequest(task_id)

        # Mock 响应
        mock_response = Mock()
        mock_response.headers = {
            X_TLS_REQUEST_ID: 'test-request-id',
            'Content-Type': 'application/json'
        }
        mock_response.text = '{}'
        mock_response.status_code = 200

        with patch.object(self.tls_service, '_TLSService__request', return_value=mock_response):
            response = self.tls_service.delete_import_task(request)

            self.assertIsInstance(response, DeleteImportTaskResponse)
            self.assertEqual(response.request_id, 'test-request-id')

    def test_delete_import_task_with_empty_task_id(self):
        """测试使用空 task_id 的情况，应该抛出异常"""
        request = DeleteImportTaskRequest("")

        with self.assertRaises(TLSException) as context:
            self.tls_service.delete_import_task(request)

        self.assertIn("Invalid request", str(context.exception))

    def test_delete_import_task_api_response_with_data(self):
        """测试 API 返回包含数据的响应"""
        task_id = "test-import-task-456"
        request = DeleteImportTaskRequest(task_id)

        # Mock 响应包含数据
        mock_response = Mock()
        mock_response.headers = {
            X_TLS_REQUEST_ID: 'test-request-id-2',
            'Content-Type': 'application/json'
        }
        mock_response.text = '{"key": "value", "status": "deleted"}'
        mock_response.status_code = 200

        with patch.object(self.tls_service, '_TLSService__request', return_value=mock_response):
            response = self.tls_service.delete_import_task(request)

            self.assertIsInstance(response, DeleteImportTaskResponse)
            self.assertEqual(response.request_id, 'test-request-id-2')
            self.assertEqual(response.response, {"key": "value", "status": "deleted"})


if __name__ == '__main__':
    unittest.main()
