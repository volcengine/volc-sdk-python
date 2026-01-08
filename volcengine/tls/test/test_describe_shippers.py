# coding=utf-8
"""DescribeShippers 接口的单元测试"""
import os
import unittest
import random
import string

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import (
    CreateProjectRequest, CreateTopicRequest,
    DeleteTopicRequest, DeleteProjectRequest,
    DescribeShippersRequest
)


class TestDescribeShippers(unittest.TestCase):
    """DescribeShippers 接口的单元测试"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = os.environ.get(
            "VOLCENGINE_ENDPOINT", "tls-cn-beijing.ivolces.com"
        )
        self.region = os.environ.get("VOLCENGINE_REGION", "cn-beijing")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "")
        self.access_key_secret = os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET", "")
        self.tls_service = TLSService(
            self.endpoint, self.access_key_id, self.access_key_secret, self.region
        )

    def _generate_random_string(self, length=10):
        """生成随机字符串"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def test_describe_shippers_with_project_id(self):
        """测试使用 ProjectId 查询投递配置"""
        # 创建测试项目
        project_name = f"tls-python-sdk-test-shipper-project-{self._generate_random_string()}"
        create_project_request = CreateProjectRequest(project_name=project_name, region=self.region)
        project_response = self.tls_service.create_project(create_project_request)
        project_id = project_response.get_project_id()

        try:
            # 创建测试主题
            topic_name = f"tls-python-sdk-test-shipper-topic-{self._generate_random_string()}"
            create_topic_request = CreateTopicRequest(
                project_id=project_id,
                topic_name=topic_name,
                shard_count=1,
                ttl=1
            )
            topic_response = self.tls_service.create_topic(create_topic_request)
            topic_id = topic_response.get_topic_id()

            try:
                # 测试 DescribeShippers 接口
                describe_shippers_request = DescribeShippersRequest(project_id=project_id)
                shippers_response = self.tls_service.describe_shippers(describe_shippers_request)

                # 验证响应结构
                self.assertIsInstance(shippers_response.get_total(), int)
                self.assertIsInstance(shippers_response.get_shippers(), list)

                # 验证每个 shipper 的结构
                shippers = shippers_response.get_shippers()
                for shipper in shippers:
                    self.assertTrue(hasattr(shipper, 'shipper_id'))
                    self.assertTrue(hasattr(shipper, 'shipper_name'))
                    self.assertTrue(hasattr(shipper, 'project_id'))
                    self.assertTrue(hasattr(shipper, 'topic_id'))
                    self.assertTrue(hasattr(shipper, 'shipper_type'))
                    self.assertTrue(hasattr(shipper, 'status'))

            finally:
                # 清理测试主题
                delete_topic_request = DeleteTopicRequest(topic_id=topic_id)
                self.tls_service.delete_topic(delete_topic_request)

        finally:
            # 清理测试项目
            delete_project_request = DeleteProjectRequest(project_id=project_id)
            self.tls_service.delete_project(delete_project_request)

    def test_describe_shippers_with_topic_id(self):
        """测试使用 TopicId 查询投递配置"""
        # 创建测试项目
        project_name = f"tls-python-sdk-test-shipper-project-{self._generate_random_string()}"
        create_project_request = CreateProjectRequest(project_name=project_name, region=self.region)
        project_response = self.tls_service.create_project(create_project_request)
        project_id = project_response.get_project_id()

        try:
            # 创建测试主题
            topic_name = f"tls-python-sdk-test-shipper-topic-{self._generate_random_string()}"
            create_topic_request = CreateTopicRequest(
                project_id=project_id,
                topic_name=topic_name,
                shard_count=1,
                ttl=1
            )
            topic_response = self.tls_service.create_topic(create_topic_request)
            topic_id = topic_response.get_topic_id()

            try:
                # 测试使用 TopicId 查询
                describe_shippers_request = DescribeShippersRequest(topic_id=topic_id)
                shippers_response = self.tls_service.describe_shippers(describe_shippers_request)

                # 验证响应
                self.assertIsInstance(shippers_response.get_total(), int)
                self.assertIsInstance(shippers_response.get_shippers(), list)

            finally:
                # 清理测试主题
                delete_topic_request = DeleteTopicRequest(topic_id=topic_id)
                self.tls_service.delete_topic(delete_topic_request)

        finally:
            # 清理测试项目
            delete_project_request = DeleteProjectRequest(project_id=project_id)
            self.tls_service.delete_project(delete_project_request)

    def test_describe_shippers_with_multiple_params(self):
        """测试使用多个参数组合查询投递配置"""
        describe_shippers_request = DescribeShippersRequest(
            project_name="test-project",
            shipper_name="test-shipper",
            shipper_type="tos",
            page_number=1,
            page_size=20
        )
        shippers_response = self.tls_service.describe_shippers(describe_shippers_request)

        # 验证响应结构
        self.assertIsInstance(shippers_response.get_total(), int)
        self.assertIsInstance(shippers_response.get_shippers(), list)

    def test_describe_shippers_response_structure(self):
        """测试响应数据结构完整性"""
        describe_shippers_request = DescribeShippersRequest()
        shippers_response = self.tls_service.describe_shippers(describe_shippers_request)

        # 验证基本响应结构
        self.assertTrue(hasattr(shippers_response, 'total'))
        self.assertTrue(hasattr(shippers_response, 'shippers'))
        self.assertTrue(hasattr(shippers_response, 'response'))
        self.assertTrue(hasattr(shippers_response, 'request_id'))

        # 验证 get 方法
        self.assertEqual(shippers_response.get_total(), shippers_response.total)
        self.assertEqual(shippers_response.get_shippers(), shippers_response.shippers)

    def test_describe_shippers_empty_result(self):
        """测试空结果情况"""
        # 使用不存在的 project_id 查询
        describe_shippers_request = DescribeShippersRequest(project_id="non-existent-project-id")
        shippers_response = self.tls_service.describe_shippers(describe_shippers_request)

        # 验证空结果
        self.assertEqual(shippers_response.get_total(), 0)
        self.assertEqual(len(shippers_response.get_shippers()), 0)

    def test_describe_shippers_request_validation(self):
        """测试请求参数验证"""
        # 测试所有参数都可以为 None
        describe_shippers_request = DescribeShippersRequest()

        # 验证默认值
        self.assertEqual(describe_shippers_request.page_number, 1)
        self.assertEqual(describe_shippers_request.page_size, 20)
        self.assertIsNone(describe_shippers_request.project_id)
        self.assertIsNone(describe_shippers_request.project_name)
        self.assertIsNone(describe_shippers_request.shipper_id)
        self.assertIsNone(describe_shippers_request.shipper_name)
        self.assertIsNone(describe_shippers_request.topic_id)
        self.assertIsNone(describe_shippers_request.topic_name)
        self.assertIsNone(describe_shippers_request.shipper_type)


if __name__ == '__main__':
    unittest.main()
