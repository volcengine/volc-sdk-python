import json
import threading
import redo

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo
from requests import exceptions


class CodePipelineService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(CodePipelineService, "_instance"):
            with CodePipelineService._instance_lock:
                if not hasattr(CodePipelineService, "_instance"):
                    CodePipelineService._instance = object.__new__(cls)
        return CodePipelineService._instance

    def __init__(self):
        self.service_info = CodePipelineService.get_service_info()
        self.api_info = CodePipelineService.get_api_info()
        super(CodePipelineService, self).__init__(
            self.service_info, self.api_info)

    @staticmethod
    def get_service_info():
        service_info = ServiceInfo("open.volcengineapi.com", {'Accept': 'application/json'},
                                   Credentials('', '', 'cp', 'cn-north-1'), 5, 5)
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            "UpdateWorkspace": ApiInfo(
                "POST", "/", {"Action": "UpdateWorkspace", "Version": "2021-03-03"}, {}, {}),
            "DeleteWorkspace": ApiInfo(
                "POST", "/", {"Action": "DeleteWorkspace", "Version": "2021-03-03"}, {}, {}),
            "GetWorkspace": ApiInfo(
                "POST", "/", {"Action": "GetWorkspace", "Version": "2021-03-03"}, {}, {}),
            "CreateWorkspace": ApiInfo(
                "POST", "/", {"Action": "CreateWorkspace", "Version": "2021-03-03"}, {}, {}),
            "ListWorkspaces": ApiInfo(
                "POST", "/", {"Action": "ListWorkspaces", "Version": "2021-03-03"}, {}, {}),
            "CopyWorkspace": ApiInfo(
                "POST", "/", {"Action": "CopyWorkspace", "Version": "2021-03-03"}, {}, {}),
            "CreatePipeline": ApiInfo(
                "POST", "/", {"Action": "CreatePipeline", "Version": "2021-03-03"}, {}, {}),
            "ListPipelines": ApiInfo(
                "POST", "/", {"Action": "ListPipelines", "Version": "2021-03-03"}, {}, {}),
            "DeletePipeline": ApiInfo(
                "POST", "/", {"Action": "DeletePipeline", "Version": "2021-03-03"}, {}, {}),
            "UpdatePipeline": ApiInfo(
                "POST", "/", {"Action": "UpdatePipeline", "Version": "2021-03-03"}, {}, {}),
            "GetPipeline": ApiInfo(
                "POST", "/", {"Action": "GetPipeline", "Version": "2021-03-03"}, {}, {}),
            "UpdatePipelineProperties": ApiInfo(
                "POST", "/", {"Action": "UpdatePipelineProperties", "Version": "2021-03-03"}, {}, {}),
            "GetPipelineHookUrl": ApiInfo(
                "POST", "/", {"Action": "GetPipelineHookUrl", "Version": "2021-03-03"}, {}, {}),
            "RunPipeline": ApiInfo(
                "POST", "/", {"Action": "RunPipeline", "Version": "2021-03-03"}, {}, {}),
            "RunRollingUpdate": ApiInfo(
                "POST", "/", {"Action": "RunRollingUpdate", "Version": "2021-03-03"}, {}, {}),
            "DeletePipelineCache": ApiInfo(
                "POST", "/", {"Action": "DeletePipelineCache", "Version": "2021-03-03"}, {}, {}),
            "ListPipelineRecords": ApiInfo(
                "POST", "/", {"Action": "ListPipelineRecords", "Version": "2021-03-03"}, {}, {}),
            "GetPipelineRecord": ApiInfo(
                "POST", "/", {"Action": "GetPipelineRecord", "Version": "2021-03-03"}, {}, {}),
            "StopPipelineRecord": ApiInfo(
                "POST", "/", {"Action": "StopPipelineRecord", "Version": "2021-03-03"}, {}, {}),
            "RetryPipelineRecord": ApiInfo(
                "POST", "/", {"Action": "RetryPipelineRecord", "Version": "2021-03-03"}, {}, {}),
            "DeletePipelineRecord": ApiInfo(
                "POST", "/", {"Action": "DeletePipelineRecord", "Version": "2021-03-03"}, {}, {}),
            "ListPipelineTemplates": ApiInfo(
                "POST", "/", {"Action": "ListPipelineTemplates", "Version": "2021-03-03"}, {}, {}),
            "GetPipelineTemplate": ApiInfo(
                "POST", "/", {"Action": "GetPipelineTemplate", "Version": "2021-03-03"}, {}, {})}

        return api_info

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def update_workspace(self, params, body):
        res = self.json("UpdateWorkspace", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def delete_workspace(self, params, body):
        res = self.json("DeleteWorkspace", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def get_workspace(self, params, body):
        res = self.json("GetWorkspace", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def create_workspace(self, params, body):
        res = self.json("CreateWorkspace", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def list_workspaces(self, params, body):
        res = self.json("ListWorkspaces", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def copy_workspace(self, params, body):
        res = self.json("CopyWorkspace", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def create_pipeline(self, params, body):
        res = self.json("CreatePipeline", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def list_pipelines(self, params, body):
        res = self.json("ListPipelines", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def delete_pipeline(self, params, body):
        res = self.json("DeletePipeline", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def update_pipeline(self, params, body):
        res = self.json("UpdatePipeline", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def get_pipeline(self, params, body):
        res = self.json("GetPipeline", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def update_pipeline_properties(self, params, body):
        res = self.json("UpdatePipelineProperties", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def get_pipeline_hook_url(self, params, body):
        res = self.json("GetPipelineHookUrl", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def run_pipeline(self, params, body):
        res = self.json("RunPipeline", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def run_rolling_update(self, params, body):
        res = self.json("RunRollingUpdate", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def delete_pipeline_cache(self, params, body):
        res = self.json("DeletePipelineCache", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def list_pipeline_records(self, params, body):
        res = self.json("ListPipelineRecords", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def get_pipeline_record(self, params, body):
        res = self.json("GetPipelineRecord", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def stop_pipeline_record(self, params, body):
        res = self.json("StopPipelineRecord", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def retry_pipeline_record(self, params, body):
        res = self.json("RetryPipelineRecord", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def delete_pipeline_record(self, params, body):
        res = self.json("DeletePipelineRecord", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def list_pipeline_templates(self, params, body):
        res = self.json("ListPipelineTemplates", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def get_pipeline_template(self, params, body):
        res = self.json("GetPipelineTemplate", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
