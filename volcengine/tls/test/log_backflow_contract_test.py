import json
import unittest

from requests import Response

from volcengine.tls.data import (
    ContentInfo,
    EvaluationSetFieldMapping,
    EvaluationSetFieldSchema,
    EvaluationSetSchema,
    EvaluationSetShipperInfo,
    LogBackFlowETLTaskInfo,
    LogBackFlowQueryField,
    LogBackFlowQueryFilter,
    LogBackFlowQueryParams,
    LogBackFlowScheduleSqlTaskInfo,
    LogBackFlowShipperToAgentLoopInfo,
    LogBackFlowShipperToTosInfo,
    LogBackFlowTaskSource,
    LogBackFlowTaskTopicSource,
    ParquetField,
    ParquetInfo,
    TargetResource,
)
from volcengine.tls.tls_requests import (
    CreateLogBackFlowTaskRequest,
    DeleteLogBackFlowTaskRequest,
    DescribeLogBackFlowTasksRequest,
    ModifyLogBackFlowTaskRequest,
)
from volcengine.tls.tls_responses import DescribeLogBackFlowTasksResponse


class LogBackFlowContractTest(unittest.TestCase):
    def _etl_task_info(self):
        return LogBackFlowETLTaskInfo(
            script='f_set("key", "value")',
            target_resources=[TargetResource(alias="target", topic_id="topic-dest", region="cn-test")],
        )

    def _source(self):
        return LogBackFlowTaskSource(
            source_type="Topic",
            log_back_flow_task_topic_source=LogBackFlowTaskTopicSource(
                project_id="project-source", topic_id="topic-source"
            ),
        )

    def _agent_loop(self):
        return LogBackFlowShipperToAgentLoopInfo(
            evaluation_set_shipper_info=EvaluationSetShipperInfo(
                workspace_id="workspace",
                evaluation_set_name="dataset",
                evaluation_set_schema=EvaluationSetSchema(field_schemas=[
                    EvaluationSetFieldSchema(
                        name="input",
                        key="input",
                        content_type="Text",
                        default_display_format=1,
                        is_required=True,
                    )
                ]),
                field_mappings=[EvaluationSetFieldMapping(source="message", target="input")],
                item_key_field="__source__",
                batch_size=10,
                skip_invalid_items=True,
                allow_partial_add=True,
            ),
            content_info=ContentInfo(format="json"),
        )

    def test_create_uses_etl_and_agent_loop_contract(self):
        request = CreateLogBackFlowTaskRequest(
            task_name="task",
            log_back_flow_task_source=self._source(),
            back_flow_start_time=1,
            etl_task_info=self._etl_task_info(),
            shipper_to_agent_loop_info=self._agent_loop(),
        )

        self.assertTrue(request.check_validation())
        body = request.get_api_input()
        self.assertEqual('f_set("key", "value")', body["ETLTaskInfo"]["Script"])
        self.assertEqual("topic-dest", body["ETLTaskInfo"]["TargetResources"][0]["TopicId"])
        self.assertEqual("workspace", body["ShipperToAgentLoopInfo"]
                         ["EvaluationSetShipperInfo"]["WorkspaceId"])
        self.assertNotIn("EtlTaskInfo", body)
        self.assertNotIn("ScheduleSqlTaskInfo", body)
        self.assertNotIn("QueryParams", body)
        json.dumps(body)

    def test_create_rejects_missing_required_fields_and_conflicting_shippers(self):
        base = dict(
            task_name="task",
            log_back_flow_task_source=self._source(),
            back_flow_start_time=1,
            etl_task_info=self._etl_task_info(),
        )
        self.assertFalse(CreateLogBackFlowTaskRequest(
            **{**base, "etl_task_info": None}
        ).check_validation())
        self.assertFalse(CreateLogBackFlowTaskRequest(
            **{**base, "back_flow_start_time": 0}
        ).check_validation())
        invalid_source = self._source()
        invalid_source.log_back_flow_task_topic_source.project_id = ""
        self.assertFalse(CreateLogBackFlowTaskRequest(
            **{**base, "log_back_flow_task_source": invalid_source}
        ).check_validation())
        self.assertFalse(CreateLogBackFlowTaskRequest(
            **dict(base, query_params=LogBackFlowQueryParams())
        ).check_validation())
        self.assertFalse(CreateLogBackFlowTaskRequest(
            **dict(base, shipper_to_tos_info=LogBackFlowShipperToTosInfo(),
                   shipper_to_agent_loop_info=self._agent_loop())
        ).check_validation())
        legacy_request = CreateLogBackFlowTaskRequest(
            **dict(base, schedule_sql_task_info=LogBackFlowScheduleSqlTaskInfo())
        )
        self.assertFalse(legacy_request.check_validation())
        self.assertNotIn("ScheduleSqlTaskInfo", legacy_request.get_api_input())

    def test_describe_uses_string_status_and_etl_task_id(self):
        request = DescribeLogBackFlowTasksRequest(
            status="RUNFAILED", etl_task_id="etl-task", schedule_sql_task_id="legacy-task"
        )

        self.assertFalse(request.check_validation())
        params = request.get_api_input()
        self.assertEqual("RUNFAILED", params["Status"])
        self.assertEqual("etl-task", params["ETLTaskId"])
        self.assertNotIn("ScheduleSQLTaskId", params)

        self.assertTrue(DescribeLogBackFlowTasksRequest(status="DONE").check_validation())
        self.assertFalse(DescribeLogBackFlowTasksRequest(status="UNKNOWN").check_validation())

    def test_modify_validates_new_contract_and_never_sends_schedule_sql(self):
        request = ModifyLogBackFlowTaskRequest(
            task_id="task",
            etl_task_info=self._etl_task_info(),
            query_params=LogBackFlowQueryParams(fields=[LogBackFlowQueryField(column="message")]),
            shipper_to_agent_loop_info=self._agent_loop(),
        )

        self.assertTrue(request.check_validation())
        body = request.get_api_input()
        self.assertIn("ETLTaskInfo", body)
        self.assertNotIn("EtlTaskInfo", body)
        self.assertIn("ShipperToAgentLoopInfo", body)
        self.assertNotIn("ScheduleSqlTaskInfo", body)
        json.dumps(body)

        self.assertFalse(ModifyLogBackFlowTaskRequest(
            task_id="task", query_params=LogBackFlowQueryParams()
        ).check_validation())
        self.assertFalse(ModifyLogBackFlowTaskRequest(
            task_id="task", etl_task_info=self._etl_task_info(),
            shipper_to_tos_info=LogBackFlowShipperToTosInfo(),
            shipper_to_agent_loop_info=self._agent_loop(),
        ).check_validation())
        legacy_request = ModifyLogBackFlowTaskRequest(
            task_id="task", schedule_sql_task_info=LogBackFlowScheduleSqlTaskInfo()
        )
        self.assertFalse(legacy_request.check_validation())
        self.assertNotIn("ScheduleSqlTaskInfo", legacy_request.get_api_input())

    def test_delete_rejects_empty_task_id(self):
        self.assertFalse(DeleteLogBackFlowTaskRequest(task_id=None).check_validation())
        self.assertFalse(DeleteLogBackFlowTaskRequest(task_id="").check_validation())
        self.assertTrue(DeleteLogBackFlowTaskRequest(task_id="task").check_validation())

    def test_content_info_supports_parquet(self):
        content = ContentInfo(format="parquet", parquet_info=ParquetInfo(
            fields=[ParquetField(key="count", trans_type="int64")]
        ))
        wire = content.json()
        self.assertEqual("int64", wire["ParquetInfo"]["Fields"][0]["TransType"])
        decoded = ContentInfo.set_attributes(wire)
        self.assertIsInstance(decoded.parquet_info, ParquetInfo)  # pylint: disable=no-member
        self.assertIsInstance(decoded.parquet_info.fields[0], ParquetField)  # pylint: disable=no-member

    def test_describe_response_types_new_nested_models(self):
        raw = {
            "Total": 1,
            "LogBackFlowTasks": [{
                "TaskId": "task",
                "Status": 2,
                "ETLTaskInfo": {
                    "Script": "script",
                    "TargetResources": [{"Alias": "target", "TopicId": "topic", "Region": "cn-test"}],
                },
                "ShipperToAgentLoopInfo": {
                    "EvaluationSetShipperInfo": {
                        "WorkspaceId": "workspace",
                        "FieldMappings": [{"Source": "message", "Target": "input"}],
                    },
                    "ContentInfo": {"Format": "json"},
                },
                "QueryParams": {
                    "Fields": [{"Column": "message", "Alias": "msg"}],
                    "Filters": [{"Field": "level", "Operator": "IN", "Values": [1, "error"]}],
                },
                "RelaTasksInfo": {"ETLTaskId": "etl-task", "ETLTaskName": "etl-name"},
            }],
        }
        response = Response()
        response.status_code = 200
        response._content = json.dumps(raw).encode("utf-8")
        response.headers["Content-Type"] = "application/json"
        response.headers["X-Tls-Requestid"] = "request-id"

        task = DescribeLogBackFlowTasksResponse(response).log_back_flow_tasks[0]
        self.assertIsInstance(task.etl_task_info, LogBackFlowETLTaskInfo)
        self.assertIsInstance(task.etl_task_info.target_resources[0], TargetResource)
        self.assertIsInstance(task.shipper_to_agent_loop_info, LogBackFlowShipperToAgentLoopInfo)
        self.assertIsInstance(task.query_params.fields[0], LogBackFlowQueryField)
        self.assertIsInstance(task.query_params.filters[0], LogBackFlowQueryFilter)
        self.assertEqual([1, "error"], task.query_params.filters[0].values)
        self.assertEqual("workspace", task.shipper_to_agent_loop_info.evaluation_set_shipper_info.workspace_id)
        self.assertEqual("etl-task", task.rela_tasks_info.etl_task_id)
        self.assertEqual("etl-name", task.rela_tasks_info.etl_task_name)


if __name__ == "__main__":
    unittest.main()
