import json
import threading


from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo
import redo
from requests import exceptions
class AdBlockService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(AdBlockService, "_instance"):
            with AdBlockService._instance_lock:
                if not hasattr(AdBlockService, "_instance"):
                    AdBlockService._instance = object.__new__(cls)
        return AdBlockService._instance

    def __init__(self):
        self.service_info = AdBlockService.get_service_info()
        self.api_info = AdBlockService.get_api_info()
        super(AdBlockService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info():
        service_info = ServiceInfo("open.volcengineapi.com", {'Accept': 'application/json'},
                                   Credentials('', '', 'AdBlocker', 'cn-north-1'), 5, 5)
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {"AdBlock": ApiInfo("POST", "/", {"Action": "AdBlock", "Version": "2021-01-06"}, {}, {})}
        return api_info

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def ad_block(self, params, body):
        res = self.json("AdBlock", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json



