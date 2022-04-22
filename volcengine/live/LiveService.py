# coding:utf-8
import json
import threading

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service
from volcengine.const.Const import REGION_CN_NORTH1

LIVE_SERVICE_VERSION = "2020-08-01"
service_info_map = {
    REGION_CN_NORTH1: ServiceInfo("live.volcengineapi.com", {'Accept': 'application/json', },
                                  Credentials('', '', "live", REGION_CN_NORTH1), 5, 5, "https"),
}

api_info = {
    "ListCommonTransPresetDetail": ApiInfo("POST", "/",
                                           {"Action": "ListCommonTransPresetDetail", "Version": LIVE_SERVICE_VERSION},
                                           {}, {}),
    "UpdateCallback": ApiInfo("POST", "/", {"Action": "UpdateCallback", "Version": LIVE_SERVICE_VERSION}, {}, {}),
    "DescribeCallback": ApiInfo("POST", "/", {"Action": "DescribeCallback", "Version": LIVE_SERVICE_VERSION}, {},
                                {}),
    "DeleteCallback": ApiInfo("POST", "/", {"Action": "DeleteCallback", "Version": LIVE_SERVICE_VERSION},
                              {}, {}),

    "CreateDomain": ApiInfo("POST", "/", {"Action": "CreateDomain", "Version": LIVE_SERVICE_VERSION}, {}, {}),

    "DeleteDomain": ApiInfo("POST", "/", {"Action": "DeleteDomain", "Version": LIVE_SERVICE_VERSION},
                            {},
                            {}),
    "ListDomainDetail": ApiInfo("POST", "/",
                                {"Action": "ListDomainDetail", "Version": LIVE_SERVICE_VERSION},
                                {}, {}),
    "DescribeDomain": ApiInfo("POST", "/",
                              {"Action": "DescribeDomain", "Version": LIVE_SERVICE_VERSION},
                              {}, {}),
    "EnableDomain": ApiInfo("POST", "/",
                            {"Action": "EnableDomain", "Version": LIVE_SERVICE_VERSION},
                            {}, {}),
    "DisableDomain": ApiInfo("POST", "/",
                             {"Action": "DisableDomain", "Version": LIVE_SERVICE_VERSION},
                             {}, {}),
    "ManagerPullPushDomainBind": ApiInfo("POST", "/",
                                         {"Action": "ManagerPullPushDomainBind", "Version": LIVE_SERVICE_VERSION},
                                         {},
                                         {}),
    "UpdateAuthKey": ApiInfo("POST", "/", {"Action": "UpdateAuthKey", "Version": LIVE_SERVICE_VERSION}, {}, {}),
    "EnableAuth": ApiInfo("POST", "/", {"Action": "EnableAuth", "Version": LIVE_SERVICE_VERSION}, {}, {}),
    "DisableAuth": ApiInfo("POST", "/", {"Action": "DisableAuth", "Version": LIVE_SERVICE_VERSION}, {}, {}),
    "DescribeAuth": ApiInfo("POST", "/", {"Action": "DescribeAuth", "Version": LIVE_SERVICE_VERSION}, {}, {}),
    "ForbidStream": ApiInfo("POST", "/", {"Action": "ForbidStream", "Version": LIVE_SERVICE_VERSION}, {},
                            {}),
    "ResumeStream": ApiInfo("POST", "/", {"Action": "ResumeStream", "Version": LIVE_SERVICE_VERSION}, {},
                            {}),
    "ListCert": ApiInfo("POST", "/", {"Action": "ListCert", "Version": LIVE_SERVICE_VERSION}, {},
                        {}),
    "CreateCert": ApiInfo("POST", "/", {"Action": "CreateCert", "Version": LIVE_SERVICE_VERSION}, {},
                          {}),
    "DescribeCertDetailSecret": ApiInfo("POST", "/",
                                        {"Action": "DescribeCertDetailSecret", "Version": LIVE_SERVICE_VERSION}, {},
                                        {}),
    "UpdateCert": ApiInfo("POST", "/", {"Action": "UpdateCert", "Version": LIVE_SERVICE_VERSION}, {},
                          {}),
    "BindCert": ApiInfo("POST", "/", {"Action": "BindCert", "Version": LIVE_SERVICE_VERSION}, {},
                        {}),
    "UnbindCert": ApiInfo("POST", "/", {"Action": "UnbindCert", "Version": LIVE_SERVICE_VERSION}, {},
                          {}),
    "DeleteCert": ApiInfo("POST", "/", {"Action": "DeleteCert", "Version": LIVE_SERVICE_VERSION}, {},
                          {}),
    "UpdateReferer": ApiInfo("POST", "/", {"Action": "UpdateReferer", "Version": LIVE_SERVICE_VERSION}, {},
                             {}),
    "DeleteReferer": ApiInfo("POST", "/", {"Action": "DeleteReferer", "Version": LIVE_SERVICE_VERSION}, {},
                             {}),
    "DescribeReferer": ApiInfo("POST", "/", {"Action": "DescribeReferer", "Version": LIVE_SERVICE_VERSION}, {},
                               {}),
    "CreateRecordPreset": ApiInfo("POST", "/", {"Action": "CreateRecordPreset", "Version": LIVE_SERVICE_VERSION}, {},
                                  {}),
    "UpdateRecordPreset": ApiInfo("POST", "/", {"Action": "UpdateRecordPreset", "Version": LIVE_SERVICE_VERSION}, {},
                                  {}),
    "DeleteRecordPreset": ApiInfo("POST", "/", {"Action": "DeleteRecordPreset", "Version": LIVE_SERVICE_VERSION}, {},
                                  {}),
    "ListVhostRecordPreset": ApiInfo("POST", "/", {"Action": "ListVhostRecordPreset", "Version": LIVE_SERVICE_VERSION},
                                     {},
                                     {}),
    "CreateTranscodePreset": ApiInfo("POST", "/", {"Action": "CreateTranscodePreset", "Version": LIVE_SERVICE_VERSION},
                                     {},
                                     {}),
    "UpdateTranscodePreset": ApiInfo("POST", "/", {"Action": "UpdateTranscodePreset", "Version": LIVE_SERVICE_VERSION},
                                     {},
                                     {}),
    "DeleteTranscodePreset": ApiInfo("POST", "/", {"Action": "DeleteTranscodePreset", "Version": LIVE_SERVICE_VERSION},
                                     {},
                                     {}),
    "ListVhostTransCodePreset": ApiInfo("POST", "/",
                                        {"Action": "ListVhostTransCodePreset", "Version": LIVE_SERVICE_VERSION}, {},
                                        {}),
    "CreateSnapshotPreset": ApiInfo("POST", "/", {"Action": "CreateSnapshotPreset", "Version": LIVE_SERVICE_VERSION},
                                    {},
                                    {}),
    "UpdateSnapshotPreset": ApiInfo("POST", "/", {"Action": "UpdateSnapshotPreset", "Version": LIVE_SERVICE_VERSION},
                                    {},
                                    {}),
    "DeleteSnapshotPreset": ApiInfo("POST", "/", {"Action": "DeleteSnapshotPreset", "Version": LIVE_SERVICE_VERSION},
                                    {},
                                    {}),
    "ListVhostSnapshotPreset": ApiInfo("POST", "/",
                                       {"Action": "ListVhostSnapshotPreset", "Version": LIVE_SERVICE_VERSION}, {},
                                       {}),
}


class LiveService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(LiveService, "_instance"):
            with LiveService._instance_lock:
                if not hasattr(LiveService, "_instance"):
                    LiveService._instance = object.__new__(cls)
        return LiveService._instance

    def __init__(self, region=REGION_CN_NORTH1):
        self.service_info = LiveService.get_service_info(region)
        self.api_info = LiveService.get_api_info()
        super(LiveService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(region_name):
        service_info = service_info_map.get(region_name, None)
        if not service_info:
            raise Exception('do not support region %s' % region_name)
        return service_info

    @staticmethod
    def get_api_info():
        return api_info

    def list_common_trans_preset_detail(self, params):
        action = "ListCommonTransPresetDetail"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def update_callback(self, params):
        action = "UpdateCallback"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_callback(self, params):
        action = "DescribeCallback"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def delete_callback(self, params):
        action = "DeleteCallback"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def create_domain(self, params):
        action = "CreateDomain"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def delete_domain(self, params):
        action = "DeleteDomain"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def list_domain_detail(self, params):
        action = "ListDomainDetail"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_domain(self, params):
        action = "DescribeDomain"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def enable_domain(self, params):
        action = "EnableDomain"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def disable_domain(self, params):
        action = "DisableDomain"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def manager_pull_push_domain_bind(self, params):
        action = "ManagerPullPushDomainBind"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def update_auth_key(self, params):
        action = "UpdateAuthKey"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def enable_auth(self, params):
        action = "EnableAuth"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def disable_auth(self, params):
        action = "DisableAuth"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_auth(self, params):
        action = "DescribeAuth"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def forbid_stream(self, params):
        action = "ForbidStream"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def resume_stream(self, params):
        action = "ResumeStream"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def list_cert(self, params):
        action = "ListCert"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def create_cert(self, params):
        action = "CreateCert"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_cert_detail_secret(self, params):
        action = "DescribeCertDetailSecret"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def update_cert(self, params):
        action = "UpdateCert"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def bind_cert(self, params):
        action = "BindCert"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def un_bind_cert(self, params):
        action = "UnbindCert"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def delete_cert(self, params):
        action = "DeleteCert"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def update_referer(self, params):
        action = "UpdateReferer"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def delete_referer(self, params):
        action = "DeleteReferer"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_referer(self, params):
        action = "DescribeReferer"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def create_record_preset(self, params):
        action = "CreateRecordPreset"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def update_record_preset(self, params):
        action = "UpdateRecordPreset"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def delete_record_preset(self, params):
        action = "DeleteRecordPreset"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def list_vhost_record_preset(self, params):
        action = "ListVhostRecordPreset"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def create_transcode_preset(self, params):
        action = "CreateTranscodePreset"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def update_transcode_preset(self, params):
        action = "UpdateTranscodePreset"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def delete_transcode_preset(self, params):
        action = "DeleteTranscodePreset"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def list_vhost_transcode_preset(self, params):
        action = "ListVhostTransCodePreset"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def create_snapshot_preset(self, params):
        action = "CreateSnapshotPreset"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def update_snapshot_preset(self, params):
        action = "UpdateSnapshotPreset"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def delete_snapshot_preset(self, params):
        action = "DeleteSnapshotPreset"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def list_vhost_snapshot_preset(self, params):
        action = "ListVhostSnapshotPreset"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json
