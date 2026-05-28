"""Wire snapshot dumper for Python SDK.

通过环境变量 WIRE_SNAPSHOT_OUT_DIR 指定输出目录；按 cospec/.../context/l2-fixtures.json 字面量
构造 5 接口请求，输出到 ${WIRE_SNAPSHOT_OUT_DIR}/python.json，与 4 SDK 一致格式
{sdk, sdk_repo, interfaces}。

Python SDK 的 get_api_input() 既可能返回扁平 body dict，也可能返回
{PARAMS: {...}, BODY: {...}} 信封，本脚本统一拆开。Path/Method 取自
volcengine.tls.TLSService.api_info 表。
"""

import json
import os
import sys
import unittest

from volcengine.tls.const import (
    BODY, PARAMS, CREATE_ALARM, CREATE_INDEX,
    DESCRIBE_CHECKPOINT, DESCRIBE_CURSOR, SEARCH_LOGS,
)
from volcengine.tls.tls_requests import (
    CreateAlarmRequest, CreateIndexRequest, DescribeCheckpointRequest,
    DescribeCursorRequest, QueryRequest, RequestCycle, SearchLogsRequest,
)
from volcengine.tls.TLSService import API_INFO


def _split(api_input):
    if isinstance(api_input, dict) and PARAMS in api_input and BODY in api_input:
        return dict(api_input[PARAMS]), dict(api_input[BODY])
    return {}, dict(api_input)


def _snap(api_path, req):
    info = API_INFO[api_path]
    api = req.get_api_input()
    params, body = _split(api)
    # 全部转成 str -> 与 Go/Java/C++ 的 query 形态一致
    return {
        "method": info.method,
        "path": api_path,
        "query": {k: ("" if v is None else str(v)) for k, v in params.items()},
        "body": body,
    }


class WireSnapshotTest(unittest.TestCase):
    @unittest.skipUnless(os.getenv("WIRE_SNAPSHOT_OUT_DIR") or os.getenv("L2_OUT_DIR"),
                         "WIRE_SNAPSHOT_OUT_DIR not set")
    def test_dump(self):
        out_dir = os.getenv("WIRE_SNAPSHOT_OUT_DIR") or os.getenv("L2_OUT_DIR")
        os.makedirs(out_dir, exist_ok=True)

        ifaces = {}
        ifaces["DescribeCursor"] = _snap(
            DESCRIBE_CURSOR,
            DescribeCursorRequest(topic_id="tid-cursor", shard_id=1, from_time="begin"),
        )
        ifaces["DescribeCheckPoint"] = _snap(
            DESCRIBE_CHECKPOINT,
            DescribeCheckpointRequest(
                project_id="pid-ck", topic_id="tid-ck", shard_id=2, consumer_group_name="g1",
            ),
        )
        ifaces["SearchLogs"] = _snap(
            SEARCH_LOGS,
            SearchLogsRequest(
                topic_id="tid-search",
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
            ),
        )
        ifaces["CreateIndex"] = _snap(
            CREATE_INDEX,
            CreateIndexRequest(
                topic_id="tid-idx",
                full_text=None,
                key_value=None,
                user_inner_key_value=None,
                max_text_len=2048,
                enable_auto_index=True,
                enable_phrase_index=True,
            ),
        )
        ifaces["CreateAlarm"] = _snap(
            CREATE_ALARM,
            CreateAlarmRequest(
                project_id="pid-alarm",
                alarm_name="alarm-1",
                query_request=[],
                request_cycle=RequestCycle(cycle_type="Period", time=5),
                condition="x>1",
                alarm_period=5,
                alarm_notify_group=["g-1"],
                status=True,
                trigger_period=1,
                user_define_msg="msg",
                severity="warning",
                send_resolved=False,
            ),
        )

        out = {
            "sdk": "python",
            "sdk_repo": "volc-sdk-python",
            "interfaces": ifaces,
        }
        target = os.path.join(out_dir, "python.json")
        with open(target, "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=2, ensure_ascii=False, sort_keys=True, default=_json_default)
            fh.write("\n")
        sys.stderr.write(f"wire snapshot written: {target}\n")


def _json_default(obj):
    """fallback：把 SDK 自定义对象（QueryRequest / RequestCycle）转 dict。"""
    if hasattr(obj, "__dict__"):
        return {k: v for k, v in vars(obj).items() if not k.startswith("_")}
    return str(obj)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
