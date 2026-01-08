import os
import unittest
from unittest.mock import Mock, patch

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import UntagResourcesRequest
from volcengine.tls.tls_responses import UntagResourcesResponse


class TestUntagResources(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = os.environ.get("VOLCENGINE_ENDPOINT", "https://tls-cn-beijing.ivolces.com")
        self.region = os.environ.get("VOLCENGINE_REGION", "cn-beijing")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "test-ak")
        self.access_key_secret = os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET", "test-sk")

    def setUp(self):
        self.tls_service = TLSService(
            self.endpoint, self.access_key_id, self.access_key_secret, self.region)

    def test_untag_resources_request_validation(self):
        """测试 UntagResourcesRequest 参数验证"""
        # 测试正常情况
        request = UntagResourcesRequest(
            resource_type="project",
            resources_ids=["project-123"],
            tag_keys=["env", "owner"]
        )
        self.assertTrue(request.check_validation())

        # 测试缺少 resource_type
        request = UntagResourcesRequest(
            resource_type=None,
            resources_ids=["project-123"],
            tag_keys=["env", "owner"]
        )
        self.assertFalse(request.check_validation())

        # 测试缺少 resources_ids
        request = UntagResourcesRequest(
            resource_type="project",
            resources_ids=None,
            tag_keys=["env", "owner"]
        )
        self.assertFalse(request.check_validation())

        # 测试缺少 tag_keys
        request = UntagResourcesRequest(
            resource_type="project",
            resources_ids=["project-123"],
            tag_keys=None
        )
        self.assertFalse(request.check_validation())

    def test_untag_resources_request_api_input(self):
        """测试 UntagResourcesRequest 的 API 输入格式"""
        request = UntagResourcesRequest(
            resource_type="topic",
            resources_ids=["topic-123", "topic-456"],
            tag_keys=["env", "team", "project"]
        )
        
        api_input = request.get_api_input()

        self.assertEqual(api_input["ResourceType"], "topic")
        self.assertEqual(api_input["ResourcesIds"], ["topic-123", "topic-456"])
        self.assertEqual(api_input["TagKeys"], ["env", "team", "project"])

    @patch('volcengine.tls.TLSService.TLSService._TLSService__request')
    def test_untag_resources_service_call(self, mock_request):
        """测试 TLSService.untag_resources 方法调用"""
        # 模拟响应
        mock_response = Mock()
        mock_response.headers = {
            'X-Tls-Requestid': 'test-request-id',
            'Content-Type': 'application/json',
        }
        mock_response.text = '{}'
        mock_request.return_value = mock_response

        request = UntagResourcesRequest(
            resource_type="project",
            resources_ids=["project-123"],
            tag_keys=["env", "owner"]
        )

        response = self.tls_service.untag_resources(request)

        # 验证调用了正确的 API
        mock_request.assert_called_once_with(
            api='/UntagResources',
            body={
                'ResourceType': 'project',
                'ResourcesIds': ['project-123'],
                'TagKeys': ['env', 'owner']
            }
        )

        # 验证响应类型
        self.assertIsInstance(response, UntagResourcesResponse)
        self.assertEqual(response.get_request_id(), 'test-request-id')

    @patch('volcengine.tls.TLSService.TLSService._TLSService__request')
    def test_untag_resources_with_topic_resource(self, mock_request):
        """测试使用 topic 资源的解绑标签"""
        mock_response = Mock()
        mock_response.headers = {
            'X-Tls-Requestid': 'test-request-id',
            'Content-Type': 'application/json',
        }
        mock_response.text = '{}'
        mock_request.return_value = mock_response

        request = UntagResourcesRequest(
            resource_type="topic",
            resources_ids=["topic-123"],
            tag_keys=["team"]
        )

        response = self.tls_service.untag_resources(request)

        mock_request.assert_called_once_with(
            api='/UntagResources',
            body={
                'ResourceType': 'topic',
                'ResourcesIds': ['topic-123'],
                'TagKeys': ['team']
            }
        )

        self.assertIsInstance(response, UntagResourcesResponse)

    @patch('volcengine.tls.TLSService.TLSService._TLSService__request')
    def test_untag_resources_with_multiple_resources(self, mock_request):
        """测试多个资源的解绑标签"""
        mock_response = Mock()
        mock_response.headers = {
            'X-Tls-Requestid': 'test-request-id',
            'Content-Type': 'application/json',
        }
        mock_response.text = '{}'
        mock_request.return_value = mock_response

        request = UntagResourcesRequest(
            resource_type="topic",
            resources_ids=["topic-123", "topic-456", "topic-789"],
            tag_keys=["key1", "key2", "key3", "key4"]
        )

        response = self.tls_service.untag_resources(request)

        mock_request.assert_called_once_with(
            api='/UntagResources',
            body={
                'ResourceType': 'topic',
                'ResourcesIds': ['topic-123', 'topic-456', 'topic-789'],
                'TagKeys': ['key1', 'key2', 'key3', 'key4']
            }
        )

        self.assertIsInstance(response, UntagResourcesResponse)

    def test_untag_resources_invalid_request(self):
        """测试无效请求参数时的异常处理"""
        request = UntagResourcesRequest(
            resource_type=None,
            resources_ids=["project-123"],
            tag_keys=["env"]
        )

        with self.assertRaises(Exception) as context:
            self.tls_service.untag_resources(request)

        # 验证抛出了 TLSException
        self.assertIn("InvalidArgument", str(context.exception))


if __name__ == '__main__':
    unittest.main()
