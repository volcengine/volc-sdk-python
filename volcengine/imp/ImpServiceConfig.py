# coding:utf-8

from __future__ import print_function

import threading
from zlib import crc32

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service


class ImpServiceConfig(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, region='cn-north-1'):
        self.service_info = ImpServiceConfig.get_service_info(region)
        self.api_info = ImpServiceConfig.get_api_info()
        self.domain_cache = {}
        self.fallback_domain_weights = {}
        self.update_interval = 10
        self.lock = threading.Lock()
        super(ImpServiceConfig, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(region):
        service_info_map = {
            'cn-north-1': ServiceInfo("imp.volcengineapi.com", {'Accept': 'application/json'},
                                      Credentials('', '', 'imp', 'cn-north-1'), 10, 10),
        }
        service_info = service_info_map.get(region, None)
        if not service_info:
            raise Exception('Cant find the region, please check it carefully')

        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            "SubmitJob": ApiInfo("GET", "/", {"Action": "SubmitJob", "Version": "2021-06-11"}, {}, {}),
            "KillJob": ApiInfo("GET", "/", {"Action": "KillJob", "Version": "2021-06-11"}, {}, {}),
            "RetrieveJob": ApiInfo("GET", "/", {"Action": "RetrieveJob", "Version": "2021-06-11"}, {}, {}),
        }
        return api_info

    @staticmethod
    def crc32(file_path):
        prev = 0
        for eachLine in open(file_path, "rb"):
            prev = crc32(eachLine, prev)
        return prev & 0xFFFFFFFF
