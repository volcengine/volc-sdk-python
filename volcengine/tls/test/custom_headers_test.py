"""Python SDK 用户自定义 header 入口回归 UT。

与 Go SDK CommonRequest.Headers + assembleHeader 行为对齐：
- set_custom_headers / add_custom_header 实例级生效
- 用户 header 抵达 wire
- SDK 内部 header（HEADER_API_VERSION、Content-Type、SourceType）后写覆盖用户值
- 清空（None / {}）后用户 header 不再注入
"""
import unittest
from unittest.mock import MagicMock, patch

from volcengine.tls.TLSService import TLSService, HEADER_API_VERSION
from volcengine.tls.tls_requests import SearchLogsRequest


def _make_200():
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
    assert mock.call_args is not None, "session.request 未被调用"
    return mock.call_args.kwargs.get("headers") or {}


def _build_search_req():
    return SearchLogsRequest(topic_id="tid", query="*", start_time=1, end_time=2, limit=1)


class CustomHeadersTest(unittest.TestCase):
    def test_custom_headers_pass_through_to_wire(self):
        svc = _new_service()
        svc.set_custom_headers({"X-Trace-Id": "trace-abc", "X-Tenant-Tag": "team-foo"})
        with patch.object(svc.session, "request", return_value=_make_200()) as m:
            try:
                svc.search_logs(_build_search_req())
            except Exception:
                pass
            headers = _captured_headers(m)
            self.assertEqual("trace-abc", headers.get("X-Trace-Id"))
            self.assertEqual("team-foo", headers.get("X-Tenant-Tag"))

    def test_add_custom_header_appends(self):
        svc = _new_service()
        svc.add_custom_header("X-Trace-Id", "trace-1")
        svc.add_custom_header("X-Tenant-Tag", "team-bar")
        with patch.object(svc.session, "request", return_value=_make_200()) as m:
            try:
                svc.search_logs(_build_search_req())
            except Exception:
                pass
            headers = _captured_headers(m)
            self.assertEqual("trace-1", headers.get("X-Trace-Id"))
            self.assertEqual("team-bar", headers.get("X-Tenant-Tag"))

    def test_sdk_header_overrides_user_header(self):
        svc = _new_service()
        # 用户尝试覆盖 SDK 协议字段：API_VERSION + SourceType
        svc.set_custom_headers({
            HEADER_API_VERSION: "9.9.9",
            "SourceType": "user-injected",
        })
        req = _build_search_req()
        req.highlight = True  # 触发 SDK 写入 SourceType=front
        with patch.object(svc.session, "request", return_value=_make_200()) as m:
            try:
                svc.search_logs(req)
            except Exception:
                pass
            headers = _captured_headers(m)
            # SDK 内部 header 必须后写覆盖
            self.assertEqual("0.2.0", headers.get(HEADER_API_VERSION),
                             "SDK 应覆盖用户 HEADER_API_VERSION")
            self.assertEqual("front", headers.get("SourceType"),
                             "SDK 应覆盖用户 SourceType")

    def test_clear_custom_headers_via_none(self):
        svc = _new_service()
        svc.set_custom_headers({"X-Trace-Id": "trace-abc"})
        svc.set_custom_headers(None)
        with patch.object(svc.session, "request", return_value=_make_200()) as m:
            try:
                svc.search_logs(_build_search_req())
            except Exception:
                pass
            headers = _captured_headers(m)
            self.assertNotIn("X-Trace-Id", headers)

    def test_get_custom_headers_returns_copy(self):
        svc = _new_service()
        svc.set_custom_headers({"X-Trace-Id": "trace-abc"})
        snap = svc.get_custom_headers()
        snap["X-Should-Not-Leak"] = "x"
        # 内部状态应不受外部修改影响
        self.assertNotIn("X-Should-Not-Leak", svc.get_custom_headers())


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
