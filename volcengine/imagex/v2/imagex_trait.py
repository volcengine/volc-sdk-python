# coding:utf-8

import json
from volcengine.base.Service import Service
from volcengine.const.Const import *
from volcengine.util.Util import *
from volcengine.Policy import *
from volcengine.imagex.v2.imagex_config import *  # Modify it if necessary


class ImagexTrait(Service):
    def __init__(self, param=None):
        if param is None:
            param = {}
        self.param = param
        region = param.get('region', REGION_CN_NORTH1)
        self.service_info = ImagexTrait.get_service_info(region)
        self.api_info = ImagexTrait.get_api_info()
        if param.get('ak', None) and param.get('sk', None):
            self.set_ak(param['ak'])
            self.set_sk(param['sk'])
        super(ImagexTrait, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(region):
        service_info = service_info_map.get(region, None)
        if not service_info:
            raise Exception('Not support region %s' % region)
        return service_info

    @staticmethod
    def get_api_info():
        return api_info

    def imagex_get(self, action, params, doseq=0):
        res = self.get(action, params, doseq)
        try:
            res_json = json.loads(res)
        except Exception as e:
            raise Exception("res body is not json, %s, %s" % (e, res))
        if "ResponseMetadata" not in res_json:
            raise Exception("ResponseMetadata not in resp body, action %s, resp %s" % (action, res))
        elif "Error" in res_json["ResponseMetadata"]:
            raise Exception("%s failed, %s" %(action,res))
        return res_json

    def imagex_post(self, action, params, body):
        res = self.json(action, params, body)
        try:
            res_json = json.loads(res)
        except Exception as e:
            raise Exception("res body is not json, %s, %s" % (e, res))
        if "ResponseMetadata" not in res_json:
            raise Exception("ResponseMetadata not in resp body, action %s, resp %s" % (action, res))
        elif "Error" in res_json["ResponseMetadata"]:
            raise Exception("%s failed, %s" %(action,res))
        return res_json


    def update_image_domain_volc_origin(self, query={}, body={}):
        return self.imagex_post('UpdateImageDomainVolcOrigin', query, json.dumps(body))
            
    def del_domain(self, query={}, body={}):
        return self.imagex_post('DelDomain', query, json.dumps(body))
            
    def add_domain_v_1(self, query={}, body={}):
        return self.imagex_post('AddDomainV1', query, json.dumps(body))
            
    def update_image_domain_ip_auth(self, query={}, body={}):
        return self.imagex_post('UpdateImageDomainIPAuth', query, json.dumps(body))
            
    def update_refer(self, query={}, body={}):
        return self.imagex_post('UpdateRefer', query, json.dumps(body))
            
    def update_image_domain_ua_access(self, query={}, body={}):
        return self.imagex_post('UpdateImageDomainUaAccess', query, json.dumps(body))
            
    def update_https(self, query={}, body={}):
        return self.imagex_post('UpdateHttps', query, json.dumps(body))
            
    def update_image_domain_download_speed_limit(self, query={}, body={}):
        return self.imagex_post('UpdateImageDomainDownloadSpeedLimit', query, json.dumps(body))
            
    def update_response_header(self, query={}, body={}):
        return self.imagex_post('UpdateResponseHeader', query, json.dumps(body))
            
    def update_image_domain_area_access(self, query={}, body={}):
        return self.imagex_post('UpdateImageDomainAreaAccess', query, json.dumps(body))
            
    def update_domain_adaptive_fmt(self, query={}, body={}):
        return self.imagex_post('UpdateDomainAdaptiveFmt', query, json.dumps(body))
            
    def update_image_domain_config(self, query={}, body={}):
        return self.imagex_post('UpdateImageDomainConfig', query, json.dumps(body))
            
    def update_advance(self, query={}, body={}):
        return self.imagex_post('UpdateAdvance', query, json.dumps(body))
            
    def update_image_domain_bandwidth_limit(self, query={}, body={}):
        return self.imagex_post('UpdateImageDomainBandwidthLimit', query, json.dumps(body))
            
    def update_slim_config(self, query={}, body={}):
        return self.imagex_post('UpdateSlimConfig', query, json.dumps(body))
            
    def set_default_domain(self, body={}):
        return self.imagex_post('SetDefaultDomain', [], json.dumps(body))
            
    def describe_image_volc_cdn_access_log(self, query={}, body={}):
        return self.imagex_post('DescribeImageVolcCdnAccessLog', query, json.dumps(body))
            
    def verify_domain_owner(self, query={}, body={}):
        return self.imagex_post('VerifyDomainOwner', query, json.dumps(body))
            
    def get_response_header_validate_keys(self):
        return self.imagex_get('GetResponseHeaderValidateKeys', {})
            
    def get_domain_config(self, query={}):
        return self.imagex_get('GetDomainConfig', query)
            
    def get_domain_owner_verify_content(self, query={}):
        return self.imagex_get('GetDomainOwnerVerifyContent', query)
            
    def get_service_domains(self, query={}):
        return self.imagex_get('GetServiceDomains', query)
            
    def delete_image_monitor_rules(self, query={}, body={}):
        return self.imagex_post('DeleteImageMonitorRules', query, json.dumps(body))
            
    def delete_image_monitor_records(self, query={}, body={}):
        return self.imagex_post('DeleteImageMonitorRecords', query, json.dumps(body))
            
    def create_image_monitor_rule(self, query={}, body={}):
        return self.imagex_post('CreateImageMonitorRule', query, json.dumps(body))
            
    def update_image_monitor_rule(self, query={}, body={}):
        return self.imagex_post('UpdateImageMonitorRule', query, json.dumps(body))
            
    def update_image_monitor_rule_status(self, query={}, body={}):
        return self.imagex_post('UpdateImageMonitorRuleStatus', query, json.dumps(body))
            
    def get_image_alert_records(self, query={}, body={}):
        return self.imagex_post('GetImageAlertRecords', query, json.dumps(body))
            
    def get_image_monitor_rules(self, query={}):
        return self.imagex_get('GetImageMonitorRules', query)
            
    def create_image_setting_rule(self, query={}, body={}):
        return self.imagex_post('CreateImageSettingRule', query, json.dumps(body))
            
    def delete_image_setting_rule(self, query={}, body={}):
        return self.imagex_post('DeleteImageSettingRule', query, json.dumps(body))
            
    def update_image_setting_rule_priority(self, query={}, body={}):
        return self.imagex_post('UpdateImageSettingRulePriority', query, json.dumps(body))
            
    def update_image_setting_rule(self, query={}, body={}):
        return self.imagex_post('UpdateImageSettingRule', query, json.dumps(body))
            
    def get_image_settings(self, query={}):
        return self.imagex_get('GetImageSettings', query)
            
    def get_image_setting_rule_history(self, query={}):
        return self.imagex_get('GetImageSettingRuleHistory', query)
            
    def get_image_setting_rules(self, query={}):
        return self.imagex_get('GetImageSettingRules', query)
            
    def create_image_migrate_task(self, body={}):
        return self.imagex_post('CreateImageMigrateTask', [], json.dumps(body))
            
    def delete_image_migrate_task(self, query={}, body={}):
        return self.imagex_post('DeleteImageMigrateTask', query, json.dumps(body))
            
    def export_failed_migrate_task(self, query={}):
        return self.imagex_get('ExportFailedMigrateTask', query)
            
    def update_image_task_strategy(self, body={}):
        return self.imagex_post('UpdateImageTaskStrategy', [], json.dumps(body))
            
    def terminate_image_migrate_task(self, query={}, body={}):
        return self.imagex_post('TerminateImageMigrateTask', query, json.dumps(body))
            
    def get_vendor_buckets(self, body={}):
        return self.imagex_post('GetVendorBuckets', [], json.dumps(body))
            
    def get_image_migrate_tasks(self, query={}):
        return self.imagex_get('GetImageMigrateTasks', query)
            
    def rerun_image_migrate_task(self, query={}, body={}):
        return self.imagex_post('RerunImageMigrateTask', query, json.dumps(body))
            
    def get_image_add_on_tag(self, query={}):
        return self.imagex_get('GetImageAddOnTag', query)
            
    def describe_imagex_cube_usage(self, query={}):
        return self.imagex_get('DescribeImageXCubeUsage', query)
            
    def describe_imagex_source_request_bandwidth(self, query={}):
        return self.imagex_get('DescribeImageXSourceRequestBandwidth', query)
            
    def describe_imagex_source_request_traffic(self, query={}):
        return self.imagex_get('DescribeImageXSourceRequestTraffic', query)
            
    def describe_imagex_source_request(self, query={}):
        return self.imagex_get('DescribeImageXSourceRequest', query)
            
    def describe_imagex_storage_usage(self, query={}):
        return self.imagex_get('DescribeImageXStorageUsage', query)
            
    def describe_imagex_bucket_retrieval_usage(self, query={}):
        return self.imagex_get('DescribeImageXBucketRetrievalUsage', query)
            
    def describe_imagexai_request_cnt_usage(self, query={}):
        return self.imagex_get('DescribeImageXAIRequestCntUsage', query)
            
    def describe_imagex_summary(self, query={}):
        return self.imagex_get('DescribeImageXSummary', query)
            
    def describe_imagex_domain_traffic_data(self, query={}):
        return self.imagex_get('DescribeImageXDomainTrafficData', query)
            
    def describe_imagex_domain_bandwidth_data(self, query={}):
        return self.imagex_get('DescribeImageXDomainBandwidthData', query)
            
    def describe_imagex_domain_bandwidth_ninety_five_data(self, query={}):
        return self.imagex_get('DescribeImageXDomainBandwidthNinetyFiveData', query)
            
    def describe_imagex_bucket_usage(self, query={}):
        return self.imagex_get('DescribeImageXBucketUsage', query)
            
    def describe_imagex_billing_request_cnt_usage(self, query={}):
        return self.imagex_get('DescribeImageXBillingRequestCntUsage', query)
            
    def describe_imagex_request_cnt_usage(self, query={}):
        return self.imagex_get('DescribeImageXRequestCntUsage', query)
            
    def describe_imagex_base_op_usage(self, query={}):
        return self.imagex_get('DescribeImageXBaseOpUsage', query)
            
    def describe_imagex_compress_usage(self, query={}):
        return self.imagex_get('DescribeImageXCompressUsage', query)
            
    def describe_imagex_screenshot_usage(self, query={}):
        return self.imagex_get('DescribeImageXScreenshotUsage', query)
            
    def describe_imagex_video_clip_duration_usage(self, query={}):
        return self.imagex_get('DescribeImageXVideoClipDurationUsage', query)
            
    def describe_imagex_multi_compress_usage(self, query={}):
        return self.imagex_get('DescribeImageXMultiCompressUsage', query)
            
    def describe_imagex_edge_request(self, query={}):
        return self.imagex_get('DescribeImageXEdgeRequest', query)
            
    def describe_imagex_edge_request_bandwidth(self, query={}):
        return self.imagex_get('DescribeImageXEdgeRequestBandwidth', query)
            
    def describe_imagex_edge_request_traffic(self, query={}):
        return self.imagex_get('DescribeImageXEdgeRequestTraffic', query)
            
    def describe_imagex_edge_request_regions(self, query={}):
        return self.imagex_get('DescribeImageXEdgeRequestRegions', query)
            
    def describe_imagex_mirror_request_http_code_by_time(self, body={}):
        return self.imagex_post('DescribeImageXMirrorRequestHttpCodeByTime', [], json.dumps(body))
            
    def describe_imagex_mirror_request_http_code_overview(self, body={}):
        return self.imagex_post('DescribeImageXMirrorRequestHttpCodeOverview', [], json.dumps(body))
            
    def describe_imagex_mirror_request_traffic(self, body={}):
        return self.imagex_post('DescribeImageXMirrorRequestTraffic', [], json.dumps(body))
            
    def describe_imagex_mirror_request_bandwidth(self, body={}):
        return self.imagex_post('DescribeImageXMirrorRequestBandwidth', [], json.dumps(body))
            
    def describe_imagex_server_qps_usage(self, query={}):
        return self.imagex_get('DescribeImageXServerQPSUsage', query)
            
    def describe_imagex_hit_rate_traffic_data(self, query={}):
        return self.imagex_get('DescribeImageXHitRateTrafficData', query)
            
    def describe_imagex_hit_rate_request_data(self, query={}):
        return self.imagex_get('DescribeImageXHitRateRequestData', query)
            
    def describe_imagexcdn_top_request_data(self, query={}):
        return self.imagex_get('DescribeImageXCDNTopRequestData', query)
            
    def describe_imagex_heif_encode_file_in_size_by_time(self, query={}, body={}):
        return self.imagex_post('DescribeImageXHeifEncodeFileInSizeByTime', query, json.dumps(body))
            
    def describe_imagex_heif_encode_file_out_size_by_time(self, query={}, body={}):
        return self.imagex_post('DescribeImageXHeifEncodeFileOutSizeByTime', query, json.dumps(body))
            
    def describe_imagex_heif_encode_success_count_by_time(self, query={}, body={}):
        return self.imagex_post('DescribeImageXHeifEncodeSuccessCountByTime', query, json.dumps(body))
            
    def describe_imagex_heif_encode_success_rate_by_time(self, query={}, body={}):
        return self.imagex_post('DescribeImageXHeifEncodeSuccessRateByTime', query, json.dumps(body))
            
    def describe_imagex_heif_encode_duration_by_time(self, query={}, body={}):
        return self.imagex_post('DescribeImageXHeifEncodeDurationByTime', query, json.dumps(body))
            
    def describe_imagex_heif_encode_error_code_by_time(self, query={}, body={}):
        return self.imagex_post('DescribeImageXHeifEncodeErrorCodeByTime', query, json.dumps(body))
            
    def describe_imagex_exceed_resolution_ratio_all(self, body={}):
        return self.imagex_post('DescribeImageXExceedResolutionRatioAll', [], json.dumps(body))
            
    def describe_imagex_exceed_file_size(self, body={}):
        return self.imagex_post('DescribeImageXExceedFileSize', [], json.dumps(body))
            
    def describe_imagex_exceed_count_by_time(self, body={}):
        return self.imagex_post('DescribeImageXExceedCountByTime', [], json.dumps(body))
            
    def describe_imagex_service_quality(self, query={}):
        return self.imagex_get('DescribeImageXServiceQuality', query)
            
    def get_imagex_query_apps(self, query={}):
        return self.imagex_get('GetImageXQueryApps', query)
            
    def get_imagex_query_regions(self, query={}):
        return self.imagex_get('GetImageXQueryRegions', query)
            
    def get_imagex_query_dims(self, query={}):
        return self.imagex_get('GetImageXQueryDims', query)
            
    def get_imagex_query_vals(self, query={}):
        return self.imagex_get('GetImageXQueryVals', query)
            
    def describe_imagex_upload_count_by_time(self, body={}):
        return self.imagex_post('DescribeImageXUploadCountByTime', [], json.dumps(body))
            
    def describe_imagex_upload_duration(self, body={}):
        return self.imagex_post('DescribeImageXUploadDuration', [], json.dumps(body))
            
    def describe_imagex_upload_success_rate_by_time(self, body={}):
        return self.imagex_post('DescribeImageXUploadSuccessRateByTime', [], json.dumps(body))
            
    def describe_imagex_upload_file_size(self, body={}):
        return self.imagex_post('DescribeImageXUploadFileSize', [], json.dumps(body))
            
    def describe_imagex_upload_error_code_by_time(self, body={}):
        return self.imagex_post('DescribeImageXUploadErrorCodeByTime', [], json.dumps(body))
            
    def describe_imagex_upload_error_code_all(self, body={}):
        return self.imagex_post('DescribeImageXUploadErrorCodeAll', [], json.dumps(body))
            
    def describe_imagex_upload_speed(self, body={}):
        return self.imagex_post('DescribeImageXUploadSpeed', [], json.dumps(body))
            
    def describe_imagex_upload_segment_speed_by_time(self, body={}):
        return self.imagex_post('DescribeImageXUploadSegmentSpeedByTime', [], json.dumps(body))
            
    def describe_imagex_cdn_success_rate_by_time(self, body={}):
        return self.imagex_post('DescribeImageXCdnSuccessRateByTime', [], json.dumps(body))
            
    def describe_imagex_cdn_success_rate_all(self, body={}):
        return self.imagex_post('DescribeImageXCdnSuccessRateAll', [], json.dumps(body))
            
    def describe_imagex_cdn_error_code_by_time(self, body={}):
        return self.imagex_post('DescribeImageXCdnErrorCodeByTime', [], json.dumps(body))
            
    def describe_imagex_cdn_error_code_all(self, body={}):
        return self.imagex_post('DescribeImageXCdnErrorCodeAll', [], json.dumps(body))
            
    def describe_imagex_cdn_duration_detail_by_time(self, body={}):
        return self.imagex_post('DescribeImageXCdnDurationDetailByTime', [], json.dumps(body))
            
    def describe_imagex_cdn_duration_all(self, body={}):
        return self.imagex_post('DescribeImageXCdnDurationAll', [], json.dumps(body))
            
    def describe_imagex_cdn_reuse_rate_by_time(self, body={}):
        return self.imagex_post('DescribeImageXCdnReuseRateByTime', [], json.dumps(body))
            
    def describe_imagex_cdn_reuse_rate_all(self, body={}):
        return self.imagex_post('DescribeImageXCdnReuseRateAll', [], json.dumps(body))
            
    def describe_imagex_cdn_protocol_rate_by_time(self, body={}):
        return self.imagex_post('DescribeImageXCdnProtocolRateByTime', [], json.dumps(body))
            
    def describe_imagex_client_failure_rate(self, body={}):
        return self.imagex_post('DescribeImageXClientFailureRate', [], json.dumps(body))
            
    def describe_imagex_client_decode_success_rate_by_time(self, body={}):
        return self.imagex_post('DescribeImageXClientDecodeSuccessRateByTime', [], json.dumps(body))
            
    def describe_imagex_client_decode_duration_by_time(self, body={}):
        return self.imagex_post('DescribeImageXClientDecodeDurationByTime', [], json.dumps(body))
            
    def describe_imagex_client_queue_duration_by_time(self, body={}):
        return self.imagex_post('DescribeImageXClientQueueDurationByTime', [], json.dumps(body))
            
    def describe_imagex_client_error_code_by_time(self, body={}):
        return self.imagex_post('DescribeImageXClientErrorCodeByTime', [], json.dumps(body))
            
    def describe_imagex_client_error_code_all(self, body={}):
        return self.imagex_post('DescribeImageXClientErrorCodeAll', [], json.dumps(body))
            
    def describe_imagex_client_load_duration(self, body={}):
        return self.imagex_post('DescribeImageXClientLoadDuration', [], json.dumps(body))
            
    def describe_imagex_client_load_duration_all(self, body={}):
        return self.imagex_post('DescribeImageXClientLoadDurationAll', [], json.dumps(body))
            
    def describe_imagex_client_sdk_ver_by_time(self, body={}):
        return self.imagex_post('DescribeImageXClientSdkVerByTime', [], json.dumps(body))
            
    def describe_imagex_client_file_size(self, body={}):
        return self.imagex_post('DescribeImageXClientFileSize', [], json.dumps(body))
            
    def describe_imagex_client_top_file_size(self, body={}):
        return self.imagex_post('DescribeImageXClientTopFileSize', [], json.dumps(body))
            
    def describe_imagex_client_count_by_time(self, body={}):
        return self.imagex_post('DescribeImageXClientCountByTime', [], json.dumps(body))
            
    def describe_imagex_client_quality_rate_by_time(self, body={}):
        return self.imagex_post('DescribeImageXClientQualityRateByTime', [], json.dumps(body))
            
    def describe_imagex_client_top_quality_url(self, body={}):
        return self.imagex_post('DescribeImageXClientTopQualityURL', [], json.dumps(body))
            
    def describe_imagex_client_demotion_rate_by_time(self, body={}):
        return self.imagex_post('DescribeImageXClientDemotionRateByTime', [], json.dumps(body))
            
    def describe_imagex_client_top_demotion_url(self, body={}):
        return self.imagex_post('DescribeImageXClientTopDemotionURL', [], json.dumps(body))
            
    def describe_imagex_client_score_by_time(self, body={}):
        return self.imagex_post('DescribeImageXClientScoreByTime', [], json.dumps(body))
            
    def describe_imagex_sensible_count_by_time(self, body={}):
        return self.imagex_post('DescribeImageXSensibleCountByTime', [], json.dumps(body))
            
    def describe_imagex_sensible_cache_hit_rate_by_time(self, body={}):
        return self.imagex_post('DescribeImageXSensibleCacheHitRateByTime', [], json.dumps(body))
            
    def describe_imagex_sensible_top_size_url(self, body={}):
        return self.imagex_post('DescribeImageXSensibleTopSizeURL', [], json.dumps(body))
            
    def describe_imagex_sensible_top_resolution_url(self, body={}):
        return self.imagex_post('DescribeImageXSensibleTopResolutionURL', [], json.dumps(body))
            
    def describe_imagex_sensible_top_ram_url(self, body={}):
        return self.imagex_post('DescribeImageXSensibleTopRamURL', [], json.dumps(body))
            
    def describe_imagex_sensible_top_unknown_url(self, body={}):
        return self.imagex_post('DescribeImageXSensibleTopUnknownURL', [], json.dumps(body))
            
    def create_batch_process_task(self, query={}, body={}):
        return self.imagex_post('CreateBatchProcessTask', query, json.dumps(body))
            
    def get_batch_process_result(self, query={}, body={}):
        return self.imagex_post('GetBatchProcessResult', query, json.dumps(body))
            
    def get_batch_task_info(self, query={}):
        return self.imagex_get('GetBatchTaskInfo', query)
            
    def ai_process(self, query={}, body={}):
        return self.imagex_post('AIProcess', query, json.dumps(body))
            
    def create_image_ai_task(self, query={}, body={}):
        return self.imagex_post('CreateImageAITask', query, json.dumps(body))
            
    def get_image_ai_tasks(self, query={}):
        return self.imagex_get('GetImageAITasks', query)
            
    def get_image_ai_details(self, query={}):
        return self.imagex_get('GetImageAIDetails', query)
            
    def update_image_resource_status(self, query={}, body={}):
        return self.imagex_post('UpdateImageResourceStatus', query, json.dumps(body))
            
    def update_file_storage_class(self, query={}, body={}):
        return self.imagex_post('UpdateFileStorageClass', query, json.dumps(body))
            
    def get_image_storage_files(self, query={}):
        return self.imagex_get('GetImageStorageFiles', query)
            
    def delete_image_upload_files(self, query={}, body={}):
        return self.imagex_post('DeleteImageUploadFiles', query, json.dumps(body))
            
    def create_file_restore(self, query={}, body={}):
        return self.imagex_post('CreateFileRestore', query, json.dumps(body))
            
    def update_image_upload_files(self, query={}, body={}):
        return self.imagex_post('UpdateImageUploadFiles', query, json.dumps(body))
            
    def commit_image_upload(self, query={}, body={}):
        return self.imagex_post('CommitImageUpload', query, json.dumps(body))
            
    def update_image_file_ct(self, query={}, body={}):
        return self.imagex_post('UpdateImageFileCT', query, json.dumps(body))
            
    def apply_vpc_upload_info(self, query={}):
        return self.imagex_get('ApplyVpcUploadInfo', query)
            
    def apply_image_upload(self, query={}):
        return self.imagex_get('ApplyImageUpload', query)
            
    def get_image_upload_file(self, query={}):
        return self.imagex_get('GetImageUploadFile', query)
            
    def get_image_upload_files(self, query={}):
        return self.imagex_get('GetImageUploadFiles', query)
            
    def get_image_update_files(self, query={}):
        return self.imagex_get('GetImageUpdateFiles', query)
            
    def preview_image_upload_file(self, query={}):
        return self.imagex_get('PreviewImageUploadFile', query)
            
    def get_image_erase_result(self, body={}):
        return self.imagex_post('GetImageEraseResult', [], json.dumps(body))
            
    def get_image_service(self, query={}):
        return self.imagex_get('GetImageService', query)
            
    def get_all_image_services(self, query={}):
        return self.imagex_get('GetAllImageServices', query)
            
    def create_image_compress_task(self, query={}, body={}):
        return self.imagex_post('CreateImageCompressTask', query, json.dumps(body))
            
    def fetch_image_url(self, body={}):
        return self.imagex_post('FetchImageUrl', [], json.dumps(body))
            
    def update_image_storage_ttl(self, body={}):
        return self.imagex_post('UpdateImageStorageTTL', [], json.dumps(body))
            
    def get_compress_task_info(self, query={}):
        return self.imagex_get('GetCompressTaskInfo', query)
            
    def get_url_fetch_task(self, query={}):
        return self.imagex_get('GetUrlFetchTask', query)
            
    def get_resource_url(self, query={}):
        return self.imagex_get('GetResourceURL', query)
            
    def create_image_from_uri(self, query={}, body={}):
        return self.imagex_post('CreateImageFromUri', query, json.dumps(body))
            
    def update_image_file_key(self, query={}, body={}):
        return self.imagex_post('UpdateImageFileKey', query, json.dumps(body))
            
    def create_image_content_task(self, query={}, body={}):
        return self.imagex_post('CreateImageContentTask', query, json.dumps(body))
            
    def get_image_content_task_detail(self, body={}):
        return self.imagex_post('GetImageContentTaskDetail', [], json.dumps(body))
            
    def get_image_content_block_list(self, query={}, body={}):
        return self.imagex_post('GetImageContentBlockList', query, json.dumps(body))
            
    def create_image_transcode_queue(self, body={}):
        return self.imagex_post('CreateImageTranscodeQueue', [], json.dumps(body))
            
    def delete_image_transcode_queue(self, body={}):
        return self.imagex_post('DeleteImageTranscodeQueue', [], json.dumps(body))
            
    def update_image_transcode_queue(self, body={}):
        return self.imagex_post('UpdateImageTranscodeQueue', [], json.dumps(body))
            
    def update_image_transcode_queue_status(self, body={}):
        return self.imagex_post('UpdateImageTranscodeQueueStatus', [], json.dumps(body))
            
    def get_image_transcode_queues(self, query={}):
        return self.imagex_get('GetImageTranscodeQueues', query)
            
    def create_image_transcode_task(self, body={}):
        return self.imagex_post('CreateImageTranscodeTask', [], json.dumps(body))
            
    def get_image_transcode_details(self, query={}):
        return self.imagex_get('GetImageTranscodeDetails', query)
            
    def create_image_transcode_callback(self, body={}):
        return self.imagex_post('CreateImageTranscodeCallback', [], json.dumps(body))
            
    def delete_image_transcode_detail(self, body={}):
        return self.imagex_post('DeleteImageTranscodeDetail', [], json.dumps(body))
            
    def get_image_ps_detection(self, query={}, body={}):
        return self.imagex_post('GetImagePSDetection', query, json.dumps(body))
            
    def get_image_super_resolution_result(self, body={}):
        return self.imagex_post('GetImageSuperResolutionResult', [], json.dumps(body))
            
    def get_denoising_image(self, query={}, body={}):
        return self.imagex_post('GetDenoisingImage', query, json.dumps(body))
            
    def get_image_duplicate_detection(self, query={}, body={}):
        return self.imagex_post('GetImageDuplicateDetection', query, json.dumps(body))
            
    def get_image_ocr_v2(self, query={}, body={}):
        return self.imagex_post('GetImageOCRV2', query, json.dumps(body))
            
    def get_image_bg_fill_result(self, body={}):
        return self.imagex_post('GetImageBgFillResult', [], json.dumps(body))
            
    def get_segment_image(self, query={}, body={}):
        return self.imagex_post('GetSegmentImage', query, json.dumps(body))
            
    def get_image_smart_crop_result(self, body={}):
        return self.imagex_post('GetImageSmartCropResult', [], json.dumps(body))
            
    def get_image_comic_result(self, body={}):
        return self.imagex_post('GetImageComicResult', [], json.dumps(body))
            
    def get_image_enhance_result(self, body={}):
        return self.imagex_post('GetImageEnhanceResult', [], json.dumps(body))
            
    def get_image_quality(self, query={}, body={}):
        return self.imagex_post('GetImageQuality', query, json.dumps(body))
            
    def get_license_plate_detection(self, query={}, body={}):
        return self.imagex_post('GetLicensePlateDetection', query, json.dumps(body))
            
    def get_private_image_type(self, query={}, body={}):
        return self.imagex_post('GetPrivateImageType', query, json.dumps(body))
            
    def create_cv_image_generate_task(self, query={}, body={}):
        return self.imagex_post('CreateCVImageGenerateTask', query, json.dumps(body))
            
    def create_hidden_watermark_image(self, query={}, body={}):
        return self.imagex_post('CreateHiddenWatermarkImage', query, json.dumps(body))
            
    def create_hm_extract_task(self, query={}, body={}):
        return self.imagex_post('CreateHmExtractTask', query, json.dumps(body))
            
    def update_image_exif_data(self, query={}, body={}):
        return self.imagex_post('UpdateImageExifData', query, json.dumps(body))
            
    def get_image_detect_result(self, query={}, body={}):
        return self.imagex_post('GetImageDetectResult', query, json.dumps(body))
            
    def get_cv_image_generate_result(self, query={}, body={}):
        return self.imagex_post('GetCVImageGenerateResult', query, json.dumps(body))
            
    def create_image_hm_extract(self, query={}, body={}):
        return self.imagex_post('CreateImageHmExtract', query, json.dumps(body))
            
    def get_cv_text_generate_image(self, query={}, body={}):
        return self.imagex_post('GetCVTextGenerateImage', query, json.dumps(body))
            
    def get_cv_image_generate_task(self, query={}, body={}):
        return self.imagex_post('GetCVImageGenerateTask', query, json.dumps(body))
            
    def create_image_hm_embed(self, body={}):
        return self.imagex_post('CreateImageHmEmbed', [], json.dumps(body))
            
    def get_cv_anime_generate_image(self, query={}, body={}):
        return self.imagex_post('GetCVAnimeGenerateImage', query, json.dumps(body))
            
    def get_comprehensive_enhance_image(self, body={}):
        return self.imagex_post('GetComprehensiveEnhanceImage', [], json.dumps(body))
            
    def get_image_ai_generate_task(self, query={}):
        return self.imagex_get('GetImageAiGenerateTask', query)
            
    def get_product_aigc_result(self, query={}, body={}):
        return self.imagex_post('GetProductAIGCResult', query, json.dumps(body))
            
    def get_image_erase_models(self, query={}):
        return self.imagex_get('GetImageEraseModels', query)
            
    def get_dedup_task_status(self, query={}):
        return self.imagex_get('GetDedupTaskStatus', query)
            
    def get_image_hm_extract_task_info(self, query={}, body={}):
        return self.imagex_post('GetImageHmExtractTaskInfo', query, json.dumps(body))
            
    def create_image_service(self, body={}):
        return self.imagex_post('CreateImageService', [], json.dumps(body))
            
    def delete_image_service(self, query={}, body={}):
        return self.imagex_post('DeleteImageService', query, json.dumps(body))
            
    def update_image_auth_key(self, query={}, body={}):
        return self.imagex_post('UpdateImageAuthKey', query, json.dumps(body))
            
    def update_res_event_rule(self, query={}, body={}):
        return self.imagex_post('UpdateResEventRule', query, json.dumps(body))
            
    def update_service_name(self, query={}, body={}):
        return self.imagex_post('UpdateServiceName', query, json.dumps(body))
            
    def update_storage_rules(self, query={}, body={}):
        return self.imagex_post('UpdateStorageRules', query, json.dumps(body))
            
    def update_storage_rules_v_2(self, query={}, body={}):
        return self.imagex_post('UpdateStorageRulesV2', query, json.dumps(body))
            
    def update_image_object_access(self, query={}, body={}):
        return self.imagex_post('UpdateImageObjectAccess', query, json.dumps(body))
            
    def update_image_upload_overwrite(self, query={}, body={}):
        return self.imagex_post('UpdateImageUploadOverwrite', query, json.dumps(body))
            
    def update_image_mirror_conf(self, query={}, body={}):
        return self.imagex_post('UpdateImageMirrorConf', query, json.dumps(body))
            
    def get_image_service_subscription(self, query={}):
        return self.imagex_get('GetImageServiceSubscription', query)
            
    def get_image_auth_key(self, query={}):
        return self.imagex_get('GetImageAuthKey', query)
            
    def create_image_analyze_task(self, body={}):
        return self.imagex_post('CreateImageAnalyzeTask', [], json.dumps(body))
            
    def delete_image_analyze_task_run(self, body={}):
        return self.imagex_post('DeleteImageAnalyzeTaskRun', [], json.dumps(body))
            
    def delete_image_analyze_task(self, body={}):
        return self.imagex_post('DeleteImageAnalyzeTask', [], json.dumps(body))
            
    def update_image_analyze_task_status(self, body={}):
        return self.imagex_post('UpdateImageAnalyzeTaskStatus', [], json.dumps(body))
            
    def update_image_analyze_task(self, body={}):
        return self.imagex_post('UpdateImageAnalyzeTask', [], json.dumps(body))
            
    def get_image_analyze_tasks(self, query={}):
        return self.imagex_get('GetImageAnalyzeTasks', query)
            
    def get_image_analyze_result(self, query={}):
        return self.imagex_get('GetImageAnalyzeResult', query)
            
    def delete_image_elements(self, query={}, body={}):
        return self.imagex_post('DeleteImageElements', query, json.dumps(body))
            
    def delete_image_background_colors(self, query={}, body={}):
        return self.imagex_post('DeleteImageBackgroundColors', query, json.dumps(body))
            
    def delete_image_style(self, query={}, body={}):
        return self.imagex_post('DeleteImageStyle', query, json.dumps(body))
            
    def create_image_style(self, query={}, body={}):
        return self.imagex_post('CreateImageStyle', query, json.dumps(body))
            
    def update_image_style_meta(self, query={}, body={}):
        return self.imagex_post('UpdateImageStyleMeta', query, json.dumps(body))
            
    def add_image_elements(self, query={}, body={}):
        return self.imagex_post('AddImageElements', query, json.dumps(body))
            
    def add_image_background_colors(self, query={}, body={}):
        return self.imagex_post('AddImageBackgroundColors', query, json.dumps(body))
            
    def update_image_style(self, query={}, body={}):
        return self.imagex_post('UpdateImageStyle', query, json.dumps(body))
            
    def get_image_fonts(self, query={}):
        return self.imagex_get('GetImageFonts', query)
            
    def get_image_elements(self, query={}):
        return self.imagex_get('GetImageElements', query)
            
    def get_image_background_colors(self, query={}):
        return self.imagex_get('GetImageBackgroundColors', query)
            
    def get_image_styles(self, query={}):
        return self.imagex_get('GetImageStyles', query)
            
    def get_image_style_detail(self, query={}):
        return self.imagex_get('GetImageStyleDetail', query)
            
    def get_image_style_result(self, query={}, body={}):
        return self.imagex_post('GetImageStyleResult', query, json.dumps(body))
            
    def download_cert(self, query={}):
        return self.imagex_get('DownloadCert', query)
            
    def get_image_all_domain_cert(self, query={}):
        return self.imagex_get('GetImageAllDomainCert', query)
            
    def get_cert_info(self, query={}):
        return self.imagex_get('GetCertInfo', query)
            
    def get_all_certs(self, query={}):
        return self.imagex_get('GetAllCerts', query)
            
    def create_image_template(self, query={}, body={}):
        return self.imagex_post('CreateImageTemplate', query, json.dumps(body))
            
    def delete_templates_from_bin(self, query={}, body={}):
        return self.imagex_post('DeleteTemplatesFromBin', query, json.dumps(body))
            
    def delete_image_template(self, query={}, body={}):
        return self.imagex_post('DeleteImageTemplate', query, json.dumps(body))
            
    def create_image_templates_by_import(self, query={}, body={}):
        return self.imagex_post('CreateImageTemplatesByImport', query, json.dumps(body))
            
    def create_templates_from_bin(self, query={}, body={}):
        return self.imagex_post('CreateTemplatesFromBin', query, json.dumps(body))
            
    def get_image_template(self, query={}):
        return self.imagex_get('GetImageTemplate', query)
            
    def get_templates_from_bin(self, query={}):
        return self.imagex_get('GetTemplatesFromBin', query)
            
    def get_all_image_templates(self, query={}):
        return self.imagex_get('GetAllImageTemplates', query)
            
    def create_image_audit_task(self, body={}):
        return self.imagex_post('CreateImageAuditTask', [], json.dumps(body))
            
    def delete_image_audit_result(self, body={}):
        return self.imagex_post('DeleteImageAuditResult', [], json.dumps(body))
            
    def get_sync_audit_result(self, query={}, body={}):
        return self.imagex_post('GetSyncAuditResult', query, json.dumps(body))
            
    def update_image_audit_task_status(self, body={}):
        return self.imagex_post('UpdateImageAuditTaskStatus', [], json.dumps(body))
            
    def update_image_audit_task(self, body={}):
        return self.imagex_post('UpdateImageAuditTask', [], json.dumps(body))
            
    def update_audit_image_status(self, body={}):
        return self.imagex_post('UpdateAuditImageStatus', [], json.dumps(body))
            
    def get_image_audit_tasks(self, query={}):
        return self.imagex_get('GetImageAuditTasks', query)
            
    def get_image_audit_result(self, query={}):
        return self.imagex_get('GetImageAuditResult', query)
            
    def get_audit_entrys_count(self, query={}):
        return self.imagex_get('GetAuditEntrysCount', query)
            
    def create_image_retry_audit_task(self, body={}):
        return self.imagex_post('CreateImageRetryAuditTask', [], json.dumps(body))