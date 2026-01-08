import unittest
# pylint: disable=no-member
from unittest.mock import Mock, patch

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import DescribeScheduleSqlTaskRequest
from volcengine.tls.tls_responses import DescribeScheduleSqlTaskResponse
from volcengine.tls.data import ScheduleSqlTaskInfo, RequestCycleInfo


class TestDescribeScheduleSqlTask(unittest.TestCase):

    def setUp(self):
        self.mock_response = Mock()
        self.mock_response.headers = {
            'X-Tls-Requestid': 'test-request-id',
            'Content-Type': 'application/json'
        }
        self.mock_response.text = '''{
            "TaskId": "f3e901c3-b17f-42fd-aa8c-dc91a6c7****",
            "TaskName": "test-schedule-sql-task",
            "Description": "Test schedule SQL task",
            "SourceProjectID": "source-project-id",
            "SourceProjectName": "source-project-name",
            "SourceTopicID": "source-topic-id",
            "SourceTopicName": "source-topic-name",
            "DestRegion": "cn-beijing",
            "DestProjectID": "dest-project-id",
            "DestTopicID": "dest-topic-id",
            "DestTopicName": "dest-topic-name",
            "Status": 1,
            "ProcessStartTime": 1640995200,
            "ProcessEndTime": 1672531200,
            "ProcessSqlDelay": 300,
            "ProcessTimeWindow": "[1640995200, 1672531200]",
            "Query": "SELECT * FROM log WHERE status = 'error'",
            "RequestCycle": {
                "Time": 60,
                "Type": "Period",
                "CronTab": null,
                "CronTimeZone": null
            },
            "CreateTimeStamp": 1640995200,
            "ModifyTimeStamp": 1640995200
        }'''

    def test_describe_schedule_sql_task_request_validation(self):
        """测试 DescribeScheduleSqlTaskRequest 参数验证"""
        # 有效请求
        request = DescribeScheduleSqlTaskRequest(task_id="test-task-id")
        self.assertTrue(request.check_validation())
        
        # 无效请求 - 缺少 task_id
        request = DescribeScheduleSqlTaskRequest(task_id=None)
        self.assertFalse(request.check_validation())

    def test_describe_schedule_sql_task_request_api_input(self):
        """测试 DescribeScheduleSqlTaskRequest 的 API 输入转换"""
        request = DescribeScheduleSqlTaskRequest(task_id="test-task-id")
        api_input = request.get_api_input()
        
        self.assertEqual(api_input["TaskId"], "test-task-id")

    def test_describe_schedule_sql_task_response_parsing(self):
        """测试 DescribeScheduleSqlTaskResponse 响应解析"""
        self.mock_response.status_code = 200
        
        response = DescribeScheduleSqlTaskResponse(self.mock_response)
        
        # 验证基础响应字段
        self.assertEqual(response.get_request_id(), "test-request-id")
        
        # 验证调度SQL任务信息
        task_info: ScheduleSqlTaskInfo = response.get_schedule_sql_task_info()
        self.assertIsInstance(task_info, ScheduleSqlTaskInfo)
        
        # 验证任务基本信息
        self.assertEqual(task_info.task_id, "f3e901c3-b17f-42fd-aa8c-dc91a6c7****")
        self.assertEqual(task_info.task_name, "test-schedule-sql-task")
        self.assertEqual(task_info.description, "Test schedule SQL task")
        
        # 验证源项目信息
        self.assertEqual(task_info.source_project_id, "source-project-id")
        self.assertEqual(task_info.source_project_name, "source-project-name")
        self.assertEqual(task_info.source_topic_id, "source-topic-id")
        self.assertEqual(task_info.source_topic_name, "source-topic-name")
        
        # 验证目标项目信息
        self.assertEqual(task_info.dest_region, "cn-beijing")
        self.assertEqual(task_info.dest_project_id, "dest-project-id")
        self.assertEqual(task_info.dest_topic_id, "dest-topic-id")
        self.assertEqual(task_info.dest_topic_name, "dest-topic-name")
        
        # 验证处理配置
        self.assertEqual(task_info.status, 1)
        self.assertEqual(task_info.process_start_time, 1640995200)
        self.assertEqual(task_info.process_end_time, 1672531200)
        self.assertEqual(task_info.process_sql_delay, 300)
        self.assertEqual(task_info.process_time_window, "[1640995200, 1672531200]")
        self.assertEqual(task_info.query, "SELECT * FROM log WHERE status = 'error'")
        
        # 验证调度周期
        self.assertIsInstance(task_info.request_cycle, RequestCycleInfo)
        self.assertEqual(task_info.request_cycle.time, 60)
        self.assertEqual(task_info.request_cycle.type, "Period")
        self.assertIsNone(task_info.request_cycle.cron_tab)
        self.assertIsNone(task_info.request_cycle.cron_time_zone)
        
        # 验证时间戳
        self.assertEqual(task_info.create_time_stamp, 1640995200)
        self.assertEqual(task_info.modify_time_stamp, 1640995200)

    @patch('volcengine.tls.TLSService.TLSService._TLSService__request')
    def test_describe_schedule_sql_task_service_call(self, mock_request):
        """测试 TLSService.describe_schedule_sql_task 方法调用"""
        # 准备模拟响应
        self.mock_response.status_code = 200
        mock_request.return_value = self.mock_response
        
        # 创建服务实例
        service = TLSService(
            endpoint="test-endpoint",
            access_key_id="test-ak",
            access_key_secret="test-sk",
            region="test-region"
        )
        
        # 创建请求
        request = DescribeScheduleSqlTaskRequest(task_id="test-task-id")
        
        # 调用服务方法
        response = service.describe_schedule_sql_task(request)
        
        # 验证响应类型
        self.assertIsInstance(response, DescribeScheduleSqlTaskResponse)
        
        # 验证请求参数
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        self.assertEqual(call_args[1]['api'], '/DescribeScheduleSqlTask')
        
        # 验证响应内容
        task_info: ScheduleSqlTaskInfo = response.get_schedule_sql_task_info()
        self.assertEqual(task_info.task_id, "f3e901c3-b17f-42fd-aa8c-dc91a6c7****")

    def test_schedule_sql_task_info_with_cron_schedule(self):
        """测试包含 Cron 表达式的调度SQL任务信息"""
        mock_response = Mock()
        mock_response.headers = {
            'X-Tls-Requestid': 'test-request-id',
            'Content-Type': 'application/json'
        }
        mock_response.text = '''{
            "TaskId": "cron-task-id",
            "TaskName": "cron-schedule-sql-task",
            "RequestCycle": {
                "Time": 0,
                "Type": "Cron",
                "CronTab": "0 18 * * *",
                "CronTimeZone": "Asia/Shanghai"
            },
            "CreateTimeStamp": 1640995200,
            "ModifyTimeStamp": 1640995200
        }'''
        
        response = DescribeScheduleSqlTaskResponse(mock_response)
        task_info: ScheduleSqlTaskInfo = response.get_schedule_sql_task_info()
        
        # 验证 Cron 调度信息
        self.assertEqual(task_info.task_id, "cron-task-id")
        self.assertEqual(task_info.task_name, "cron-schedule-sql-task")
        self.assertIsInstance(task_info.request_cycle, RequestCycleInfo)
        self.assertEqual(task_info.request_cycle.type, "Cron")
        self.assertEqual(task_info.request_cycle.cron_tab, "0 18 * * *")
        self.assertEqual(task_info.request_cycle.cron_time_zone, "Asia/Shanghai")

    def test_request_cycle_info_data_class(self):
        """测试 RequestCycleInfo 数据类"""
        # 测试 Period 类型
        period_cycle = RequestCycleInfo(
            time=60,
            task_type="Period",
            cron_tab=None,
            cron_time_zone=None
        )
        
        self.assertEqual(period_cycle.time, 60)
        self.assertEqual(period_cycle.type, "Period")
        self.assertIsNone(period_cycle.cron_tab)
        self.assertIsNone(period_cycle.cron_time_zone)
        
        # 测试 Cron 类型
        cron_cycle = RequestCycleInfo(
            time=0,
            task_type="Cron",
            cron_tab="0 18 * * *",
            cron_time_zone="Asia/Shanghai"
        )
        
        self.assertEqual(cron_cycle.time, 0)
        self.assertEqual(cron_cycle.type, "Cron")
        self.assertEqual(cron_cycle.cron_tab, "0 18 * * *")
        self.assertEqual(cron_cycle.cron_time_zone, "Asia/Shanghai")


if __name__ == '__main__':
    unittest.main()