# coding=utf-8

"""Unit tests for TagResources request and TLSService integration (without real backend).

本文件仅关注请求体结构与 TLSService 调用参数，不依赖真实后端环境。
"""

import os
import unittest
from unittest.mock import Mock, patch

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import TagResourcesRequest
from volcengine.tls.tls_responses import TagResourcesResponse
from volcengine.tls.data import TagInfo


class TestTagResources(unittest.TestCase):
    """测试 TagResourcesRequest 与 TLSService.tag_resources 的请求体结构"""

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

    def test_tag_resources_request_validation(self):
        """测试 TagResourcesRequest.check_validation 参数校验"""
        # 正常情况
        request = TagResourcesRequest(
            resource_type="project",
            resources_ids=["project-123"],
            tags=[TagInfo(key="env", value="test")],
        )
        self.assertTrue(request.check_validation())

        # 缺少 resource_type
        request = TagResourcesRequest(
            resource_type=None,
            resources_ids=["project-123"],
            tags=[TagInfo(key="env", value="test")],
        )
        self.assertFalse(request.check_validation())

        # 缺少 resources_ids
        request = TagResourcesRequest(
            resource_type="project",
            resources_ids=None,
            tags=[TagInfo(key="env", value="test")],
        )
        self.assertFalse(request.check_validation())

        # 缺少 tags
        request = TagResourcesRequest(
            resource_type="project",
            resources_ids=["project-123"],
            tags=None,
        )
        self.assertFalse(request.check_validation())

    def test_tag_resources_request_api_input(self):
        """测试 TagResourcesRequest.get_api_input 顶层键名与 Tags 结构"""
        request = TagResourcesRequest(
            resource_type="topic",
            resources_ids=["topic-123", "topic-456"],
            tags=[
                TagInfo(key="k1", value="v1"),
                TagInfo(key="k2", value="v2"),
            ],
        )

        body = request.get_api_input()

        # 顶层字段
        self.assertEqual(body["ResourceType"], "topic")
        self.assertEqual(body["ResourcesIds"], ["topic-123", "topic-456"])
        self.assertIn("Tags", body)
        self.assertEqual(len(body["Tags"]), 2)

        first = body["Tags"][0]
        self.assertEqual(first["Key"], "k1")
        self.assertEqual(first["Value"], "v1")

        second = body["Tags"][1]
        self.assertEqual(second["Key"], "k2")
        self.assertEqual(second["Value"], "v2")

    @patch("volcengine.tls.TLSService.TLSService._TLSService__request")
    def test_tag_resources_service_call(self, mock_request):
        """测试 TLSService.tag_resources 调用时的 API 名称与请求体结构"""
        # 模拟 HTTP 响应
        mock_response = Mock()
        mock_response.headers = {
            "X-Tls-Requestid": "test-request-id",
            "Content-Type": "application/json",
        }
        mock_response.text = "{}"
        mock_request.return_value = mock_response

        request = TagResourcesRequest(
            resource_type="project",
            resources_ids=["project-123"],
            tags=[
                TagInfo(key="env", value="test"),
                TagInfo(key="owner", value="alice"),
            ],
        )

        response = self.tls_service.tag_resources(request)

        # 验证底层 __request 被正确调用
        mock_request.assert_called_once_with(
            api="/TagResources",
            body={
                "ResourceType": "project",
                "ResourcesIds": ["project-123"],
                "Tags": [
                    {"Key": "env", "Value": "test"},
                    {"Key": "owner", "Value": "alice"},
                ],
            },
        )

        # 验证响应类型与 RequestId 解析
        self.assertIsInstance(response, TagResourcesResponse)
        self.assertEqual(response.get_request_id(), "test-request-id")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
