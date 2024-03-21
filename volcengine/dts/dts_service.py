import json
import threading

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service

SERVICE_VERSION = "2022-10-01"
PRE_SERVICE_VERSION = "2018-01-01"
SERVICE_HOST = "dts.volcengineapi.com"
SERVICE_NAME = "dts"
REST_API_METHOD = "POST"

service_info_map = {
    "cn-beijing": ServiceInfo(SERVICE_HOST, {'accept': 'application/json', },
                              Credentials('', '', SERVICE_NAME, "cn-beijing"), 60 * 5, 60 * 5, "https"),
    "cn-guangzhou": ServiceInfo(SERVICE_HOST, {'accept': 'application/json', },
                                Credentials('', '', SERVICE_NAME, "cn-guangzhou"), 60 * 5, 60 * 5, "https"),
    "cn-shanghai": ServiceInfo(SERVICE_HOST, {'accept': 'application/json', },
                               Credentials('', '', SERVICE_NAME, "cn-shanghai"), 60 * 5, 60 * 5, "https"),
}

api_info = {
    "StartTransmissionTask": ApiInfo(REST_API_METHOD, "/",
                                     {"Action": "StartTransmissionTask", "Version": SERVICE_VERSION}, {}, {}),
    "CreateTransmissionTask": ApiInfo(REST_API_METHOD, "/",
                                      {"Action": "CreateTransmissionTask", "Version": SERVICE_VERSION}, {},
                                      {}),
    "StopTransmissionTask": ApiInfo(REST_API_METHOD, "/",
                                    {"Action": "StopTransmissionTask", "Version": SERVICE_VERSION}, {}, {}),
    "SuspendTransmissionTask": ApiInfo(REST_API_METHOD, "/",
                                       {"Action": "SuspendTransmissionTask", "Version": SERVICE_VERSION}, {},
                                       {}),
    "ResumeTransmissionTask": ApiInfo(REST_API_METHOD, "/",
                                      {"Action": "ResumeTransmissionTask", "Version": SERVICE_VERSION}, {},
                                      {}),
    "RetryTransmissionTask": ApiInfo(REST_API_METHOD, "/",
                                     {"Action": "RetryTransmissionTask", "Version": SERVICE_VERSION}, {}, {}),
    "DeleteTransmissionTask": ApiInfo(REST_API_METHOD, "/",
                                      {"Action": "DeleteTransmissionTask", "Version": SERVICE_VERSION}, {},
                                      {}),
    "ModifyTransmissionTask": ApiInfo(REST_API_METHOD, "/",
                                      {"Action": "ModifyTransmissionTask", "Version": SERVICE_VERSION}, {},
                                      {}),
    "DescribeTransmissionTaskProgress": ApiInfo(REST_API_METHOD, "/",
                                                {"Action": "DescribeTransmissionTaskProgress",
                                                 "Version": SERVICE_VERSION},
                                                {}, {}),
    "DescribeTransmissionTaskInfo": ApiInfo(REST_API_METHOD, "/",
                                            {"Action": "DescribeTransmissionTaskInfo", "Version": SERVICE_VERSION}, {},
                                            {}),
    "DescribeTransmissionTasks": ApiInfo(REST_API_METHOD, "/",
                                         {"Action": "DescribeTransmissionTasks", "Version": SERVICE_VERSION},
                                         {}, {}),
    "PreCheckAsync": ApiInfo(REST_API_METHOD, "/",
                             {"Action": "PreCheckAsync", "Version": PRE_SERVICE_VERSION},
                             {}, {}),
    "GetAsyncPreCheckResult": ApiInfo(REST_API_METHOD, "/",
                                      {"Action": "GetAsyncPreCheckResult", "Version": PRE_SERVICE_VERSION},
                                      {}, {}),
}


class DtsService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(DtsService, "_instance"):
            with DtsService._instance_lock:
                if not hasattr(DtsService, "_instance"):
                    DtsService._instance = object.__new__(cls)
        return DtsService._instance

    def __init__(self, region):
        self.service_info = DtsService.get_service_info(region)
        self.api_info = DtsService.get_api_info()
        super(DtsService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(region):
        service_info = service_info_map.get(region, None)
        if not service_info:
            raise Exception('do not support region %s' % region)
        return service_info

    @staticmethod
    def get_api_info():
        return api_info

    def stop_transmission_task(self, params, body):
        res = self.json('StopTransmissionTask', params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def suspend_transmission_task(self, params, body):
        res = self.json('SuspendTransmissionTask', params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def resume_transmission_task(self, params, body):
        res = self.json('ResumeTransmissionTask', params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def create_transmission_task(self, params, body):
        res = self.json('CreateTransmissionTask', params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def start_transmission_task(self, params, body):
        res = self.json('StartTransmissionTask', params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def modify_transmission_task(self, params, body):
        res = self.json('ModifyTransmissionTask', params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def delete_transmission_task(self, params, body):
        res = self.json('DeleteTransmissionTask', params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def retry_transmission_task(self, params, body):
        res = self.json('RetryTransmissionTask', params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def describe_transmission_tasks(self, params, body):
        res = self.json('DescribeTransmissionTasks', params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def describe_transmission_task_info(self, params, body):
        res = self.json('DescribeTransmissionTaskInfo', params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def describe_transmission_task_progress(self, params, body):
        res = self.json('DescribeTransmissionTaskProgress', params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def pre_check_async(self, params, body):
        res = self.json('PreCheckAsync', params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def get_async_pre_check_result(self, params, body):
        res = self.json('GetAsyncPreCheckResult', params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
