"""Contract tests for index phrase switch and processor request models."""

import json
import unittest

from volcengine.tls.const import CONTENT_TYPE, X_TLS_REQUEST_ID
from volcengine.tls.tls_requests import (
    CreateIndexRequest,
    ModifyIndexRequest,
    CreateProcessorRequest,
)
from volcengine.tls.tls_responses import DescribeIndexResponse


class MockResponse:
    def __init__(self, json_body):
        self.headers = {
            X_TLS_REQUEST_ID: "test-request-id",
            CONTENT_TYPE: "application/json",
        }
        self.text = json.dumps(json_body)
        self.content = self.text.encode("utf-8")


class TestProcessorContract(unittest.TestCase):
    def test_index_requests_include_enable_phrase_index(self):
        create_input = CreateIndexRequest("topic-id", enable_phrase_index=True).get_api_input()
        modify_input = ModifyIndexRequest("topic-id", enable_phrase_index=True).get_api_input()

        self.assertTrue(create_input["EnablePhraseIndex"])
        self.assertTrue(modify_input["EnablePhraseIndex"])

    def test_describe_index_response_parses_enable_phrase_index(self):
        response = DescribeIndexResponse(MockResponse({
            "TopicId": "topic-id",
            "FullText": None,
            "KeyValue": [],
            "UserInnerKeyValue": [],
            "CreateTime": "2026-05-01 00:00:00",
            "ModifyTime": "2026-05-01 00:00:00",
            "EnablePhraseIndex": True,
        }))

        self.assertTrue(response.get_enable_phrase_index())

    def test_create_processor_request_uses_service_contract_fields(self):
        api_input = CreateProcessorRequest(
            project_id="project-id",
            processor_name="processor-name",
            dsl_content='f_set("k", "v")',
            processor_type="ingester",
            processor_dsl_type="dsl",
            processor_status="enabled",
            fail_strategy="keep_raw",
            timeout_ms=5000,
            max_qps=10,
        ).get_api_input()

        self.assertEqual("project-id", api_input["ProjectId"])
        self.assertEqual("processor-name", api_input["ProcessorName"])
        self.assertEqual("ingester", api_input["ProcessorType"])
        self.assertEqual("dsl", api_input["ProcessorDSLType"])
        self.assertEqual("enabled", api_input["ProcessorStatus"])
        self.assertEqual("keep_raw", api_input["FailStrategy"])
        self.assertEqual(5000, api_input["TimeoutMs"])
        self.assertEqual(10, api_input["MaxQps"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

