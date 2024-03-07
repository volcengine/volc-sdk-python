#  -*- coding: utf-8 -*-
import json
import threading

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo

SERVICE_VERSION = "2021-04-30"

service_info_map = {
    "cn-north-1": ServiceInfo("veenedge.volcengineapi.com", {'accept': 'application/json', },
                              Credentials('', '', "veenedge", "cn-north-1"), 60 * 5, 60 * 5, "https"),
}

api_info = {
    # 创建边缘服务: https://www.volcengine.com/docs/6499/76856
    "CreateCloudServer": ApiInfo("POST", "/", {
        "Action": "CreateCloudServer", "Version": SERVICE_VERSION}, {}, {}),

    # 获取边缘服务列表: https://www.volcengine.com/docs/6499/76857
    "ListCloudServers": ApiInfo("GET", "/", {
        "Action": "ListCloudServers", "Version": SERVICE_VERSION}, {}, {}),

    # 获取边缘服务详情: https://www.volcengine.com/docs/6499/76858
    "GetCloudServer": ApiInfo("GET", "/", {
        "Action": "GetCloudServer", "Version": SERVICE_VERSION}, {}, {}),

    # 启动边缘服务: https://www.volcengine.com/docs/6499/81036
    "StartCloudServer": ApiInfo("POST", "/", {
        "Action": "StartCloudServer", "Version": SERVICE_VERSION}, {}, {}),

    # 停止边缘服务: https://www.volcengine.com/docs/6499/81035
    "StopCloudServer": ApiInfo("POST", "/", {
        "Action": "StopCloudServer", "Version": SERVICE_VERSION}, {}, {}),

    # 重启边缘服务: https://www.volcengine.com/docs/6499/81037
    "RebootCloudServer": ApiInfo("POST", "/", {
        "Action": "RebootCloudServer", "Version": SERVICE_VERSION}, {}, {}),

    # 删除边缘服务: https://www.volcengine.com/docs/6499/76859
    "DeleteCloudServer": ApiInfo("POST", "/", {
        "Action": "DeleteCloudServer", "Version": SERVICE_VERSION}, {}, {}),

    # 获取可开通的实例规格: https://www.volcengine.com/docs/6499/76860
    "ListInstanceTypes": ApiInfo("GET", "/", {
        "Action": "ListInstanceTypes", "Version": SERVICE_VERSION}, {}, {}),

    # 获取支持的区域和运营商: https://www.volcengine.com/docs/6499/76861
    "ListAvailableResourceInfo": ApiInfo("GET", "/", {
        "Action": "ListAvailableResourceInfo", "Version": SERVICE_VERSION}, {}, {}),

    # 新增边缘实例: https://www.volcengine.com/docs/6499/76863
    "CreateInstance": ApiInfo("POST", "/", {
        "Action": "CreateInstance", "Version": SERVICE_VERSION}, {}, {}),

    # 获取边缘实例列表: https://www.volcengine.com/docs/6499/76862
    "ListInstances": ApiInfo("GET", "/", {
        "Action": "ListInstances", "Version": SERVICE_VERSION}, {}, {}),

    # 获取边缘实例详情: https://www.volcengine.com/docs/6499/76865
    "GetInstance": ApiInfo("GET", "/", {
        "Action": "GetInstance", "Version": SERVICE_VERSION}, {}, {}),

    # 启动边缘实例: https://www.volcengine.com/docs/6499/76868
    "StartInstances": ApiInfo("POST", "/", {
        "Action": "StartInstances", "Version": SERVICE_VERSION}, {}, {}),

    # 停止边缘实例: https://www.volcengine.com/docs/6499/76866
    "StopInstances": ApiInfo("POST", "/", {
        "Action": "StopInstances", "Version": SERVICE_VERSION}, {}, {}),

    # 重启边缘实例: https://www.volcengine.com/docs/6499/76864
    "RebootInstances": ApiInfo("POST", "/", {
        "Action": "RebootInstances", "Version": SERVICE_VERSION}, {}, {}),

    # 删除边缘实例: https://www.volcengine.com/docs/6499/81039
    "OfflineInstances": ApiInfo("POST", "/", {
        "Action": "OfflineInstances", "Version": SERVICE_VERSION}, {}, {}),

    # 编辑边缘实例名称: https://www.volcengine.com/docs/6499/76867
    "SetInstanceName": ApiInfo("POST", "/", {
        "Action": "SetInstanceName", "Version": SERVICE_VERSION}, {}, {}),

    # 重置边缘实例密码: https://www.volcengine.com/docs/6499/76869
    "ResetLoginCredential": ApiInfo("POST", "/", {
        "Action": "ResetLoginCredential", "Version": SERVICE_VERSION}, {}, {}),

    # 获取实例云盘信息: https://www.volcengine.com/docs/6499/174016
    "GetInstanceCloudDiskInfo": ApiInfo("GET", "/", {
        "Action": "GetInstanceCloudDiskInfo", "Version": SERVICE_VERSION}, {}, {}),

    # 扩容实例云盘: https://www.volcengine.com/docs/6499/174017
    "ScaleInstanceCloudDiskCapacity": ApiInfo("POST", "/", {
        "Action": "ScaleInstanceCloudDiskCapacity", "Version": SERVICE_VERSION}, {}, {}),

    # 创建边缘云盘
    "CreateEbsInstances": ApiInfo("POST", "/", {
        "Action": "CreateEbsInstances", "Version": SERVICE_VERSION}, {}, {}),

    # 获取边缘云盘列表
    "ListEbsInstances": ApiInfo("POST", "/", {
        "Action": "ListEbsInstances", "Version": SERVICE_VERSION}, {}, {}),

    # 获取边缘云盘详情
    "GetEbsInstance": ApiInfo("POST", "/", {
        "Action": "GetEbsInstance", "Version": SERVICE_VERSION}, {}, {}),

    # 边缘云盘扩容
    "ScaleEbsInstanceCapacity": ApiInfo("POST", "/", {
        "Action": "ScaleEbsInstanceCapacity", "Version": SERVICE_VERSION}, {}, {}),

    # 边缘云盘挂载
    "AttachEbs": ApiInfo("POST", "/", {
        "Action": "AttachEbs", "Version": SERVICE_VERSION}, {}, {}),

    # 边缘云盘卸载
    "DetachEbs": ApiInfo("POST", "/", {
        "Action": "DetachEbs", "Version": SERVICE_VERSION}, {}, {}),

    # 边缘云盘删除
    "DeleteEbsInstance": ApiInfo("POST", "/", {
        "Action": "DeleteEbsInstance", "Version": SERVICE_VERSION}, {}, {}),

    # 批量重置系统或更换镜像 https://www.volcengine.com/docs/6499/196711
    "BatchResetSystem": ApiInfo("POST", "/", {
        "Action": "BatchResetSystem", "Version": SERVICE_VERSION}, {}, {}),
}


class VeenService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(VeenService, "_instance"):
            with VeenService._instance_lock:
                if not hasattr(VeenService, "_instance"):
                    VeenService._instance = object.__new__(cls)
        return VeenService._instance

    def __init__(self, region="cn-north-1"):
        self.service_info = VeenService.get_service_info(region)
        self.api_info = VeenService.get_api_info()
        super(VeenService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(region_name):
        service_info = service_info_map.get(region_name, None)
        if not service_info:
            raise Exception('do not support region %s' % region_name)
        return service_info

    @staticmethod
    def get_api_info():
        return api_info

    def create_cloudserver(self, body=None):
        if body is None:
            body = {}
        action = "CreateCloudServer"
        res = self.json(action,[],json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def list_cloudservers(self, query=None):
        if query is None:
            query = {}
        action = "ListCloudServers"
        res = self.get(action,query)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def get_cloudserver(self, query=None):
        if query is None:
            query = {}
        action = "GetCloudServer"
        res = self.get(action,query)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json
    
    def start_cloudserver(self, body=None):
        if body is None:
            body = {}
        action = "StartCloudServer"
        res = self.json(action,[],json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def stop_cloudserver(self, body=None):
        if body is None:
            body = {}
        action = "StopCloudServer"
        res = self.json(action,[],json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def reboot_cloudserver(self, body=None):
        if body is None:
            body = {}
        action = "RebootCloudServer"
        res = self.json(action,[],json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def delete_cloudserver(self, body=None):
        if body is None:
            body = {}
        action = "DeleteCloudServer"
        res = self.json(action,[],json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def list_instance_types(self, query=None):
        if query is None:
            query = {}
        action = "ListInstanceTypes"
        res = self.get(action,query)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def list_available_resource_info(self, query=None):
        if query is None:
            query = {}
        action = "ListAvailableResourceInfo"
        res = self.get(action,query)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def create_instance(self, body=None):
        if body is None:
            body = {}
        action = "CreateInstance"
        res = self.json(action,[],json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def list_instances(self, query=None):
        if query is None:
            query = {}
        action = "ListInstances"
        res = self.get(action,query)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def get_instance(self, query=None):
        if query is None:
            query = {}
        action = "GetInstance"
        res = self.get(action,query)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def start_instances(self, body=None):
        if body is None:
            body = {}
        action = "StartInstances"
        res = self.json(action,[],json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def stop_instances(self, body=None):
        if body is None:
            body = {}
        action = "StopInstances"
        res = self.json(action,[],json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def reboot_instances(self, body=None):
        if body is None:
            body = {}
        action = "RebootInstances"
        res = self.json(action,[],json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def offline_instances(self, body=None):
        if body is None:
            body = {}
        action = "OfflineInstances"
        res = self.json(action,[],json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def set_instance_name(self, body=None):
        if body is None:
            body = {}
        action = "SetInstanceName"
        res = self.json(action,[],json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def reset_login_credential(self, body=None):
        if body is None:
            body = {}
        action = "ResetLoginCredential"
        res = self.json(action,[],json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def get_instance_cloud_disk_info(self, query=None):
        if query is None:
            query = {}
        action = "GetInstanceCloudDiskInfo"
        res = self.get(action,query)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def scale_instance_cloud_disk_capacity(self, body=None):
        if body is None:
            body = {}
        action = "ScaleInstanceCloudDiskCapacity"
        res = self.json(action,[],json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def create_ebs_instances(self, body=None):
        if body is None:
            body = {}
        action = "CreateEbsInstances"
        res = self.json(action,[],json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def list_ebs_instances(self, body=None):
        if body is None:
            body = {}
        action = "ListEbsInstances"
        res = self.json(action,[],json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def get_ebs_instance(self, body=None):
        if body is None:
            body = {}
        action = "GetEbsInstance"
        res = self.json(action,[],json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def scale_ebs_instance_capacity(self, body=None):
        if body is None:
            body = {}
        action = "ScaleEbsInstanceCapacity"
        res = self.json(action,[],json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def attach_ebs(self, body=None):
        if body is None:
            body = {}
        action = "AttachEbs"
        res = self.json(action,[],json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def detach_ebs(self, body=None):
        if body is None:
            body = {}
        action = "DetachEbs"
        res = self.json(action,[],json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def delete_ebs_instance(self, body=None):
        if body is None:
            body = {}
        action = "DeleteEbsInstance"
        res = self.json(action,[],json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def batch_reset_system(self, body=None):
        if body is None:
            body = {}
        action = "BatchResetSystem"
        res = self.json(action,[],json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json