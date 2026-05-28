"""Python SDK SearchLogs / SearchLogsV2 highlight=true 自动注入 SourceType=front 头回归 UT。

与 Go SDK 行为对齐 (service/tls/index.go:193-194)：
- highlight=True  → header SourceType=front 必现
- highlight=False / None → header 不出现 SourceType
- 同时校验 V0.2 与 V0.3 两条路径
"""
import unittest
from unittest.mock import MagicMock, patch

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import SearchLogsRequest


def _make_200_search_response():
    resp = MagicMock()
    resp.status_code = 200
    resp.headers = {"x-tls-requestid": "rid"}
    resp.text = "{}"
    resp.content = b"{}"
    return resp


def _new_service():
    return TLSService(
        endpoint="http://example.test",
        access_key_id="ak",
        access_key_secret="sk",
        region="cn-guilin-boe",
    )


def _captured_headers(mock):
    # session.request(method, url, params=..., data=..., headers=..., timeout=...)
    assert mock.call_args is not None, "session.request 未被调用"
    return mock.call_args.kwargs.get("headers") or {}


class SearchLogsSourceTypeHeaderTest(unittest.TestCase):
    def _build_req(self, highlight):
        return SearchLogsRequest(
            topic_id="tid",
            query="*",
            start_time=1,
            end_time=2,
            limit=1,
            highlight=highlight,
        )

    def test_v0_2_highlight_true_injects_source_type(self):
        svc = _new_service()
        with patch.object(svc.session, "request", return_value=_make_200_search_response()) as m:
            try:
                svc.search_logs(self._build_req(True))
            except Exception:
                pass
            headers = _captured_headers(m)
            self.assertEqual("front", headers.get("SourceType"),
                             "highlight=True 必须注入 SourceType=front, 实际: %r" % headers.get("SourceType"))

    def test_v0_2_highlight_false_no_source_type(self):
        svc = _new_service()
        with patch.object(svc.session, "request", return_value=_make_200_search_response()) as m:
            try:
                svc.search_logs(self._build_req(False))
            except Exception:
                pass
            headers = _captured_headers(m)
            self.assertNotIn("SourceType", headers,
                             "highlight=False 不应注入 SourceType, 实际: %r" % headers.get("SourceType"))

    def test_v0_2_highlight_none_no_source_type(self):
        svc = _new_service()
        with patch.object(svc.session, "request", return_value=_make_200_search_response()) as m:
            try:
                svc.search_logs(self._build_req(None))
            except Exception:
                pass
            headers = _captured_headers(m)
            self.assertNotIn("SourceType", headers)

    def test_v0_3_highlight_true_injects_source_type(self):
        svc = _new_service()
        with patch.object(svc.session, "request", return_value=_make_200_search_response()) as m:
            try:
                svc.search_logs_v2(self._build_req(True))
            except Exception:
                pass
            headers = _captured_headers(m)
            self.assertEqual("front", headers.get("SourceType"))

    def test_v0_3_highlight_false_no_source_type(self):
        svc = _new_service()
        with patch.object(svc.session, "request", return_value=_make_200_search_response()) as m:
            try:
                svc.search_logs_v2(self._build_req(False))
            except Exception:
                pass
            headers = _captured_headers(m)
            self.assertNotIn("SourceType", headers)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
