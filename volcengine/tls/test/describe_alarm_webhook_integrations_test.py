# coding=utf-8
"""Unit tests for DescribeAlarmWebhookIntegrations request and TLSService integration (without real backend).

本文件仅关注 DescribeAlarmWebhookIntegrations 请求参数构造与 TLSService 调用参数，不依赖真实后端环境。
"""
import os
import unittest
from unittest.mock import Mock, patch

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import DescribeAlarmWebhookIntegrationsRequest
from volcengine.tls.tls_responses import DescribeAlarmWebhookIntegrationsResponse


class TestDescribeAlarmWebhookIntegrations(unittest.TestCase):
    """DescribeAlarmWebhookIntegrations 单元测试。"""

    def setUp(self):
        self.endpoint = os.environ.get(
            "VOLCENGINE_ENDPOINT", "https://tls-cn-beijing.ivolces.com"
        )
        self.region = os.environ.get("VOLCENGINE_REGION", "cn-beijing")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "test-ak")
        self.access_key_secret = os.environ.get(
            "VOLCENGINE_ACCESS_KEY_SECRET", "test-sk"
        )
        self.tls_service = TLSService(
            self.endpoint,
            self.access_key_id,
            self.access_key_secret,
            self.region,
        )

    def test_basic_request_fields_and_validation(self):
        """测试仅分页参数场景下的字段与校验。"""
        request = DescribeAlarmWebhookIntegrationsRequest(page_number=1, page_size=20)
        self.assertIsInstance(request, DescribeAlarmWebhookIntegrationsRequest)
        self.assertEqual(request.page_number, 1)
        self.assertEqual(request.page_size, 20)
        self.assertTrue(request.check_validation())

        api_input = request.get_api_input()
        self.assertEqual(api_input["PageNumber"], 1)
        self.assertEqual(api_input["PageSize"], 20)
        self.assertNotIn("WebhookID", api_input)
        self.assertNotIn("WebhookName", api_input)
        self.assertNotIn("WebhookType", api_input)

    def test_request_with_filters_and_pagination(self):
        """测试携带过滤条件与分页参数时的字段构造与校验。"""
        request = DescribeAlarmWebhookIntegrationsRequest(
            webhook_id="test-webhook-id",
            webhook_name="test-webhook-name",
            webhook_type="general",
            page_number=2,
            page_size=10,
        )

        self.assertEqual(request.webhook_id, "test-webhook-id")
        self.assertEqual(request.webhook_name, "test-webhook-name")
        self.assertEqual(request.webhook_type, "general")
        self.assertEqual(request.page_number, 2)
        self.assertEqual(request.page_size, 10)
        self.assertTrue(request.check_validation())

        api_input = request.get_api_input()
        self.assertEqual(api_input["WebhookID"], "test-webhook-id")
        self.assertEqual(api_input["WebhookName"], "test-webhook-name")
        self.assertEqual(api_input["WebhookType"], "general")
        self.assertEqual(api_input["PageNumber"], 2)
        self.assertEqual(api_input["PageSize"], 10)

    def test_request_validation_optional_fields(self):
        """测试所有参数可选场景下的校验逻辑。"""
        request = DescribeAlarmWebhookIntegrationsRequest()
        self.assertTrue(request.check_validation())

        request = DescribeAlarmWebhookIntegrationsRequest(
            webhook_id="",
            webhook_name="",
            webhook_type="",
        )
        self.assertTrue(request.check_validation())

    def test_get_api_input_field_mapping(self):
        """测试 get_api_input 字段命名与键名映射。"""
        request = DescribeAlarmWebhookIntegrationsRequest(
            webhook_id="test-id",
            webhook_name="test-name",
            webhook_type="test-type",
            page_number=1,
            page_size=20,
        )

        api_input = request.get_api_input()
        self.assertEqual(api_input["WebhookID"], "test-id")
        self.assertEqual(api_input["WebhookName"], "test-name")
        self.assertEqual(api_input["WebhookType"], "test-type")
        self.assertEqual(api_input["PageNumber"], 1)
        self.assertEqual(api_input["PageSize"], 20)

    @patch("volcengine.tls.TLSService.TLSService._TLSService__request")
    def test_describe_alarm_webhook_integrations_service_call_basic(self, mock_request):
        """测试 TLSService.describe_alarm_webhook_integrations 基础分页场景的调用路径与 params。"""
        request = DescribeAlarmWebhookIntegrationsRequest(page_number=1, page_size=20)

        mock_response = Mock()
        mock_response.headers = {
            "X-Tls-Requestid": "test-request-id",
            "Content-Type": "application/json",
        }
        mock_response.text = '{"Total": 0, "WebhookIntegrations": []}'
        mock_request.return_value = mock_response

        response = self.tls_service.describe_alarm_webhook_integrations(request)

        expected_params = request.get_api_input()
        mock_request.assert_called_once_with(
            api="/DescribeAlarmWebhookIntegrations",
            params=expected_params,
        )
        self.assertIsInstance(response, DescribeAlarmWebhookIntegrationsResponse)
        self.assertEqual(response.get_total(), 0)
        self.assertEqual(response.get_webhook_integrations(), [])
        self.assertEqual(response.get_request_id(), "test-request-id")

    @patch("volcengine.tls.TLSService.TLSService._TLSService__request")
    def test_describe_alarm_webhook_integrations_service_call_with_filters(self, mock_request):
        """测试 TLSService.describe_alarm_webhook_integrations 携带过滤条件与分页参数时的调用。"""
        request = DescribeAlarmWebhookIntegrationsRequest(
            webhook_id="test-id",
            webhook_name="test-name",
            webhook_type="custom",
            page_number=3,
            page_size=50,
        )

        mock_response = Mock()
        mock_response.headers = {
            "X-Tls-Requestid": "test-request-id",
            "Content-Type": "application/json",
        }
        mock_response.text = '{"Total": 1, "WebhookIntegrations": []}'
        mock_request.return_value = mock_response

        response = self.tls_service.describe_alarm_webhook_integrations(request)

        expected_params = request.get_api_input()
        mock_request.assert_called_once_with(
            api="/DescribeAlarmWebhookIntegrations",
            params=expected_params,
        )
        self.assertIsInstance(response, DescribeAlarmWebhookIntegrationsResponse)
        self.assertEqual(response.get_total(), 1)
        self.assertEqual(response.get_request_id(), "test-request-id")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
