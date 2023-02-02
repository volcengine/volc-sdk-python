# coding:utf-8
import json
import threading

from retry import retry

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service


class RiskService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(RiskService, "_instance"):
            with RiskService._instance_lock:
                if not hasattr(RiskService, "_instance"):
                    RiskService._instance = object.__new__(cls)
        return RiskService._instance

    def __init__(self, region='cn-north-1'):
        self.service_info = RiskService.get_service_info(region)
        self.api_info = RiskService.get_api_info()
        self.domain_cache = {}
        self.fallback_domain_weights = {}
        self.update_interval = 10
        self.lock = threading.Lock()
        super(RiskService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(region):
        service_info_map = {
            'cn-north-1': ServiceInfo("cloud-vms.volcengineapi.com", {'Accept': 'application/json'},
                                      Credentials('', '', 'volc_risk_http', 'cn-north-1'), 10, 10),
        }
        service_info = service_info_map.get(region, None)
        if not service_info:
            raise Exception('Cant find the region, please check it carefully')

        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            "QueryCanCall": ApiInfo("POST", "/", {"Action": "QueryCanCall", "Version": "2021-01-01"}, {}, {}),
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

    @retry(tries=2, delay=0)
    def query_call_call(self, form):
        try:
            return self.common_handler("QueryCanCall", form)
        except Exception as e:
            raise Exception(str(e))

