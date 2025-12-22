import os
import unittest
from unittest.mock import Mock, patch

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import ModifyTraceInstanceRequest
from volcengine.tls.tls_responses import ModifyTraceInstanceResponse
from volcengine.tls.const import MODIFY_TRACE_INSTANCE


class TestModifyTraceInstance(unittest.TestCase):

    def setUp(self):
        self.endpoint = os.environ.get(
            "VOLCENGINE_ENDPOINT", "tls-cn-beijing.ivolces.com"
        )
        self.region = os.environ.get("VOLCENGINE_REGION", "cn-beijing")
        self.access_key_id = os.environ.get(
            "VOLCENGINE_ACCESS_KEY_ID", "test_ak"
        )
        self.access_key_secret = os.environ.get(
            "VOLCENGINE_ACCESS_KEY_SECRET", "test_sk"
        )

        self.tls_service = TLSService(
            self.endpoint,
            self.access_key_id,
            self.access_key_secret,
            self.region
        )

    def test_modify_trace_instance_request_validation(self):
        # Test with valid parameters
        request = ModifyTraceInstanceRequest(
            trace_instance_id="test-trace-instance-id",
            description="Updated description"
        )
        self.assertTrue(request.check_validation())

        # Test with missing required parameter
        request_invalid = ModifyTraceInstanceRequest(
            trace_instance_id=None,
            description="Updated description"
        )
        self.assertFalse(request_invalid.check_validation())

    @patch('volcengine.tls.TLSService.TLSService._TLSService__request')
    def test_modify_trace_instance_success(self, mock_request):
        # Mock successful response
        mock_response = Mock()
        mock_response.headers = {
            'X-Tls-Requestid': 'test-request-id',
            'Content-Type': 'application/json'
        }
        mock_response.text = '{"Response": {}}'
        mock_request.return_value = mock_response

        # Create request
        request = ModifyTraceInstanceRequest(
            trace_instance_id="test-trace-instance-id",
            description="Updated description"
        )

        # Call the method
        response = self.tls_service.modify_trace_instance(request)

        # Verify the response
        self.assertIsInstance(response, ModifyTraceInstanceResponse)
        self.assertEqual(response.get_request_id(), 'test-request-id')

        # Verify the API was called correctly
        mock_request.assert_called_once_with(
            api=MODIFY_TRACE_INSTANCE,
            body={
                'TraceInstanceId': 'test-trace-instance-id',
                'Description': 'Updated description'
            }
        )

    def test_modify_trace_instance_integration_style(self):
        """Integration style test similar to the Node.js test"""
        # This test demonstrates the usage pattern similar to the Node.js test
        # In a real integration test, you would:
        # 1. Create a trace instance
        # 2. Modify it
        # 3. Verify the modification
        # 4. Clean up

        # For unit testing, we just verify the request structure
        trace_instance_id = "test-trace-instance-id"
        new_description = "jest-modify"

        request = ModifyTraceInstanceRequest(
            trace_instance_id=trace_instance_id,
            description=new_description
        )

        # Verify request structure
        api_input = request.get_api_input()
        expected_input = {
            'TraceInstanceId': trace_instance_id,
            'Description': new_description
        }
        self.assertEqual(api_input, expected_input)


if __name__ == '__main__':
    unittest.main()