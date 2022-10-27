#  -*- coding: utf-8 -*-
import json
import threading

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo

service_info_map = {
    "cn-beijing": ServiceInfo("open.volcengineapi.com", {'accept': 'application/json', },
                              Credentials('', '', "emr", "cn-beijing"), 60 * 5, 60 * 5, "https"),
    "cn-guangzhou": ServiceInfo("open.volcengineapi.com", {'accept': 'application/json', },
                                Credentials('', '', "emr", "cn-guangzhou"), 60 * 5, 60 * 5, "https"),
    "cn-shanghai": ServiceInfo("open.volcengineapi.com", {'accept': 'application/json', },
                               Credentials('', '', "emr", "cn-shanghai"), 60 * 5, 60 * 5, "https"),
}

api_info = {
    # https://www.volcengine.com/docs/6491/145561
    "CreateCluster": ApiInfo("POST", "/", {
        "Action": "CreateCluster", "Version": "2022-06-30"}, {}, {}),
    # https://www.volcengine.com/docs/6491/145562
    "ResizeCluster": ApiInfo("GET", "/", {
        "Action": "ResizeCluster", "Version": "2022-04-15"}, {}, {}),

    # https://www.volcengine.com/docs/6491/145563
    "DescribeCluster": ApiInfo("GET", "/", {
        "Action": "DescribeCluster", "Version": "2022-04-15"}, {}, {}),

    # https://www.volcengine.com/docs/6491/145564
    "ListInstances": ApiInfo("GET", "/", {
        "Action": "ListInstances", "Version": "2022-06-30"}, {}, {}),

    # https://www.volcengine.com/docs/6491/145565
    "ListClusters": ApiInfo("GET", "/", {
        "Action": "ListClusters", "Version": "2021-09-15"}, {}, {}),

    # https://www.volcengine.com/docs/6491/145566
    "ListInstanceGroups": ApiInfo("POST", "/", {
        "Action": "ListInstanceGroups", "Version": "2022-06-30"}, {}, {}),

    # https://www.volcengine.com/docs/6491/145567
    "ReleaseCluster": ApiInfo("POST", "/", {
        "Action": "ReleaseCluster", "Version": "2022-04-15"}, {}, {}),

    # https://www.volcengine.com/docs/6491/145568
    "AddTags": ApiInfo("POST", "/", {
        "Action": "AddTags", "Version": "2022-06-30"}, {}, {}),

    # https://www.volcengine.com/docs/6491/145569
    "RemoveTags": ApiInfo("POST", "/", {
        "Action": "RemoveTags", "Version": "2022-06-30"}, {}, {}),
}


class EMRService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(EMRService, "_instance"):
            with EMRService._instance_lock:
                if not hasattr(EMRService, "_instance"):
                    EMRService._instance = object.__new__(cls)
        return EMRService._instance

    def __init__(self, region="cn-beijing"):
        self.service_info = EMRService.get_service_info(region)
        self.api_info = EMRService.get_api_info()
        super(EMRService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(region):
        service_info = service_info_map.get(region, None)
        if not service_info:
            raise Exception('do not support region %s' % region)
        return service_info

    @staticmethod
    def get_api_info():
        return api_info

    def create_cluster(self, params, body):
        res = self.json("CreateCluster", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def describe_cluster(self, params):
        res = self.get("DescribeCluster", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def list_instances(self, params):
        res = self.get("ListInstances", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def list_clusters(self, params):
        res = self.get("ListClusters", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def list_instance_groups(self, params, body):
        res = self.json("ListInstanceGroups", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def release_cluster(self, params, body):
        res = self.json("ReleaseCluster", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def add_tags(self, params, body):
        res = self.json("AddTags", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def remove_tags(self, params, body):
        res = self.json("RemoveTags", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
