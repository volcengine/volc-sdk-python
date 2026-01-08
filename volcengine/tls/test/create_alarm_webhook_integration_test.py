# coding=utf-8
"""Unit tests for CreateAlarmWebhookIntegration request and TLSService integration (without real backend).

本文件仅关注 CreateAlarmWebhookIntegration 请求体结构与 TLSService 调用参数，不依赖真实后端环境。
"""
import os
import unittest
from unittest.mock import Mock, patch

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import CreateAlarmWebhookIntegrationRequest, GeneralWebhookHeaderKV
from volcengine.tls.tls_responses import CreateAlarmWebhookIntegrationResponse


class TestCreateAlarmWebhookIntegration(unittest.TestCase):
    """CreateAlarmWebhookIntegration 单元测试类。"""

    def setUp(self):
        """使用本地默认配置构造 TLSService，避免依赖真实环境变量和后端。"""
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
        """测试请求参数验证逻辑（必填字段与 GeneralWebhook 约束）。"""
        # 缺少必填参数
        request = CreateAlarmWebhookIntegrationRequest(
            webhook_name="",
            webhook_type="Lark",
            webhook_url="",
        )
        self.assertFalse(request.check_validation())

        # GeneralWebhook 类型但缺少 method/headers
        request = CreateAlarmWebhookIntegrationRequest(
            webhook_name="test-webhook",
            webhook_type="GeneralWebhook",
            webhook_url="https://example.com/webhook",
        )
        self.assertFalse(request.check_validation())

        # 正确的 Lark 配置（非 GeneralWebhook 类型，仅要求 Name/Type/Url 非空）
        request = CreateAlarmWebhookIntegrationRequest(
            webhook_name="test-webhook",
            webhook_type="Lark",
            webhook_url="https://example.com/webhook",
        )
        self.assertTrue(request.check_validation())

        # 正确的 GeneralWebhook 配置（Type 为 GeneralWebhook 时需要 Method + Headers）
        headers = [GeneralWebhookHeaderKV(key="Content-Type", value="application/json")]
        request = CreateAlarmWebhookIntegrationRequest(
            webhook_name="test-webhook",
            webhook_type="GeneralWebhook",
            webhook_url="https://example.com/webhook",
            webhook_method="POST",
            webhook_headers=headers,
        )
        self.assertTrue(request.check_validation())

    def test_get_api_input_general_type(self):
        """测试非 GeneralWebhook 类型（如 Lark）下顶层键名与字段构造。"""
        request = CreateAlarmWebhookIntegrationRequest(
            webhook_name="lark-webhook",
            webhook_type="Lark",
            webhook_url="https://example.com/lark",
        )

        api_input = request.get_api_input()
        self.assertEqual(api_input["WebhookName"], "lark-webhook")
        self.assertEqual(api_input["WebhookType"], "Lark")
        self.assertEqual(api_input["WebhookUrl"], "https://example.com/lark")
        # 非 GeneralWebhook 场景下 Method / Headers / Secret 可选，不应强制出现在请求体中
        self.assertNotIn("WebhookMethod", api_input)
        self.assertNotIn("WebhookHeaders", api_input)
        self.assertNotIn("WebhookSecret", api_input)

    def test_get_api_input_general_webhook_type(self):
        """测试 GeneralWebhook 类型下顶层键名与 Headers 序列化。"""
        headers = [
            GeneralWebhookHeaderKV(key="Content-Type", value="application/json"),
            GeneralWebhookHeaderKV(key="Authorization", value="Bearer AUTH_PLACEHOLDER"),
        ]
        request = CreateAlarmWebhookIntegrationRequest(
            webhook_name="custom-webhook",
            webhook_type="GeneralWebhook",
            webhook_url="https://example.com/custom",
            webhook_method="POST",
            webhook_headers=headers,
            webhook_secret="example-secret",
        )

        api_input = request.get_api_input()
        self.assertEqual(api_input["WebhookName"], "custom-webhook")
        self.assertEqual(api_input["WebhookType"], "GeneralWebhook")
        self.assertEqual(api_input["WebhookUrl"], "https://example.com/custom")
        self.assertEqual(api_input["WebhookMethod"], "POST")
        self.assertEqual(api_input["WebhookSecret"], "example-secret")

        self.assertIn("WebhookHeaders", api_input)
        self.assertEqual(len(api_input["WebhookHeaders"]), 2)
        self.assertEqual(
            api_input["WebhookHeaders"][0],
            {"Key": "Content-Type", "Value": "application/json"},
        )
        self.assertEqual(
            api_input["WebhookHeaders"][1],
            {"Key": "Authorization", "Value": "Bearer AUTH_PLACEHOLDER"},
        )

    @patch("volcengine.tls.TLSService.TLSService._TLSService__request")
    def test_create_alarm_webhook_integration_service_call_lark(self, mock_request):
        """测试 TLSService.create_alarm_webhook_integration 在 Lark 类型下的调用路径与请求体。"""
        request = CreateAlarmWebhookIntegrationRequest(
            webhook_name="lark-webhook",
            webhook_type="Lark",
            webhook_url="https://example.com/lark",
        )

        mock_response = Mock()
        mock_response.headers = {
            "X-Tls-Requestid": "test-request-id",
            "Content-Type": "application/json",
        }
        mock_response.text = '{"AlarmWebhookIntegrationId": "webhook-123"}'
        mock_request.return_value = mock_response

        response = self.tls_service.create_alarm_webhook_integration(request)

        expected_body = request.get_api_input()
        mock_request.assert_called_once_with(
            api="/CreateAlarmWebhookIntegration",
            body=expected_body,
        )
        self.assertIsInstance(response, CreateAlarmWebhookIntegrationResponse)
        self.assertEqual(response.get_alarm_webhook_integration_id(), "webhook-123")
        self.assertEqual(response.get_request_id(), "test-request-id")

    @patch("volcengine.tls.TLSService.TLSService._TLSService__request")
    def test_create_alarm_webhook_integration_service_call_general_webhook(self, mock_request):
        """测试 TLSService.create_alarm_webhook_integration 在 GeneralWebhook 类型下的调用路径与请求体。"""
        headers = [GeneralWebhookHeaderKV(key="Content-Type", value="application/json")]
        request = CreateAlarmWebhookIntegrationRequest(
            webhook_name="custom-webhook",
            webhook_type="GeneralWebhook",
            webhook_url="https://example.com/custom",
            webhook_method="POST",
            webhook_headers=headers,
        )

        mock_response = Mock()
        mock_response.headers = {
            "X-Tls-Requestid": "test-request-id",
            "Content-Type": "application/json",
        }
        mock_response.text = '{"AlarmWebhookIntegrationId": "webhook-456"}'
        mock_request.return_value = mock_response

        response = self.tls_service.create_alarm_webhook_integration(request)

        expected_body = request.get_api_input()
        mock_request.assert_called_once_with(
            api="/CreateAlarmWebhookIntegration",
            body=expected_body,
        )
        self.assertIsInstance(response, CreateAlarmWebhookIntegrationResponse)
        self.assertEqual(response.get_alarm_webhook_integration_id(), "webhook-456")
        self.assertEqual(response.get_request_id(), "test-request-id")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
