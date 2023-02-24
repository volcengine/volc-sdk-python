# coding:utf-8
import json
import threading

from retry import retry

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service


class NumberPoolService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(NumberPoolService, "_instance"):
            with NumberPoolService._instance_lock:
                if not hasattr(NumberPoolService, "_instance"):
                    NumberPoolService._instance = object.__new__(cls)
        return NumberPoolService._instance

    def __init__(self, region='cn-north-1'):
        self.service_info = NumberPoolService.get_service_info(region)
        self.api_info = NumberPoolService.get_api_info()
        self.domain_cache = {}
        self.fallback_domain_weights = {}
        self.update_interval = 10
        self.lock = threading.Lock()
        super(NumberPoolService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(region):
        service_info_map = {
            'cn-north-1': ServiceInfo("cloud-vms.volcengineapi.com", {'Accept': 'application/json'},
                                      Credentials('', '', 'comm_number_pool', 'cn-north-1'), 10, 10),
        }
        service_info = service_info_map.get(region, None)
        if not service_info:
            raise Exception('Cant find the region, please check it carefully')

        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            "NumberPoolList": ApiInfo("POST", "/", {"Action": "NumberPoolList", "Version": "2020-09-01"}, {}, {}),
            "NumberList": ApiInfo("GET", "/", {"Action": "NumberList", "Version": "2020-09-01"}, {}, {}),
            "CreateNumberPool": ApiInfo("POST", "/", {"Action": "CreateNumberPool", "Version": "2020-09-01"}, {}, {}),
            "UpdateNumberPool": ApiInfo("POST", "/", {"Action": "UpdateNumberPool", "Version": "2020-09-01"}, {}, {}),
            "EnableOrDisableNumber": ApiInfo("POST", "/", {"Action": "EnableOrDisableNumber", "Version": "2021-01-01"}, {}, {}),
            "SelectNumber": ApiInfo("GET", "/", {"Action": "SelectNumber", "Version": "2021-01-01"}, {}, {}),

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



