# coding=utf-8
"""Unit tests for ModifyAlarmWebhookIntegration request and TLSService integration (without real backend).

本文件仅关注 ModifyAlarmWebhookIntegration 请求体结构与 TLSService 调用参数，不依赖真实后端环境。
"""
import os
import unittest
from unittest.mock import Mock, patch

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import ModifyAlarmWebhookIntegrationRequest, GeneralWebhookHeaderKV
from volcengine.tls.tls_responses import ModifyAlarmWebhookIntegrationResponse


class TestModifyAlarmWebhookIntegration(unittest.TestCase):
    """ModifyAlarmWebhookIntegration 单元测试。"""

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

    def test_request_validation(self):
        """测试 ModifyAlarmWebhookIntegrationRequest.check_validation 必填约束。"""
        # 缺少 WebhookID
        request = ModifyAlarmWebhookIntegrationRequest(
            webhook_id="",
            webhook_name="test-webhook",
            webhook_type="Lark",
            webhook_url="https://example.com/webhook",
        )
        self.assertFalse(request.check_validation())

        # GeneralWebhook 类型但缺少 Method/Headers
        request = ModifyAlarmWebhookIntegrationRequest(
            webhook_id="webhook-123",
            webhook_name="test-webhook",
            webhook_type="GeneralWebhook",
            webhook_url="https://example.com/webhook",
        )
        self.assertFalse(request.check_validation())

        # 非 GeneralWebhook 类型，仅要求 ID/Name/Type/Url 非空
        request = ModifyAlarmWebhookIntegrationRequest(
            webhook_id="webhook-123",
            webhook_name="test-webhook",
            webhook_type="Lark",
            webhook_url="https://example.com/webhook",
        )
        self.assertTrue(request.check_validation())

        # GeneralWebhook 类型完整参数
        headers = [GeneralWebhookHeaderKV(key="Content-Type", value="application/json")]
        request = ModifyAlarmWebhookIntegrationRequest(
            webhook_id="webhook-123",
            webhook_name="test-webhook",
            webhook_type="GeneralWebhook",
            webhook_url="https://example.com/webhook",
            webhook_method="POST",
            webhook_headers=headers,
        )
        self.assertTrue(request.check_validation())

    def test_get_api_input_general_webhook_type(self):
        """测试 GeneralWebhook 类型下 get_api_input 顶层键名与 Headers 序列化。"""
        headers = [GeneralWebhookHeaderKV(key="Content-Type", value="application/json")]

        request = ModifyAlarmWebhookIntegrationRequest(
            webhook_id="webhook-123",
            webhook_name="test-webhook",
            webhook_type="GeneralWebhook",
            webhook_url="https://example.com/webhook",
            webhook_method="POST",
            webhook_headers=headers,
            webhook_secret="example-secret",
        )

        api_input = request.get_api_input()
        self.assertEqual(api_input["WebhookID"], "webhook-123")
        self.assertEqual(api_input["WebhookName"], "test-webhook")
        self.assertEqual(api_input["WebhookType"], "GeneralWebhook")
        self.assertEqual(api_input["WebhookUrl"], "https://example.com/webhook")
        self.assertEqual(api_input["WebhookMethod"], "POST")
        self.assertEqual(api_input["WebhookSecret"], "example-secret")
        self.assertIn("WebhookHeaders", api_input)
        self.assertEqual(len(api_input["WebhookHeaders"]), 1)
        self.assertEqual(api_input["WebhookHeaders"][0]["Key"], "Content-Type")
        self.assertEqual(api_input["WebhookHeaders"][0]["Value"], "application/json")

    def test_response_parsing(self):
        """测试 ModifyAlarmWebhookIntegrationResponse 对 RequestId 的解析。"""

        class MockResponse:
            def __init__(self):
                self.headers = {"X-Tls-Requestid": "test-request-id", "Content-Type": "application/json"}
                self.text = ""
                self.content = b""

        mock_response = MockResponse()
        response = ModifyAlarmWebhookIntegrationResponse(mock_response)
        self.assertEqual(response.request_id, "test-request-id")
        self.assertEqual(response.headers, mock_response.headers)

    @patch("volcengine.tls.TLSService.TLSService._TLSService__request")
    def test_modify_alarm_webhook_integration_service_call(self, mock_request):
        """测试 TLSService.modify_alarm_webhook_integration 调用路径与请求体结构。"""
        headers = [GeneralWebhookHeaderKV(key="Content-Type", value="application/json")]
        request = ModifyAlarmWebhookIntegrationRequest(
            webhook_id="webhook-123",
            webhook_name="test-webhook",
            webhook_type="GeneralWebhook",
            webhook_url="https://example.com/webhook",
            webhook_method="POST",
            webhook_headers=headers,
        )

        mock_response = Mock()
        mock_response.headers = {
            "X-Tls-Requestid": "test-request-id",
            "Content-Type": "application/json",
        }
        mock_response.text = "{}"
        mock_request.return_value = mock_response

        response = self.tls_service.modify_alarm_webhook_integration(request)

        expected_body = request.get_api_input()
        mock_request.assert_called_once_with(
            api="/ModifyAlarmWebhookIntegration",
            body=expected_body,
        )
        self.assertIsInstance(response, ModifyAlarmWebhookIntegrationResponse)
        self.assertEqual(response.get_request_id(), "test-request-id")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
