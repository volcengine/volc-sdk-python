# coding:utf-8
import json
import threading

import redo

from retry import retry

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service
from volcengine.Policy import *
from requests import exceptions

SERVICE_VERSION = "2022-01-01"


class VmsService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(VmsService, "_instance"):
            with VmsService._instance_lock:
                if not hasattr(VmsService, "_instance"):
                    VmsService._instance = object.__new__(cls)
        return VmsService._instance

    def __init__(self, region='cn-north-1'):
        self.service_info = VmsService.get_service_info(region)
        self.api_info = VmsService.get_api_info()
        self.domain_cache = {}
        self.fallback_domain_weights = {}
        self.update_interval = 10
        self.lock = threading.Lock()
        super(VmsService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(region):
        service_info_map = {
            'cn-north-1': ServiceInfo("cloud-vms.volcengineapi.com", {'Accept': 'application/json'},
                                      Credentials('', '', 'vms', 'cn-north-1'), 10, 10),
        }
        service_info = service_info_map.get(region, None)
        if not service_info:
            raise Exception('Cant find the region, please check it carefully')

        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            "BindAXB": ApiInfo("POST", "/", {"Action": "BindAXB", "Version": SERVICE_VERSION}, {}, {}),
            "SelectNumberAndBindAXB": ApiInfo("POST", "/",
                                              {"Action": "SelectNumberAndBindAXB", "Version": SERVICE_VERSION}, {}, {}),
            "UnbindAXB": ApiInfo("POST", "/", {"Action": "UnbindAXB", "Version": SERVICE_VERSION}, {}, {}),
            "QuerySubscription": ApiInfo("POST", "/",
                                         {"Action": "QuerySubscription", "Version": SERVICE_VERSION}, {}, {}),
            "QuerySubscriptionForList": ApiInfo("POST", "/",
                                                {"Action": "QuerySubscriptionForList", "Version": SERVICE_VERSION}, {},
                                                {}),
            "UpgradeAXToAXB": ApiInfo("POST", "/", {"Action": "UpgradeAXToAXB", "Version": SERVICE_VERSION}, {}, {}),
            "UpdateAXB": ApiInfo("POST", "/", {"Action": "UpdateAXB", "Version": SERVICE_VERSION}, {}, {}),
            "BindAXN": ApiInfo("POST", "/", {"Action": "BindAXN", "Version": SERVICE_VERSION}, {}, {}),
            "UpdateAXN": ApiInfo("POST", "/", {"Action": "UpdateAXN", "Version": SERVICE_VERSION}, {}, {}),
            "UnbindAXN": ApiInfo("POST", "/", {"Action": "UnbindAXN", "Version": SERVICE_VERSION}, {}, {}),
            "SelectNumberAndBindAXN": ApiInfo("POST", "/",
                                              {"Action": "SelectNumberAndBindAXN", "Version": SERVICE_VERSION}, {}, {}),
            "Click2Call": ApiInfo("POST", "/", {"Action": "Click2Call", "Version": SERVICE_VERSION}, {}, {}),
            "CancelClick2Call": ApiInfo("POST", "/",
                                        {"Action": "CancelClick2Call", "Version": SERVICE_VERSION}, {}, {}),
            "Click2CallLite": ApiInfo("POST", "/", {"Action": "Click2CallLite", "Version": SERVICE_VERSION}, {}, {}),
            "BindAXNE": ApiInfo("POST", "/", {"Action": "BindAXNE", "Version": SERVICE_VERSION}, {}, {}),
            "UnbindAXNE": ApiInfo("POST", "/", {"Action": "UnbindAXNE", "Version": SERVICE_VERSION}, {}, {}),
            "UpdateAXNE": ApiInfo("POST", "/", {"Action": "UpdateAXNE", "Version": SERVICE_VERSION}, {}, {}),
            "BindAXBForAXNE": ApiInfo("POST", "/", {"Action": "BindAXBForAXNE", "Version": SERVICE_VERSION}, {}, {}),
            "BindAXYB": ApiInfo("POST", "/", {"Action": "BindAXYB", "Version": SERVICE_VERSION}, {}, {}),
            "BindYBForAXYB": ApiInfo("POST", "/", {"Action": "BindYBForAXYB", "Version": SERVICE_VERSION}, {}, {}),
            "UpdateAXYB": ApiInfo("POST", "/", {"Action": "UpdateAXYB", "Version": SERVICE_VERSION}, {}, {}),
            "UnbindAXYB": ApiInfo("POST", "/", {"Action": "UnbindAXYB", "Version": SERVICE_VERSION}, {}, {}),
            "RouteAAuth": ApiInfo("POST", "/", {"Action": "RouteAAuth", "Version": SERVICE_VERSION}, {}, {}),
            "NumberPoolList": ApiInfo("POST", "/", {"Action": "NumberPoolList", "Version": SERVICE_VERSION}, {}, {}),
            "NumberList": ApiInfo("GET", "/", {"Action": "NumberList", "Version": SERVICE_VERSION}, {}, {}),
            "CreateNumberPool": ApiInfo("POST", "/",
                                        {"Action": "CreateNumberPool", "Version": SERVICE_VERSION}, {}, {}),
            "UpdateNumberPool": ApiInfo("POST", "/",
                                        {"Action": "UpdateNumberPool", "Version": SERVICE_VERSION}, {}, {}),
            "EnableOrDisableNumber": ApiInfo("POST", "/",
                                             {"Action": "EnableOrDisableNumber", "Version": SERVICE_VERSION}, {}, {}),
            "SelectNumber": ApiInfo("GET", "/", {"Action": "SelectNumber", "Version": SERVICE_VERSION}, {}, {}),
            "QueryCanCall": ApiInfo("POST", "/", {"Action": "QueryCanCall", "Version": SERVICE_VERSION}, {}, {}),
            "QueryCallRecordMsg": ApiInfo("POST", "/", {"Action": "QueryCallRecordMsg", "Version": SERVICE_VERSION}, {}, {}),
            "QueryAudioRecordFileUrl": ApiInfo("POST", "/",
                                               {"Action": "QueryAudioRecordFileUrl", "Version": SERVICE_VERSION}, {}, {}),
            "QueryAudioRecordToTextFileUrl": ApiInfo("POST", "/",
                                                     {"Action": "QueryAudioRecordToTextFileUrl", "Version": SERVICE_VERSION}, {}, {}),
            "CreateTask": ApiInfo("POST", "/", {"Action": "CreateTask", "Version": SERVICE_VERSION}, {}, {}),
            "BatchAppend": ApiInfo("POST", "/", {"Action": "BatchAppend", "Version": SERVICE_VERSION}, {}, {}),
            "PauseTask": ApiInfo("POST", "/", {"Action": "PauseTask", "Version": SERVICE_VERSION}, {}, {}),
            "ResumeTask": ApiInfo("POST", "/", {"Action": "ResumeTask", "Version": SERVICE_VERSION}, {}, {}),
            "StopTask": ApiInfo("POST", "/", {"Action": "StopTask", "Version": SERVICE_VERSION}, {}, {}),
            "UpdateTask": ApiInfo("POST", "/", {"Action": "UpdateTask", "Version": SERVICE_VERSION}, {}, {}),
            "SingleBatchAppend": ApiInfo("POST", "/", {"Action": "SingleBatchAppend", "Version": SERVICE_VERSION}, {}, {}),
            "SingleInfo": ApiInfo("GET", "/", {"Action": "SingleInfo", "Version": SERVICE_VERSION}, {}, {}),
            "SingleCancel": ApiInfo("GET", "/", {"Action": "SingleCancel", "Version": SERVICE_VERSION}, {}, {}),
            "FetchResource": ApiInfo("POST", "/", {"Action": "FetchResource", "Version": SERVICE_VERSION}, {}, {}),
            "OpenCreateTts": ApiInfo("POST", "/", {"Action": "OpenCreateTts", "Version": SERVICE_VERSION}, {}, {}),
            "OpenDeleteResource": ApiInfo("POST", "/", {"Action": "OpenDeleteResource", "Version": SERVICE_VERSION}, {}, {}),
            "GetResourceUploadUrl": ApiInfo("POST", "/", {"Action": "GetResourceUploadUrl", "Version": SERVICE_VERSION}, {}, {}),
            "CommitResourceUpload": ApiInfo("POST", "/", {"Action": "CommitResourceUpload", "Version": SERVICE_VERSION}, {}, {}),
            "OpenUpdateResource": ApiInfo("POST", "/", {"Action": "OpenUpdateResource", "Version": SERVICE_VERSION}, {}, {}),
            "QueryUsableResource": ApiInfo("POST", "/", {"Action": "QueryUsableResource", "Version": SERVICE_VERSION}, {}, {}),
            "QueryOpenGetResource": ApiInfo("POST", "/", {"Action": "QueryOpenGetResource", "Version": SERVICE_VERSION}, {}, {}),
        }
        return api_info

    def common_handler(self, api, form):
        params = dict()
        try:
            res = self.post(api, params, form)
            res_json = json.loads(res)
            return res_json
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


    @retry(tries=2, delay=0)
    def bind_axb(self, form):
        try:
            return self.common_handler("BindAXB", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def select_number_and_bind_axb(self, form):
        try:
            return self.common_handler("SelectNumberAndBindAXB", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def unbind_axb(self, form):
        try:
            return self.common_handler("UnbindAXB", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def query_subscription(self, form):
        try:
            return self.common_handler("QuerySubscription", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def query_subscription_for_list(self, form):
        try:
            return self.common_handler("QuerySubscriptionForList", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def upgrade_ax_to_axb(self, form):
        try:
            return self.common_handler("UpgradeAXToAXB", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def update_axb(self, form):
        try:
            return self.common_handler("UpdateAXB", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def bind_axn(self, form):
        try:
            return self.common_handler("BindAXN", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def update_axn(self, form):
        try:
            return self.common_handler("UpdateAXN", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def unbind_axn(self, form):
        try:
            return self.common_handler("UnbindAXN", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def select_number_and_bind_axn(self, form):
        try:
            return self.common_handler("SelectNumberAndBindAXN", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def click2_call(self, form):
        try:
            return self.common_handler("Click2Call", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def cancel_click2_call(self, form):
        try:
            return self.common_handler("CancelClick2Call", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def click2_call_lite(self, form):
        try:
            return self.common_handler("Click2CallLite", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def bind_axne(self, form):
        try:
            return self.common_handler("BindAXNE", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def unbind_axne(self, form):
        try:
            return self.common_handler("UnbindAXNE", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def update_axne(self, form):
        try:
            return self.common_handler("UpdateAXNE", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def bind_axb_for_axne(self, form):
        try:
            return self.common_handler("BindAXBForAXNE", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def bind_axyb(self, form):
        try:
            return self.common_handler("BindAXYB", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def bind_yb_for_axyb(self, form):
        try:
            return self.common_handler("BindYBForAXYB", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def update_axyb(self, form):
        try:
            return self.common_handler("UpdateAXYB", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def unbind_axyb(self, form):
        try:
            return self.common_handler("UnbindAXYB", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def route_a_auth(self, form):
        try:
            return self.common_handler("RouteAAuth", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def number_pool_list(self, form):
        try:
            return self.common_handler("NumberPoolList", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def number_list(self, params):
        try:
            return self.do_query_handler("NumberList", params)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def create_number_pool(self, form):
        try:
            return self.common_handler("CreateNumberPool", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def update_number_pool(self, form):
        try:
            return self.common_handler("UpdateNumberPool", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def enable_or_disable_number(self, form):
        try:
            return self.common_handler("EnableOrDisableNumber", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def select_number(self, params):
        try:
            return self.do_query_handler("SelectNumber", params)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def query_call_call(self, form):
        try:
            return self.common_handler("QueryCanCall", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def query_call_record_msg(self, form):
        try:
            return self.common_handler("QueryCallRecordMsg", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def query_audio_record_file_url(self, form):
        try:
            return self.common_handler("QueryAudioRecordFileUrl", form)
        except Exception as e:
            raise Exception(str(e))

    @retry(tries=2, delay=0)
    def query_audio_record_to_text_file_url(self, form):
        try:
            return self.common_handler("QueryAudioRecordToTextFileUrl", form)
        except Exception as e:
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

