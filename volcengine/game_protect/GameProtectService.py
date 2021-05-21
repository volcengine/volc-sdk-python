import json
import threading


from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo
import redo
from requests import exceptions
class GameProtectService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(GameProtectService, "_instance"):
            with GameProtectService._instance_lock:
                if not hasattr(GameProtectService, "_instance"):
                    GameProtectService._instance = object.__new__(cls)
        return GameProtectService._instance

    def __init__(self):
        self.service_info = GameProtectService.get_service_info()
        self.api_info = GameProtectService.get_api_info()
        super(GameProtectService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info():
        service_info = ServiceInfo("open.volcengineapi.com", {'Accept': 'application/json'},
                                   Credentials('', '', 'game_protect', 'cn-north-1'), 5, 5)
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {"RiskResult": ApiInfo("GET", "/", {"Action": "RiskResult", "Version": "2021-04-25"}, {}, {})}
        return api_info

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def risk_result(self, params, body):
        params['Service'] = 'anti_plugin'
        res = self.get("RiskResult", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json



