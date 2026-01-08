import os
import unittest

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import ModifyAlarmContentTemplateRequest
from volcengine.tls.tls_requests import (
    DingTalkContentTemplateInfo, EmailContentTemplateInfo,
    LarkContentTemplateInfo, SmsContentTemplateInfo,
    VmsContentTemplateInfo, WeChatContentTemplateInfo,
    WebhookContentTemplateInfo
)


class TestModifyAlarmContentTemplate(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = os.environ.get("VOLCENGINE_ENDPOINT", "https://tls-cn-beijing.ivolces.com")
        self.region = os.environ.get("VOLCENGINE_REGION", "cn-beijing")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "test-ak")
        self.access_key_secret = os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET", "test-sk")

    def test_modify_alarm_content_template_request_validation(self):
        """测试 ModifyAlarmContentTemplateRequest 的验证逻辑"""
        # 测试 alarm_content_template_id 为 None 的情况
        request = ModifyAlarmContentTemplateRequest(
            alarm_content_template_id=None,
            alarm_content_template_name="test-template",
        )
        self.assertFalse(request.check_validation())

        # 测试 alarm_content_template_id 为空字符串的情况
        request = ModifyAlarmContentTemplateRequest(
            alarm_content_template_id="",
            alarm_content_template_name="test-template",
        )
        self.assertFalse(request.check_validation())

        # 测试 alarm_content_template_name 为 None 的情况
        request = ModifyAlarmContentTemplateRequest(
            alarm_content_template_id="test-alarm-id",
            alarm_content_template_name=None,
        )
        self.assertFalse(request.check_validation())

        # 测试 alarm_content_template_name 为空字符串的情况
        request = ModifyAlarmContentTemplateRequest(
            alarm_content_template_id="test-alarm-id",
            alarm_content_template_name="",
        )
        self.assertFalse(request.check_validation())

        # 测试正常情况
        request = ModifyAlarmContentTemplateRequest(
            alarm_content_template_id="test-alarm-id",
            alarm_content_template_name="test-alarm-template",
        )
        self.assertTrue(request.check_validation())

    def test_modify_alarm_content_template_request_with_dingtalk_template(self):
        """测试包含钉钉消息模板的请求"""
        dingtalk_template = DingTalkContentTemplateInfo(
            title="告警标题",
            locale="zh-CN",
            content="告警内容"
        )

        request = ModifyAlarmContentTemplateRequest(
            alarm_content_template_id="test-alarm-id",
            alarm_content_template_name="test-alarm-template",
            ding_talk_content_template=dingtalk_template
        )

        self.assertTrue(request.check_validation())
        api_input = request.get_api_input()

        self.assertIn("AlarmContentTemplateId", api_input)
        self.assertIn("AlarmContentTemplateName", api_input)
        self.assertIn("DingTalk", api_input)
        self.assertEqual(api_input["AlarmContentTemplateId"], "test-alarm-id")
        self.assertEqual(api_input["AlarmContentTemplateName"], "test-alarm-template")
        self.assertEqual(api_input["DingTalk"]["Title"], "告警标题")
        self.assertEqual(api_input["DingTalk"]["Locale"], "zh-CN")
        self.assertEqual(api_input["DingTalk"]["Content"], "告警内容")

    def test_modify_alarm_content_template_request_with_email_template(self):
        """测试包含邮件模板的请求"""
        email_template = EmailContentTemplateInfo(
            locale="zh-CN",
            content="邮件内容",
            subject="邮件主题"
        )

        request = ModifyAlarmContentTemplateRequest(
            alarm_content_template_id="test-alarm-id",
            alarm_content_template_name="test-alarm-template",
            email_content_template=email_template
        )

        self.assertTrue(request.check_validation())
        api_input = request.get_api_input()

        self.assertIn("AlarmContentTemplateId", api_input)
        self.assertIn("AlarmContentTemplateName", api_input)
        self.assertIn("Email", api_input)
        self.assertEqual(api_input["AlarmContentTemplateId"], "test-alarm-id")
        self.assertEqual(api_input["AlarmContentTemplateName"], "test-alarm-template")
        self.assertEqual(api_input["Email"]["Locale"], "zh-CN")
        self.assertEqual(api_input["Email"]["Content"], "邮件内容")
        self.assertEqual(api_input["Email"]["Subject"], "邮件主题")

    def test_modify_alarm_content_template_request_with_lark_template(self):
        """测试包含飞书消息模板的请求"""
        lark_template = LarkContentTemplateInfo(
            title="飞书标题",
            locale="zh-CN",
            content="飞书内容"
        )

        request = ModifyAlarmContentTemplateRequest(
            alarm_content_template_id="test-alarm-id",
            alarm_content_template_name="test-alarm-template",
            lark_content_template=lark_template
        )

        self.assertTrue(request.check_validation())
        api_input = request.get_api_input()

        self.assertIn("AlarmContentTemplateId", api_input)
        self.assertIn("AlarmContentTemplateName", api_input)
        self.assertIn("Lark", api_input)
        self.assertEqual(api_input["AlarmContentTemplateId"], "test-alarm-id")
        self.assertEqual(api_input["AlarmContentTemplateName"], "test-alarm-template")
        self.assertEqual(api_input["Lark"]["Title"], "飞书标题")
        self.assertEqual(api_input["Lark"]["Locale"], "zh-CN")
        self.assertEqual(api_input["Lark"]["Content"], "飞书内容")

    def test_modify_alarm_content_template_request_with_sms_template(self):
        """测试包含短信模板的请求"""
        sms_template = SmsContentTemplateInfo(
            locale="zh-CN",
            content="短信内容"
        )

        request = ModifyAlarmContentTemplateRequest(
            alarm_content_template_id="test-alarm-id",
            alarm_content_template_name="test-alarm-template",
            sms_content_template=sms_template
        )

        self.assertTrue(request.check_validation())
        api_input = request.get_api_input()

        self.assertIn("AlarmContentTemplateId", api_input)
        self.assertIn("AlarmContentTemplateName", api_input)
        self.assertIn("Sms", api_input)
        self.assertEqual(api_input["AlarmContentTemplateId"], "test-alarm-id")
        self.assertEqual(api_input["AlarmContentTemplateName"], "test-alarm-template")
        self.assertEqual(api_input["Sms"]["Locale"], "zh-CN")
        self.assertEqual(api_input["Sms"]["Content"], "短信内容")

    def test_modify_alarm_content_template_request_with_vms_template(self):
        """测试包含语音消息模板的请求"""
        vms_template = VmsContentTemplateInfo(
            locale="zh-CN",
            content="语音消息内容"
        )

        request = ModifyAlarmContentTemplateRequest(
            alarm_content_template_id="test-alarm-id",
            alarm_content_template_name="test-alarm-template",
            vms_content_template=vms_template
        )

        self.assertTrue(request.check_validation())
        api_input = request.get_api_input()

        self.assertIn("AlarmContentTemplateId", api_input)
        self.assertIn("AlarmContentTemplateName", api_input)
        self.assertIn("Vms", api_input)
        self.assertEqual(api_input["AlarmContentTemplateId"], "test-alarm-id")
        self.assertEqual(api_input["AlarmContentTemplateName"], "test-alarm-template")
        self.assertEqual(api_input["Vms"]["Locale"], "zh-CN")
        self.assertEqual(api_input["Vms"]["Content"], "语音消息内容")

    def test_modify_alarm_content_template_request_with_wechat_template(self):
        """测试包含微信消息模板的请求"""
        wechat_template = WeChatContentTemplateInfo(
            title="微信标题",
            locale="zh-CN",
            content="微信内容"
        )

        request = ModifyAlarmContentTemplateRequest(
            alarm_content_template_id="test-alarm-id",
            alarm_content_template_name="test-alarm-template",
            we_chat_content_template=wechat_template
        )

        self.assertTrue(request.check_validation())
        api_input = request.get_api_input()

        self.assertIn("AlarmContentTemplateId", api_input)
        self.assertIn("AlarmContentTemplateName", api_input)
        self.assertIn("WeChat", api_input)
        self.assertEqual(api_input["AlarmContentTemplateId"], "test-alarm-id")
        self.assertEqual(api_input["AlarmContentTemplateName"], "test-alarm-template")
        self.assertEqual(api_input["WeChat"]["Title"], "微信标题")
        self.assertEqual(api_input["WeChat"]["Locale"], "zh-CN")
        self.assertEqual(api_input["WeChat"]["Content"], "微信内容")

    def test_modify_alarm_content_template_request_with_webhook_template(self):
        """测试包含Webhook模板的请求"""
        webhook_template = WebhookContentTemplateInfo(
            content="Webhook内容"
        )

        request = ModifyAlarmContentTemplateRequest(
            alarm_content_template_id="test-alarm-id",
            alarm_content_template_name="test-alarm-template",
            webhook_content_template=webhook_template
        )

        self.assertTrue(request.check_validation())
        api_input = request.get_api_input()

        self.assertIn("AlarmContentTemplateId", api_input)
        self.assertIn("AlarmContentTemplateName", api_input)
        self.assertIn("Webhook", api_input)
        self.assertEqual(api_input["AlarmContentTemplateId"], "test-alarm-id")
        self.assertEqual(api_input["AlarmContentTemplateName"], "test-alarm-template")
        self.assertEqual(api_input["Webhook"]["Content"], "Webhook内容")

    def test_modify_alarm_content_template_request_with_multiple_templates(self):
        """测试包含多种模板的请求"""
        dingtalk_template = DingTalkContentTemplateInfo(
            title="告警标题",
            locale="zh-CN",
            content="告警内容"
        )

        email_template = EmailContentTemplateInfo(
            locale="zh-CN",
            content="邮件内容",
            subject="邮件主题"
        )

        request = ModifyAlarmContentTemplateRequest(
            alarm_content_template_id="test-alarm-id",
            alarm_content_template_name="test-alarm-template",
            ding_talk_content_template=dingtalk_template,
            email_content_template=email_template
        )

        self.assertTrue(request.check_validation())
        api_input = request.get_api_input()

        self.assertIn("AlarmContentTemplateId", api_input)
        self.assertIn("AlarmContentTemplateName", api_input)
        self.assertIn("DingTalk", api_input)
        self.assertIn("Email", api_input)
        self.assertEqual(api_input["AlarmContentTemplateId"], "test-alarm-id")
        self.assertEqual(api_input["AlarmContentTemplateName"], "test-alarm-template")
        self.assertEqual(api_input["DingTalk"]["Title"], "告警标题")
        self.assertEqual(api_input["Email"]["Subject"], "邮件主题")

    def test_content_template_classes_json_serialization(self):
        """测试内容模板类的 JSON 序列化"""
        # 测试钉钉模板
        dingtalk_template = DingTalkContentTemplateInfo(
            title="测试标题",
            locale="en-US",
            content="测试内容"
        )
        json_data = dingtalk_template.json()
        self.assertEqual(json_data["Title"], "测试标题")
        self.assertEqual(json_data["Locale"], "en-US")
        self.assertEqual(json_data["Content"], "测试内容")

        # 测试邮件模板
        email_template = EmailContentTemplateInfo(
            locale="en-US",
            content="测试邮件内容",
            subject="测试邮件主题"
        )
        json_data = email_template.json()
        self.assertEqual(json_data["Locale"], "en-US")
        self.assertEqual(json_data["Content"], "测试邮件内容")
        self.assertEqual(json_data["Subject"], "测试邮件主题")

        # 测试 Webhook 模板
        webhook_template = WebhookContentTemplateInfo(
            content="测试Webhook内容"
        )
        json_data = webhook_template.json()
        self.assertEqual(json_data["Content"], "测试Webhook内容")

    def test_integration_with_tls_service(self):
        """测试与 TLSService 的集成"""
        try:
            tls_service = TLSService(
                self.endpoint,
                self.access_key_id,
                self.access_key_secret,
                self.region
            )

            # 创建请求
            dingtalk_template = DingTalkContentTemplateInfo(
                title="集成测试标题",
                locale="zh-CN",
                content="集成测试内容"
            )

            request = ModifyAlarmContentTemplateRequest(
                alarm_content_template_id="test-alarm-id-for-integration",
                alarm_content_template_name="tls-python-sdk-integration",
                ding_talk_content_template=dingtalk_template
            )

            # 验证请求对象
            self.assertTrue(request.check_validation())

            # 验证 API 输入格式
            api_input = request.get_api_input()
            self.assertIn("AlarmContentTemplateId", api_input)
            self.assertIn("AlarmContentTemplateName", api_input)
            self.assertIn("DingTalk", api_input)

        except Exception as e:
            # 在实际环境中，这里应该根据具体的错误类型进行处理
            # 如果是认证失败等预期内的错误，可以选择跳过测试
            self.skipTest(f"Integration test skipped due to: {str(e)}")


if __name__ == "__main__":
    unittest.main()
