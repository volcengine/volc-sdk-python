import os
import unittest
import random

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import *


class TestTrace(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = os.environ.get("VOLCENGINE_ENDPOINT", "")
        self.region = os.environ.get("VOLCENGINE_REGION", "")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "")
        self.access_key_secret = os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET", "")

    def test_describe_trace_instance(self):
        """测试 DescribeTraceInstance API"""
        if not all([self.endpoint, self.access_key_id, self.access_key_secret, self.region]):
            self.skipTest("缺少必要的环境变量")

        tls_service = TLSService(
            self.endpoint, self.access_key_id, self.access_key_secret, self.region)

        # 模拟测试数据
        trace_instance_id = "test-trace-instance-id"
        
        # 创建请求
        request = DescribeTraceInstanceRequest(trace_instance_id=trace_instance_id)
        
        # 验证请求参数
        self.assertTrue(request.check_validation())
        self.assertEqual(request.trace_instance_id, trace_instance_id)
        
        # 测试空参数验证
        invalid_request = DescribeTraceInstanceRequest(trace_instance_id=None)
        self.assertFalse(invalid_request.check_validation())

    def test_trace_instance_request_serialization(self):
        """测试请求参数的序列化"""
        trace_instance_id = "test-trace-instance-id"
        request = DescribeTraceInstanceRequest(trace_instance_id=trace_instance_id)
        
        api_input = request.get_api_input()
        expected = {"TraceInstanceId": trace_instance_id}
        self.assertEqual(api_input, expected)


if __name__ == '__main__':
    unittest.main()