import json
import threading
import redo

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo
from requests import exceptions


class RiskDetectService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(RiskDetectService, "_instance"):
            with RiskDetectService._instance_lock:
                if not hasattr(RiskDetectService, "_instance"):
                    RiskDetectService._instance = object.__new__(cls)
        return RiskDetectService._instance

    def __init__(self):
        self.service_info = RiskDetectService.get_service_info()
        self.api_info = RiskDetectService.get_api_info()
        super(RiskDetectService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info():
        service_info = ServiceInfo("open.volcengineapi.com", {'Accept': 'application/json'},
                                   Credentials('', '', 'BusinessSecurity', 'cn-north-1'), 5, 5)
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {"RiskDetection": ApiInfo("POST", "/", {"Action": "RiskDetection", "Version": "2021-02-02"}, {}, {}),
                    "AsyncRiskDetection": ApiInfo("POST", "/", {"Action": "AsyncRiskDetection", "Version": "2021-02-25"}, {}, {}),
                    "RiskResult": ApiInfo("GET", "/", {"Action": "RiskResult", "Version": "2021-03-10"}, {}, {}),
                    "AccountRisk": ApiInfo("POST", "/", {"Action": "AccountRisk", "Version": "2020-12-25"}, {}, {}),
                    "MobileStatus": ApiInfo("POST", "/", {"Action": "MobileStatus", "Version": "2020-12-25"}, {}, {}),
                    "ElementVerify": ApiInfo("POST", "/", {"Action": "ElementVerify", "Version": "2021-11-23"}, {}, {}),
                    "MobileStatusV2": ApiInfo("POST", "/", {"Action": "MobileStatus", "Version": "2022-04-13"}, {}, {}),
                    "ElementVerifyV2": ApiInfo("POST", "/", {"Action": "ElementVerify", "Version": "2022-04-13"}, {}, {})}

        return api_info

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def risk_detect(self, params, body):
        res = self.json("RiskDetection", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def async_risk_detect(self, params, body):
        res = self.json("AsyncRiskDetection", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def risk_result(self, params, body):
        res = self.get("RiskResult", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def account_risk(self, params, body):
        res = self.json("AccountRisk", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def mobile_status(self, params, body):
        res = self.json("MobileStatus", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def element_verify(self, params, body):
        res = self.json("ElementVerify", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def mobile_status_v2(self, params, body):
        res = self.json("MobileStatusV2", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def element_verify_v2(self, params, body):
        res = self.json("ElementVerifyV2", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json