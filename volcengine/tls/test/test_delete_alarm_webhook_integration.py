"""Unit tests for DeleteAlarmWebhookIntegration functionality."""
import os
import unittest
from unittest.mock import Mock, patch

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import DeleteAlarmWebhookIntegrationRequest
from volcengine.tls.tls_responses import DeleteAlarmWebhookIntegrationResponse


class TestDeleteAlarmWebhookIntegration(unittest.TestCase):
    """Test cases for DeleteAlarmWebhookIntegration functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.endpoint = os.environ.get("VOLCENGINE_ENDPOINT", "tls-cn-beijing.ivolces.com")
        self.region = os.environ.get("VOLCENGINE_REGION", "cn-beijing")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "test-ak")
        self.access_key_secret = os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET", "test-sk")
        self.tls_service = TLSService(
            self.endpoint, self.access_key_id, self.access_key_secret, self.region)

    def test_delete_alarm_webhook_integration_request_validation(self):
        """Test DeleteAlarmWebhookIntegrationRequest validation."""
        # Test with valid webhook ID
        request = DeleteAlarmWebhookIntegrationRequest(webhook_id="test-webhook-id-12345")
        self.assertTrue(request.check_validation())

        # Test with None webhook ID
        request = DeleteAlarmWebhookIntegrationRequest(webhook_id=None)
        self.assertFalse(request.check_validation())

    def test_delete_alarm_webhook_integration_request_api_input(self):
        """Test DeleteAlarmWebhookIntegrationRequest API input generation."""
        webhook_id = "test-webhook-id-12345"
        request = DeleteAlarmWebhookIntegrationRequest(webhook_id=webhook_id)
        api_input = request.get_api_input()

        expected_input = {
            "WebhookID": webhook_id
        }
        self.assertEqual(api_input, expected_input)

    @patch('volcengine.tls.TLSService.TLSService._TLSService__request')
    def test_delete_alarm_webhook_integration_success(self, mock_request):
        """Test successful delete alarm webhook integration."""
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
        webhook_id = "test-webhook-id-12345"
        request = DeleteAlarmWebhookIntegrationRequest(webhook_id=webhook_id)

        # Call the method
        response = self.tls_service.delete_alarm_webhook_integration(request)

        # Verify the response
        self.assertIsInstance(response, DeleteAlarmWebhookIntegrationResponse)
        self.assertEqual(response.get_request_id(), 'test-request-id')

        # Verify the API was called correctly
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        self.assertEqual(call_args[1]['api'], '/DeleteAlarmWebhookIntegration')

    @patch('volcengine.tls.TLSService.TLSService._TLSService__request')
    def test_delete_alarm_webhook_integration_invalid_request(self, mock_request):
        """Test delete alarm webhook integration with invalid request."""
        # Test with invalid request
        request = DeleteAlarmWebhookIntegrationRequest(webhook_id=None)

        # Should raise exception for invalid request
        with self.assertRaises(Exception):
            self.tls_service.delete_alarm_webhook_integration(request)

        # Verify the API was not called
        mock_request.assert_not_called()

    def test_delete_alarm_webhook_integration_integration(self):
        """Test delete alarm webhook integration integration."""
        # This is an integration test that would require actual credentials and endpoint
        # It should only be run in a test environment with proper setup
        if not all([
            os.environ.get("VOLCENGINE_ENDPOINT"),
            os.environ.get("VOLCENGINE_REGION"),
            os.environ.get("VOLCENGINE_ACCESS_KEY_ID"),
            os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET")
        ]):
            self.skipTest("Integration test requires environment variables to be set")

        # This test would create a webhook integration first, then delete it
        # For now, we just verify the method exists and can be called
        # In a real integration test, you would:
        # 1. Create a webhook integration using CreateAlarmWebhookIntegration
        # 2. Get the webhook ID from the response
        # 3. Delete the webhook integration using DeleteAlarmWebhookIntegration
        # 4. Verify the deletion was successful

        # For this test, we just verify the method exists
        self.assertTrue(hasattr(self.tls_service, 'delete_alarm_webhook_integration'))
        self.assertTrue(callable(getattr(self.tls_service, 'delete_alarm_webhook_integration')))


if __name__ == '__main__':
    unittest.main()
