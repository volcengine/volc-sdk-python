# coding:utf-8
import json
import threading

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo


class StsService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(StsService, "_instance"):
            with StsService._instance_lock:
                if not hasattr(StsService, "_instance"):
                    StsService._instance = object.__new__(cls)
        return StsService._instance

    def __init__(self):
        self.service_info = StsService.get_service_info()
        self.api_info = StsService.get_api_info()
        super(StsService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info():
        service_info = ServiceInfo("sts.volcengineapi.com", {'Accept': 'application/json'},
                                   Credentials('', '', 'sts', 'cn-north-1'), 5, 5)
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {"AssumeRole": ApiInfo("GET", "/", {"Action": "AssumeRole", "Version": "2018-01-01"}, {}, {})}
        return api_info

    def assume_role(self, params):
        res = self.get("AssumeRole", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json