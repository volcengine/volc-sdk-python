import os
import unittest
import random
import string

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import (CreateProjectRequest, CreateTopicRequest, 
                                        DescribeShardsRequest, ManualShardSplitRequest)
from volcengine.tls.tls_responses import (CreateProjectResponse, CreateTopicResponse, 
                                       DescribeShardsResponse, ManualShardSplitResponse)


class TestManualShardSplit(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = os.environ.get("VOLCENGINE_ENDPOINT", "https://tls-cn-beijing.ivolces.com")
        self.region = os.environ.get("VOLCENGINE_REGION", "cn-beijing")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "test-ak")
        self.access_key_secret = os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET", "test-sk")
        self.tls_service = TLSService(self.endpoint, self.access_key_id, self.access_key_secret, self.region)

    def generate_random_string(self, length=10):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def test_manual_shard_split(self):
        """测试手动分区分裂功能"""
        required_env = ["VOLCENGINE_ENDPOINT", "VOLCENGINE_REGION", "VOLCENGINE_ACCESS_KEY_ID", "VOLCENGINE_ACCESS_KEY_SECRET"]
        if not all(os.environ.get(k) for k in required_env):
            self.skipTest("缺少必要的环境变量，跳过手动分区分裂集成测试")

        # 创建项目
        project_name = f"tls-python-sdk-test-manual-shard-split-project-{self.generate_random_string()}"
        create_project_request = CreateProjectRequest(project_name=project_name, region=self.region)
        
        try:
            create_project_response = self.tls_service.create_project(create_project_request)
            self.assertIsInstance(create_project_response, CreateProjectResponse)
            project_id = create_project_response.get_project_id()
            
            # 创建主题
            topic_name = f"tls-python-sdk-test-manual-shard-split-topic-{self.generate_random_string()}"
            create_topic_request = CreateTopicRequest(
                topic_name=topic_name,
                project_id=project_id,
                ttl=1,
                shard_count=2
            )
            
            create_topic_response = self.tls_service.create_topic(create_topic_request)
            self.assertIsInstance(create_topic_response, CreateTopicResponse)
            topic_id = create_topic_response.get_topic_id()
            
            # 查询分片
            describe_shards_request = DescribeShardsRequest(topic_id=topic_id, page_number=1, page_size=20)
            describe_shards_response = self.tls_service.describe_shards(describe_shards_request)
            self.assertIsInstance(describe_shards_response, DescribeShardsResponse)
            
            shards = describe_shards_response.get_shards()
            self.assertGreater(len(shards), 0, "No shards found")
            
            # 选择一个分片进行分裂
            shard_to_split = shards[0]
            shard_id = shard_to_split.get_shard_id()
            
            # 执行手动分区分裂
            manual_shard_split_request = ManualShardSplitRequest(
                topic_id=topic_id,
                shard_id=shard_id,
                number=2
            )
            
            manual_shard_split_response = self.tls_service.manual_shard_split(manual_shard_split_request)
            self.assertIsInstance(manual_shard_split_response, ManualShardSplitResponse)
            
            # 验证响应
            result_shards = manual_shard_split_response.get_shards()
            self.assertIsNotNone(result_shards, "Shards should not be None")
            self.assertGreater(len(result_shards), 0, "Result shards should not be empty")
            
            # 验证每个分片的信息
            for shard in result_shards:
                self.assertIsNotNone(shard.get_shard_id(), "Shard ID should not be None")
                self.assertIsNotNone(shard.get_topic_id(), "Topic ID should not be None")
                self.assertIsNotNone(shard.get_status(), "Status should not be None")
                self.assertIsNotNone(shard.get_inclusive_begin_key(), "Inclusive begin key should not be None")
                self.assertIsNotNone(shard.get_exclusive_end_key(), "Exclusive end key should not be None")
                self.assertIsNotNone(shard.get_modify_time(), "Modify time should not be None")
            
        except Exception as e:
            self.fail(f"Manual shard split test failed: {str(e)}")
            
        finally:
            # 清理资源
            try:
                if 'topic_id' in locals():
                    from volcengine.tls.tls_requests import DeleteTopicRequest
                    delete_topic_request = DeleteTopicRequest(topic_id=topic_id)
                    self.tls_service.delete_topic(delete_topic_request)
                
                if 'project_id' in locals():
                    from volcengine.tls.tls_requests import DeleteProjectRequest
                    delete_project_request = DeleteProjectRequest(project_id=project_id)
                    self.tls_service.delete_project(delete_project_request)
            except Exception as cleanup_e:
                print(f"Cleanup failed: {str(cleanup_e)}")

    def test_manual_shard_split_request_validation(self):
        """测试ManualShardSplitRequest参数验证"""
        # 测试缺少必需参数
        invalid_request = ManualShardSplitRequest(
            topic_id=None, shard_id=1, number=2)
        self.assertFalse(invalid_request.check_validation())

        invalid_request = ManualShardSplitRequest(
            topic_id="test-topic", shard_id=None, number=2)
        self.assertFalse(invalid_request.check_validation())

        invalid_request = ManualShardSplitRequest(
            topic_id="test-topic", shard_id=1, number=None)
        self.assertFalse(invalid_request.check_validation())

        # 测试合法参数
        valid_request = ManualShardSplitRequest(
            topic_id="test-topic", shard_id=1, number=2)
        self.assertTrue(valid_request.check_validation())


if __name__ == '__main__':
    unittest.main()
