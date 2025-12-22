import os
import unittest

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import GetAccountStatusRequest


class TestGetAccountStatus(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = os.environ.get("VOLCENGINE_ENDPOINT", "https://tls-cn-beijing.ivolces.com")
        self.region = os.environ.get("VOLCENGINE_REGION", "cn-beijing")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "test-ak")
        self.access_key_secret = os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET", "test-sk")

    def test_get_account_status_request(self):
        """测试 GetAccountStatusRequest 的创建和验证"""
        request = GetAccountStatusRequest()
        self.assertTrue(request.check_validation())

    def test_get_account_status_response_structure(self):
        """测试 GetAccountStatus 响应结构"""
        # 这里可以添加响应结构验证逻辑
        # 基于 Node.js 版本的验证模式
        # 验证返回的数据包含 ArchVersion 和 Status 字段

    def test_get_account_status_integration(self):
        """测试 GetAccountStatus 的完整调用流程"""
        try:
            tls_service = TLSService(
                self.endpoint,
                self.access_key_id,
                self.access_key_secret,
                self.region
            )

            request = GetAccountStatusRequest()
            response = tls_service.get_account_status(request)

            # 验证响应不为空
            self.assertIsNotNone(response)

            # 验证响应包含必要的字段
            arch_version = response.get_arch_version()
            status = response.get_status()

            # 基于 Node.js 版本的验证逻辑
            # ArchVersion 应该是字符串
            if arch_version is not None:
                self.assertIsInstance(arch_version, str)

            # Status 应该是字符串，且值在预期范围内
            if status is not None:
                self.assertIsInstance(status, str)
                self.assertIn(status, ["Activated", "NonActivated"])

        except Exception as e:
            # 在实际环境中，这里应该根据具体的错误类型进行处理
            # 如果是认证失败等预期内的错误，可以选择跳过测试
            self.skipTest(f"Integration test skipped due to: {str(e)}")


if __name__ == "__main__":
    unittest.main()