import os
import unittest
import random

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import DescribeTraceRequest
from volcengine.tls.tls_responses import DescribeTraceResponse
from volcengine.tls.data import TraceInfo, SpanInfo, StatusInfo, ResourceInfo, KeyValueInfo


class TestDescribeTrace(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = os.environ.get("VOLCENGINE_ENDPOINT", "")
        self.region = os.environ.get("VOLCENGINE_REGION", "")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "")
        self.access_key_secret = os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET", "")

    def test_describe_trace_request_validation(self):
        """测试 DescribeTraceRequest 参数验证"""
        # 测试有效参数
        trace_id = "test-trace-id-" + str(random.randint(1000, 9999))
        trace_instance_id = "test-trace-instance-id"
        
        request = DescribeTraceRequest(
            trace_id=trace_id,
            trace_instance_id=trace_instance_id
        )
        
        self.assertTrue(request.check_validation())
        self.assertEqual(request.trace_id, trace_id)
        self.assertEqual(request.trace_instance_id, trace_instance_id)
        
        # 测试空参数验证
        invalid_request = DescribeTraceRequest(trace_id=None, trace_instance_id=None)
        self.assertFalse(invalid_request.check_validation())
        
        # 测试部分空参数
        invalid_request1 = DescribeTraceRequest(trace_id=trace_id, trace_instance_id=None)
        self.assertFalse(invalid_request1.check_validation())
        
        invalid_request2 = DescribeTraceRequest(trace_id=None, trace_instance_id=trace_instance_id)
        self.assertFalse(invalid_request2.check_validation())

    def test_describe_trace_request_serialization(self):
        """测试请求参数的序列化"""
        trace_id = "test-trace-id-12345"
        trace_instance_id = "test-trace-instance-id"
        
        request = DescribeTraceRequest(
            trace_id=trace_id,
            trace_instance_id=trace_instance_id
        )
        
        api_input = request.get_api_input()
        expected = {
            "TraceId": trace_id,
            "TraceInstanceId": trace_instance_id
        }
        self.assertEqual(api_input, expected)

    def test_trace_data_structures(self):
        """测试 Trace 数据结构"""
        # 测试 KeyValueInfo
        key_value = KeyValueInfo(key="test_key", value="test_value")
        self.assertEqual(key_value.key, "test_key")
        self.assertEqual(key_value.value, "test_value")
        
        # 测试 StatusInfo
        status = StatusInfo(code="SUCCESS", message="Test message")
        self.assertEqual(status.code, "SUCCESS")
        self.assertEqual(status.message, "Test message")
        
        # 测试 ResourceInfo
        attributes = [KeyValueInfo(key="service", value="test-service")]
        resource = ResourceInfo(attributes=attributes)
        self.assertEqual(len(resource.attributes), 1)
        self.assertEqual(resource.attributes[0].key, "service")
        self.assertEqual(resource.attributes[0].value, "test-service")
        
        # 测试 SpanInfo
        span = SpanInfo(
            trace_id="test-trace-id",
            span_id="test-span-id",
            kind="server",
            name="test-operation",
            start_time=1640995200000000,
            end_time=1640995260000000,
            status=status,
            resource=resource
        )
        
        self.assertEqual(span.trace_id, "test-trace-id")
        self.assertEqual(span.span_id, "test-span-id")
        self.assertEqual(span.kind, "server")
        self.assertEqual(span.name, "test-operation")
        self.assertEqual(span.start_time, 1640995200000000)
        self.assertEqual(span.end_time, 1640995260000000)
        self.assertEqual(span.status.code, "SUCCESS")
        self.assertEqual(len(span.resource.attributes), 1)
        
        # 测试 TraceInfo
        trace = TraceInfo(spans=[span])
        self.assertEqual(len(trace.spans), 1)
        self.assertEqual(trace.spans[0].trace_id, "test-trace-id")

    def test_describe_trace_response(self):
        """测试 DescribeTraceResponse"""
        # 模拟响应数据
        mock_response_data = {
            "Trace": {
                "Spans": [
                    {
                        "TraceId": "test-trace-id",
                        "SpanId": "test-span-id",
                        "Kind": "server",
                        "Name": "test-operation",
                        "StartTime": 1640995200000000,
                        "EndTime": 1640995260000000,
                        "Status": {
                            "Code": "SUCCESS",
                            "Message": "Test message"
                        },
                        "Resource": {
                            "Attributes": [
                                {
                                    "Key": "service",
                                    "Value": "test-service"
                                }
                            ]
                        }
                    }
                ]
            }
        }
        
        # 创建模拟响应对象
        class MockResponse:
            def __init__(self):
                self.headers = {"X-Tls-Requestid": "test-request-id", "Content-Type": "application/json"}
                self.text = str(mock_response_data).replace("'", '"')
                
        mock_response = MockResponse()
        
        # 测试响应解析
        response = DescribeTraceResponse(mock_response)
        trace = response.get_trace()
        
        self.assertIsNotNone(trace)
        self.assertEqual(len(trace.spans), 1)  # pylint: disable=no-member
        self.assertEqual(trace.spans[0].trace_id, "test-trace-id")  # pylint: disable=no-member
        self.assertEqual(trace.spans[0].span_id, "test-span-id")  # pylint: disable=no-member
        self.assertEqual(trace.spans[0].kind, "server")  # pylint: disable=no-member
        self.assertEqual(trace.spans[0].name, "test-operation")  # pylint: disable=no-member
        self.assertEqual(trace.spans[0].status.code, "SUCCESS")  # pylint: disable=no-member
        self.assertEqual(len(trace.spans[0].resource.attributes), 1)  # pylint: disable=no-member
        self.assertEqual(trace.spans[0].resource.attributes[0].key, "service")  # pylint: disable=no-member
        self.assertEqual(trace.spans[0].resource.attributes[0].value, "test-service")  # pylint: disable=no-member

    def test_describe_trace_integration(self):
        """测试 DescribeTrace 集成（需要环境变量）"""
        if not all([self.endpoint, self.access_key_id, self.access_key_secret, self.region]):
            self.skipTest("缺少必要的环境变量")

        tls_service = TLSService(
            self.endpoint, self.access_key_id, self.access_key_secret, self.region)

        # 模拟测试数据
        trace_id = "test-trace-id-" + str(random.randint(1000, 9999))
        trace_instance_id = "test-trace-instance-id"
        
        try:
            # 尝试调用 DescribeTrace 方法
            describe_trace_request = DescribeTraceRequest(
                trace_id=trace_id,
                trace_instance_id=trace_instance_id
            )
            
            # 验证请求参数
            self.assertTrue(describe_trace_request.check_validation())
            
            # 注意：由于我们没有真实的 trace 数据，这个调用可能会失败
            # 这里主要是测试请求构建和参数验证
            response = tls_service.describe_trace(describe_trace_request)
            
            # 如果调用成功，验证响应
            trace = response.get_trace()
            self.assertIsNotNone(trace)
            
        except Exception as e:  # pylint: disable=broad-exception-caught
            # 如果 trace 不存在，应该抛出异常
            # 这里我们主要验证请求构建是正确的
            self.assertIn("Trace", str(e))


if __name__ == '__main__':
    unittest.main()
