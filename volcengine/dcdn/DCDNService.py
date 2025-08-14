#  -*- coding: utf-8 -*-
import json
import threading

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo

SERVICE_VERSION = "2021-04-01"
SERVICE_VERSION_V2 = "2023-01-01"

service_info = ServiceInfo("open.volcengineapi.com", {'Accept': 'application/json'},
                           Credentials('', '', 'dcdn', 'cn-north-1'), 60 * 5, 60 * 5, "https")

api_info = {
    # 查询域名列表: https://www.volcengine.com/docs/6559/192391
    "DescribeUserDomains": ApiInfo("POST", "/", {
        "Action": "DescribeUserDomains", "Version": SERVICE_VERSION_V2}, {}, {}),
    
    # 查询全站加速域名的详细配置: https://www.volcengine.com/docs/6559/94321
    "DescribeDomainConfig": ApiInfo("POST", "/", {
        "Action": "DescribeDomainConfig", "Version": SERVICE_VERSION}, {}, {}),

    # 新增全站加速域名: https://www.volcengine.com/docs/6559/79725
    "CreateDomain": ApiInfo("POST", "/", {
        "Action": "CreateDomain", "Version": SERVICE_VERSION}, {}, {}),

    # 新增全站加速域名V2,支持识别Project: https://www.volcengine.com/docs/6559/191870
    "CreateDomainV2": ApiInfo("POST", "/", {
        "Action": "CreateDomain", "Version": SERVICE_VERSION_V2}, {}, {}),

    # 启动全站加速域名: https://www.volcengine.com/docs/6559/94320
    "StartDomain": ApiInfo("POST", "/", {
        "Action": "StartDomain", "Version": SERVICE_VERSION}, {}, {}),

    # 停止全站加速域名: https://www.volcengine.com/docs/6559/94319
    "StopDomain": ApiInfo("POST", "/", {
        "Action": "StopDomain", "Version": SERVICE_VERSION}, {}, {}),

    # 删除全站加速域名: https://www.volcengine.com/docs/6559/95181
    "DeleteDomain": ApiInfo("POST", "/", {
        "Action": "DeleteDomain", "Version": SERVICE_VERSION}, {}, {}),

    # 变更域名配置: https://www.volcengine.com/docs/6559/95183
    "UpdateDomainConfig": ApiInfo("POST", "/", {
        "Action": "UpdateDomainConfig", "Version": SERVICE_VERSION}, {}, {}),

    # 变更域名配置V2,支持识别Project: https://www.volcengine.com/docs/6559/191883
    "UpdateDomainConfigV2": ApiInfo("POST", "/", {
        "Action": "UpdateDomainConfig", "Version": SERVICE_VERSION_V2}, {}, {}),

    # 查询域名的资源用量数据: https://www.volcengine.com/docs/6559/79733
    "DescribeStatistics": ApiInfo("POST", "/", {
        "Action": "DescribeStatistics", "Version": SERVICE_VERSION}, {}, {}),

    # 查询域名的回源资源用量数据: https://www.volcengine.com/docs/6559/79734
    "DescribeOriginStatistics": ApiInfo("POST", "/", {
        "Action": "DescribeOriginStatistics", "Version": SERVICE_VERSION}, {}, {}),

    # 查询域名的实时资源用量数据: https://www.volcengine.com/docs/6559/79735
    "DescribeRealtimeData": ApiInfo("POST", "/", {
        "Action": "DescribeRealtimeData", "Version": SERVICE_VERSION}, {}, {}),

    # 查询域名的回源实时资源用量数据: https://www.volcengine.com/docs/6559/79737
    "DescribeOriginRealtimeData": ApiInfo("POST", "/", {
        "Action": "DescribeOriginRealtimeData", "Version": SERVICE_VERSION}, {}, {}),

    # 统计域名的区域分布数据: https://www.volcengine.com/docs/6559/79738
    "DescribeDomainRegionData": ApiInfo("POST", "/", {
        "Action": "DescribeDomainRegionData", "Version": SERVICE_VERSION}, {}, {}),

    # 统计域名的运营商分布数据: https://www.volcengine.com/docs/6559/79739
    "DescribeDomainIspData": ApiInfo("POST", "/", {
        "Action": "DescribeDomainIspData", "Version": SERVICE_VERSION}, {}, {}),

    # 统计域名的排行数据: https://www.volcengine.com/docs/6559/79740
    "DescribeTopDomains": ApiInfo("POST", "/", {
        "Action": "DescribeTopDomains", "Version": SERVICE_VERSION}, {}, {}),

    # 统计URL的排行数据: https://www.volcengine.com/docs/6559/79741
    "DescribeTopURLs": ApiInfo("POST", "/", {
        "Action": "DescribeTopURLs", "Version": SERVICE_VERSION}, {}, {}),

    # 统计IP的排行数据: https://www.volcengine.com/docs/6559/79742
    "DescribeTopIPs": ApiInfo("POST", "/", {
        "Action": "DescribeTopIPs", "Version": SERVICE_VERSION}, {}, {}),

    # 统计Referer的排行数据: https://www.volcengine.com/docs/6559/79743
    "DescribeTopReferers": ApiInfo("POST", "/", {
        "Action": "DescribeTopReferers", "Version": SERVICE_VERSION}, {}, {}),

    # 查询域名的PV数据: https://www.volcengine.com/docs/6559/79747
    "DescribeDomainPVData": ApiInfo("POST", "/", {
        "Action": "DescribeDomainPVData", "Version": SERVICE_VERSION}, {}, {}),

    # 查询域名的UV数据: https://www.volcengine.com/docs/6559/79749
    "DescribeDomainUVData": ApiInfo("POST", "/", {
        "Action": "DescribeDomainUVData", "Version": SERVICE_VERSION}, {}, {}),

    # 查询地域和运营商信息: https://www.volcengine.com/docs/6559/126042
    "DescribeDcdnRegionAndIsp": ApiInfo("GET", "/", {
        "Action": "DescribeDcdnRegionAndIsp", "Version": SERVICE_VERSION}, {}, {}),

    # 查询访问资源用量细节: https://www.volcengine.com/docs/6559/131240
    "DescribeStatisticsDetail": ApiInfo("POST", "/", {
        "Action": "DescribeStatisticsDetail", "Version": SERVICE_VERSION}, {}, {}),

    # 查询访问回源资源用量细节: https://www.volcengine.com/docs/6559/131253
    "DescribeOriginStatisticsDetail": ApiInfo("POST", "/", {
        "Action": "DescribeOriginStatisticsDetail", "Version": SERVICE_VERSION}, {}, {}),

    # 查询访问日志: https://www.volcengine.com/docs/6559/79745
    "DescribeDomainLogs": ApiInfo("POST", "/", {
        "Action": "DescribeDomainLogs", "Version": SERVICE_VERSION}, {}, {}),

    # 新增全站加速预热刷新任务: https://www.volcengine.com/docs/6559/102400
    "CreatePurgePrefetchTask": ApiInfo("POST", "/", {
        "Action": "CreatePurgePrefetchTask", "Version": SERVICE_VERSION}, {}, {}),

    # 查询全站加速预热刷新任务: https://www.volcengine.com/docs/6559/102401
    "CheckPurgePrefetchTask": ApiInfo("POST", "/", {
        "Action": "CheckPurgePrefetchTask", "Version": SERVICE_VERSION}, {}, {}),

    # 查询全站加速预热刷新任务Quota: https://www.volcengine.com/docs/6559/102402
    "GetPurgePrefetchTaskQuota": ApiInfo("GET", "/", {
        "Action": "GetPurgePrefetchTaskQuota", "Version": SERVICE_VERSION}, {}, {}),

    # 查询全站加速预热刷新任务Quota: https://www.volcengine.com/docs/6559/102403
    "RetryPurgePrefetchTask": ApiInfo("POST", "/", {
        "Action": "RetryPurgePrefetchTask", "Version": SERVICE_VERSION}, {}, {}),

    # 更新全站加速域名拨测配置:
    "UpdateDomainProbeSetting": ApiInfo("POST", "/", {
        "Action": "UpdateDomainProbeSetting", "Version": SERVICE_VERSION}, {}, {}),

    # 查询全站加速域名拨测配置:
    "DescribeDomainProbeSetting": ApiInfo("POST", "/", {
        "Action": "DescribeDomainProbeSetting", "Version": SERVICE_VERSION}, {}, {}),

    # 获取边缘层节点的所有 IP:
    "DescribeDcdnEdgeIp": ApiInfo("POST", "/", {
        "Action": "DescribeDcdnEdgeIp", "Version": SERVICE_VERSION}, {}, {}),

    # 查询封禁IP
    "DescribeBlockIP": ApiInfo("POST", "/", {
        "Action": "DescribeBlockIP", "Version": SERVICE_VERSION}, {}, {}),

    # 海量IP封禁
    "BatchBlockIP":  ApiInfo("POST", "/", {
        "Action": "BatchBlockIP", "Version": SERVICE_VERSION}, {}, {}),

    "DescribeDcdnOriginIp": ApiInfo("POST", "/", {
        "Action": "DescribeDcdnOriginIp", "Version": SERVICE_VERSION}, {}, {}),

    "DescribeL2IPs": ApiInfo("POST", "/", {
        "Action": "DescribeL2IPs", "Version": SERVICE_VERSION}, {}, {}),

    # 查询域名归属验证信息: https://www.volcengine.com/docs/6559/1339302
    "DescribeVerifyContent": ApiInfo("GET", "/", {
        "Action": "DescribeVerifyContent", "Version": SERVICE_VERSION}, {}, {}),

    # 验证域名归属关系: https://www.volcengine.com/docs/6559/1339303
    "VerifyDomainOwnership": ApiInfo("POST", "/", {
        "Action": "VerifyDomainOwnership", "Version": SERVICE_VERSION}, {}, {}),
    
    # 更新GA源站的回源策略:
    "UpdateGAOriginPolicy": ApiInfo("POST", "/", {
        "Action": "UpdateGAOriginPolicy", "Version": SERVICE_VERSION}, {}, {}),
    
    # 查询GA源站的回源策略:
    "DescribeGAOriginPolicy": ApiInfo("POST", "/", {
        "Action": "DescribeGAOriginPolicy", "Version": SERVICE_VERSION}, {}, {}),

    # 查询WS的监控数据:
    "DescribeWSStatistics": ApiInfo("POST", "/", {
        "Action": "DescribeWSStatistics", "Version": SERVICE_VERSION}, {}, {}),
}


class DCDNService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(DCDNService, "_instance"):
            with DCDNService._instance_lock:
                if not hasattr(DCDNService, "_instance"):
                    DCDNService._instance = object.__new__(cls)
        return DCDNService._instance

    def __init__(self):
        self.service_info = DCDNService.get_service_info()
        self.api_info = DCDNService.get_api_info()
        super(DCDNService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info():
        return service_info

    @staticmethod
    def get_api_info():
        return api_info

    def describe_user_domains(self, params=None):
        if params is None:
            params = {}
        action = "DescribeUserDomains"
        res = self.json(action,[], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_domain_config(self, params=None):
        if params is None:
            params = {}
        action = "DescribeDomainConfig"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def create_domain(self, params=None):
        if params is None:
            params = {}
        action = "CreateDomain"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json
    
    def create_domain_v2(self, params=None):
        if params is None:
            params = {}
        action = "CreateDomainV2"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def start_domain(self, params=None):
        if params is None:
            params = {}
        action = "StartDomain"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def stop_domain(self, params=None):
        if params is None:
            params = {}
        action = "StopDomain"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def delete_domain(self, params=None):
        if params is None:
            params = {}
        action = "DeleteDomain"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def update_domain_config(self, params=None):
        if params is None:
            params = {}
        action = "UpdateDomainConfig"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json
    
    def update_domain_config_v2(self, params=None):
        if params is None:
            params = {}
        action = "UpdateDomainConfigV2"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_statistics(self, params=None):
        if params is None:
            params = {}
        action = "DescribeStatistics"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_ws_statistics(self, params=None):
        if params is None:
            params = {}
        action = "DescribeWSStatistics"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_origin_statistics(self, params=None):
        if params is None:
            params = {}
        action = "DescribeOriginStatistics"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_realtime_data(self, params=None):
        if params is None:
            params = {}
        action = "DescribeRealtimeData"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_origin_realtime_data(self, params=None):
        if params is None:
            params = {}
        action = "DescribeOriginRealtimeData"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_domain_region_data(self, params=None):
        if params is None:
            params = {}
        action = "DescribeDomainRegionData"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_domain_isp_data(self, params=None):
        if params is None:
            params = {}
        action = "DescribeDomainIspData"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_top_domains(self, params=None):
        if params is None:
            params = {}
        action = "DescribeTopDomains"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_top_urls(self, params=None):
        if params is None:
            params = {}
        action = "DescribeTopURLs"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_top_ips(self, params=None):
        if params is None:
            params = {}
        action = "DescribeTopIPs"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_top_referers(self, params=None):
        if params is None:
            params = {}
        action = "DescribeTopReferers"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_domain_pv_data(self, params=None):
        if params is None:
            params = {}
        action = "DescribeDomainPVData"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_domain_uv_data(self, params=None):
        if params is None:
            params = {}
        action = "DescribeDomainUVData"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_dcdn_region_and_isp(self, params=None):
        if params is None:
            params = {}
        action = "DescribeDcdnRegionAndIsp"
        res = self.get(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_statistics_detail(self, params=None):
        if params is None:
            params = {}
        action = "DescribeStatisticsDetail"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_origin_statistics_detail(self, params=None):
        if params is None:
            params = {}
        action = "DescribeOriginStatisticsDetail"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_domain_logs(self, params=None):
        if params is None:
            params = {}
        action = "DescribeDomainLogs"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def create_purge_prefetch_task(self, params=None):
        if params is None:
            params = {}
        action = "CreatePurgePrefetchTask"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def check_purge_prefetch_task(self, params=None):
        if params is None:
            params = {}
        action = "CheckPurgePrefetchTask"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def get_purge_prefetch_task_quota(self, params=None):
        if params is None:
            params = {}
        action = "GetPurgePrefetchTaskQuota"
        res = self.get(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def retry_purge_prefetch_task(self, params=None):
        if params is None:
            params = {}
        action = "RetryPurgePrefetchTask"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def update_domain_probe_setting(self, params=None):
        if params is None:
            params = {}
        action = "UpdateDomainProbeSetting"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_domain_probe_setting(self, params=None):
        if params is None:
            params = {}
        action = "DescribeDomainProbeSetting"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_dcdn_edge_ip(self, params=None):
        if params is None:
            params = {}
        action = "DescribeDcdnEdgeIp"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_block_ip(self, params=None):
        if params is None:
            params = {}
        action = "DescribeBlockIP"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def batch_block_ip(self, params=None):
        if params is None:
            params = {}
        action = "BatchBlockIP"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def update_ga_origin_policy(self, params=None):
        if params is None:
            params = {}
        action = "UpdateGAOriginPolicy"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_dcdn_origin_ip(self, params=None):
        if params is None:
            params = {}
        action = "DescribeDcdnOriginIp"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json
    
    def describe_ga_origin_policy(self, params=None):
        if params is None:
            params = {}
        action = "DescribeGAOriginPolicy"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_l2_ips(self, params=None):
        if params is None:
            params = {}
        action = "DescribeL2IPs"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_verify_content(self, params=None):
        if params is None:
            params = {}
        action = "DescribeVerifyContent"
        res = self.get(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def verify_domain_ownership(self, params=None):
        if params is None:
            params = {}
        action = "VerifyDomainOwnership"
        res = self.json(action, [], json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json
