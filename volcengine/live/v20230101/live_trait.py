# coding:utf-8

import json
from volcengine.base.Service import Service
from volcengine.const.Const import *
from volcengine.util.Util import *
from volcengine.Policy import *
from volcengine.live.v20230101.live_config import *  # Modify it if necessary


class LiveTrait(Service):
    def __init__(self, param=None):
        if param is None:
            param = {}
        self.param = param
        region = param.get('region', REGION_CN_NORTH1)
        self.service_info = LiveTrait.get_service_info(region)
        self.api_info = LiveTrait.get_api_info()
        if param.get('ak', None) and param.get('sk', None):
            self.set_ak(param['ak'])
            self.set_sk(param['sk'])
        super(LiveTrait, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(region):
        service_info = service_info_map.get(region, None)
        if not service_info:
            raise Exception('Not support region %s' % region)
        return service_info

    @staticmethod
    def get_api_info():
        return api_info

    def api_get(self, action, params, doseq=0):
        res = self.get(action, params, doseq)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(json.dumps(res))
        return res_json

    def api_post(self, action, params, body):
        res = self.json(action, params, body)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(json.dumps(res))
        return res_json


    def delete_transcode_preset(self, body):
        res = self.api_post('DeleteTranscodePreset', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def update_transcode_preset(self, body):
        res = self.api_post('UpdateTranscodePreset', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def list_common_trans_preset_detail(self, body):
        res = self.api_post('ListCommonTransPresetDetail', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def list_vhost_trans_code_preset(self, body):
        res = self.api_post('ListVhostTransCodePreset', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def create_transcode_preset(self, body):
        res = self.api_post('CreateTranscodePreset', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def create_watermark_preset(self, body):
        res = self.api_post('CreateWatermarkPreset', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def update_watermark_preset(self, body):
        res = self.api_post('UpdateWatermarkPreset', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def delete_watermark_preset(self, body):
        res = self.api_post('DeleteWatermarkPreset', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def list_watermark_preset(self, body):
        res = self.api_post('ListWatermarkPreset', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def list_vhost_watermark_preset(self, body):
        res = self.api_post('ListVhostWatermarkPreset', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def stop_pull_record_task(self, body):
        res = self.api_post('StopPullRecordTask', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def create_pull_record_task(self, body):
        res = self.api_post('CreatePullRecordTask', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def delete_record_preset(self, body):
        res = self.api_post('DeleteRecordPreset', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def update_record_preset_v2(self, body):
        res = self.api_post('UpdateRecordPresetV2', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_record_task_file_history(self, body):
        res = self.api_post('DescribeRecordTaskFileHistory', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def list_vhost_record_preset_v2(self, body):
        res = self.api_post('ListVhostRecordPresetV2', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def list_pull_record_task(self, body):
        res = self.api_post('ListPullRecordTask', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def create_record_preset_v2(self, body):
        res = self.api_post('CreateRecordPresetV2', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def delete_snapshot_preset(self, body):
        res = self.api_post('DeleteSnapshotPreset', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def update_snapshot_preset(self, body):
        res = self.api_post('UpdateSnapshotPreset', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def update_snapshot_preset_v2(self, body):
        res = self.api_post('UpdateSnapshotPresetV2', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_cdn_snapshot_history(self, body):
        res = self.api_post('DescribeCDNSnapshotHistory', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def list_vhost_snapshot_preset(self, body):
        res = self.api_post('ListVhostSnapshotPreset', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def list_vhost_snapshot_preset_v2(self, body):
        res = self.api_post('ListVhostSnapshotPresetV2', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def create_snapshot_preset(self, body):
        res = self.api_post('CreateSnapshotPreset', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def create_snapshot_preset_v2(self, body):
        res = self.api_post('CreateSnapshotPresetV2', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def delete_time_shift_preset_v3(self, body):
        res = self.api_post('DeleteTimeShiftPresetV3', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def update_time_shift_preset_v3(self, body):
        res = self.api_post('UpdateTimeShiftPresetV3', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def list_time_shift_preset_v2(self, body):
        res = self.api_post('ListTimeShiftPresetV2', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def create_time_shift_preset_v3(self, body):
        res = self.api_post('CreateTimeShiftPresetV3', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def delete_callback(self, body):
        res = self.api_post('DeleteCallback', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_callback(self, body):
        res = self.api_post('DescribeCallback', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def update_callback(self, body):
        res = self.api_post('UpdateCallback', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_auth(self, body):
        res = self.api_post('DescribeAuth', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def delete_cert(self, body):
        res = self.api_post('DeleteCert', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_cert_detail_secret_v2(self, body):
        res = self.api_post('DescribeCertDetailSecretV2', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def list_cert_v2(self, body):
        res = self.api_post('ListCertV2', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def create_cert(self, body):
        res = self.api_post('CreateCert', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def bind_cert(self, body):
        res = self.api_post('BindCert', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def unbind_cert(self, body):
        res = self.api_post('UnbindCert', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def create_verify_content(self, body):
        res = self.api_post('CreateVerifyContent', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def verify_domain_owner(self, body):
        res = self.api_post('VerifyDomainOwner', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def delete_domain(self, body):
        res = self.api_post('DeleteDomain', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def enable_domain(self, body):
        res = self.api_post('EnableDomain', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def create_domain_v2(self, body):
        res = self.api_post('CreateDomainV2', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def update_domain_vhost(self, body):
        res = self.api_post('UpdateDomainVhost', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_domain(self, body):
        res = self.api_post('DescribeDomain', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def list_domain_detail(self, body):
        res = self.api_post('ListDomainDetail', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def create_domain(self, body):
        res = self.api_post('CreateDomain', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def disable_domain(self, body):
        res = self.api_post('DisableDomain', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def stop_pull_to_push_task(self, body):
        res = self.api_post('StopPullToPushTask', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def create_pull_to_push_task(self, body):
        res = self.api_post('CreatePullToPushTask', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def delete_pull_to_push_task(self, body):
        res = self.api_post('DeletePullToPushTask', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def restart_pull_to_push_task(self, body):
        res = self.api_post('RestartPullToPushTask', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def update_pull_to_push_task(self, body):
        res = self.api_post('UpdatePullToPushTask', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def list_pull_to_push_task(self, query):
        res = self.api_get('ListPullToPushTask', query)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def delete_relay_source_v4(self, body):
        res = self.api_post('DeleteRelaySourceV4', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def delete_relay_source_v3(self, body):
        res = self.api_post('DeleteRelaySourceV3', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def update_relay_source_v4(self, body):
        res = self.api_post('UpdateRelaySourceV4', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def list_relay_source_v4(self, body):
        res = self.api_post('ListRelaySourceV4', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_relay_source_v3(self, body):
        res = self.api_post('DescribeRelaySourceV3', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def create_relay_source_v4(self, body):
        res = self.api_post('CreateRelaySourceV4', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def update_relay_source_v3(self, body):
        res = self.api_post('UpdateRelaySourceV3', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def kill_stream(self, body):
        res = self.api_post('KillStream', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_closed_stream_info_by_page(self, query):
        res = self.api_get('DescribeClosedStreamInfoByPage', query)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_stream_info_by_page(self, query):
        res = self.api_get('DescribeLiveStreamInfoByPage', query)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_stream_state(self, query):
        res = self.api_get('DescribeLiveStreamState', query)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_forbidden_stream_info_by_page(self, query):
        res = self.api_get('DescribeForbiddenStreamInfoByPage', query)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def forbid_stream(self, body):
        res = self.api_post('ForbidStream', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def resume_stream(self, body):
        res = self.api_post('ResumeStream', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def generate_play_url(self, body):
        res = self.api_post('GeneratePlayURL', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def generate_push_url(self, body):
        res = self.api_post('GeneratePushURL', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def delete_stream_quota_config(self, body):
        res = self.api_post('DeleteStreamQuotaConfig', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_stream_quota_config(self, body):
        res = self.api_post('DescribeStreamQuotaConfig', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def update_stream_quota_config(self, body):
        res = self.api_post('UpdateStreamQuotaConfig', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def list_vqos_metrics_dimensions(self, query):
        res = self.api_get('ListVqosMetricsDimensions', query)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def stop_pull_cdn_snapshot_task(self, body):
        res = self.api_post('StopPullCDNSnapshotTask', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def create_pull_cdn_snapshot_task(self, body):
        res = self.api_post('CreatePullCDNSnapshotTask', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def get_pull_cdn_snapshot_task(self, body):
        res = self.api_post('GetPullCDNSnapshotTask', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def list_pull_cdn_snapshot_task(self, body):
        res = self.api_post('ListPullCDNSnapshotTask', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def get_pull_record_task(self, body):
        res = self.api_post('GetPullRecordTask', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def delete_snapshot_audit_preset(self, body):
        res = self.api_post('DeleteSnapshotAuditPreset', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def update_snapshot_audit_preset(self, body):
        res = self.api_post('UpdateSnapshotAuditPreset', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_snapshot_audit_preset_detail(self, body):
        res = self.api_post('DescribeSnapshotAuditPresetDetail', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def list_vhost_snapshot_audit_preset(self, body):
        res = self.api_post('ListVhostSnapshotAuditPreset', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def create_snapshot_audit_preset(self, body):
        res = self.api_post('CreateSnapshotAuditPreset', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_ip_info(self, body):
        res = self.api_post('DescribeIpInfo', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_region_data(self, body):
        res = self.api_post('DescribeLiveRegionData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_source_stream_metrics(self, body):
        res = self.api_post('DescribeLiveSourceStreamMetrics', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_push_stream_metrics(self, body):
        res = self.api_post('DescribeLivePushStreamMetrics', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_play_status_code_data(self, body):
        res = self.api_post('DescribeLivePlayStatusCodeData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_batch_source_stream_metrics(self, body):
        res = self.api_post('DescribeLiveBatchSourceStreamMetrics', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_batch_push_stream_metrics(self, body):
        res = self.api_post('DescribeLiveBatchPushStreamMetrics', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_stream_count_data(self, body):
        res = self.api_post('DescribeLiveStreamCountData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_push_stream_count_data(self, body):
        res = self.api_post('DescribeLivePushStreamCountData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_source_bandwidth_data(self, body):
        res = self.api_post('DescribeLiveSourceBandwidthData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_source_traffic_data(self, body):
        res = self.api_post('DescribeLiveSourceTrafficData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_metric_bandwidth_data(self, body):
        res = self.api_post('DescribeLiveMetricBandwidthData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_metric_traffic_data(self, body):
        res = self.api_post('DescribeLiveMetricTrafficData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_batch_stream_traffic_data(self, body):
        res = self.api_post('DescribeLiveBatchStreamTrafficData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_batch_stream_transcode_data(self, body):
        res = self.api_post('DescribeLiveBatchStreamTranscodeData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_stream_session_data(self, body):
        res = self.api_post('DescribeLiveStreamSessionData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_isp_data(self, body):
        res = self.api_post('DescribeLiveISPData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_p95_peak_bandwidth_data(self, body):
        res = self.api_post('DescribeLiveP95PeakBandwidthData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_audit_data(self, body):
        res = self.api_post('DescribeLiveAuditData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_pull_to_push_bandwidth_data(self, body):
        res = self.api_post('DescribeLivePullToPushBandwidthData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_pull_to_push_data(self, body):
        res = self.api_post('DescribeLivePullToPushData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_bandwidth_data(self, body):
        res = self.api_post('DescribeLiveBandwidthData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_record_data(self, body):
        res = self.api_post('DescribeLiveRecordData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_snapshot_data(self, body):
        res = self.api_post('DescribeLiveSnapshotData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_traffic_data(self, body):
        res = self.api_post('DescribeLiveTrafficData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_transcode_data(self, body):
        res = self.api_post('DescribeLiveTranscodeData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_time_shift_data(self, body):
        res = self.api_post('DescribeLiveTimeShiftData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_customized_log_data(self, body):
        res = self.api_post('DescribeLiveCustomizedLogData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_log_data(self, body):
        res = self.api_post('DescribeLiveLogData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def delete_referer(self, body):
        res = self.api_post('DeleteReferer', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_deny_config(self, body):
        res = self.api_post('DescribeDenyConfig', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_referer(self, body):
        res = self.api_post('DescribeReferer', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def update_deny_config(self, body):
        res = self.api_post('UpdateDenyConfig', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def update_referer(self, body):
        res = self.api_post('UpdateReferer', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def update_auth_key(self, body):
        res = self.api_post('UpdateAuthKey', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_activity_bandwidth_data(self, body):
        res = self.api_post('DescribeLiveActivityBandwidthData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
            
    def describe_live_stream_usage_data(self, body):
        res = self.api_post('DescribeLiveStreamUsageData', [], json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json