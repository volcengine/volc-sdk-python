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
            "CheckSmsVerifyCode": ApiInfo("POST", "/", {"Action": "CheckSmsVerifyCode", "Version": "2020-01-01"}, {},
                                          {}),
            "SendBatchSms": ApiInfo("POST", "/", {"Action": "SendBatchSms", "Version": "2021-01-01"}, {}, {}),
            "Conversion": ApiInfo("POST", "/", {"Action": "Conversion", "Version": "2020-01-01"}, {}, {}),
            "GetSmsTemplateAndOrderList": ApiInfo("GET", "/",
                                                  {"Action": "GetSmsTemplateAndOrderList", "Version": "2021-01-11"}, {},
                                                  {}),
            "ApplySmsTemplate": ApiInfo("POST", "/", {"Action": "ApplySmsTemplate", "Version": "2021-01-11"}, {}, {}),
            "DeleteSmsTemplate": ApiInfo("POST", "/", {"Action": "DeleteSmsTemplate", "Version": "2021-01-11"}, {}, {}),
            "GetSubAccountList": ApiInfo("GET", "/", {"Action": "GetSubAccountList", "Version": "2021-01-11"}, {}, {}),
            "GetSubAccountDetail": ApiInfo("GET", "/", {"Action": "GetSubAccountDetail", "Version": "2021-01-11"}, {},
                                           {}),
            "GetSignatureAndOrderList": ApiInfo("GET", "/",
                                                {"Action": "GetSignatureAndOrderList", "Version": "2021-01-11"}, {},
                                                {}),
            "ApplySmsSignature": ApiInfo("POST", "/", {"Action": "ApplySmsSignature", "Version": "2021-01-11"}, {}, {}),
            "DeleteSignature": ApiInfo("POST", "/", {"Action": "DeleteSignature", "Version": "2021-01-11"}, {},
                                       {}),
        }
        return api_info

    @retry(tries=2, delay=0)
    def send_sms(self, body):
        res = self.json('SendSms', {}, body)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)

        return res_json

    @retry(tries=2, delay=0)
    def send_sms_verify_code(self, body):
        res = self.json('SendSmsVerifyCode', {}, body)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)

        return res_json

    @retry(tries=2, delay=0)
    def check_sms_verify_code(self, body):
        res = self.json('CheckSmsVerifyCode', {}, body)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)

        return res_json

    @retry(tries=2, delay=0)
    def send_batch_sms(self, body):
        res = self.json('SendBatchSms', {}, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)

        return res_json

    @retry(tries=2, delay=0)
    def conversion(self, body):
        res = self.json('Conversion', {}, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)

        return res_json

    @retry(tries=2, delay=0)
    def get_sms_template_and_order_list(self, param):
        res = self.get('GetSmsTemplateAndOrderList', param)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)

        return res_json

    @retry(tries=2, delay=0)
    def apply_sms_template(self, body):
        res = self.json('ApplySmsTemplate', {}, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)

        return res_json

    @retry(tries=2, delay=0)
    def delete_sms_template(self, body):
        res = self.post('DeleteSmsTemplate', {}, body)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)

        return res_json

    @retry(tries=2, delay=0)
    def get_sub_account_list(self, param):
        res = self.get('GetSubAccountList', param)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)

        return res_json

    @retry(tries=2, delay=0)
    def get_sub_account_detail(self, param):
        res = self.get('GetSubAccountDetail', param)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)

        return res_json

    @retry(tries=2, delay=0)
    def get_signature_and_order_list(self, param):
        res = self.get('GetSignatureAndOrderList', param)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)

        return res_json

    @retry(tries=2, delay=0)
    def apply_sms_signature(self, body):
        res = self.json('ApplySmsSignature', {}, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)

        return res_json

    @retry(tries=2, delay=0)
    def delete_signature(self, body):
        res = self.json('DeleteSignature', {}, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)

        return res_json
