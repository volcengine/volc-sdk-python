import os
import unittest
import random
import string

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import CreateAlarmContentTemplateRequest
from volcengine.tls.tls_responses import CreateAlarmContentTemplateResponse
from volcengine.tls.data import (
    DingTalkContentTemplateInfo, EmailContentTemplateInfo, 
    LarkContentTemplateInfo, SmsContentTemplateInfo, VmsContentTemplateInfo,
    WeChatContentTemplateInfo, WebhookContentTemplateInfo
)


class TestCreateAlarmContentTemplate(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = os.environ.get("VOLCENGINE_ENDPOINT", "")
        self.region = os.environ.get("VOLCENGINE_REGION", "")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "")
        self.access_key_secret = os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET", "")

    def generate_random_string(self, length=10):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def test_create_alarm_content_template(self):
        """Test creating an alarm content template with all notification types"""
        if not all([self.endpoint, self.region, self.access_key_id, 
                   self.access_key_secret]):
            self.skipTest("Missing required environment variables")

        tls_service = TLSService(
            self.endpoint, self.access_key_id, self.access_key_secret, 
            self.region)

        # Create content template with all notification types
        template_name = f"tls-python-sdk-test-alarm-content-template-" \
                       f"{self.generate_random_string()}"
        
        # Email content template
        email_template = EmailContentTemplateInfo(
            subject="告警通知",
            content="告警策略：{{Alarm}}<br> 告警日志项目：{{ProjectName}}<br>",
            locale="zh-CN"
        )
        
        # DingTalk content template
        dingtalk_content = "尊敬的用户，您好！\n您的账号（主账户ID：{{AccountID}} ）" \
                          "的日志服务{%if NotifyType==1%}触发告警{%else%}告警恢复" \
                          "{%endif%}\n告警策略：{{Alarm}}\n告警日志主题：{{AlarmTopicName}}" \
                          "\n触发时间：{{StartTime}}\n触发条件：{{Condition}}\n" \
                          "当前查询结果：[{%-for x in TriggerParams-%}]{{-x-}} {%-endfor-%}]" \
                          "\n通知内容：{{NotifyMsg|escapejs}}\n日志检索详情：[查看详情]({{QueryUrl}})" \
                          "\n告警详情：[查看详情]({{SignInUrl}})\n\n感谢对火山引擎的支持"
        dingtalk_template = DingTalkContentTemplateInfo(
            title="告警通知",
            content=dingtalk_content,
            locale="zh-CN"
        )
        
        # Lark content template
        lark_content = "尊敬的用户，您好！\n您的账号（主账户ID：{{AccountID}} ）" \
                      "的日志服务{%if NotifyType==1%}触发告警{%else%}告警恢复" \
                      "{%endif%}\n告警策略：{{Alarm}}\n告警日志主题：{{AlarmTopicName}}" \
                      "\n触发时间：{{StartTime}}\n触发条件：{{Condition}}\n" \
                      "当前查询结果：[{%-for x in TriggerParams-%}]{{-x-}} {%-endfor-%}]" \
                      "\n通知内容：{{NotifyMsg|escapejs}}\n日志检索详情：[查看详情]({{QueryUrl}})" \
                      "\n告警详情：[查看详情]({{SignInUrl}})\n\n感谢对火山引擎的支持"
        lark_template = LarkContentTemplateInfo(
            title="告警通知",
            content=lark_content,
            locale="zh-CN"
        )
        
        # WeChat content template
        wechat_content = "尊敬的用户，您好！\n您的账号（主账户ID：{{AccountID}} ）" \
                        "的日志服务{%if NotifyType==1%}触发告警{%else%}告警恢复" \
                        "{%endif%}\n告警策略：{{Alarm}}\n告警日志主题：{{AlarmTopicName}}" \
                        "\n触发时间：{{StartTime}}\n触发条件：{{Condition}}\n" \
                        "当前查询结果：[{%-for x in TriggerParams-%}]{{-x-}} {%-endfor-%}]" \
                        "\n通知内容：{{NotifyMsg|escapejs}}\n日志检索详情：[查看详情]({{QueryUrl}})" \
                        "\n告警详情：[查看详情]({{SignInUrl}})\n\n感谢对火山引擎支持"
        wechat_template = WeChatContentTemplateInfo(
            title="告警通知",
            content=wechat_content,
            locale="zh-CN"
        )
        
        # SMS content template
        sms_content = "告警策略{{Alarm}}， 告警日志项目：{{ProjectName}}， " \
                     "告警日志主题：{{AlarmTopicName}}， 告警级别：{{Severity}}， " \
                     "通知类型：{%if NotifyType==1%}触发告警{%else%}告警恢复{%endif%}，" \
                     "触发时间：{{StartTime}}， 触发条件：{{Condition}}， " \
                     "当前查询结果：[{%-for x in TriggerParams-%}]{{-x-}} {%-endfor-%}]， " \
                     "通知内容：{{NotifyMsg}}"
        sms_template = SmsContentTemplateInfo(
            content=sms_content,
            locale="zh-CN"
        )
        
        # VMS content template
        vms_template = VmsContentTemplateInfo(
            content="通知类型：{%if NotifyType==1%}触发告警{%else%}告警恢复{%endif%}",
            locale="zh-CN"
        )
        
        # Webhook content template
        webhook_content = '{ "msg_type": "interactive", "card": { "config": ' \
                         '{ "wide_screen_mode": true }, "elements": [ { "content": ' \
                         '"尊敬的用户，您好！\\n您的账号（主账户ID：{{AccountID}} ）的日志服务' \
                         '{%if NotifyType==1%}触发告警{%else%}告警恢复{%endif%}\\n告警策略：{{Alarm}}' \
                         '\\n告警日志主题：{{AlarmTopicName}}\\n触发时间：{{StartTime}}\\n触发条件：{{Condition}}' \
                         '\\n当前查询结果：[{%-for x in TriggerParams-%}]{{-x-}} {%-endfor-%}];\\n' \
                         '通知内容：{{NotifyMsg|escapejs}}\\n\\n感谢对火山引擎支持", "tag": "markdown" } ], ' \
                         '"header": { "template": "{%if NotifyType==1%}red{%else%}green{%endif%}", ' \
                         '"title": { "content": "【火山引擎】【日志服务】{%if NotifyType==1%}触发告警' \
                         '{%else%}告警恢复{%endif%}", "tag": "plain_text" } } }'
        webhook_template = WebhookContentTemplateInfo(
            content=webhook_content
        )
        
        # Create the request
        request = CreateAlarmContentTemplateRequest(
            alarm_content_template_name=template_name,
            email=email_template,
            ding_talk=dingtalk_template,
            lark=lark_template,
            we_chat=wechat_template,
            sms=sms_template,
            vms=vms_template,
            webhook=webhook_template,
            need_valid_content=True
        )
        
        # Execute the request
        try:
            response = tls_service.create_alarm_content_template(request)
            
            # Verify the response
            self.assertIsNotNone(response)
            template_id = response.get_alarm_content_template_id()
            self.assertIsNotNone(template_id)
            self.assertIsInstance(template_id, str)
            self.assertGreater(len(template_id), 0)
            
            print(f"Successfully created alarm content template: {template_name} "
                  f"with ID: {template_id}")
            
        except Exception as exc:
            # In a real test environment, we would handle specific exceptions
            # For now, we'll just print the error and fail the test
            self.fail(f"Failed to create alarm content template: {str(exc)}")

    def test_create_alarm_content_template_minimal(self):
        """Test creating an alarm content template with minimal required fields"""
        if not all([self.endpoint, self.region, self.access_key_id, 
                   self.access_key_secret]):
            self.skipTest("Missing required environment variables")

        tls_service = TLSService(
            self.endpoint, self.access_key_id, self.access_key_secret, 
            self.region)

        # Create content template with only required field
        template_name = f"tls-python-sdk-test-minimal-" \
                       f"{self.generate_random_string()}"
        
        request = CreateAlarmContentTemplateRequest(
            alarm_content_template_name=template_name
        )
        
        # Execute the request
        try:
            response = tls_service.create_alarm_content_template(request)
            
            # Verify the response
            self.assertIsNotNone(response)
            template_id = response.get_alarm_content_template_id()
            self.assertIsNotNone(template_id)
            self.assertIsInstance(template_id, str)
            self.assertGreater(len(template_id), 0)
            
            print(f"Successfully created minimal alarm content template: "
                  f"{template_name} with ID: {template_id}")
            
        except Exception as exc:
            self.fail(f"Failed to create minimal alarm content template: {str(exc)}")

    def test_create_alarm_content_template_validation(self):
        """Test that validation fails when required fields are missing"""
        
        # Test with missing template name
        request = CreateAlarmContentTemplateRequest(
            alarm_content_template_name=None
        )
        
        # Check validation
        self.assertFalse(request.check_validation())
        
        # Test with empty template name
        request = CreateAlarmContentTemplateRequest(
            alarm_content_template_name=""
        )
        
        # Check validation
        self.assertFalse(request.check_validation())
        
        # Test with valid template name
        request = CreateAlarmContentTemplateRequest(
            alarm_content_template_name="valid-template-name"
        )
        
        # Check validation
        self.assertTrue(request.check_validation())


if __name__ == '__main__':
    unittest.main()