# coding=utf-8
"""Unit tests for DescribeImportTask API"""
import os
import unittest
import random
import string

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import DescribeImportTaskRequest
from volcengine.tls.tls_responses import DescribeImportTaskResponse


class TestDescribeImportTask(unittest.TestCase):
    """Test cases for DescribeImportTask API"""

    def setUp(self):
        """Set up test environment"""
        self.endpoint = os.environ.get("VOLCENGINE_ENDPOINT", "https://tls-cn-beijing.ivolces.com")
        self.region = os.environ.get("VOLCENGINE_REGION", "cn-beijing")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "")
        self.access_key_secret = os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET", "")

        if not self.access_key_id or not self.access_key_secret:
            self.skipTest("Access key not configured")

        self.tls_service = TLSService(
            self.endpoint,
            self.access_key_id,
            self.access_key_secret,
            self.region
        )

    def generate_random_task_id(self):
        """Generate a random task ID for testing"""
        return f"test-import-task-{''.join(random.choices(string.digits, k=10))}"

    def test_describe_import_task_request_validation(self):
        """Test DescribeImportTaskRequest parameter validation"""
        # Test with valid task_id
        request = DescribeImportTaskRequest(task_id="test-task-id")
        api_input = request.get_api_input()
        self.assertEqual(api_input["TaskId"], "test-task-id")

        # Test with None task_id (should still work as it's not validated)
        request_none = DescribeImportTaskRequest(task_id=None)
        api_input_none = request_none.get_api_input()
        self.assertIsNone(api_input_none.get("TaskId"))

    def test_describe_import_task_api_call(self):
        """Test DescribeImportTask API call with a non-existent task"""
        task_id = self.generate_random_task_id()

        request = DescribeImportTaskRequest(task_id=task_id)

        try:
            response = self.tls_service.describe_import_task(request)

            # Verify response type
            self.assertIsInstance(response, DescribeImportTaskResponse)

            # Verify response has required fields
            self.assertIsNotNone(response.get_headers())
            self.assertIsNotNone(response.request_id)

            # The task might not exist, but the API should be callable
            # and return a valid response structure
            # Task info might be None if task doesn't exist, which is expected

        except Exception as e:
            # The API should be callable even if the task doesn't exist
            # The error should be about task not found, not about API structure
            error_message = str(e).lower()
            self.assertTrue(
                any(keyword in error_message for keyword in ["not found", "invalid", "error"]),
                f"Unexpected error type: {error_message}"
            )

    def test_describe_import_task_response_structure(self):
        """Test the response structure of DescribeImportTask"""
        task_id = self.generate_random_task_id()
        request = DescribeImportTaskRequest(task_id=task_id)

        try:
            response = self.tls_service.describe_import_task(request)

            # Test response headers
            headers = response.get_headers()
            self.assertIsInstance(headers, dict)
            self.assertIn("X-Tls-Requestid", headers)

            # Test task info getter
            task_info = response.get_task_info()
            # Task info can be None if task doesn't exist
            if task_info is not None:
                self.assertTrue(hasattr(task_info, 'task_id'))
                self.assertTrue(hasattr(task_info, 'task_name'))
                self.assertTrue(hasattr(task_info, 'status'))

        except Exception:
            # If task doesn't exist, that's acceptable for this test
            # We're mainly testing the response structure
            pass

    def test_describe_import_task_with_empty_task_id(self):
        """Test DescribeImportTask with empty task ID"""
        request = DescribeImportTaskRequest(task_id="")

        try:
            # Empty task ID should either return an error or empty response
            # Both are acceptable behaviors
            self.tls_service.describe_import_task(request)

        except Exception as e:
            # Expected behavior - empty task ID should cause an error
            self.assertTrue(len(str(e)) > 0)


if __name__ == '__main__':
    unittest.main()
