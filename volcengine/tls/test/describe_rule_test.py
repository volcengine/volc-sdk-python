"""Unit tests for DescribeRuleResponse and RuleInfo pause field."""
# pylint: disable=no-member

import json
import unittest

from volcengine.tls.const import (
    X_TLS_REQUEST_ID,
    CONTENT_TYPE,
    PROJECT_ID,
    PROJECT_NAME,
    TOPIC_ID,
    TOPIC_NAME,
    RULE_INFO,
    HOST_GROUP_INFOS,
    PAUSE,
)
from volcengine.tls.tls_responses import DescribeRuleResponse
from volcengine.tls.data import RuleInfo


class MockResponse:
    """Simple mock of requests.Response used by TLSResponse."""

    def __init__(self, json_body):
        self.headers = {
            X_TLS_REQUEST_ID: "test-request-id",
            CONTENT_TYPE: "application/json",
        }
        self.text = json.dumps(json_body)
        self.content = self.text.encode("utf-8")


class TestDescribeRule(unittest.TestCase):
    """Tests for DescribeRuleResponse mapping Pause field into RuleInfo."""

    def test_describe_rule_response_includes_pause_field(self):
        """Verify that Pause field is parsed into RuleInfo.get_pause()."""
        rule_info_body = {
            # Only Pause field is required for this test; other fields are optional.
            PAUSE: 1,
        }

        response_body = {
            PROJECT_ID: "project-id",
            PROJECT_NAME: "project-name",
            TOPIC_ID: "topic-id",
            TOPIC_NAME: "topic-name",
            RULE_INFO: rule_info_body,
            HOST_GROUP_INFOS: [],
        }

        response = DescribeRuleResponse(MockResponse(response_body))
        rule_info: RuleInfo = response.get_rule_info()

        self.assertEqual(1, rule_info.get_pause())


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
