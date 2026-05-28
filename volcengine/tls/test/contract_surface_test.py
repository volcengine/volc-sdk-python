import unittest
from urllib.parse import parse_qs, urlparse
from unittest.mock import patch

from requests import Response

from volcengine.tls.const import BODY, PARAMS
from volcengine.tls.TLSService import TLSService
from volcengine.tls import log_pb2
from volcengine.tls.tls_responses import (
    ConsumeLogsResponse,
    DescribeConsumerGroupsResponse,
    DescribeIndexResponse,
    DescribeTopicsResponse,
    DescribeTraceInstanceResponse,
)
from volcengine.tls.tls_requests import (
    ConsumeLogsRequest,
    CreateLogBackFlowTaskRequest,
    CreateDownloadTaskRequest,
    CreateScheduleSqlTaskRequest,
    DeleteLogBackFlowTaskRequest,
    DescribeAlarmsRequest,
    DescribeAlarmNotifyGroupsRequest,
    DescribeAppSceneMetaRequest,
    DescribeBoundHostGroupsRequest,
    DescribeCursorTimeRequest,
    DescribeHostGroupRequestV2,
    DescribeHostGroupsRequestV2,
    DescribeLogBackFlowTasksRequest,
    DescribeRuleRequestV2,
    DescribeSessionAnswerRequest,
    LogBackFlowQueryParams,
    LogBackFlowTaskSource,
    ModifyImportTaskRequest,
    ModifyLogBackFlowTaskRequest,
    PutLogsRequest,
)
from volcengine.tls.data import ImportSourceInfo, RequestCycle, TargetInfo
from volcengine.tls.log_pb2 import LogGroupList


def _varint(value):
    out = bytearray()
    while value > 0x7f:
        out.append((value & 0x7f) | 0x80)
        value >>= 7
    out.append(value)
    return bytes(out)


def _length_delimited(field_number, value):
    return _varint((field_number << 3) | 2) + _varint(len(value)) + value


def _raw_log_group_list(origin_len, compress_type, data):
    body = _varint((1 << 3) | 0) + _varint(origin_len)
    body += _length_delimited(3, compress_type.encode("utf-8"))
    body += _length_delimited(5, data)
    return body


class ContractSurfaceTest(unittest.TestCase):
    def _json_response(self, body):
        response = Response()
        response.status_code = 200
        response._content = __import__("json").dumps(body).encode("utf-8")
        response.headers["Content-Type"] = "application/json"
        response.headers["X-Tls-Requestid"] = "request-id"
        return response

    def _sse_response(self):
        response = Response()
        response.status_code = 200
        response.headers["Content-Type"] = "text/event-stream"
        response.headers["X-Tls-Requestid"] = "request-id"
        return response

    def test_service_includes_official_contract_gaps(self):
        for name in [
            "create_log_back_flow_task",
            "delete_log_back_flow_task",
            "describe_log_back_flow_tasks",
            "modify_log_back_flow_task",
            "describe_cursor_time",
            "describe_host_group_v2",
            "describe_host_groups_v2",
            "describe_bound_host_groups",
            "describe_rule_v2",
        ]:
            self.assertTrue(hasattr(TLSService, name), name)

    def test_contract_gap_requests_serialize_expected_keys(self):
        cursor_time = DescribeCursorTimeRequest(topic_id="topic-id", shard_id=0, cursor="cursor")
        api_input = cursor_time.get_api_input()
        self.assertEqual({"TopicId": "topic-id", "ShardId": 0, "Cursor": "cursor"}, api_input[PARAMS])
        self.assertEqual({}, api_input[BODY])

        create = CreateLogBackFlowTaskRequest(
            task_name="task",
            log_back_flow_task_source=LogBackFlowTaskSource(source_type="Topic"),
            query_params=LogBackFlowQueryParams(),
        )
        body = create.get_api_input()
        self.assertIn("TaskName", body)
        self.assertIn("LogBackFlowTaskSource", body)
        self.assertIn("QueryParams", body)

        describe = DescribeLogBackFlowTasksRequest(topic_id_list=["topic-a", "topic-b"])
        self.assertEqual(["topic-a", "topic-b"], describe.get_api_input()["TopicIDList"])

    def test_go_baseline_request_fields_serialize_expected_keys(self):
        consume = ConsumeLogsRequest(topic_id="topic", shard_id=0, cursor="cursor", original=True)
        self.assertTrue(consume.original)

        download = CreateDownloadTaskRequest(
            task_name="task",
            topic_id="topic",
            query="*",
            start_time=1,
            end_time=2,
            data_format="json",
            sort="desc",
            limit=10,
            compression="gzip",
            must_complete=True,
        )
        self.assertTrue(download.get_api_input()["MustComplete"])

        schedule = CreateScheduleSqlTaskRequest(
            task_name="task",
            topic_id="topic",
            dest_topic_id="dest",
            process_start_time=1,
            process_time_window="@m-1m,@m",
            query="* | select count(*)",
            request_cycle=RequestCycle("Period", 1),
            status=1,
            task_type=0,
        )
        schedule_body = schedule.get_api_input()
        self.assertEqual("topic", schedule_body["TopicID"])
        self.assertEqual(0, schedule_body["TaskType"])

        notify = DescribeAlarmNotifyGroupsRequest(group_name="group", notify_group_id="ng", user_name="user")
        notify_params = notify.get_api_input()
        self.assertEqual("group", notify_params["AlarmNotifyGroupName"])
        self.assertEqual("ng", notify_params["AlarmNotifyGroupId"])
        self.assertEqual("user", notify_params["ReceiverName"])

        alarms = DescribeAlarmsRequest(
            project_id="project",
            project_name="proj-name",
            alarm_policy_id="alarm",
            alarm_disabled=False,
            severity="warning",
            iam_project_name="default",
        )
        alarm_params = alarms.get_api_input()
        self.assertEqual("proj-name", alarm_params["ProjectName"])
        self.assertEqual("alarm", alarm_params["AlarmId"])
        self.assertFalse(alarm_params["AlarmDisabled"])
        self.assertEqual("warning", alarm_params["Severity"])
        self.assertEqual("default", alarm_params["IamProjectName"])

        app_meta = DescribeAppSceneMetaRequest(instance_id="ins", id="id", meta_name="name", app_meta_type="type")
        app_meta_body = app_meta.get_api_input()
        self.assertEqual("type", app_meta_body["APPMetaType"])
        self.assertEqual("name", app_meta_body["Name"])

        modify_import = ModifyImportTaskRequest(
            task_id="task",
            status=1,
            topic_id="topic",
            task_name="name",
            source_type="tos",
            import_source_info=ImportSourceInfo(),
            target_info=TargetInfo(),
            project_id="project",
        )
        import_body = modify_import.get_api_input()
        self.assertEqual("project", import_body["ProjectID"])
        self.assertEqual("topic", import_body["TopicID"])

        put_logs = PutLogsRequest(topic_id="topic", log_group_list=LogGroupList(), compress_type="lz4")
        self.assertEqual("lz4", put_logs.compress_type)

        session_answer = DescribeSessionAnswerRequest(
            instance_id="ins", session_id="session", question="question"
        )
        self.assertEqual("text/event-stream", session_answer.accept)
        self.assertNotIn("Accept", session_answer.get_api_input())

    def test_describe_log_back_flow_topic_id_list_repeats_on_wire(self):
        service = TLSService("http://example.test", "ak", "sk", "cn-test")
        with patch.object(service.session, "request",
                          return_value=self._json_response({"Total": 0, "LogBackFlowTasks": []})) as request:
            service.describe_log_back_flow_tasks(
                DescribeLogBackFlowTasksRequest(topic_id_list=["topic-a", "topic-b"]))

        url = request.call_args.args[1]
        query = parse_qs(urlparse(url).query)
        self.assertEqual(["topic-a", "topic-b"], query["TopicIDList"])

    def test_consume_logs_original_unwraps_raw_log_group_list(self):
        service = TLSService("http://example.test", "ak", "sk", "cn-test")
        raw = self._original_consume_response()
        with patch.object(service.session, "request", return_value=raw) as request:
            original = service.consume_logs(
                ConsumeLogsRequest(topic_id="topic", shard_id=0, cursor="cursor", original=True))

        self.assertIn("/ConsumeOriginalLogs", request.call_args.args[1])
        log_groups = getattr(original.logs, "log_groups")
        self.assertEqual("source", log_groups[0].source)
        self.assertEqual("value", log_groups[0].logs[0].contents[0].value)

    def test_describe_session_answer_uses_streaming_for_sse(self):
        service = TLSService("http://example.test", "ak", "sk", "cn-test")
        with patch.object(service.session, "request", return_value=self._sse_response()) as request:
            response = service.describe_session_answer(
                DescribeSessionAnswerRequest(instance_id="ins", session_id="session", question="question"))

        self.assertTrue(request.call_args.kwargs.get("stream"))
        self.assertEqual("request-id", response.request_id)
        self.assertIs(response.raw_response, request.return_value)

    def test_describe_index_keeps_legacy_empty_full_text_object_for_wire_null(self):
        response = DescribeIndexResponse(self._json_response({
            "TopicId": "topic",
            "FullText": None,
            "KeyValue": [],
            "UserInnerKeyValue": [],
            "CreateTime": "1",
            "ModifyTime": "2",
        }))

        self.assertIsNotNone(response.get_full_text())
        self.assertFalse(response.has_full_text())

    def test_go_baseline_response_fields_are_available(self):
        consume_raw = Response()
        consume_raw.status_code = 200
        consume_raw._content = log_pb2.LogGroupList().SerializeToString()
        consume_raw.headers["Content-Type"] = "application/x-protobuf"
        consume_raw.headers["X-Tls-Requestid"] = "request-id"
        consume_raw.headers["X-Tls-Cursor"] = "cursor"
        consume_raw.headers["X-Tls-Count"] = "3"
        consume = ConsumeLogsResponse(consume_raw, compression="")
        self.assertEqual("cursor", consume.cursor)
        self.assertEqual(3, consume.count)
        self.assertIs(consume.pb_message, consume.logs)

        groups = DescribeConsumerGroupsResponse(self._json_response({
            "ConsumerGroups": [],
            "Total": 2,
            "DashboardId": "dashboard",
        }))
        self.assertEqual(2, groups.total)
        self.assertEqual("dashboard", groups.dashboard_id)

        topics = DescribeTopicsResponse(self._json_response({
            "Topics": [],
            "Total": 1,
            "Cursor": "next",
            "Regions": ["cn-test"],
        }))
        self.assertEqual("next", topics.cursor)
        self.assertEqual(["cn-test"], topics.regions)

        trace = DescribeTraceInstanceResponse(self._json_response({
            "TraceInstanceId": "trace",
            "BackendConfig": {"Type": "tls"},
            "CsAccountChannel": "cs",
        }))
        self.assertEqual({"Type": "tls"}, trace.get_trace_instance().backend_config)
        self.assertEqual("cs", trace.get_trace_instance().cs_account_channel)

    def _original_consume_response(self):
        log_group_list = log_pb2.LogGroupList()
        group = log_group_list.log_groups.add()  # pylint: disable=no-member
        group.source = "source"
        log = group.logs.add()
        log.time = 123
        content = log.contents.add()
        content.key = "key"
        content.value = "value"
        nested = log_group_list.SerializeToString()
        return self._protobuf_response(
            _length_delimited(1, _raw_log_group_list(len(nested), "", nested)),
            {
                "X-Tls-Cursor": "cursor",
                "X-Tls-Count": "1",
                "x-tls-original": "true",
            },
        )

    def _protobuf_response(self, body, headers):
        response = Response()
        response.status_code = 200
        response._content = body
        response.headers["Content-Type"] = "application/x-protobuf"
        response.headers["X-Tls-Requestid"] = "request-id"
        response.headers.update(headers)
        return response


if __name__ == "__main__":
    unittest.main()
