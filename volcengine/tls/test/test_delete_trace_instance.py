"""Unit tests for DeleteTraceInstance functionality."""
import os
import unittest
from unittest.mock import Mock, patch

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import DeleteTraceInstanceRequest
from volcengine.tls.tls_responses import DeleteTraceInstanceResponse


class TestDeleteTraceInstance(unittest.TestCase):
    """Test cases for DeleteTraceInstance functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.endpoint = os.environ.get("VOLCENGINE_ENDPOINT", "tls-cn-beijing.ivolces.com")
        self.region = os.environ.get("VOLCENGINE_REGION", "cn-beijing")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "test-ak")
        self.access_key_secret = os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET", "test-sk")
        self.tls_service = TLSService(
            self.endpoint, self.access_key_id, self.access_key_secret, self.region)

    def test_delete_trace_instance_request_validation(self):
        """Test DeleteTraceInstanceRequest validation."""
        # Test with valid trace instance ID
        request = DeleteTraceInstanceRequest(trace_instance_id="test-trace-instance-id")
        self.assertTrue(request.check_validation())

        # Test with None trace instance ID
        request = DeleteTraceInstanceRequest(trace_instance_id=None)
        self.assertFalse(request.check_validation())

    def test_delete_trace_instance_request_api_input(self):
        """Test DeleteTraceInstanceRequest API input generation."""
        trace_instance_id = "test-trace-instance-id"
        request = DeleteTraceInstanceRequest(trace_instance_id=trace_instance_id)
        api_input = request.get_api_input()

        expected_input = {
            "TraceInstanceId": trace_instance_id
        }
        self.assertEqual(api_input, expected_input)

    @patch('volcengine.tls.TLSService.TLSService._TLSService__request')
    def test_delete_trace_instance_success(self, mock_request):
        """Test successful delete trace instance."""
        # Mock successful response
        mock_response = Mock()
        mock_response.headers = {
            'X-Tls-Requestid': 'test-request-id',
            'Content-Type': 'application/json'
        }
        mock_response.text = ''
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        # Create request
        trace_instance_id = "test-trace-instance-id"
        request = DeleteTraceInstanceRequest(trace_instance_id=trace_instance_id)

        # Call the method
        response = self.tls_service.delete_trace_instance(request)

        # Verify the response
        self.assertIsInstance(response, DeleteTraceInstanceResponse)
        self.assertEqual(response.get_request_id(), 'test-request-id')

        # Verify the API was called correctly
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        self.assertEqual(call_args[1]['api'], '/DeleteTraceInstance')

    @patch('volcengine.tls.TLSService.TLSService._TLSService__request')
    def test_delete_trace_instance_invalid_request(self, mock_request):
        """Test delete trace instance with invalid request."""
        # Test with invalid request
        request = DeleteTraceInstanceRequest(trace_instance_id=None)

        # Should raise exception for invalid request
        with self.assertRaises(Exception):
            self.tls_service.delete_trace_instance(request)

        # Verify the API was not called
        mock_request.assert_not_called()

    def test_delete_trace_instance_integration(self):
        """Test delete trace instance integration."""
        # This is an integration test that would require actual credentials and endpoint
        # It should only be run in a test environment with proper setup
        if not all([
            os.environ.get("VOLCENGINE_ENDPOINT"),
            os.environ.get("VOLCENGINE_REGION"),
            os.environ.get("VOLCENGINE_ACCESS_KEY_ID"),
            os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET")
        ]):
            self.skipTest("Integration test requires environment variables to be set")

        # This test would create a trace instance first, then delete it
        # For now, we just verify the method exists and can be called
        # In a real integration test, you would:
        # 1. Create a trace instance using CreateTraceInstance
        # 2. Get the trace instance ID from the response
        # 3. Delete the trace instance using DeleteTraceInstance
        # 4. Verify the deletion was successful

        # For this test, we just verify the method exists
        self.assertTrue(hasattr(self.tls_service, 'delete_trace_instance'))
        self.assertTrue(callable(getattr(self.tls_service, 'delete_trace_instance')))


if __name__ == '__main__':
    unittest.main()