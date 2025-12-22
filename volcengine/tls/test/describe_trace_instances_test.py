"""Unit tests for DescribeTraceInstances functionality."""
import os
import unittest

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import DescribeTraceInstancesRequest
from volcengine.tls.data import TraceInstanceInfo


class TestDescribeTraceInstances(unittest.TestCase):
    """Test cases for DescribeTraceInstances functionality."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = os.environ.get("VOLCENGINE_ENDPOINT", "")
        self.region = os.environ.get("VOLCENGINE_REGION", "")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "")
        self.access_key_secret = os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET", "")

    def test_describe_trace_instances_basic(self):
        """Test basic DescribeTraceInstances functionality."""
        if not all([self.endpoint, self.region, self.access_key_id, self.access_key_secret]):
            self.skipTest("Missing required environment variables")

        # Create TLS client
        TLSService(
            self.endpoint, self.access_key_id, self.access_key_secret, self.region)

        # Create request
        request = DescribeTraceInstancesRequest(
            page_number=1,
            page_size=20
        )

        # Verify request parameters
        self.assertTrue(request.check_validation())
        self.assertEqual(request.page_number, 1)
        self.assertEqual(request.page_size, 20)

        # Test API input format
        api_input = request.get_api_input()
        self.assertIn("PageNumber", api_input)
        self.assertIn("PageSize", api_input)
        self.assertEqual(api_input["PageNumber"], 1)
        self.assertEqual(api_input["PageSize"], 20)

    def test_describe_trace_instances_with_filters(self):
        """Test DescribeTraceInstances functionality with filters."""
        request = DescribeTraceInstancesRequest(
            page_number=1,
            page_size=10,
            trace_instance_name="test-trace",
            project_id="test-project",
            status="CREATED"
        )

        # Verify request parameters
        self.assertTrue(request.check_validation())
        self.assertEqual(request.page_size, 10)
        self.assertEqual(request.trace_instance_name, "test-trace")
        self.assertEqual(request.project_id, "test-project")
        self.assertEqual(request.status, "CREATED")

        # Test API input format
        api_input = request.get_api_input()
        self.assertIn("TraceInstanceName", api_input)
        self.assertIn("ProjectId", api_input)
        self.assertIn("Status", api_input)
        self.assertEqual(api_input["TraceInstanceName"], "test-trace")
        self.assertEqual(api_input["ProjectId"], "test-project")
        self.assertEqual(api_input["Status"], "CREATED")

    def test_describe_trace_instances_validation(self):
        """Test request parameter validation."""
        # Test default parameters
        request = DescribeTraceInstancesRequest()
        self.assertTrue(request.check_validation())

        # Test custom parameters
        request = DescribeTraceInstancesRequest(
            page_number=2,
            page_size=50,
            iam_project_name="test-iam-project"
        )
        self.assertTrue(request.check_validation())

    def test_trace_instance_info_data_structure(self):
        """Test TraceInstanceInfo data structure."""
        # Create TraceInstanceInfo object
        trace_instance = TraceInstanceInfo(
            trace_instance_id="trace-123",
            trace_instance_name="test-trace-instance",
            project_id="project-456",
            project_name="test-project",
            trace_topic_id="topic-789",
            trace_topic_name="test-trace-topic",
            dependency_topic_id="dep-topic-111",
            dependency_topic_topic_name="test-dep-topic",
            trace_instance_status="CREATED",
            description="Test trace instance",
            create_time="2023-01-01T00:00:00Z",
            modify_time="2023-01-02T00:00:00Z"
        )

        # Verify getter methods
        self.assertEqual(trace_instance.get_trace_instance_id(), "trace-123")
        self.assertEqual(trace_instance.get_trace_instance_name(), "test-trace-instance")
        self.assertEqual(trace_instance.get_project_id(), "project-456")
        self.assertEqual(trace_instance.get_project_name(), "test-project")
        self.assertEqual(trace_instance.get_trace_topic_id(), "topic-789")
        self.assertEqual(trace_instance.get_trace_topic_name(), "test-trace-topic")
        self.assertEqual(trace_instance.get_dependency_topic_id(), "dep-topic-111")
        self.assertEqual(trace_instance.get_dependency_topic_topic_name(), "test-dep-topic")
        self.assertEqual(trace_instance.get_trace_instance_status(), "CREATED")
        self.assertEqual(trace_instance.get_description(), "Test trace instance")
        self.assertEqual(trace_instance.get_create_time(), "2023-01-01T00:00:00Z")
        self.assertEqual(trace_instance.get_modify_time(), "2023-01-02T00:00:00Z")


if __name__ == '__main__':
    unittest.main()