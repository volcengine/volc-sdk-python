# coding=utf-8
"""Unit tests for DescribeImportTasks functionality"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import unittest
from unittest.mock import Mock, patch

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import DescribeImportTasksRequest
from volcengine.tls.tls_responses import DescribeImportTasksResponse


class TestDescribeImportTasks(unittest.TestCase):
    """Test cases for DescribeImportTasks functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.endpoint = "https://tls-cn-beijing.ivolces.com"
        self.region = "cn-beijing"
        self.access_key_id = "test-ak"
        self.access_key_secret = "test-sk"
        self.tls_service = TLSService(
            self.endpoint,
            self.access_key_id,
            self.access_key_secret,
            self.region
        )

    def test_describe_import_tasks_request_initialization(self):
        """Test DescribeImportTasksRequest initialization with all parameters"""
        request = DescribeImportTasksRequest(
            task_id="test-task-id",
            task_name="test-task-name",
            project_id="test-project-id",
            project_name="test-project-name",
            topic_id="test-topic-id",
            topic_name="test-topic-name",
            page_number=2,
            page_size=50,
            source_type="tos",
            status=1
        )

        self.assertEqual(request.task_id, "test-task-id")
        self.assertEqual(request.task_name, "test-task-name")
        self.assertEqual(request.project_id, "test-project-id")
        self.assertEqual(request.project_name, "test-project-name")
        self.assertEqual(request.topic_id, "test-topic-id")
        self.assertEqual(request.topic_name, "test-topic-name")
        self.assertEqual(request.page_number, 2)
        self.assertEqual(request.page_size, 50)
        self.assertEqual(request.source_type, "tos")
        self.assertEqual(request.status, 1)

    def test_describe_import_tasks_request_default_values(self):
        """Test DescribeImportTasksRequest default values"""
        request = DescribeImportTasksRequest()

        self.assertIsNone(request.task_id)
        self.assertIsNone(request.task_name)
        self.assertIsNone(request.project_id)
        self.assertIsNone(request.project_name)
        self.assertIsNone(request.topic_id)
        self.assertIsNone(request.topic_name)
        self.assertEqual(request.page_number, 1)
        self.assertEqual(request.page_size, 20)
        self.assertIsNone(request.source_type)
        self.assertIsNone(request.status)

    def test_describe_import_tasks_request_get_api_input(self):
        """Test DescribeImportTasksRequest get_api_input method"""
        request = DescribeImportTasksRequest(
            task_id="test-task-id",
            task_name="test-task-name",
            project_id="test-project-id",
            topic_id="test-topic-id",
            page_number=1,
            page_size=10
        )

        api_input = request.get_api_input()

        self.assertEqual(api_input["TaskId"], "test-task-id")
        self.assertEqual(api_input["TaskName"], "test-task-name")
        self.assertEqual(api_input["ProjectId"], "test-project-id")
        self.assertEqual(api_input["TopicId"], "test-topic-id")
        self.assertEqual(api_input["PageNumber"], 1)
        self.assertEqual(api_input["PageSize"], 10)

    @patch('volcengine.tls.TLSService.TLSService._TLSService__request')
    def test_describe_import_tasks_success(self, mock_request):
        """Test successful describe_import_tasks call"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({
            "Total": 2,
            "TaskInfo": [
                {
                    "TaskId": "task-1",
                    "TaskName": "import-task-1",
                    "TopicId": "topic-1",
                    "TopicName": "topic-name-1",
                    "ProjectId": "project-1",
                    "ProjectName": "project-name-1",
                    "Status": 1,
                    "CreateTime": "2023-12-01T10:00:00Z",
                    "ModifyTime": "2023-12-01T10:30:00Z",
                    "SourceType": "tos",
                    "Description": "Test import task"
                },
                {
                    "TaskId": "task-2",
                    "TaskName": "import-task-2",
                    "TopicId": "topic-2",
                    "TopicName": "topic-name-2",
                    "ProjectId": "project-2",
                    "ProjectName": "project-name-2",
                    "Status": 0,
                    "CreateTime": "2023-12-01T11:00:00Z",
                    "ModifyTime": "2023-12-01T11:30:00Z",
                    "SourceType": "kafka",
                    "Description": "Another test import task"
                }
            ]
        })
        mock_response.headers = {
            "X-Tls-Requestid": "test-request-id",
            "Content-Type": "application/json"
        }
        mock_request.return_value = mock_response

        # Create request
        request = DescribeImportTasksRequest(
            project_id="test-project",
            page_number=1,
            page_size=10
        )

        # Call the method
        response = self.tls_service.describe_import_tasks(request)

        # Verify the response
        self.assertIsInstance(response, DescribeImportTasksResponse)
        self.assertEqual(response.get_total(), 2)
        self.assertEqual(len(response.get_task_info()), 2)

        # Verify first task
        first_task = response.get_task_info()[0]
        self.assertEqual(first_task.task_id, "task-1")
        self.assertEqual(first_task.task_name, "import-task-1")
        self.assertEqual(first_task.status, 1)

        # Verify second task
        second_task = response.get_task_info()[1]
        self.assertEqual(second_task.task_id, "task-2")
        self.assertEqual(second_task.task_name, "import-task-2")
        self.assertEqual(second_task.status, 0)

    @patch('volcengine.tls.TLSService.TLSService._TLSService__request')
    def test_describe_import_tasks_empty_result(self, mock_request):
        """Test describe_import_tasks with empty result"""
        # Mock empty response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({
            "Total": 0,
            "TaskInfo": []
        })
        mock_response.headers = {
            "X-Tls-Requestid": "test-request-id",
            "Content-Type": "application/json"
        }
        mock_request.return_value = mock_response

        # Create request
        request = DescribeImportTasksRequest(
            project_id="empty-project"
        )

        # Call the method
        response = self.tls_service.describe_import_tasks(request)

        # Verify the response
        self.assertEqual(response.get_total(), 0)
        self.assertEqual(len(response.get_task_info()), 0)

    @patch('volcengine.tls.TLSService.TLSService._TLSService__request')
    def test_describe_import_tasks_with_filters(self, mock_request):
        """Test describe_import_tasks with various filters"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({
            "Total": 1,
            "TaskInfo": [
                {
                    "TaskId": "filtered-task",
                    "TaskName": "filtered-task-name",
                    "TopicId": "filtered-topic",
                    "TopicName": "filtered-topic-name",
                    "ProjectId": "filtered-project",
                    "ProjectName": "filtered-project-name",
                    "Status": 1,
                    "CreateTime": "2023-12-01T10:00:00Z",
                    "ModifyTime": "2023-12-01T10:30:00Z",
                    "SourceType": "tos"
                }
            ]
        })
        mock_response.headers = {
            "X-Tls-Requestid": "test-request-id",
            "Content-Type": "application/json"
        }
        mock_request.return_value = mock_response

        # Create request with multiple filters
        request = DescribeImportTasksRequest(
            task_id="filtered-task",
            task_name="filtered-task-name",
            topic_id="filtered-topic",
            project_name="filtered-project-name",
            source_type="tos",
            status=1,
            page_number=1,
            page_size=20
        )

        # Call the method
        response = self.tls_service.describe_import_tasks(request)

        # Verify the request was called
        self.assertTrue(mock_request.called)

        # Verify response
        self.assertEqual(response.get_total(), 1)
        self.assertEqual(len(response.get_task_info()), 1)

        task = response.get_task_info()[0]
        self.assertEqual(task.task_id, "filtered-task")
        self.assertEqual(task.task_name, "filtered-task-name")

    def test_describe_import_tasks_request_validation(self):
        """Test that request validation works correctly"""
        # DescribeImportTasksRequest does not have check_validation method
        # This test verifies that the request can be created without validation errors
        request = DescribeImportTasksRequest()

        # Should be able to create request without required parameters
        self.assertIsNotNone(request)

        # All parameters should be optional, but default values will be included
        api_input = request.get_api_input()
        # The request will include default values for page_number and page_size
        self.assertIn('PageNumber', api_input)
        self.assertIn('PageSize', api_input)
        self.assertEqual(api_input['PageNumber'], 1)
        self.assertEqual(api_input['PageSize'], 20)


if __name__ == "__main__":
    unittest.main()
