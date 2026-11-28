import datetime
import hashlib
import unittest
from collections import OrderedDict
from unittest.mock import patch
from urllib.parse import parse_qsl

from volcengine.Credentials import Credentials
from volcengine.auth.SignParam import SignParam
from volcengine.auth.SignerV4 import SignerV4
from volcengine.base.Request import Request


class TestSignOnly(unittest.TestCase):
    def make_param(self, is_sign_url=True):
        param = SignParam()
        param.method = "GET"
        param.path = "/"
        param.host = "open.volcengineapi.com"
        param.date = datetime.datetime(2026, 1, 2, 3, 4, 5)
        param.query = OrderedDict([
            ("Action", "ListUsers"),
            ("Version", "2018-01-01"),
            ("Limit", "5"),
        ])
        param.header_list = OrderedDict([("Host", param.host)])
        param.is_sign_url = is_sign_url
        return param

    def make_request(self, param):
        request = Request()
        request.method = param.method
        request.path = param.path
        request.host = param.host
        request.query = param.query.copy()
        request.headers = param.header_list.copy()
        request.body = param.body
        return request

    def test_url_result_matches_sign_url(self):
        for token in ("", "test-session-token"):
            with self.subTest(token=token):
                param = self.make_param()
                credentials = Credentials("test-ak", "test-sk", "iam", "cn-north-1", token)
                request = self.make_request(param)
                with patch.object(SignerV4, "get_current_format_date", return_value="20260102T030405Z"):
                    query = dict(parse_qsl(SignerV4.sign_url(request, credentials), keep_blank_values=True))

                result = SignerV4.sign_only(param, credentials)

                self.assertEqual(result.xSignature, query["X-Signature"])
                self.assertEqual(result.xCredential, query["X-Credential"])
                self.assertEqual(result.xSignedQueries, query["X-SignedQueries"])
                self.assertEqual(result.xdate, query["X-Date"])
                self.assertEqual(result.xAlgorithm, query["X-Algorithm"])
                self.assertEqual(result.xSecurityToken, token)
                self.assertEqual(result.xSignedHeaders, "")
                self.assertEqual(result.xContextSha256, "")

    def test_url_result_does_not_require_headers(self):
        param = self.make_param()
        param.header_list.clear()
        result = SignerV4.sign_only(param, Credentials("test-ak", "test-sk", "iam", "cn-north-1"))

        self.assertEqual(len(result.xSignature), 64)
        self.assertEqual(result.xContextSha256, "")
        self.assertNotIn("X-Content-Sha256", param.header_list)

    def test_url_signature_does_not_depend_on_body(self):
        credentials = Credentials("test-ak", "test-sk", "iam", "cn-north-1")
        for method in ("GET", "POST"):
            signatures = []
            for body in ("", "a body", b"a binary body"):
                with self.subTest(method=method, body=body):
                    param = self.make_param()
                    param.method = method
                    param.body = body
                    result = SignerV4.sign_only(param, credentials)
                    signatures.append(result.xSignature)
                    self.assertEqual(result.xContextSha256, "")
            self.assertEqual(len(set(signatures)), 1)

    def test_url_result_does_not_return_unused_payload_hash(self):
        param = self.make_param()
        param.header_list["X-Content-Sha256"] = "unused-header-value"
        result = SignerV4.sign_only(param, Credentials("test-ak", "test-sk", "iam", "cn-north-1"))

        self.assertEqual(result.xContextSha256, "")
        self.assertEqual(param.header_list["X-Content-Sha256"], "unused-header-value")

    def test_header_result_still_matches_sign(self):
        for body in ("", '{"message":"hello"}', b"binary-body"):
            with self.subTest(body=body):
                param = self.make_param(is_sign_url=False)
                param.method = "POST"
                param.body = body
                param.header_list["Content-Type"] = "application/json"
                credentials = Credentials("test-ak", "test-sk", "iam", "cn-north-1", "test-session-token")
                request = self.make_request(param)
                with patch.object(SignerV4, "get_current_format_date", return_value="20260102T030405Z"):
                    SignerV4.sign(request, credentials)

                result = SignerV4.sign_only(param, credentials)

                encoded = body.encode("utf-8") if isinstance(body, str) else body
                self.assertEqual(result.xContextSha256, hashlib.sha256(encoded).hexdigest())
                self.assertEqual(result.authorization, request.headers["Authorization"])
                self.assertEqual(result.xSecurityToken, request.headers["X-Security-Token"])
                self.assertEqual(result.xSignedQueries, "")


if __name__ == "__main__":
    unittest.main()
