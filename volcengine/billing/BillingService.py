# coding:utf-8
import json
import threading

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo

SERVICE_VERSION = "2022-01-01"

class BillingService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(BillingService, "_instance"):
            with BillingService._instance_lock:
                if not hasattr(BillingService, "_instance"):
                    BillingService._instance = object.__new__(cls)
        return BillingService._instance

    def __init__(self):
        self.service_info = BillingService.get_service_info()
        self.api_info = BillingService.get_api_info()
        super(BillingService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info():
        service_info = ServiceInfo("billing.volcengineapi.com", {'Accept': 'application/json'},
                                   Credentials('', '', 'billing', 'cn-north-1'), 5, 5)
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {"ListBill": ApiInfo("POST", "/", {"Action": "ListBill", "Version": SERVICE_VERSION}, {}, {}),
                    "ListBillDetail": ApiInfo("POST", "/", {"Action": "ListBillDetail", "Version": SERVICE_VERSION}, {}, {}),
                    "ListBillOverviewByProd": ApiInfo("POST", "/", {"Action": "ListBillOverviewByProd", "Version": SERVICE_VERSION}, {}, {}),
                    "ListSplitBillDetail": ApiInfo("POST", "/", {"Action": "ListSplitBillDetail", "Version": SERVICE_VERSION}, {}, {}),
                    "ListAmortizedCostBillDetail": ApiInfo("POST", "/", {"Action": "ListAmortizedCostBillDetail", "Version": SERVICE_VERSION}, {}, {}),
                    "ListAmortizedCostBillMonthly": ApiInfo("POST", "/", {"Action": "ListAmortizedCostBillMonthly", "Version": SERVICE_VERSION}, {}, {})}
        return api_info

    def list_bill(self, params, body):
        res = self.post("ListBill", params, body)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def list_bill_detail(self, params, body):
        res = self.post("ListBillDetail", params, body)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def list_bill_overview_by_prod(self, params, body):
        res = self.post("ListBillOverviewByProd", params, body)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def list_split_bill_detail(self, params, body):
        res = self.post("ListSplitBillDetail", params, body)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def list_amortized_cost_bill_detail(self, params, body):
        res = self.post("ListAmortizedCostBillDetail", params, body)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def list_amortized_cost_bill_monthly(self, params, body):
        res = self.post("ListAmortizedCostBillMonthly", params, body)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
