# coding:utf-8
import json
import threading

from volc.ApiInfo import ApiInfo
from volc.Credentials import Credentials
from volc.base.Service import Service
from volc.ServiceInfo import ServiceInfo


class VisualService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(VisualService, "_instance"):
            with VisualService._instance_lock:
                if not hasattr(VisualService, "_instance"):
                    VisualService._instance = object.__new__(cls)
        return VisualService._instance

    def __init__(self):
        self.service_info = VisualService.get_service_info()
        self.api_info = VisualService.get_api_info()
        super(VisualService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info():
        service_info = ServiceInfo("volcengineapi-boe.byted.org", {},
                                   Credentials('', '', 'cv', 'cn-north-1'), 10, 10)
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            "JPCartoonCut": ApiInfo("POST", "/", {"Action": "JPCartoonCut", "Version": "2020-08-26"}, {}, {}),
            "JPCartoon": ApiInfo("POST", "/", {"Action": "JPCartoon", "Version": "2020-08-26"}, {}, {}),
            "IDCard": ApiInfo("POST", "/", {"Action": "IDCard", "Version": "2020-08-26"}, {}, {}),
            "FaceSwap": ApiInfo("POST", "/", {"Action": "FaceSwap", "Version": "2020-08-26"}, {}, {}),
            "OCRNormal": ApiInfo("POST", "/", {"Action": "OCRNormal", "Version": "2020-08-26"}, {}, {}),
            "BankCard": ApiInfo("POST", "/", {"Action": "BankCard", "Version": "2020-08-26"}, {}, {}),
        }
        return api_info

    def jpcartoon_cut(self, form):
        params = dict()
        try:
            res = self.post("JPCartoonCut", params, form)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            res = str(e)
            try:
                res_json = json.loads(res)
                return res_json
            except:
                raise Exception(e)

    def jpcartoon(self, form):
        params = dict()
        try:
            res = self.post("JPCartoon", params, form)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            res = str(e)
            try:
                res_json = json.loads(res)
                return res_json
            except:
                raise Exception(e)

    def id_card(self, form):
        params = dict()
        try:
            res = self.post("IDCard", params, form)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            res = str(e)
            try:
                res_json = json.loads(res)
                return res_json
            except:
                raise Exception(e)

    def face_swap(self, form):
        params = dict()
        try:
            res = self.post("FaceSwap", params, form)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            res = str(e)
            try:
                res_json = json.loads(res)
                return res_json
            except:
                raise Exception(e)

    def ocr_normal(self, form):
        params = dict()
        try:
            res = self.post("OCRNormal", params, form)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            res = str(e)
            try:
                res_json = json.loads(res)
                return res_json
            except:
                raise Exception(e)

    def bank_card(self, form):
        params = dict()
        try:
            res = self.post("BankCard", params, form)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            res = str(e)
            try:
                res_json = json.loads(res)
                return res_json
            except:
                raise Exception(e)
