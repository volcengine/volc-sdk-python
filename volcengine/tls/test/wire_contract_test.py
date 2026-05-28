"""Wire-contract tests (Python side).

锁定 5 个核心接口经 SDK 序列化后的 wire 形态：
- 对带 PARAMS/BODY 字典的接口，分别校验 keys 集合；
- 对纯 body 接口，校验 top-level keys 集合。

baseline: cospec/changes/check-tls-sdk-contract-alignment/context/wire-baseline.json
"""

import json
import os
import unittest

from volcengine.tls.tls_requests import (
    CreateAlarmRequest,
    CreateIndexRequest,
    DescribeCheckpointRequest,
    DescribeCursorRequest,
    SearchLogsRequest,
)


def _split(api_input):
    """Returns (params_keys, body_keys) regardless of whether get_api_input
    returns a flat body dict or a {PARAMS, BODY} envelope.
    """
    from volcengine.tls.const import BODY, PARAMS
    if isinstance(api_input, dict) and PARAMS in api_input and BODY in api_input:
        return sorted(api_input[PARAMS].keys()), sorted(api_input[BODY].keys())
    return [], sorted(api_input.keys())


def _baseline():
    here = os.path.dirname(os.path.abspath(__file__))
    # 4 hops up: test -> tls -> volcengine -> volc-sdk-python -> repos
    repo_root = os.path.abspath(os.path.join(here, "..", "..", "..", "..", ".."))
    path = os.path.join(
        repo_root,
        "cospec",
        "changes",
        "check-tls-sdk-contract-alignment",
        "context",
        "wire-baseline.json",
    )
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)["interfaces"]


class WireContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = _baseline()

    def test_describe_cursor(self):
        api = DescribeCursorRequest(topic_id="tid", shard_id=1, from_time="begin").get_api_input()
        params, body = _split(api)
        spec = self.baseline["DescribeCursor"]
        self.assertEqual(spec["query_keys"], params)
        self.assertEqual(spec["body_keys"], body)

    def test_describe_checkpoint(self):
        # 注意：Python 类名是 DescribeCheckpointRequest（小写 point），与 Java/Go/C++ 不同
        api = DescribeCheckpointRequest(
            project_id="pid", topic_id="tid", shard_id=1, consumer_group_name="g1"
        ).get_api_input()
        params, body = _split(api)
        spec = self.baseline["DescribeCheckPoint"]
        self.assertEqual(spec["query_keys"], params)
        self.assertEqual(spec["body_keys"], body)

    def test_search_logs(self):
        api = SearchLogsRequest(
            topic_id="tid",
            query="*",
            start_time=1,
            end_time=2,
            limit=20,
            context="",
            sort="asc",
            highlight=False,
            accurate_query=True,
            must_complete=True,
            offset=0,
        ).get_api_input()
        params, body = _split(api)
        self.assertEqual([], params)
        spec = self.baseline["SearchLogs"]
        # Python 当前没有 RegionTopics 入参，body 为 baseline.body_keys 减 RegionTopics
        expected_body = sorted(set(spec["body_keys"]) - {"RegionTopics"})
        self.assertEqual(expected_body, body)

    def test_create_index(self):
        api = CreateIndexRequest(
            topic_id="tid",
            full_text=None,
            key_value=None,
            user_inner_key_value=None,
            max_text_len=2048,
            enable_auto_index=True,
            enable_phrase_index=True,
        ).get_api_input()
        params, body = _split(api)
        self.assertEqual([], params)
        spec = self.baseline["CreateIndex"]
        allowed = set(spec["body_keys"])
        for k in body:
            self.assertIn(k, allowed, f"unexpected body key: {k}")
        for required in spec["required_keys_in_body"]:
            self.assertIn(required, body, f"missing required key: {required}")

    def test_create_alarm(self):
        from volcengine.tls.tls_requests import (
            QueryRequest,
            RequestCycle,
        )
        api = CreateAlarmRequest(
            project_id="pid",
            alarm_name="a1",
            query_request=[],
            request_cycle=RequestCycle(cycle_type="Period", time=5),
            condition="x>1",
            alarm_period=1,
            alarm_notify_group=["g"],
            status=True,
            trigger_period=1,
            user_define_msg="x",
            severity="warn",
            send_resolved=False,
        ).get_api_input()
        params, body = _split(api)
        self.assertEqual([], params)
        spec = self.baseline["CreateAlarm"]
        allowed = set(spec["body_keys"])
        for k in body:
            self.assertIn(k, allowed, f"unexpected body key: {k}")
        for required in spec["required_keys_in_body"]:
            self.assertIn(required, body, f"missing required key: {required}")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
