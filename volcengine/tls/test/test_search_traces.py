"""Unit tests for SearchTraces functionality."""
import os
import unittest
import random

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import (
    SearchTracesRequest,
    CreateTraceInstanceRequest,
    DeleteTraceInstanceRequest
)


class TestSearchTraces(unittest.TestCase):
    """Test cases for SearchTraces functionality."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = os.environ.get("VOLCENGINE_ENDPOINT", "")
        self.region = os.environ.get("VOLCENGINE_REGION", "")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "")
        self.access_key_secret = os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET", "")

    def test_search_traces_request_validation(self):
        """测试 SearchTracesRequest 参数验证"""
        # 测试有效请求
        trace_instance_id = "test-trace-instance-id"
        query = {
            "Limit": 10,
            "Offset": 0,
            "ServiceName": "test-service",
            "OperationName": "test-operation"
        }
        request = SearchTracesRequest(trace_instance_id=trace_instance_id, query=query)

        # 验证请求参数
        self.assertTrue(request.check_validation())
        self.assertEqual(request.trace_instance_id, trace_instance_id)
        self.assertEqual(request.query, query)

        # 测试空参数验证
        invalid_request = SearchTracesRequest(trace_instance_id=None)
        self.assertFalse(invalid_request.check_validation())

    def test_search_traces_request_serialization(self):
        """测试 SearchTracesRequest 序列化"""
        trace_instance_id = "test-trace-instance-id"
        query = {
            "Limit": 10,
            "Offset": 0,
            "ServiceName": "test-service"
        }
        request = SearchTracesRequest(trace_instance_id=trace_instance_id, query=query)

        api_input = request.get_api_input()
        expected = {
            "TraceInstanceId": trace_instance_id,
            "Query": query
        }
        self.assertEqual(api_input, expected)

    def test_search_traces_request_minimal(self):
        """测试最小化的 SearchTracesRequest"""
        trace_instance_id = "test-trace-instance-id"
        request = SearchTracesRequest(trace_instance_id=trace_instance_id)

        self.assertTrue(request.check_validation())
        api_input = request.get_api_input()
        expected = {
            "TraceInstanceId": trace_instance_id,
            "Query": {}
        }
        self.assertEqual(api_input, expected)

    def test_search_traces_integration(self):
        """测试 SearchTraces 完整流程"""
        if not all([self.endpoint, self.access_key_id, self.access_key_secret,
                    self.region]):
            self.skipTest("缺少必要的环境变量")

        tls_service = TLSService(
            self.endpoint, self.access_key_id, self.access_key_secret,
            self.region)

        # 创建随机名称的 Trace 实例
        random1 = str(random.randint(0, 100))
        random2 = str(random.randint(0, 100))
        trace_name = f"单元测试{random1}-{random2}"

        # 注意：这里需要一个有效的 ProjectId，可以从环境变量获取或使用默认值
        project_id = os.environ.get("TEST_PROJECT_ID", "test-project-id")

        try:
            # 创建 Trace 实例
            create_request = CreateTraceInstanceRequest(
                project_id=project_id,
                trace_instance_name=trace_name
            )
            create_response = tls_service.create_trace_instance(create_request)
            trace_instance_id = create_response.get_trace_instance_id()

            # 搜索 Traces
            search_request = SearchTracesRequest(
                trace_instance_id=trace_instance_id,
                query={
                    "Limit": 10,
                    "Offset": 0
                }
            )
            search_response = tls_service.search_traces(search_request)

            # 验证响应
            self.assertIsInstance(search_response.get_total(), int)
            self.assertIsInstance(search_response.get_trace_infos(), list)

        finally:
            # 清理：删除 Trace 实例
            if 'trace_instance_id' in locals():
                delete_request = DeleteTraceInstanceRequest(
                    trace_instance_id=trace_instance_id)
                tls_service.delete_trace_instance(delete_request)


if __name__ == '__main__':
    unittest.main()
