# coding:utf-8

from __future__ import print_function
import threading
from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service


class VodService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(VodService, "_instance"):
            with VodService._instance_lock:
                if not hasattr(VodService, "_instance"):
                    VodService._instance = object.__new__(cls)
        return VodService._instance

    def __init__(self, region='cn-north-1'):
        self.service_info = VodService.get_service_info(region)
        self.api_info = VodService.get_api_info()
        self.domain_cache = {}
        self.fallback_domain_weights = {}
        self.update_interval = 10
        self.lock = threading.Lock()
        super(VodService, self).__init__(self.service_info, self.api_info)

    # TODO 测试完毕修改回来
    @staticmethod
    def get_service_info(region):
        service_info_map = {
            # 'cn-north-1': ServiceInfo("vod.volcengineapi.com", {'Accept': 'application/json'},
            #                           Credentials('', '', 'vod', 'cn-north-1'), 5, 5),
            'cn-north-1': ServiceInfo("volcengineapi-boe.byted.org", {'Accept': 'application/json'},
                                      Credentials('', '', 'vod', 'cn-north-1'), 5, 5),
            'ap-singapore-1': ServiceInfo("vod.ap-singapore-1.volcengineapi.com", {'Accept': 'application/json'},
                                          Credentials('', '', 'vod', 'ap-singapore-1'), 5, 5),
            'us-east-1': ServiceInfo("vod.us-east-1.volcengineapi.com", {'Accept': 'application/json'},
                                     Credentials('', '', 'vod', 'us-east-1'), 5, 5),
        }
        service_info = service_info_map.get(region, None)
        if not service_info:
            raise Exception('Cant find the region, please check it carefully')

        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            "GetPlayInfo": ApiInfo("GET", "/", {"Action": "GetPlayInfo", "Version": "2020-08-01"}, {}, {}),
            "GetOriginalPlayInfo": ApiInfo("GET", "/", {"Action": "GetOriginalPlayInfo", "Version": "2020-08-01"}, {},
                                           {}),
            "RedirectPlay": ApiInfo("GET", "/", {"Action": "RedirectPlay", "Version": "2020-08-01"}, {}, {}),
            "StartWorkflow": ApiInfo("POST", "/", {"Action": "StartWorkflow", "Version": "2020-08-01"}, {}, {}),
            "UploadMediaByUrl": ApiInfo("GET", "/", {"Action": "UploadMediaByUrl", "Version": "2018-01-01"}, {}, {}),
            "ApplyUpload": ApiInfo("GET", "/", {"Action": "ApplyUpload", "Version": "2018-01-01"}, {}, {}),
            "CommitUpload": ApiInfo("POST", "/", {"Action": "CommitUpload", "Version": "2018-01-01"}, {}, {}),
            "SetVideoPublishStatus": ApiInfo("POST", "/", {"Action": "SetVideoPublishStatus", "Version": "2018-01-01"},
                                             {}, {}),
            "GetCdnDomainWeights": ApiInfo("GET", "/", {"Action": "GetCdnDomainWeights", "Version": "2019-07-01"}, {},
                                           {}),
            "ModifyVideoInfo": ApiInfo("POST", "/", {"Action": "ModifyVideoInfo", "Version": "2018-01-01"}, {}, {}),
            "UploadVideoByUrl": ApiInfo("GET", "/", {"Action": "UploadVideoByUrl", "Version": "2020-08-01"}, {}, {}),
            "QueryUploadTaskInfo": ApiInfo("GET", "/", {"Action": "QueryUploadTaskInfo", "Version": "2020-08-01"}, {},
                                           {}),
            # TODO 测试完毕后把Header去掉
            "ApplyUploadInfo": ApiInfo("GET", "/", {"Action": "ApplyUploadInfo", "Version": "2020-08-01"}, {},
                                       {"X-TT-ENV": "boe_husky_feature"}),
            "CommitUploadInfo": ApiInfo("POST", "/", {"Action": "CommitUploadInfo", "Version": "2020-08-01"}, {},
                                        {"X-TT-ENV": "boe_husky_feature"}),
        }
        return api_info
