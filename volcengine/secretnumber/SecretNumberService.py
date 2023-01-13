# coding:utf-8
import json
import threading

from retry import retry

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service


class SecretNumberService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(SecretNumberService, "_instance"):
            with SecretNumberService._instance_lock:
                if not hasattr(SecretNumberService, "_instance"):
                    SecretNumberService._instance = object.__new__(cls)
        return SecretNumberService._instance

    def __init__(self, region='cn-north-1'):
        self.service_info = SecretNumberService.get_service_info(region)
        self.api_info = SecretNumberService.get_api_info()
        self.domain_cache = {}
        self.fallback_domain_weights = {}
        self.update_interval = 10
        self.lock = threading.Lock()
        super(SecretNumberService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(region):
        service_info_map = {
            'cn-north-1': ServiceInfo("cloud-vms.volcengineapi.com", {'Accept': 'application/json'},
                                      Credentials('', '', 'volc_secret_number', 'cn-north-1'), 10, 10),
        }
        service_info = service_info_map.get(region, None)
        if not service_info:
            raise Exception('Cant find the region, please check it carefully')

        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            "BindAXB": ApiInfo("POST", "/", {"Action": "BindAXB", "Version": "2020-09-01"}, {}, {}),
            "SelectNumberAndBindAXB": ApiInfo("POST", "/",
                                              {"Action": "SelectNumberAndBindAXB", "Version": "2020-09-01"}, {}, {}),
            "UnbindAXB": ApiInfo("POST", "/", {"Action": "UnbindAXB", "Version": "2020-09-01"}, {}, {}),
            "QuerySubscription": ApiInfo("POST", "/", {"Action": "QuerySubscription", "Version": "2020-09-01"}, {}, {}),
            "QuerySubscriptionForList": ApiInfo("POST", "/",
                                                {"Action": "QuerySubscriptionForList", "Version": "2020-09-01"}, {},
                                                {}),
            "UpgradeAXToAXB": ApiInfo("POST", "/", {"Action": "UpgradeAXToAXB", "Version": "2020-09-01"}, {}, {}),
            "UpdateAXB": ApiInfo("POST", "/", {"Action": "UpdateAXB", "Version": "2020-09-01"}, {}, {}),
            "BindAXN": ApiInfo("POST", "/", {"Action": "BindAXN", "Version": "2020-09-01"}, {}, {}),
            "UpdateAXN": ApiInfo("POST", "/", {"Action": "UpdateAXN", "Version": "2020-09-01"}, {}, {}),
            "UnbindAXN": ApiInfo("POST", "/", {"Action": "UnbindAXN", "Version": "2020-09-01"}, {}, {}),
            "SelectNumberAndBindAXN": ApiInfo("POST", "/", {"Action": "SelectNumberAndBindAXN", "Version": "2020-09-01"}, {}, {}),
            "Click2Call": ApiInfo("POST", "/", {"Action": "Click2Call", "Version": "2021-09-01"}, {}, {}),
            "CancelClick2Call": ApiInfo("POST", "/", {"Action": "CancelClick2Call", "Version": "2021-09-01"}, {}, {}),
            "Click2CallLite": ApiInfo("POST", "/", {"Action": "Click2CallLite", "Version": "2021-09-01"}, {}, {}),
            "BindAXNE": ApiInfo("POST", "/", {"Action": "BindAXNE", "Version": "2020-09-01"}, {}, {}),
            "UnbindAXNE": ApiInfo("POST", "/", {"Action": "UnbindAXNE", "Version": "2020-09-01"}, {}, {}),
            "UpdateAXNE": ApiInfo("POST", "/", {"Action": "UpdateAXNE", "Version": "2020-09-01"}, {}, {}),
            "BindAXBForAXNE": ApiInfo("POST", "/", {"Action": "BindAXBForAXNE", "Version": "2020-09-01"}, {}, {}),
            "BindAXYB": ApiInfo("POST", "/", {"Action": "BindAXYB", "Version": "2020-09-01"}, {}, {}),
            "BindYBForAXYB": ApiInfo("POST", "/", {"Action": "BindYBForAXYB", "Version": "2020-09-01"}, {}, {}),
            "UpdateAXYB": ApiInfo("POST", "/", {"Action": "UpdateAXYB", "Version": "2020-09-01"}, {}, {}),
            "UnbindAXYB": ApiInfo("POST", "/", {"Action": "UnbindAXYB", "Version": "2020-09-01"}, {}, {}),
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
