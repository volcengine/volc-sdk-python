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
    "DescribeAuth": ApiInfo("POST", "/", {"Action": "DescribeAuth", "Version": LIVE_SERVICE_VERSION}, {}, {}),
    "ForbidStream": ApiInfo("POST", "/", {"Action": "ForbidStream", "Version": LIVE_SERVICE_VERSION}, {},
                            {}),
    "ResumeStream": ApiInfo("POST", "/", {"Action": "ResumeStream", "Version": LIVE_SERVICE_VERSION}, {},
                            {}),
    "ListCert": ApiInfo("POST", "/", {"Action": "ListCert", "Version": LIVE_SERVICE_VERSION}, {},
                        {}),
    "CreateCert": ApiInfo("POST", "/", {"Action": "CreateCert", "Version": LIVE_SERVICE_VERSION}, {},
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
    "DescribeLiveBandwidthData": ApiInfo("POST", "/",
                                         {"Action": "DescribeLiveBandwidthData", "Version": LIVE_SERVICE_VERSION}, {},
                                         {}),
    "DescribeLiveTrafficData": ApiInfo("POST", "/",
                                       {"Action": "DescribeLiveTrafficData", "Version": LIVE_SERVICE_VERSION}, {},
                                       {}),
    "DescribeLiveP95PeakBandwidthData": ApiInfo("POST", "/",
                                                {"Action": "DescribeLiveP95PeakBandwidthData",
                                                 "Version": LIVE_SERVICE_VERSION}, {},
                                                {}),
    "DescribeRecordData": ApiInfo("POST", "/",
                                  {"Action": "DescribeRecordData", "Version": LIVE_SERVICE_VERSION}, {},
                                  {}),
    "DescribeTranscodeData": ApiInfo("POST", "/",
                                     {"Action": "DescribeTranscodeData", "Version": LIVE_SERVICE_VERSION}, {},
                                     {}),
    "DescribeSnapshotData": ApiInfo("POST", "/",
                                    {"Action": "DescribeSnapshotData", "Version": LIVE_SERVICE_VERSION}, {},
                                    {}),

    "DescribeLiveDomainLog": ApiInfo("GET", "/",
                                     {"Action": "DescribeLiveDomainLog", "Version": LIVE_SERVICE_VERSION}, {},
                                     {}),
    "DescribePushStreamMetrics": ApiInfo("POST", "/",
                                         {"Action": "DescribePushStreamMetrics", "Version": LIVE_SERVICE_VERSION}, {},
                                         {}),
    "DescribeLiveStreamSessions": ApiInfo("POST", "/",
                                          {"Action": "DescribeLiveStreamSessions", "Version": LIVE_SERVICE_VERSION}, {},
                                          {}),
    "DescribePlayResponseStatusStat": ApiInfo("POST", "/",
                                              {"Action": "DescribePlayResponseStatusStat",
                                               "Version": LIVE_SERVICE_VERSION}, {},
                                              {}),
    "DescribeLiveMetricTrafficData": ApiInfo("POST", "/",
                                             {"Action": "DescribeLiveMetricTrafficData",
                                              "Version": LIVE_SERVICE_VERSION}, {},
                                             {}),
    "DescribeLiveMetricBandwidthData": ApiInfo("POST", "/",
                                               {"Action": "DescribeLiveMetricBandwidthData",
                                                "Version": LIVE_SERVICE_VERSION}, {},
                                               {}),
    "DescribePlayStreamList": ApiInfo("GET", "/",
                                      {"Action": "DescribePlayStreamList",
                                       "Version": LIVE_SERVICE_VERSION}, {},
                                      {}),
    "DescribePullToPushBandwidthData": ApiInfo("POST", "/",
                                               {"Action": "DescribePullToPushBandwidthData",
                                                "Version": LIVE_SERVICE_VERSION}, {},
                                               {}),
    "CreateSnapshotAuditPreset": ApiInfo("POST", "/",
                                         {"Action": "CreateSnapshotAuditPreset",
                                          "Version": LIVE_SERVICE_VERSION}, {},
                                         {}),
    "ListVhostSnapshotAuditPreset": ApiInfo("POST", "/",
                                            {"Action": "ListVhostSnapshotAuditPreset",
                                             "Version": LIVE_SERVICE_VERSION}, {},
                                            {}),
    "UpdateSnapshotAuditPreset": ApiInfo("POST", "/",
                                         {"Action": "UpdateSnapshotAuditPreset",
                                          "Version": LIVE_SERVICE_VERSION}, {},
                                         {}),
    "DeleteSnapshotAuditPreset": ApiInfo("POST", "/",
                                         {"Action": "DeleteSnapshotAuditPreset",
                                          "Version": LIVE_SERVICE_VERSION}, {},
                                         {}),
    "DescribeLiveAuditData": ApiInfo("POST", "/",
                                             {"Action": "DescribeLiveAuditData",
                                              "Version": LIVE_SERVICE_VERSION}, {},
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

    def describe_live_bandwidth_data(self, params):
        action = "DescribeLiveBandwidthData"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_live_traffic_data(self, params):
        action = "DescribeLiveTrafficData"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_live_P95Peak_bandwidth_data(self, params):
        action = "DescribeLiveP95PeakBandwidthData"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_record_data(self, params):
        action = "DescribeRecordData"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_transcode_data(self, params):
        action = "DescribeTranscodeData"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_snapshot_data(self, params):
        action = "DescribeSnapshotData"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_live_domain_log(self, params):
        action = "DescribeLiveDomainLog"
        res = self.get(action, params)
        # res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_push_stream_metrics(self, params):
        action = "DescribePushStreamMetrics"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_live_stream_sessions(self, params):
        action = "DescribeLiveStreamSessions"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_play_response_status_stat(self, params):
        action = "DescribePlayResponseStatusStat"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_live_metric_traffic_data(self, params):
        action = "DescribeLiveMetricTrafficData"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_live_metric_bandwidth_data(self, params):
        action = "DescribeLiveMetricBandwidthData"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_play_stream_list(self, params):
        action = "DescribePlayStreamList"
        res = self.get(action, params)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def describe_pull_to_push_bandwidth_data(self, params):
        action = "DescribePullToPushBandwidthData"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def create_snapshot_audit_preset(self, params):
        action = "CreateSnapshotAuditPreset"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def update_snapshot_audit_preset(self, params):
        action = "UpdateSnapshotAuditPreset"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def delete_snapshot_audit_preset(self, params):
        action = "DeleteSnapshotAuditPreset"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json

    def list_vhost_snapshot_audit_preset(self, params):
        action = "ListVhostSnapshotAuditPreset"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json
    
    def describe_live_audit_data(self, params):
        action = "DescribeLiveAuditData"
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(res)
        return res_json
