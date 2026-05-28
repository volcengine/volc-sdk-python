"""Deserialization regression tests.

消费 cospec/context/l5-fixtures/responses.json，验证 5 个 Describe* Response 类
对真实服务端响应能完整反序列化、零字段丢失。

fixture 来源：实验室经 volclog 采集（profile 2100051396-sy, region cn-guilin-boe），
与 Go/Java/C++ V2 共享同一份 responses.json（4 SDK 交叉反序列化对照）。
"""
import json
import os
import unittest
from unittest.mock import MagicMock

from volcengine.tls.data import ProjectInfo
from volcengine.tls.tls_responses import (
    DescribeCheckpointResponse,
    DescribeCursorResponse,
    DescribeIndexResponse,
    DescribeProjectResponse,
    DescribeTopicResponse,
)


def _fake_response(body: dict):
    """构造一个最小化的 requests.Response 替身，让 TLSResponse.__init__ 走 JSON 分支。"""
    fake = MagicMock()
    fake.headers = {
        "Content-Type": "application/json",
        "X-Tls-Requestid": "l5-fixture-request-id",
    }
    fake.text = json.dumps(body)
    fake.content = fake.text.encode("utf-8")
    return fake


class ResponseDeserializeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 仓库相对路径：repos/volc-sdk-python/ -> ../../cospec/.../responses.json
        here = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.environ.get("RESPONSE_FIXTURE", "") or os.environ.get("L5_FIXTURE", ""),
            os.path.normpath(os.path.join(
                here, "..", "..", "..", "..", "..",
                "cospec", "changes", "check-tls-sdk-contract-alignment",
                "context", "l5-fixtures", "responses.json")),
        ]
        for path in candidates:
            if path and os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    cls.fx = json.load(f)
                cls.fixture_path = path
                return
        raise FileNotFoundError(
            "response fixture not found, tried: " + repr(candidates))

    def test_describe_cursor_deserialize(self):
        body = self.fx["DescribeCursor"]
        resp = DescribeCursorResponse(_fake_response(body))
        self.assertEqual("AAAAAAAAAAAAAAAAAAAAAAAw", resp.cursor)

    def test_describe_checkpoint_honors_shard_id_uppercase(self):
        body = self.fx["DescribeCheckPoint"]
        resp = DescribeCheckpointResponse(_fake_response(body))
        # wire 'ShardID'（D 大写），常量 SHARD_ID_UPPERCASE
        self.assertEqual(0, resp.shard_id)
        self.assertEqual("", resp.checkpoint)

    def test_describe_index_handles_null_and_empty_array(self):
        body = self.fx["DescribeIndex"]
        resp = DescribeIndexResponse(_fake_response(body))
        # DescribeIndexResponse 暴露 topic_id，与 Go/Java/C++ V2 对齐。
        self.assertEqual("121c1bcd-6030-42c8-a02f-8465f1fc67ef", resp.topic_id)
        # Python 保持历史兼容：wire 'FullText':null 时 get_full_text() 仍返回空对象。
        self.assertIsNotNone(resp.full_text)
        self.assertFalse(resp.has_full_text())
        self.assertEqual([], resp.key_value)
        self.assertEqual([], resp.user_inner_key_value)
        self.assertTrue(resp.enable_phrase_index)
        self.assertEqual(2048, resp.max_text_len)
        self.assertTrue(resp.enable_auto_index)

    def test_describe_project_unwraps_to_project_info(self):
        body = self.fx["DescribeProject"]
        resp = DescribeProjectResponse(_fake_response(body))
        info = resp.project
        self.assertIsInstance(info, ProjectInfo)
        self.assertEqual(
            "740e2f59-08e2-41ee-b24c-dd98b79f6c35",
            getattr(info, "project_id"),
        )
        self.assertEqual("l3-sdk-align-1779612326", getattr(info, "project_name"))
        self.assertEqual("default", getattr(info, "iam_project_name"))
        self.assertEqual(1, getattr(info, "topic_count"))
        self.assertTrue(getattr(info, "inner_net_domain").startswith("https://"))

    def test_describe_topic_unwraps_to_topic_info(self):
        body = self.fx["DescribeTopic"]
        resp = DescribeTopicResponse(_fake_response(body))
        info = resp.topic
        self.assertEqual("121c1bcd-6030-42c8-a02f-8465f1fc67ef", info.topic_id)
        self.assertEqual("l3-topic-1", info.topic_name)
        self.assertEqual("2.0", info.tls_version)  # wire 'TLSVersion'
        self.assertEqual(2, info.shard_count)
        self.assertEqual("ChargeByFunction", info.metering_mode)
        self.assertEqual(1, info.ttl)
        self.assertEqual(1, info.hot_ttl)
        self.assertFalse(info.auto_split)
        self.assertFalse(info.enable_hot_ttl)
        self.assertFalse(info.log_public_ip)


if __name__ == "__main__":
    unittest.main()
