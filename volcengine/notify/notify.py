# coding:utf-8
import threading

import redo

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service
from volcengine.const.Const import *
from volcengine.Policy import *
from requests import exceptions


NOTIFY_SERVICE_NAME = "volc_voice_notify"
NOTIFY_API_VERSION = "2021-01-01"

service_info_map = {
    REGION_CN_NORTH1: ServiceInfo(
        "cloud-vms.volcengineapi.com",
        {'Accept': 'application/json'},
        Credentials('', '', NOTIFY_SERVICE_NAME, REGION_CN_NORTH1),
        10, 10
    ),
}

notify_api_info = {
    "CreateTask":
        ApiInfo("POST", "/", {"Action": "CreateTask", "Version": NOTIFY_API_VERSION}, {}, {}),
    "BatchAppend":
        ApiInfo("POST", "/", {"Action": "BatchAppend", "Version": NOTIFY_API_VERSION}, {}, {}),
    "PauseTask":
        ApiInfo("POST", "/", {"Action": "PauseTask", "Version": NOTIFY_API_VERSION}, {}, {}),
    "ResumeTask":
        ApiInfo("POST", "/", {"Action": "ResumeTask", "Version": NOTIFY_API_VERSION}, {}, {}),
    "StopTask":
        ApiInfo("POST", "/", {"Action": "StopTask", "Version": NOTIFY_API_VERSION}, {}, {}),
    "UpdateTask":
        ApiInfo("POST", "/", {"Action": "UpdateTask", "Version": NOTIFY_API_VERSION}, {}, {}),
    "SingleBatchAppend":
        ApiInfo("POST", "/", {"Action": "SingleBatchAppend", "Version": NOTIFY_API_VERSION}, {}, {}),
    "SingleInfo":
        ApiInfo("GET", "/", {"Action": "SingleInfo", "Version": NOTIFY_API_VERSION}, {}, {}),
    "SingleCancel":
        ApiInfo("GET", "/", {"Action": "SingleCancel", "Version": NOTIFY_API_VERSION}, {}, {}),
    "FetchResource":
        ApiInfo("POST", "/", {"Action": "FetchResource", "Version": NOTIFY_API_VERSION}, {}, {}),
    "OpenCreateTts":
        ApiInfo("POST", "/", {"Action": "OpenCreateTts", "Version": NOTIFY_API_VERSION}, {}, {}),
    "OpenDeleteResource":
        ApiInfo("POST", "/", {"Action": "OpenDeleteResource", "Version": NOTIFY_API_VERSION}, {}, {}),
    "GetResourceUploadUrl":
        ApiInfo("POST", "/", {"Action": "GetResourceUploadUrl", "Version": NOTIFY_API_VERSION}, {}, {}),
    "CommitResourceUpload":
        ApiInfo("POST", "/", {"Action": "CommitResourceUpload", "Version": NOTIFY_API_VERSION}, {}, {}),
    "OpenUpdateResource":
        ApiInfo("POST", "/", {"Action": "OpenUpdateResource", "Version": NOTIFY_API_VERSION}, {}, {}),
    "QueryUsableResource":
        ApiInfo("POST", "/", {"Action": "QueryUsableResource", "Version": NOTIFY_API_VERSION}, {}, {}),
    "QueryOpenGetResource":
    ApiInfo("POST", "/", {"Action": "QueryOpenGetResource", "Version": NOTIFY_API_VERSION}, {}, {}),
}


class NotifyService(Service):

    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(NotifyService, "_instance"):
            with NotifyService._instance_lock:
                if not hasattr(NotifyService, "_instance"):
                    NotifyService._instance = object.__new__(cls)
        return NotifyService._instance

    def __init__(self, region=REGION_CN_NORTH1):
        self.service_info = NotifyService.get_service_info(region)
        self.api_info = NotifyService.get_api_info()
        super(NotifyService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(region):
        service_info = service_info_map.get(region, None)
        if not service_info:
            raise Exception('Notify service not support region %s' % region)
        return service_info

    @staticmethod
    def get_api_info():
        return notify_api_info

    def do_json_handler(self, api, body, params=dict()):
        try:
            res = self.json(api, params, json.dumps(body))
            return json.loads(res)
        except Exception as e:
            res = str(e)
            try:
                res_json = json.loads(res)
                return res_json
            except:
                raise Exception(str(e))

    def do_query_handler(self, api, params):
        try:
            res = self.get(api, params)
            return json.loads(res)
        except Exception as e:
            res = str(e)
            try:
                res_json = json.loads(res)
                return res_json
            except:
                raise Exception(str(e))

    def do_post_handler(self, api, form, params=dict()):
        try:
            res = self.post(api, params, form)
            return json.loads(res)
        except Exception as e:
            res = str(e)
            try:
                res_json = json.loads(res)
                return res_json
            except:
                raise Exception(str(e))

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def create_task(self, body):
        try:
            res_json = self.do_json_handler("CreateTask", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def batch_append_task(self, body):
        try:
            res_json = self.do_json_handler("BatchAppend", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def update_task(self, body):
        try:
            res_json = self.do_json_handler("UpdateTask", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def pause_task(self, params):
        try:
            res_json = self.do_json_handler("PauseTask", dict(), params)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def resume_task(self, params):
        try:
            res_json = self.do_json_handler("ResumeTask", dict(), params)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def stop_task(self, params):
        try:
            res_json = self.do_json_handler("StopTask", dict(), params)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def single_batch_append(self, body):
        try:
            res_json = self.do_json_handler("SingleBatchAppend", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def single_info(self, params):
        try:
            res_json = self.do_query_handler("SingleInfo", params)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def single_cancel(self, params):
        try:
            res_json = self.do_query_handler("SingleCancel", params)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def fetch_resource(self, body):
        try:
            res_json = self.do_json_handler("FetchResource", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def create_tts(self, body):
        try:
            res_json = self.do_json_handler("OpenCreateTts", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def delete_resource(self, params):
        try:
            res_json = self.do_json_handler("OpenDeleteResource", dict(), params)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def get_resource_upload_url(self, body):
        try:
            res_json = self.do_json_handler("GetResourceUploadUrl", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def commit_resource_upload(self, body):
        try:
            res_json = self.do_json_handler("CommitResourceUpload", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))
    
    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def open_update_resource(self, params):
        try:
            res_json = self.do_post_handler("OpenUpdateResource", {}, params)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def query_usable_resource(self, params):
        try:
            res_json = self.do_post_handler("QueryUsableResource", {}, params)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def query_open_get_resource(self, body):
        try:
            res_json = self.do_json_handler("QueryOpenGetResource", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))
