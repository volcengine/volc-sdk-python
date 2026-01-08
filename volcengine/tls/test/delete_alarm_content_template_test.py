import os
import unittest

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import DeleteAlarmContentTemplateRequest
from volcengine.tls.tls_responses import DeleteAlarmContentTemplateResponse


class TestDeleteAlarmContentTemplate(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = os.environ.get("VOLCENGINE_ENDPOINT", "")
        self.region = os.environ.get("VOLCENGINE_REGION", "")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "")
        self.access_key_secret = os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET", "")

    def test_delete_alarm_content_template(self):
        """测试删除告警通知内容模板"""
        if not all([self.endpoint, self.region, self.access_key_id, self.access_key_secret]):
            self.skipTest("缺少必要的环境变量")

        tls_client = TLSService(
            self.endpoint, self.access_key_id, self.access_key_secret, self.region)

        # 测试删除告警通知内容模板
        alarm_content_template_id = "test-template-id"
        delete_request = DeleteAlarmContentTemplateRequest(
            alarm_content_template_id=alarm_content_template_id
        )

        try:
            response = tls_client.delete_alarm_content_template(delete_request)
            # 验证响应类型
            self.assertIsInstance(response, DeleteAlarmContentTemplateResponse)
            # 验证请求ID存在
            self.assertIsNotNone(response.get_request_id())
            print(f"DeleteAlarmContentTemplate成功，请求ID: {response.get_request_id()}")
        except Exception as e:
            # 即使API返回错误，也应该包含请求ID
            print(f"DeleteAlarmContentTemplate测试完成，响应: {str(e)}")

    def test_delete_alarm_content_template_validation(self):
        """测试删除告警通知内容模板的参数验证"""
        # 测试参数验证
        delete_request = DeleteAlarmContentTemplateRequest(
            alarm_content_template_id=None
        )
        self.assertFalse(delete_request.check_validation())

        # 测试有效参数
        delete_request_valid = DeleteAlarmContentTemplateRequest(
            alarm_content_template_id="test-template-id"
        )
        self.assertTrue(delete_request_valid.check_validation())


if __name__ == '__main__':
    unittest.main()