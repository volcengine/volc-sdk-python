# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import unittest
import time
import random

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import *
from volcengine.tls.data import ImportTaskInfo


class TestImportTask(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = os.environ.get("VOLCENGINE_ENDPOINT",
                                       "tls-cn-beijing.ivolces.com")
        self.region = os.environ.get("VOLCENGINE_REGION", "cn-beijing")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID",
                                            "test-ak")
        self.access_key_secret = os.environ.get("VOLCENGINE_ACCESS_KEY_SECRET",
                                                "test-sk")
        self.tls_service = TLSService(self.endpoint, self.access_key_id,
                                      self.access_key_secret, self.region)

    def setUp(self):
        """测试前置操作：创建项目和主题"""
        now = str(int(time.time()))
        random_suffix = str(random.randint(1000, 9999))

        # 创建日志项目
        self.project_name = f"import-task-test-project-{now}-{random_suffix}"
        create_project_request = CreateProjectRequest(
            project_name=self.project_name,
            region=self.region,
            description="项目用于导入任务测试"
        )
        try:
            create_project_response = self.tls_service.create_project(
                create_project_request)
            self.project_id = create_project_response.get_project_id()
        except Exception as e:
            self.skipTest(f"创建项目失败: {str(e)}")

        # 创建日志主题
        self.topic_name = f"import-task-test-topic-{now}-{random_suffix}"
        create_topic_request = CreateTopicRequest(
            topic_name=self.topic_name,
            project_id=self.project_id,
            ttl=1,
            description="主题用于导入任务测试",
            shard_count=1
        )
        try:
            create_topic_response = self.tls_service.create_topic(
                create_topic_request)
            self.topic_id = create_topic_response.get_topic_id()
        except Exception as e:
            self.skipTest(f"创建主题失败: {str(e)}")

    def tearDown(self):
        """测试后置操作：清理资源"""
        if hasattr(self, 'task_id'):
            try:
                delete_request = DeleteImportTaskRequest(task_id=self.task_id)
                self.tls_service.delete_import_task(delete_request)
            except Exception:
                pass

        if hasattr(self, 'kafka_task_id'):
            try:
                delete_request = DeleteImportTaskRequest(
                    task_id=self.kafka_task_id)
                self.tls_service.delete_import_task(delete_request)
            except Exception:
                pass

        if hasattr(self, 'topic_id'):
            try:
                delete_topic_request = DeleteTopicRequest(self.topic_id)
                self.tls_service.delete_topic(delete_topic_request)
            except Exception:
                pass

        if hasattr(self, 'project_id'):
            try:
                delete_project_request = DeleteProjectRequest(
                    self.project_id)
                self.tls_service.delete_project(delete_project_request)
            except Exception:
                pass

    def test_modify_import_task_with_tos_source(self):
        """测试修改TOS导入任务"""
        # 创建TOS导入任务
        tos_source_info = TosSourceInfo(
            bucket="test-bucket",
            region=self.region,
            compress_type="none",
            prefix="test-logs/"
        )

        import_source_info = ImportSourceInfo(tos_source_info=tos_source_info)

        import_extract_rule = ImportExtractRule(
            delimiter="|",
            keys=["time", "level", "message"],
            time_key="time",
            time_format="%Y-%m-%d %H:%M:%S",
            time_zone="Asia/Shanghai",
            un_match_up_load_switch=True,
            un_match_log_key="LogParseFailed"
        )

        target_info = TargetInfo(
            region=self.region,
            log_type="delimiter_log",
            extract_rule=import_extract_rule,
            log_sample="2023-12-01 10:00:00|INFO|Test log message"
        )

        create_request = CreateImportTaskRequest(
            topic_id=self.topic_id,
            task_name="test-tos-import-task",
            source_type="tos",
            import_source_info=import_source_info,
            target_info=target_info,
            project_id=self.project_id,
            description="TOS导入任务测试"
        )

        create_response = self.tls_service.create_import_task(create_request)
        self.task_id = create_response.get_task_id()
        self.assertIsNotNone(self.task_id)

        # 修改导入任务
        modify_request = ModifyImportTaskRequest(
            task_id=self.task_id,
            status=4,  # 已停止
            topic_id=self.topic_id,
            task_name="modified-tos-import-task",
            source_type="tos",
            import_source_info=import_source_info,
            target_info=target_info,
            project_id=self.project_id,
            description="修改后的TOS导入任务测试"
        )

        modify_response = self.tls_service.modify_import_task(modify_request)
        self.assertIsNotNone(modify_response)

    def test_modify_import_task_with_kafka_source(self):
        """测试修改Kafka导入任务"""
        # 创建Kafka导入任务
        kafka_source_info = KafkaSourceInfo(
            host="kafka1.example.com:9092,kafka2.example.com:9092",
            topic="test-topic",
            encode="UTF-8",
            protocol="plaintext",
            is_need_auth=False,
            initial_offset=0,
            time_source_default=0
        )

        import_source_info = ImportSourceInfo(kafka_source_info=kafka_source_info)

        import_extract_rule = ImportExtractRule(
            time_key="timestamp",
            time_format="%Y-%m-%dT%H:%M:%S.%fZ",
            time_zone="UTC",
            un_match_up_load_switch=True,
            un_match_log_key="LogParseFailed"
        )

        target_info = TargetInfo(
            region=self.region,
            log_type="json_log",
            extract_rule=import_extract_rule,
            log_sample='{"timestamp":"2023-12-01T10:00:00.000Z",'
                       '"level":"INFO","message":"Test message"}'
        )

        create_request = CreateImportTaskRequest(
            topic_id=self.topic_id,
            task_name="test-kafka-import-task",
            source_type="kafka",
            import_source_info=import_source_info,
            target_info=target_info,
            project_id=self.project_id
        )

        create_response = self.tls_service.create_import_task(create_request)
        self.kafka_task_id = create_response.get_task_id()
        self.assertIsNotNone(self.kafka_task_id)

        # 修改Kafka导入任务
        modify_request = ModifyImportTaskRequest(
            task_id=self.kafka_task_id,
            status=5,  # 重启中
            topic_id=self.topic_id,
            task_name="modified-kafka-import-task",
            source_type="kafka",
            import_source_info=import_source_info,
            target_info=target_info,
            project_id=self.project_id,
            description="修改后的Kafka导入任务测试"
        )

        modify_response = self.tls_service.modify_import_task(modify_request)
        self.assertIsNotNone(modify_response)

    def test_describe_import_tasks(self):
        """测试查询导入任务列表"""
        # 创建多个导入任务
        task_ids = []

        for i in range(2):
            tos_source_info = TosSourceInfo(
                bucket=f"test-bucket-{i}",
                region=self.region,
                compress_type="none",
                prefix=f"test-logs-{i}/"
            )

            import_source_info = ImportSourceInfo(tos_source_info=tos_source_info)

            target_info = TargetInfo(
                region=self.region,
                log_type="json_log"
            )

            create_request = CreateImportTaskRequest(
                topic_id=self.topic_id,
                task_name=f"test-import-task-{i}",
                source_type="tos",
                import_source_info=import_source_info,
                target_info=target_info,
                project_id=self.project_id
            )

            create_response = self.tls_service.create_import_task(create_request)
            task_ids.append(create_response.get_task_id())

        # 查询导入任务列表
        describe_request = DescribeImportTasksRequest(
            project_id=self.project_id,
            topic_id=self.topic_id,
            source_type="tos",
            page_number=1,
            page_size=10
        )

        describe_response = self.tls_service.describe_import_tasks(describe_request)
        self.assertIsNotNone(describe_response)
        self.assertGreaterEqual(describe_response.get_total(), 2)

        task_info_list = describe_response.get_task_info()
        self.assertIsInstance(task_info_list, list)
        self.assertGreaterEqual(len(task_info_list), 2)

        # 清理创建的任务
        for task_id in task_ids:
            try:
                delete_request = DeleteImportTaskRequest(task_id=task_id)
                self.tls_service.delete_import_task(delete_request)
            except Exception:
                pass

    def test_modify_import_task_validation(self):
        """测试修改导入任务参数验证"""
        # 测试缺少必需参数
        with self.assertRaises(Exception):
            modify_request = ModifyImportTaskRequest(
                task_id=None,  # 缺少task_id
                status=4,
                topic_id=self.topic_id,
                task_name="test-task",
                source_type="tos",
                import_source_info=None,  # 缺少import_source_info
                target_info=None  # 缺少target_info
            )
            self.tls_service.modify_import_task(modify_request)

    def test_describe_import_task_validation(self):
        """测试查询导入任务参数验证"""
        # 测试缺少必需参数
        with self.assertRaises(Exception):
            describe_request = DescribeImportTaskRequest(task_id=None)
            self.tls_service.describe_import_task(describe_request)


if __name__ == '__main__':
    unittest.main()
