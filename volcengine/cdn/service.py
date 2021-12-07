import json
import threading

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo

SERVICE_VERSION = "2021-03-01"

service_info_map = {
    "cn-north-1": ServiceInfo("cdn.volcengineapi.com", {'accept': 'application/json', },
                              Credentials('', '', "CDN", "cn-north-1"), 60, 60, "https"),
}

api_info = {
    "SubmitRefreshTask": ApiInfo("POST", "/", {"Action": "SubmitRefreshTask", "Version": SERVICE_VERSION}, {}, {}),
    "SubmitPreloadTask": ApiInfo("POST", "/", {"Action": "SubmitPreloadTask", "Version": SERVICE_VERSION}, {}, {}),
    "DescribeContentTasks": ApiInfo("POST", "/", {"Action": "DescribeContentTasks", "Version": SERVICE_VERSION}, {},
                                    {}),
    "DescribeContentQuota": ApiInfo("POST", "/", {"Action": "DescribeContentQuota", "Version": SERVICE_VERSION},
                                    {}, {}),

    "DescribeCdnData": ApiInfo("POST", "/", {"Action": "DescribeCdnData", "Version": SERVICE_VERSION}, {}, {}),

    "DescribeCdnOriginData": ApiInfo("POST", "/", {"Action": "DescribeCdnOriginData", "Version": SERVICE_VERSION}, {},
                                     {}),
    "DescribeCdnRegionAndIsp": ApiInfo("POST", "/", {"Action": "DescribeCdnRegionAndIsp", "Version": SERVICE_VERSION},
                                       {}, {}),
    "DescribeCdnDomainTopData": ApiInfo("POST", "/", {"Action": "DescribeCdnDomainTopData", "Version": SERVICE_VERSION},
                                        {}, {}),
    "DescribeCdnDataDetail": ApiInfo("POST", "/",
                                     {"Action": "DescribeCdnDataDetail", "Version": SERVICE_VERSION},
                                     {}, {}),
    "DescribeCdnAccountingData": ApiInfo("POST", "/",
                                         {"Action": "DescribeCdnAccountingData", "Version": SERVICE_VERSION},
                                         {}, {}),
    "DescribeCdnAccessLog": ApiInfo("POST", "/", {"Action": "DescribeCdnAccessLog", "Version": SERVICE_VERSION}, {},
                                    {}),
    "StartCdnDomain": ApiInfo("POST", "/", {"Action": "StartCdnDomain", "Version": SERVICE_VERSION}, {}, {}),
    "StopCdnDomain": ApiInfo("POST", "/", {"Action": "StopCdnDomain", "Version": SERVICE_VERSION}, {}, {}),
    "DeleteCdnDomain": ApiInfo("POST", "/", {"Action": "DeleteCdnDomain", "Version": SERVICE_VERSION}, {}, {}),
    "ListCdnDomains": ApiInfo("POST", "/", {"Action": "ListCdnDomains", "Version": SERVICE_VERSION}, {}, {}),
    "DescribeCdnUpperIp": ApiInfo("POST", "/", {"Action": "DescribeCdnUpperIp", "Version": SERVICE_VERSION}, {}, {}),
}


class CDNService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(CDNService, "_instance"):
            with CDNService._instance_lock:
                if not hasattr(CDNService, "_instance"):
                    CDNService._instance = object.__new__(cls)
        return CDNService._instance

    def __init__(self, region="cn-north-1"):
        self.service_info = CDNService.get_service_info(region)
        self.api_info = CDNService.get_api_info()
        super(CDNService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(region_name):
        service_info = service_info_map.get(region_name, None)
        if not service_info:
            raise Exception('do not support region %s' % region_name)
        return service_info

    @staticmethod
    def get_api_info():
        return api_info

    def submit_refresh_task(self, params):
        action = "SubmitRefreshTask"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def submit_preload_task(self, params):
        action = "SubmitPreloadTask"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_content_tasks(self, params):
        action = "DescribeContentTasks"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_content_quota(self):
        action = "DescribeContentQuota"
        res = self.json(action, [], '')
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_cdn_data(self, params):
        action = "DescribeCdnData"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_cdn_origin_data(self, params):
        action = "DescribeCdnOriginData"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_cdn_region_and_isp(self, params):
        action = "DescribeCdnRegionAndIsp"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_cdn_domain_top_data(self, params):
        action = "DescribeCdnDomainTopData"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_cdn_data_detail(self, params):
        action = "DescribeCdnDataDetail"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_cdn_accounting_data(self, params):
        action = "DescribeCdnAccountingData"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_cdn_access_log(self, params):
        action = "DescribeCdnAccessLog"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def start_cdn_domain(self, params):
        action = "StartCdnDomain"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def stop_cdn_domain(self, params):
        action = "StopCdnDomain"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def delete_cdn_domain(self, params):
        action = "DeleteCdnDomain"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def list_cdn_domains(self, params):
        action = "ListCdnDomains"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_cdn_upper_ip(self, params):
        action = "DescribeCdnUpperIp"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json
