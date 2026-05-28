"""Python SDK retry policy tests.

覆盖：
- 默认行为：POST 503 仍重试（≥2 次）
- 504 纳入可重试状态码
- Retry-After 不覆盖 SDK backoff（TLS 服务端无该响应合同）
"""
import time
import unittest
from unittest.mock import MagicMock, patch

from volcengine.tls.TLSService import TLSService
from volcengine.tls.const import PUT_LOGS, DESCRIBE_PROJECT
from volcengine.tls.retry_policy import RetryPolicy


def _make_response(status_code, headers=None):
    resp = MagicMock()
    resp.status_code = status_code
    resp.headers = headers or {}
    return resp


def _make_503_response():
    return _make_response(503)


def _make_200_response():
    return _make_response(200)


def _new_service():
    svc = TLSService(
        endpoint="http://example.test",
        access_key_id="ak",
        access_key_secret="sk",
        region="cn-guilin-boe",
    )
    svc.set_retry_policy(RetryPolicy(
        max_attempts=3,
        total_timeout=5,
        initial_interval=0.05,
        max_interval=0.2,
        multiplier=2.0,
        randomization_factor=0.0,
    ))
    return svc


class RetryPolicyTest(unittest.TestCase):
    def test_default_post_retries_on_503(self):
        svc = _new_service()
        with patch.object(svc.session, "request", return_value=_make_503_response()) as m:
            try:
                svc._TLSService__request(PUT_LOGS, body={})
            except Exception:
                pass
            self.assertGreaterEqual(m.call_count, 2,
                                    "默认应重试 POST，期望 >=2 次请求，实际 %d" % m.call_count)

    def test_retries_504(self):
        svc = _new_service()
        with patch.object(svc.session, "request", side_effect=[_make_response(504), _make_200_response()]) as m:
            svc._TLSService__request(DESCRIBE_PROJECT, params={})
            self.assertEqual(2, m.call_count)

    def test_retry_ignores_retry_after_header(self):
        svc = _new_service()
        start = time.monotonic()
        with patch.object(
            svc.session,
            "request",
            side_effect=[_make_response(503, {"Retry-After": "10"}), _make_200_response()],
        ) as m:
            svc._TLSService__request(DESCRIBE_PROJECT, params={})
        elapsed = time.monotonic() - start
        self.assertEqual(2, m.call_count)
        self.assertLess(elapsed, 1, "Retry-After must not override SDK backoff")


if __name__ == "__main__":
    unittest.main()
