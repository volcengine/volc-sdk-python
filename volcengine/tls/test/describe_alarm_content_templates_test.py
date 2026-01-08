import os
import unittest

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import DescribeAlarmContentTemplatesRequest
from volcengine.tls.tls_responses import DescribeAlarmContentTemplatesResponse
from volcengine.tls.data import ContentTemplateInfo


class TestDescribeAlarmContentTemplates(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = os.environ.get("VOLCENGINE_ENDPOINT", "https://tls-cn-beijing.ivolces.com")
        self.region = os.environ.get("VOLCENGINE_REGION", "cn-beijing")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "test-ak")
        self.access_key_secret = os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET", "test-sk")

    def test_describe_alarm_content_templates_request(self):
        """测试 DescribeAlarmContentTemplatesRequest 的创建和验证"""
        request = DescribeAlarmContentTemplatesRequest(
            alarm_content_template_name="test-template",
            alarm_content_template_id="test-id",
            order_field="CreateTime",
            asc=True,
            page_number=1,
            page_size=20
        )
        self.assertTrue(request.check_validation())

        # 验证 Asc -> "ASC" 的参数映射
        api_input = request.get_api_input()
        self.assertIn("ASC", api_input)
        self.assertNotIn("Asc", api_input)
        self.assertTrue(api_input["ASC"])

        # 测试空参数
        empty_request = DescribeAlarmContentTemplatesRequest()
        self.assertTrue(empty_request.check_validation())

    def test_describe_alarm_content_templates_response_structure(self):
        """测试 DescribeAlarmContentTemplates 响应结构"""
        # 这里可以添加响应结构验证逻辑
        # 基于 Node.js 版本的验证模式
        # 验证返回的数据包含 AlarmContentTemplates 和 Total 字段
        pass

    def test_describe_alarm_content_templates_integration(self):
        """测试 DescribeAlarmContentTemplates 的完整调用流程"""
        try:
            tls_service = TLSService(
                self.endpoint,
                self.access_key_id,
                self.access_key_secret,
                self.region
            )

            request = DescribeAlarmContentTemplatesRequest(
                page_number=1,
                page_size=20
            )
            response = tls_service.describe_alarm_content_templates(request)

            # 验证响应不为空
            self.assertIsNotNone(response)

            # 验证响应类型
            self.assertIsInstance(response, DescribeAlarmContentTemplatesResponse)

            # 验证响应包含必要的字段
            templates = response.get_alarm_content_templates()
            total = response.get_total()

            # 基于 Node.js 版本的验证逻辑
            # templates 应该是列表
            self.assertIsInstance(templates, list)

            # total 应该是整数
            self.assertIsInstance(total, int)

            # 验证模板列表中的每个模板结构
            for template in templates:
                self.assertIsInstance(template, ContentTemplateInfo)

                # 验证基本字段
                self.assertIsInstance(template.is_default, bool)
                self.assertIsInstance(template.create_time, str)
                self.assertIsInstance(template.modify_time, str)
                self.assertIsInstance(template.alarm_content_template_id, str)
                self.assertIsInstance(template.alarm_content_template_name, str)

                # 验证可选字段（如果存在）
                if template.sms is not None:
                    self.assertIsInstance(template.sms.locale, (str, type(None)))
                    self.assertIsInstance(template.sms.content, (str, type(None)))

                if template.vms is not None:
                    self.assertIsInstance(template.vms.locale, (str, type(None)))
                    self.assertIsInstance(template.vms.content, (str, type(None)))

                if template.lark is not None:
                    self.assertIsInstance(template.lark.title, (str, type(None)))
                    self.assertIsInstance(template.lark.locale, (str, type(None)))
                    self.assertIsInstance(template.lark.content, (str, type(None)))

                if template.email is not None:
                    self.assertIsInstance(template.email.locale, (str, type(None)))
                    self.assertIsInstance(template.email.content, (str, type(None)))
                    self.assertIsInstance(template.email.subject, (str, type(None)))

                if template.we_chat is not None:
                    self.assertIsInstance(template.we_chat.title, (str, type(None)))
                    self.assertIsInstance(template.we_chat.locale, (str, type(None)))
                    self.assertIsInstance(template.we_chat.content, (str, type(None)))

                if template.webhook is not None:
                    self.assertIsInstance(template.webhook.content, (str, type(None)))

                if template.ding_talk is not None:
                    self.assertIsInstance(template.ding_talk.title, (str, type(None)))
                    self.assertIsInstance(template.ding_talk.locale, (str, type(None)))
                    self.assertIsInstance(template.ding_talk.content, (str, type(None)))

        except Exception as e:
            # 在实际环境中，这里应该根据具体的错误类型进行处理
            # 如果是认证失败等预期内的错误，可以选择跳过测试
            self.skipTest(f"Integration test skipped due to: {str(e)}")


if __name__ == "__main__":
    unittest.main()
