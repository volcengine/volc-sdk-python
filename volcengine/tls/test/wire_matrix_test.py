"""真实环境矩阵 dump：5 接口 × 1 case，落 wire fixture + 服务端 status/req_id。

必需 env：WIRE_MATRIX_OUT_DIR / LOG_SERVICE_ENDPOINT / LOG_SERVICE_AK / LOG_SERVICE_SK
          LOG_SERVICE_REGION / WIRE_PROJECT_ID / WIRE_TOPIC_ID / WIRE_CONSUMER_GROUP。缺一即 skip。
输出：${WIRE_MATRIX_OUT_DIR}/python.jsonl，每行 {iface, case, method, path, query, body, status, req_id, err}。
"""

import json
import os
import unittest

from volcengine.tls.TLSService import TLSService, API_INFO
from volcengine.tls.const import (
    BODY, PARAMS,
    CREATE_ALARM, CREATE_INDEX,
    DESCRIBE_CHECKPOINT, DESCRIBE_CURSOR, SEARCH_LOGS,
)
from volcengine.tls.tls_requests import (
    CreateAlarmRequest, CreateIndexRequest, DescribeCheckpointRequest,
    DescribeCursorRequest, RequestCycle, SearchLogsRequest,
)
from volcengine.tls.tls_exception import TLSException


_REQUIRED = [
    ("WIRE_MATRIX_OUT_DIR", "L3_OUT_DIR"),
    ("LOG_SERVICE_ENDPOINT", None),
    ("LOG_SERVICE_AK", None),
    ("LOG_SERVICE_SK", None),
    ("LOG_SERVICE_REGION", None),
    ("WIRE_PROJECT_ID", "L3_PROJECT_ID"),
    ("WIRE_TOPIC_ID", "L3_TOPIC_ID"),
    ("WIRE_CONSUMER_GROUP", "L3_CONSUMER_GROUP"),
]


def _env(name, fallback=None):
    return os.getenv(name) or (os.getenv(fallback) if fallback else None)


def _split(api_input):
    if isinstance(api_input, dict) and PARAMS in api_input and BODY in api_input:
        return dict(api_input[PARAMS]), dict(api_input[BODY])
    return {}, dict(api_input)


def _wire(api_path, req):
    info = API_INFO[api_path]
    params, body = _split(req.get_api_input())
    return {
        "method": info.method,
        "path": api_path,
        "query": {k: ("" if v is None else str(v)) for k, v in params.items()},
        "body": body,
    }


class WireMatrixDump(unittest.TestCase):
    @unittest.skipUnless(all(_env(k, fallback) for k, fallback in _REQUIRED),
                         "wire matrix env not set")
    def test_dump(self):
        out_dir = _env("WIRE_MATRIX_OUT_DIR", "L3_OUT_DIR")
        os.makedirs(out_dir, exist_ok=True)
        project_id = _env("WIRE_PROJECT_ID", "L3_PROJECT_ID")
        topic_id = _env("WIRE_TOPIC_ID", "L3_TOPIC_ID")
        cg_name = _env("WIRE_CONSUMER_GROUP", "L3_CONSUMER_GROUP")
        svc = TLSService(
            endpoint=os.getenv("LOG_SERVICE_ENDPOINT"),
            access_key_id=os.getenv("LOG_SERVICE_AK"),
            access_key_secret=os.getenv("LOG_SERVICE_SK"),
            region=os.getenv("LOG_SERVICE_REGION"),
        )

        # iface -> (wire-fixture, caller)
        cases = []

        # DescribeCursor
        req = DescribeCursorRequest(topic_id=topic_id, shard_id=0, from_time="begin")
        cases.append(("DescribeCursor", _wire(DESCRIBE_CURSOR, req),
                      lambda r=req: svc.describe_cursor(r)))

        # DescribeCheckPoint
        req = DescribeCheckpointRequest(
            project_id=project_id, topic_id=topic_id, shard_id=0, consumer_group_name=cg_name)
        cases.append(("DescribeCheckPoint", _wire(DESCRIBE_CHECKPOINT, req),
                      lambda r=req: svc.describe_checkpoint(r)))

        # SearchLogs
        req = SearchLogsRequest(
            topic_id=topic_id,
            query="*",
            start_time=1700000000,
            end_time=1700001000,
            limit=20,
            context="",
            sort="asc",
            highlight=False,
            accurate_query=True,
            must_complete=True,
            offset=0,
        )
        cases.append(("SearchLogs", _wire(SEARCH_LOGS, req),
                      lambda r=req: svc.search_logs(r)))

        # CreateIndex
        req = CreateIndexRequest(
            topic_id=topic_id,
            full_text=None,
            key_value=None,
            user_inner_key_value=None,
            max_text_len=2048,
            enable_auto_index=True,
            enable_phrase_index=True,
        )
        cases.append(("CreateIndex", _wire(CREATE_INDEX, req),
                      lambda r=req: svc.create_index(r)))

        # CreateAlarm（伪 NotifyGroup → 期望 4xx）
        req = CreateAlarmRequest(
            project_id=project_id,
            alarm_name="l3-sdk-align-fake-alarm",
            query_request=[],
            request_cycle=RequestCycle(cycle_type="Period", time=5),
            condition="x>1",
            alarm_period=5,
            alarm_notify_group=["g-fake"],
            status=True,
            trigger_period=1,
            user_define_msg="msg",
            severity="warning",
            send_resolved=False,
        )
        cases.append(("CreateAlarm", _wire(CREATE_ALARM, req),
                      lambda r=req: svc.create_alarm(r)))

        # iface 字母序输出
        cases.sort(key=lambda x: x[0])

        out_path = os.path.join(out_dir, "python.jsonl")
        with open(out_path, "w", encoding="utf-8") as fh:
            for iface, wire, caller in cases:
                rec = {
                    "iface": iface,
                    "case": "default",
                    "method": wire["method"],
                    "path": wire["path"],
                    "query": wire["query"],
                    "body": wire["body"],
                }
                try:
                    resp = caller()
                    rec["status"] = 200
                    rec["req_id"] = resp.get_request_id() or ""
                except TLSException as e:
                    rec["status"] = getattr(e, "http_code", 0) or 0
                    rec["req_id"] = getattr(e, "request_id", "") or ""
                    rec["err"] = f"{e.error_code}: {e.error_message}"
                fh.write(json.dumps(rec, ensure_ascii=False, sort_keys=True, default=_json_default) + "\n")


def _json_default(obj):
    if hasattr(obj, "__dict__"):
        return {k: v for k, v in vars(obj).items() if not k.startswith("_")}
    return str(obj)


if __name__ == "__main__":
    unittest.main()
