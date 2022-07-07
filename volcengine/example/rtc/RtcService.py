# coding:utf-8
import json
import threading

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo


class RtcService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(RtcService, "_instance"):
            with RtcService._instance_lock:
                if not hasattr(RtcService, "_instance"):
                    RtcService._instance = object.__new__(cls)
        return RtcService._instance

    def __init__(self):
        self.service_info = RtcService.get_service_info()
        self.api_info = RtcService.get_api_info()
        super(RtcService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info():
        service_info = ServiceInfo("rtc.volcengineapi.com", {'Accept': 'application/json'},
                                   Credentials('', '', 'rtc', 'cn-north-1'), 5, 5)
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            "ListRoomInformation": ApiInfo(
                "GET", "/", {"Action": "ListRoomInformation", "Version": "2020-12-01"}, {}, {}
            ),
            "ListIndicators": ApiInfo("POST", "/", {"Action": "ListIndicators", "Version": "2020-12-01"}, {}, {}),
        }
        return api_info

    def list_room_information(self, params):
        res = self.get("ListRoomInformation", params)
        if res == '':
            raise Exception("ListRoomInformation: empty response")
        res_json = json.loads(res)
        return res_json

    def list_indicators(self, body):
        res = self.json("ListIndicators", {}, body)
        if res == '':
            raise Exception("ListIndicators: empty response")
        res_json = json.loads(res)
        return res_json
