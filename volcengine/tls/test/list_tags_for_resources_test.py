"""Unit tests for ListTagsForResources request and TLSService integration.

本文件仅构造请求并通过 Mock 拦截 TLSService._TLSService__request，
不依赖真实后端环境或 TLS 资源。
"""

import os
import unittest
from unittest.mock import Mock, patch

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import ListTagsForResourcesRequest
from volcengine.tls.tls_responses import ListTagsForResourcesResponse


class TestListTagsForResources(unittest.TestCase):
    """测试 ListTagsForResourcesRequest 与 TLSService.list_tags_for_resources"""

    def setUp(self):
        # 使用本地默认配置构造 TLSService，避免依赖真实环境变量和后端
        self.endpoint = os.environ.get("VOLCENGINE_ENDPOINT", "https://tls-cn-beijing.ivolces.com")
        self.region = os.environ.get("VOLCENGINE_REGION", "cn-beijing")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "test-ak")
        self.access_key_secret = os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET", "test-sk")

        self.tls_service = TLSService(
            self.endpoint,
            self.access_key_id,
            self.access_key_secret,
            self.region,
        )

    def test_list_tags_for_resources_request_validation(self):
        """测试 ListTagsForResourcesRequest.check_validation 仅校验 resource_type 非空"""
        request = ListTagsForResourcesRequest(resource_type="project")
        self.assertTrue(request.check_validation())

        request = ListTagsForResourcesRequest(resource_type=None)
        self.assertFalse(request.check_validation())

    def test_list_tags_for_resources_request_body_fields(self):
        """测试 JSON 请求体顶层字段与 TagFilters 内部结构"""
        request = ListTagsForResourcesRequest(
            resource_type="project",
            resources_ids=["res-1"],
            tag_filters=[
                {"key": "k1", "values": ["v1", "v2"]},
                {"Key": "k2", "Values": ["v3"]},
            ],
            max_results=50,
            next_token="cursor-1",
        )

        body = request.get_api_input()

        # 顶层字段命名
        self.assertEqual(body["ResourceType"], "project")
        self.assertEqual(body["ResourcesIds"], ["res-1"])
        self.assertEqual(body["MaxResults"], 50)
        self.assertEqual(body["NextToken"], "cursor-1")

        # TagFilters 结构
        self.assertIn("TagFilters", body)
        self.assertEqual(len(body["TagFilters"]), 2)

        first = body["TagFilters"][0]
        self.assertEqual(first["Key"], "k1")
        self.assertEqual(first["Values"], ["v1", "v2"])

        second = body["TagFilters"][1]
        self.assertEqual(second["Key"], "k2")
        self.assertEqual(second["Values"], ["v3"])

    @patch("volcengine.tls.TLSService.TLSService._TLSService__request")
    def test_list_tags_for_resources_service_call_basic(self, mock_request):
        """测试基础场景下 TLSService.list_tags_for_resources 的调用"""
        # 构造模拟 HTTP 响应
        mock_response = Mock()
        mock_response.headers = {
            "X-Tls-Requestid": "test-request-id",
            "Content-Type": "application/json",
        }
        mock_response.text = '{"ResourceTags": [], "nextToken": ""}'
        mock_request.return_value = mock_response

        request = ListTagsForResourcesRequest(
            resource_type="project",
            resources_ids=["project-123"],
        )

        response = self.tls_service.list_tags_for_resources(request)

        # 验证底层 __request 调用参数
        mock_request.assert_called_once_with(
            api="/ListTagsForResources",
            body={
                "ResourceType": "project",
                "ResourcesIds": ["project-123"],
            },
        )

        # 验证响应类型与字段解析
        self.assertIsInstance(response, ListTagsForResourcesResponse)
        self.assertIsInstance(response.get_resource_tags(), list)
        self.assertIsInstance(response.get_next_token(), str)

    @patch("volcengine.tls.TLSService.TLSService._TLSService__request")
    def test_list_tags_for_resources_with_tag_filters_and_pagination(self, mock_request):
        """测试携带 TagFilters 与分页参数时的调用与请求体结构"""
        mock_response = Mock()
        mock_response.headers = {
            "X-Tls-Requestid": "test-request-id",
            "Content-Type": "application/json",
        }
        mock_response.text = '{"ResourceTags": [], "nextToken": "cursor-next"}'
        mock_request.return_value = mock_response

        request = ListTagsForResourcesRequest(
            resource_type="topic",
            resources_ids=["topic-1"],
            tag_filters=[{"key": "env", "values": ["test"]}],
            max_results=10,
            next_token="cursor-1",
        )

        body = request.get_api_input()
        response = self.tls_service.list_tags_for_resources(request)

        # 顶层字段
        self.assertEqual(body["ResourceType"], "topic")
        self.assertEqual(body["ResourcesIds"], ["topic-1"])
        self.assertEqual(body["MaxResults"], 10)
        self.assertEqual(body["NextToken"], "cursor-1")

        # TagFilters 结构
        self.assertIn("TagFilters", body)
        self.assertEqual(len(body["TagFilters"]), 1)
        self.assertEqual(body["TagFilters"][0]["Key"], "env")
        self.assertEqual(body["TagFilters"][0]["Values"], ["test"])

        # __request 调用体中也应携带规范化后的 TagFilters
        mock_request.assert_called_once_with(api="/ListTagsForResources", body=body)

        # 响应解析
        self.assertIsInstance(response, ListTagsForResourcesResponse)
        self.assertEqual(response.get_next_token(), "cursor-next")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
