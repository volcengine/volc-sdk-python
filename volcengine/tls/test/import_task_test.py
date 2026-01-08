# coding=utf-8
"""
Unit tests for CreateImportTask functionality in TLS SDK.

This module contains comprehensive tests for the CreateImportTask API,
including both TOS and Kafka import scenarios.
"""
# pylint: disable=no-member
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import unittest
import time
import random

from volcengine.tls.TLSService import TLSService
from volcengine.tls.data import ImportTaskInfo
from volcengine.tls.tls_requests import (
    CreateProjectRequest, CreateTopicRequest, DeleteProjectRequest,
    DeleteTopicRequest, CreateImportTaskRequest, DescribeImportTaskRequest,
    DescribeImportTasksRequest, TosSourceInfo, KafkaSourceInfo,
    ImportSourceInfo, TargetInfo, ImportExtractRule
)


class TestImportTask(unittest.TestCase):
    """Test class for ImportTask related functionality."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = os.environ.get("VOLCENGINE_ENDPOINT", "")
        self.region = os.environ.get("VOLCENGINE_REGION", "")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "")
        self.access_key_secret = os.environ.get(
            "VOLCENGINE_ACCESS_KEY_SECRET", ""
        )
        self.tls_service = None
        self.test_suffix = None
        self.project_id = None
        self.topic_id = None

        # Skip tests if environment variables are not set
        self.skip_tests = not all([
            self.endpoint, self.region, self.access_key_id,
            self.access_key_secret
        ])

    def setUp(self):
        """Set up test environment before each test."""
        if self.skip_tests:
            self.skipTest("Environment variables not configured")

        self.tls_service = TLSService(
            self.endpoint, self.access_key_id, self.access_key_secret,
            self.region
        )

        # Generate unique identifiers for this test run
        self.test_suffix = str(int(time.time())) + str(
            random.randint(1000, 9999)
        )

        # Create project and topic for testing
        self.project_id = self._create_test_project()
        self.topic_id = self._create_test_topic()

    def tearDown(self):
        """Clean up test environment after each test."""
        # Clean up: delete topic and project
        try:
            if hasattr(self, 'topic_id') and self.topic_id:
                delete_topic_request = DeleteTopicRequest(
                    topic_id=self.topic_id
                )
                self.tls_service.delete_topic(delete_topic_request)

            if hasattr(self, 'project_id') and self.project_id:
                delete_project_request = DeleteProjectRequest(
                    project_id=self.project_id
                )
                self.tls_service.delete_project(delete_project_request)
        except Exception:  # pylint: disable=broad-exception-caught
            # Ignore cleanup errors
            pass

    def _create_test_project(self):
        """Create a test project and return its ID."""
        project_name = (
            f"tls-python-sdk-test-import-task-project-{self.test_suffix}"
        )
        create_project_request = CreateProjectRequest(
            project_name=project_name,
            region=self.region,
            description="Test project for import task"
        )
        response = self.tls_service.create_project(create_project_request)
        return response.get_project_id()

    def _create_test_topic(self):
        """Create a test topic and return its ID."""
        topic_name = f"tls-python-sdk-test-import-task-topic-{self.test_suffix}"
        create_topic_request = CreateTopicRequest(
            topic_name=topic_name,
            project_id=self.project_id,
            shard_count=1,
            ttl=1,
            description="Test topic for import task"
        )
        response = self.tls_service.create_topic(create_topic_request)
        return response.get_topic_id()

    def test_create_import_task_tos(self):
        """Test creating TOS import task."""
        # TOS source info
        tos_source_info = TosSourceInfo(
            bucket="test-bucket",
            prefix="test-prefix/",
            region="cn-shanghai",
            compress_type="none"
        )

        # Import source info
        import_source_info = ImportSourceInfo(tos_source_info=tos_source_info)

        # Target info
        target_info = TargetInfo(
            region=self.region,
            log_type="json_log"
        )

        # Create import task request
        task_name = f"tls-python-sdk-test-import-task-{self.test_suffix}"
        create_request = CreateImportTaskRequest(
            topic_id=self.topic_id,
            task_name=task_name,
            source_type="tos",
            import_source_info=import_source_info,
            target_info=target_info,
            project_id=self.project_id,
            description="Test TOS import task"
        )

        # Execute request
        response = self.tls_service.create_import_task(create_request)

        # Verify response
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.get_task_id())
        task_id = response.get_task_id()
        self.assertIsInstance(task_id, str)
        self.assertGreater(len(task_id), 0)

        # Verify we can query the task
        describe_request = DescribeImportTaskRequest(task_id=task_id)
        describe_response = self.tls_service.describe_import_task(
            describe_request
        )

        self.assertIsNotNone(describe_response)
        task_info: ImportTaskInfo = describe_response.get_task_info()
        self.assertIsNotNone(task_info)
        self.assertEqual(task_info.task_name, task_name)
        self.assertEqual(task_info.source_type, "tos")

    def test_create_import_task_kafka(self):
        """Test creating Kafka import task."""
        # Kafka source info
        kafka_source_info = KafkaSourceInfo(
            host="kafka-host1:9092,kafka-host2:9092",
            topic="test-topic",
            encode="UTF-8",
            protocol="plaintext",
            is_need_auth=False,
            initial_offset=1,
            time_source_default=0
        )

        # Import source info
        import_source_info = ImportSourceInfo(
            kafka_source_info=kafka_source_info
        )

        # Target info with extract rule
        extract_rule = ImportExtractRule(
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
            extract_rule=extract_rule,
            log_sample="2023-12-01 10:00:00|INFO|This is a sample log"
        )

        # Create import task request
        task_name = f"tls-python-sdk-test-kafka-import-task-{self.test_suffix}"
        create_request = CreateImportTaskRequest(
            topic_id=self.topic_id,
            task_name=task_name,
            source_type="kafka",
            import_source_info=import_source_info,
            target_info=target_info,
            project_id=self.project_id,
            description="Test Kafka import task"
        )

        # Execute request
        response = self.tls_service.create_import_task(create_request)

        # Verify response
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.get_task_id())
        task_id = response.get_task_id()
        self.assertIsInstance(task_id, str)
        self.assertGreater(len(task_id), 0)

        # Verify we can query the task
        describe_request = DescribeImportTaskRequest(task_id=task_id)
        describe_response = self.tls_service.describe_import_task(
            describe_request
        )

        self.assertIsNotNone(describe_response)
        task_info: ImportTaskInfo = describe_response.get_task_info()
        self.assertIsNotNone(task_info)
        self.assertEqual(task_info.task_name, task_name)
        self.assertEqual(task_info.source_type, "kafka")

    def test_create_import_task_validation(self):
        """Test input validation for CreateImportTaskRequest."""
        # Test missing required parameters
        with self.assertRaises(Exception):
            CreateImportTaskRequest(
                topic_id=None,  # Missing required topic_id
                task_name="test-task",
                source_type="tos",
                import_source_info=None,
                target_info=None
            )

    def test_describe_import_tasks(self):
        """Test querying multiple import tasks."""
        # Create a test task first
        self.test_create_import_task_tos()

        # Query tasks
        describe_request = DescribeImportTasksRequest(
            project_id=self.project_id,
            topic_id=self.topic_id,
            page_number=1,
            page_size=10
        )

        response = self.tls_service.describe_import_tasks(describe_request)

        # Verify response
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.get_task_infos())
        self.assertIsInstance(response.get_task_infos(), list)
        self.assertGreater(len(response.get_task_infos()), 0)


if __name__ == "__main__":
    unittest.main()
