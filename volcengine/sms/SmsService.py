# coding:utf-8
import json
import threading

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo
from volcengine.const.Const import *
from retry import retry


class SmsService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(SmsService, "_instance"):
            with SmsService._instance_lock:
                if not hasattr(SmsService, "_instance"):
                    SmsService._instance = object.__new__(cls)
        return SmsService._instance

    def __init__(self, region=REGION_CN_NORTH1):
        self.service_info = SmsService.get_service_info(self, region)
        self.api_info = SmsService.get_api_info()
        super(SmsService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(self, region):
        if region == REGION_AP_SINGAPORE1:
            service_info = ServiceInfo("sms.byteplusapi.com", {'Accept': 'application/json'},
                                       Credentials('', '', 'volcSMS', region), 5, 5)
        else:
            service_info = ServiceInfo("sms.volcengineapi.com", {'Accept': 'application/json'},
                                       Credentials('', '', 'volcSMS', region), 5, 5)
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            "SendSms": ApiInfo("POST", "/", {"Action": "SendSms", "Version": "2020-01-01"}, {}, {}),
            "SendSmsVerifyCode": ApiInfo("POST", "/", {"Action": "SendSmsVerifyCode", "Version": "2020-01-01"}, {}, {}),
            "CheckSmsVerifyCode": ApiInfo("POST", "/", {"Action": "CheckSmsVerifyCode", "Version": "2020-01-01"}, {}, {}),
        }
        return api_info

    @retry(tries=2, delay=0)
    def send_sms(self, body):
        res = self.json('SendSms', {}, body)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)

        return res_json

    def send_sms_verify_code(self, body):
        res = self.json('SendSmsVerifyCode', {}, body)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)

        return res_json

    def check_sms_verify_code(self, body):
        res = self.json('CheckSmsVerifyCode', {}, body)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)

        return res_json