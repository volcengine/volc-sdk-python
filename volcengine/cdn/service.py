#  -*- coding: utf-8 -*-
import json
import threading

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo

GET = "GET"
POST = "POST"
SERVICE_VERSION = "2021-03-01"

service_info_map = {
    "cn-north-1": ServiceInfo("cdn.volcengineapi.com", {'accept': 'application/json', },
                              Credentials('', '', "CDN", "cn-north-1"), 60 * 5, 60 * 5, "https"),
}

api_info = {
    # 添加加速域名: https://www.volcengine.com/docs/6454/97340
    "AddCdnDomain": ApiInfo("POST", "/", {
        "Action": "AddCdnDomain", "Version": SERVICE_VERSION}, {}, {}),

    # 上线加速域名: https://www.volcengine.com/docs/6454/74667
    "StartCdnDomain": ApiInfo("POST", "/", {
        "Action": "StartCdnDomain", "Version": SERVICE_VERSION}, {}, {}),

    # 下线加速域名: https://www.volcengine.com/docs/6454/75129
    "StopCdnDomain": ApiInfo("POST", "/", {
        "Action": "StopCdnDomain", "Version": SERVICE_VERSION}, {}, {}),

    # 删除加速域名: https://www.volcengine.com/docs/6454/75130
    "DeleteCdnDomain": ApiInfo("POST", "/", {
        "Action": "DeleteCdnDomain", "Version": SERVICE_VERSION}, {}, {}),

    # 获取域名列表: https://www.volcengine.com/docs/6454/75269
    "ListCdnDomains": ApiInfo("POST", "/", {
        "Action": "ListCdnDomains", "Version": SERVICE_VERSION}, {}, {}),

    # 获取域名配置详情: https://www.volcengine.com/docs/6454/80320
    "DescribeCdnConfig": ApiInfo("POST", "/", {
        "Action": "DescribeCdnConfig", "Version": SERVICE_VERSION}, {}, {}),

    # 修改加速域名配置: https://www.volcengine.com/docs/6454/97266
    "UpdateCdnConfig": ApiInfo("POST", "/", {
        "Action": "UpdateCdnConfig", "Version": SERVICE_VERSION}, {}, {}),

    # 获取访问统计的细分数据: https://www.volcengine.com/docs/6454/70442
    "DescribeCdnData": ApiInfo("POST", "/", {
        "Action": "DescribeCdnData", "Version": SERVICE_VERSION}, {}, {}),

    # 获取访问统计的汇总数据: https://www.volcengine.com/docs/6454/96132
    "DescribeEdgeNrtDataSummary": ApiInfo("POST", "/", {
        "Action": "DescribeEdgeNrtDataSummary", "Version": SERVICE_VERSION}, {}, {}),

    # 获取回源统计的细分数据: https://www.volcengine.com/docs/6454/70443
    "DescribeCdnOriginData": ApiInfo("POST", "/", {
        "Action": "DescribeCdnOriginData", "Version": SERVICE_VERSION}, {}, {}),

    # 获取回源统计的汇总数据: https://www.volcengine.com/docs/6454/96133
    "DescribeOriginNrtDataSummary": ApiInfo("POST", "/", {
        "Action": "DescribeOriginNrtDataSummary", "Version": SERVICE_VERSION}, {}, {}),

    # 获取省份运营商的细分数据: https://www.volcengine.com/docs/6454/75159
    "DescribeCdnDataDetail": ApiInfo("POST", "/", {
        "Action": "DescribeCdnDataDetail", "Version": SERVICE_VERSION}, {}, {}),

    # 获取多个域名的省份和运营商的细分数据: https://www.volcengine.com/docs/6454/145577
    "DescribeDistrictIspData": ApiInfo("POST", "/", {
        "Action": "DescribeDistrictIspData", "Version": SERVICE_VERSION}, {}, {}),

    # 获取独立访客的细分数据: https://www.volcengine.com/docs/6454/79321
    "DescribeEdgeStatisticalData": ApiInfo("POST", "/", {
        "Action": "DescribeEdgeStatisticalData", "Version": SERVICE_VERSION}, {}, {}),

    # 获取访问统计的排行数据: https://www.volcengine.com/docs/6454/96145
    "DescribeEdgeTopNrtData": ApiInfo("POST", "/", {
        "Action": "DescribeEdgeTopNrtData", "Version": SERVICE_VERSION}, {}, {}),

    # 获取回源数据的统计排序: https://www.volcengine.com/docs/6454/104892
    "DescribeOriginTopNrtData": ApiInfo("POST", "/", {
        "Action": "DescribeOriginTopNrtData", "Version": SERVICE_VERSION}, {}, {}),

    # 获取访问状态码的统计排序: https://www.volcengine.com/docs/6454/104888
    "DescribeEdgeTopStatusCode": ApiInfo("POST", "/", {
        "Action": "DescribeEdgeTopStatusCode", "Version": SERVICE_VERSION}, {}, {}),

    # 获取回源状态码的统计排序: https://www.volcengine.com/docs/6454/104891
    "DescribeOriginTopStatusCode": ApiInfo("POST", "/", {
        "Action": "DescribeOriginTopStatusCode", "Version": SERVICE_VERSION}, {}, {}),

    # 获取热点及访客排行数据: https://www.volcengine.com/docs/6454/79322
    "DescribeEdgeTopStatisticalData": ApiInfo("POST", "/", {
        "Action": "DescribeEdgeTopStatisticalData", "Version": SERVICE_VERSION}, {}, {}),

    # 获取区域和 ISP 列表: https://www.volcengine.com/docs/6454/70445
    "DescribeCdnRegionAndIsp": ApiInfo("POST", "/", {
        "Action": "DescribeCdnRegionAndIsp", "Version": SERVICE_VERSION}, {}, {}),

    # 获取服务相关信息: https://www.volcengine.com/docs/6454/78999
    "DescribeCdnService": ApiInfo("POST", "/", {
        "Action": "DescribeCdnService", "Version": SERVICE_VERSION}, {}, {}),

    # 获取计费指标的细分数据: https://www.volcengine.com/docs/6454/96167
    "DescribeAccountingData": ApiInfo("POST", "/", {
        "Action": "DescribeAccountingData", "Version": SERVICE_VERSION}, {}, {}),

    # 提交刷新任务: https://www.volcengine.com/docs/6454/70438
    "SubmitRefreshTask": ApiInfo("POST", "/", {
        "Action": "SubmitRefreshTask", "Version": SERVICE_VERSION}, {}, {}),

    # 提交预热任务: https://www.volcengine.com/docs/6454/70436
    "SubmitPreloadTask": ApiInfo("POST", "/", {
        "Action": "SubmitPreloadTask", "Version": SERVICE_VERSION}, {}, {}),

    # 获取刷新预热任务信息: https://www.volcengine.com/docs/6454/70437
    "DescribeContentTasks": ApiInfo("POST", "/", {
        "Action": "DescribeContentTasks", "Version": SERVICE_VERSION}, {}, {}),

    # 获取刷新预热配额信息: https://www.volcengine.com/docs/6454/70439
    "DescribeContentQuota": ApiInfo("POST", "/", {
        "Action": "DescribeContentQuota", "Version": SERVICE_VERSION}, {}, {}),

    # 提交封禁任务: https://www.volcengine.com/docs/6454/79890
    "SubmitBlockTask": ApiInfo("POST", "/", {
        "Action": "SubmitBlockTask", "Version": SERVICE_VERSION}, {}, {}),

    # 提交解封任务: https://www.volcengine.com/docs/6454/79893
    "SubmitUnblockTask": ApiInfo("POST", "/", {
        "Action": "SubmitUnblockTask", "Version": SERVICE_VERSION}, {}, {}),

    # 获取封禁解封任务信息: https://www.volcengine.com/docs/6454/79906
    "DescribeContentBlockTasks": ApiInfo("POST", "/", {
        "Action": "DescribeContentBlockTasks", "Version": SERVICE_VERSION}, {}, {}),

    # 获取访问日志下载链接: https://www.volcengine.com/docs/6454/70446
    "DescribeCdnAccessLog": ApiInfo("POST", "/", {
        "Action": "DescribeCdnAccessLog", "Version": SERVICE_VERSION}, {}, {}),

    # 获取 IP 归属信息: https://www.volcengine.com/docs/6454/75233
    "DescribeIPInfo": ApiInfo("POST", "/", {
        "Action": "DescribeIPInfo", "Version": SERVICE_VERSION}, {}, {}),

    # 批量获取 IP 归属信息: https://www.volcengine.com/docs/6454/106852
    "DescribeIPListInfo": ApiInfo("POST", "/", {
        "Action": "DescribeIPListInfo", "Version": SERVICE_VERSION}, {}, {}),

    # 获取回源节点 IP 列表: https://www.volcengine.com/docs/6454/75273
    "DescribeCdnUpperIp": ApiInfo("POST", "/", {
        "Action": "DescribeCdnUpperIp", "Version": SERVICE_VERSION}, {}, {}),

    # 添加资源标签: https://www.volcengine.com/docs/6454/80308
    "AddResourceTags": ApiInfo("POST", "/", {
        "Action": "AddResourceTags", "Version": SERVICE_VERSION}, {}, {}),

    # 更新资源标签: https://www.volcengine.com/docs/6454/80313
    "UpdateResourceTags": ApiInfo("POST", "/", {
        "Action": "UpdateResourceTags", "Version": SERVICE_VERSION}, {}, {}),

    # 查询标签清单: https://www.volcengine.com/docs/6454/80315
    "ListResourceTags": ApiInfo("POST", "/", {
        "Action": "ListResourceTags", "Version": SERVICE_VERSION}, {}, {}),

    # 删除资源标签: https://www.volcengine.com/docs/6454/80316
    "DeleteResourceTags": ApiInfo("POST", "/", {
        "Action": "DeleteResourceTags", "Version": SERVICE_VERSION}, {}, {}),

    # 上传证书: https://www.volcengine.com/docs/6454/125708
    "AddCdnCertificate": ApiInfo("POST", "/", {
        "Action": "AddCdnCertificate", "Version": SERVICE_VERSION}, {}, {}),

    # 查询CDN证书列表: https://www.volcengine.com/docs/6454/125709
    "ListCertInfo": ApiInfo("POST", "/", {
        "Action": "ListCertInfo", "Version": SERVICE_VERSION}, {}, {}),

    # 查询CDN有关联域名的证书列表: https://www.volcengine.com/docs/6454/125710
    "ListCdnCertInfo": ApiInfo("POST", "/", {
        "Action": "ListCdnCertInfo", "Version": SERVICE_VERSION}, {}, {}),

    # 获取特定证书的域名关联信息: https://www.volcengine.com/docs/6454/125711
    "DescribeCertConfig": ApiInfo("POST", "/", {
        "Action": "DescribeCertConfig", "Version": SERVICE_VERSION}, {}, {}),

    # 批量关联证书: https://www.volcengine.com/docs/6454/125712
    "BatchDeployCert": ApiInfo("POST", "/", {
        "Action": "BatchDeployCert", "Version": SERVICE_VERSION}, {}, {}),

    # 删除托管在内容分发网络的证书: https://www.volcengine.com/docs/6454/597589
    "DeleteCdnCertificate": ApiInfo("POST", "/", {
        "Action": "DeleteCdnCertificate", "Version": SERVICE_VERSION}, {}, {}),

    # 查询计费结果数据: 
    "DescribeAccountingSummary": ApiInfo("POST", "/", {
        "Action": "DescribeAccountingSummary", "Version": SERVICE_VERSION}, {}, {}),

    # 获取访问统计的细分数据: 
    "DescribeDistrictData": ApiInfo("POST", "/", {
        "Action": "DescribeDistrictData", "Version": SERVICE_VERSION}, {}, {}),

    # 获取计费区域的细分数据: 
    "DescribeEdgeData": ApiInfo("POST", "/", {
        "Action": "DescribeEdgeData", "Version": SERVICE_VERSION}, {}, {}),

    # 获取访问统计的汇总数据: 
    "DescribeDistrictSummary": ApiInfo("POST", "/", {
        "Action": "DescribeDistrictSummary", "Version": SERVICE_VERSION}, {}, {}),

    # 获取计费区域的汇总数据: 
    "DescribeEdgeSummary": ApiInfo("POST", "/", {
        "Action": "DescribeEdgeSummary", "Version": SERVICE_VERSION}, {}, {}),

    # 获取回源统计的细分数据: 
    "DescribeOriginData": ApiInfo("POST", "/", {
        "Action": "DescribeOriginData", "Version": SERVICE_VERSION}, {}, {}),

    # 获取回源统计的汇总数据: 
    "DescribeOriginSummary": ApiInfo("POST", "/", {
        "Action": "DescribeOriginSummary", "Version": SERVICE_VERSION}, {}, {}),

    # 获取独立访客的细分数据: 
    "DescribeUserData": ApiInfo("POST", "/", {
        "Action": "DescribeUserData", "Version": SERVICE_VERSION}, {}, {}),

    # 获取访问数据的统计排名: 
    "DescribeDistrictRanking": ApiInfo("POST", "/", {
        "Action": "DescribeDistrictRanking", "Version": SERVICE_VERSION}, {}, {}),

    # 获取计费区域的统计排名: 
    "DescribeEdgeRanking": ApiInfo("POST", "/", {
        "Action": "DescribeEdgeRanking", "Version": SERVICE_VERSION}, {}, {}),

    # 获取回源数据的统计排名: 
    "DescribeOriginRanking": ApiInfo("POST", "/", {
        "Action": "DescribeOriginRanking", "Version": SERVICE_VERSION}, {}, {}),

    # 获取访问状态码排名数据: 
    "DescribeEdgeStatusCodeRanking": ApiInfo("POST", "/", {
        "Action": "DescribeEdgeStatusCodeRanking", "Version": SERVICE_VERSION}, {}, {}),

    # 获取回源状态码的统计排名: 
    "DescribeOriginStatusCodeRanking": ApiInfo("POST", "/", {
        "Action": "DescribeOriginStatusCodeRanking", "Version": SERVICE_VERSION}, {}, {}),

    # 获取热门对象的统计排名: 
    "DescribeStatisticalRanking": ApiInfo("POST", "/", {
        "Action": "DescribeStatisticalRanking", "Version": SERVICE_VERSION}, {}, {}),

    # 批量更新加速域名: 
    "BatchUpdateCdnConfig": ApiInfo("POST", "/", {
        "Action": "BatchUpdateCdnConfig", "Version": SERVICE_VERSION}, {}, {}),

    # 上传证书新版: 
    "AddCertificate": ApiInfo("POST", "/", {
        "Action": "AddCertificate", "Version": SERVICE_VERSION}, {}, {}),

    # 删除用量导出任务: 
    "DeleteUsageReport": ApiInfo("POST", "/", {
        "Action": "DeleteUsageReport", "Version": SERVICE_VERSION}, {}, {}),

    # 创建用量导出任务: 
    "CreateUsageReport": ApiInfo("POST", "/", {
        "Action": "CreateUsageReport", "Version": SERVICE_VERSION}, {}, {}),

    # 获取用量导出任务列表: 
    "ListUsageReports": ApiInfo("POST", "/", {
        "Action": "ListUsageReports", "Version": SERVICE_VERSION}, {}, {}),

    # 查询全局配置: 
    "DescribeSharedConfig": ApiInfo("POST", "/", {
        "Action": "DescribeSharedConfig", "Version": SERVICE_VERSION}, {}, {}),

    # 查询全局配置列表: 
    "ListSharedConfig": ApiInfo("POST", "/", {
        "Action": "ListSharedConfig", "Version": SERVICE_VERSION}, {}, {}),

    # 删除全局配置: 
    "DeleteSharedConfig": ApiInfo("POST", "/", {
        "Action": "DeleteSharedConfig", "Version": SERVICE_VERSION}, {}, {}),

    # 修改全局配置: 
    "UpdateSharedConfig": ApiInfo("POST", "/", {
        "Action": "UpdateSharedConfig", "Version": SERVICE_VERSION}, {}, {}),

    # 新增全局配置: 
    "AddSharedConfig": ApiInfo("POST", "/", {
        "Action": "AddSharedConfig", "Version": SERVICE_VERSION}, {}, {}),

    # 接入域名校验: 
    "CheckDomain": ApiInfo("POST", "/", {
        "Action": "CheckDomain", "Version": SERVICE_VERSION}, {}, {}),

    # DNS校验信息生成: 
    "DescribeRetrieveInfo": ApiInfo("POST", "/", {
        "Action": "DescribeRetrieveInfo", "Version": SERVICE_VERSION}, {}, {}),


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
        
    @staticmethod
    def use_post():
        return POST

    @staticmethod
    def use_get():
        return GET

    def send_request(self, action, params, method=POST):
        method = str(method).upper()
        if method == 'POST':
            res = self.json(action, [], json.dumps(params))
        elif method == "GET":
            self.get_api_info()[action].method = self.use_get()
            res = self.request(action, params, json.dumps({}))
            self.get_api_info()[action].method = self.use_post()
        else:
            raise Exception("not support method %s" % method)
        return res

    def add_cdn_domain(self, params=None):
        if params is None:
            params = {}
        action = "AddCdnDomain"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def start_cdn_domain(self, params=None):
        if params is None:
            params = {}
        action = "StartCdnDomain"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def stop_cdn_domain(self, params=None):
        if params is None:
            params = {}
        action = "StopCdnDomain"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def delete_cdn_domain(self, params=None):
        if params is None:
            params = {}
        action = "DeleteCdnDomain"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def list_cdn_domains(self, params=None, method=POST):
        if params is None:
            params = {}
        action = "ListCdnDomains"
        res = self.send_request(action, params, method)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_cdn_config(self, params=None):
        if params is None:
            params = {}
        action = "DescribeCdnConfig"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def update_cdn_config(self, params=None):
        if params is None:
            params = {}
        action = "UpdateCdnConfig"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_cdn_data(self, params=None, method=POST):
        if params is None:
            params = {}
        action = "DescribeCdnData"
        res = self.send_request(action, params, method)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_edge_nrt_data_summary(self, params=None, method=POST):
        if params is None:
            params = {}
        action = "DescribeEdgeNrtDataSummary"
        res = self.send_request(action, params, method)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_cdn_origin_data(self, params=None, method=POST):
        if params is None:
            params = {}
        action = "DescribeCdnOriginData"
        res = self.send_request(action, params, method)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_origin_nrt_data_summary(self, params=None, method=POST):
        if params is None:
            params = {}
        action = "DescribeOriginNrtDataSummary"
        res = self.send_request(action, params, method)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_cdn_data_detail(self, params=None, method=POST):
        if params is None:
            params = {}
        action = "DescribeCdnDataDetail"
        res = self.send_request(action, params, method)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_district_isp_data(self, params=None, method=POST):
        if params is None:
            params = {}
        action = "DescribeDistrictIspData"
        res = self.send_request(action, params, method)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_edge_statistical_data(self, params=None, method=POST):
        if params is None:
            params = {}
        action = "DescribeEdgeStatisticalData"
        res = self.send_request(action, params, method)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_edge_top_nrt_data(self, params=None, method=POST):
        if params is None:
            params = {}
        action = "DescribeEdgeTopNrtData"
        res = self.send_request(action, params, method)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_origin_top_nrt_data(self, params=None, method=POST):
        if params is None:
            params = {}
        action = "DescribeOriginTopNrtData"
        res = self.send_request(action, params, method)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_edge_top_status_code(self, params=None, method=POST):
        if params is None:
            params = {}
        action = "DescribeEdgeTopStatusCode"
        res = self.send_request(action, params, method)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_origin_top_status_code(self, params=None, method=POST):
        if params is None:
            params = {}
        action = "DescribeOriginTopStatusCode"
        res = self.send_request(action, params, method)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_edge_top_statistical_data(self, params=None, method=POST):
        if params is None:
            params = {}
        action = "DescribeEdgeTopStatisticalData"
        res = self.send_request(action, params, method)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_cdn_region_and_isp(self, params=None, method=POST):
        if params is None:
            params = {}
        action = "DescribeCdnRegionAndIsp"
        res = self.send_request(action, params, method)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_cdn_service(self, params=None):
        if params is None:
            params = {}
        action = "DescribeCdnService"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_accounting_data(self, params=None):
        if params is None:
            params = {}
        action = "DescribeAccountingData"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def submit_refresh_task(self, params=None):
        if params is None:
            params = {}
        action = "SubmitRefreshTask"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def submit_preload_task(self, params=None):
        if params is None:
            params = {}
        action = "SubmitPreloadTask"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_content_tasks(self, params=None):
        if params is None:
            params = {}
        action = "DescribeContentTasks"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_content_quota(self, params=None, method=POST):
        if params is None:
            params = {}
        action = "DescribeContentQuota"
        res = self.send_request(action, params, method)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def submit_block_task(self, params=None):
        if params is None:
            params = {}
        action = "SubmitBlockTask"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def submit_unblock_task(self, params=None):
        if params is None:
            params = {}
        action = "SubmitUnblockTask"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_content_block_tasks(self, params=None):
        if params is None:
            params = {}
        action = "DescribeContentBlockTasks"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_cdn_access_log(self, params=None, method=POST):
        if params is None:
            params = {}
        action = "DescribeCdnAccessLog"
        res = self.send_request(action, params, method)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_ip_info(self, params=None):
        if params is None:
            params = {}
        action = "DescribeIPInfo"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_ip_list_info(self, params=None):
        if params is None:
            params = {}
        action = "DescribeIPListInfo"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    # deprecated, use describe_ip_list_info instead
    def describe_iplist_info(self, params=None):
        return self.describe_ip_list_info(params)

    def describe_cdn_upper_ip(self, params=None):
        if params is None:
            params = {}
        action = "DescribeCdnUpperIp"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def add_resource_tags(self, params=None):
        if params is None:
            params = {}
        action = "AddResourceTags"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def update_resource_tags(self, params=None):
        if params is None:
            params = {}
        action = "UpdateResourceTags"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def list_resource_tags(self, params=None):
        if params is None:
            params = {}
        action = "ListResourceTags"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def delete_resource_tags(self, params=None):
        if params is None:
            params = {}
        action = "DeleteResourceTags"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def add_cdn_certificate(self, params=None):
        if params is None:
            params = {}
        action = "AddCdnCertificate"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def list_cert_info(self, params=None):
        if params is None:
            params = {}
        action = "ListCertInfo"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def list_cdn_cert_info(self, params=None):
        if params is None:
            params = {}
        action = "ListCdnCertInfo"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_cert_config(self, params=None):
        if params is None:
            params = {}
        action = "DescribeCertConfig"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def batch_deploy_cert(self, params=None):
        if params is None:
            params = {}
        action = "BatchDeployCert"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def delete_cdn_certificate(self, params=None):
        if params is None:
            params = {}
        action = "DeleteCdnCertificate"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_accounting_summary(self, params=None):
        if params is None:
            params = {}
        action = "DescribeAccountingSummary"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_district_data(self, params=None):
        if params is None:
            params = {}
        action = "DescribeDistrictData"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_edge_data(self, params=None):
        if params is None:
            params = {}
        action = "DescribeEdgeData"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_district_summary(self, params=None):
        if params is None:
            params = {}
        action = "DescribeDistrictSummary"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_edge_summary(self, params=None):
        if params is None:
            params = {}
        action = "DescribeEdgeSummary"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_origin_data(self, params=None):
        if params is None:
            params = {}
        action = "DescribeOriginData"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_origin_summary(self, params=None):
        if params is None:
            params = {}
        action = "DescribeOriginSummary"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_user_data(self, params=None):
        if params is None:
            params = {}
        action = "DescribeUserData"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_district_ranking(self, params=None):
        if params is None:
            params = {}
        action = "DescribeDistrictRanking"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_edge_ranking(self, params=None):
        if params is None:
            params = {}
        action = "DescribeEdgeRanking"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_origin_ranking(self, params=None):
        if params is None:
            params = {}
        action = "DescribeOriginRanking"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_edge_status_code_ranking(self, params=None):
        if params is None:
            params = {}
        action = "DescribeEdgeStatusCodeRanking"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_origin_status_code_ranking(self, params=None):
        if params is None:
            params = {}
        action = "DescribeOriginStatusCodeRanking"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_statistical_ranking(self, params=None):
        if params is None:
            params = {}
        action = "DescribeStatisticalRanking"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def batch_update_cdn_config(self, params=None):
        if params is None:
            params = {}
        action = "BatchUpdateCdnConfig"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def add_certificate(self, params=None):
        if params is None:
            params = {}
        action = "AddCertificate"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def delete_usage_report(self, params=None):
        if params is None:
            params = {}
        action = "DeleteUsageReport"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def create_usage_report(self, params=None):
        if params is None:
            params = {}
        action = "CreateUsageReport"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def list_usage_reports(self, params=None):
        if params is None:
            params = {}
        action = "ListUsageReports"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_shared_config(self, params=None):
        if params is None:
            params = {}
        action = "DescribeSharedConfig"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def list_shared_config(self, params=None):
        if params is None:
            params = {}
        action = "ListSharedConfig"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def delete_shared_config(self, params=None):
        if params is None:
            params = {}
        action = "DeleteSharedConfig"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def update_shared_config(self, params=None):
        if params is None:
            params = {}
        action = "UpdateSharedConfig"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def add_shared_config(self, params=None):
        if params is None:
            params = {}
        action = "AddSharedConfig"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def check_domain(self, params=None):
        if params is None:
            params = {}
        action = "CheckDomain"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_retrieve_info(self, params=None):
        if params is None:
            params = {}
        action = "DescribeRetrieveInfo"
        res = self.send_request(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json
