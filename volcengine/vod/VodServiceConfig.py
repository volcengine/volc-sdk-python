# coding:utf-8

from __future__ import print_function

import threading
from zlib import crc32

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service


class VodServiceConfig(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, region='cn-north-1'):
        self.service_info = VodServiceConfig.get_service_info(region)
        self.api_info = VodServiceConfig.get_api_info()
        self.domain_cache = {}
        self.fallback_domain_weights = {}
        self.update_interval = 10
        self.lock = threading.Lock()
        super(VodServiceConfig, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(region):
        service_info_map = {
            'cn-north-1': ServiceInfo("vod.volcengineapi.com", {'Accept': 'application/json'},
                                      Credentials('', '', 'vod', 'cn-north-1'), 60, 60,"https"),
            'ap-southeast-1': ServiceInfo("vod.ap-southeast-1.volcengineapi.com", {'Accept': 'application/json'},
                                      Credentials('', '', 'vod', 'ap-southeast-1'), 60, 60,"https"),
        }
        service_info = service_info_map.get(region, None)
        if not service_info:
            service_info = ServiceInfo("vod.{}.volcengineapi.com".format(region), {'Accept': 'application/json'},
                                       Credentials('', '', 'vod', region), 60, 60, "https")

        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            # 播放
            "GetPlayInfo": ApiInfo("GET", "/", {"Action": "GetPlayInfo", "Version": "2020-08-01"}, {}, {}),
            "GetAllPlayInfo": ApiInfo("GET", "/", {"Action": "GetAllPlayInfo", "Version": "2022-01-01"}, {}, {}),
            "GetPrivateDrmPlayAuth": ApiInfo("GET", "/", {"Action": "GetPrivateDrmPlayAuth", "Version": "2020-08-01"}, {}, {}),
            "CreateHlsDecryptionKey": ApiInfo("GET", "/", {"Action": "CreateHlsDecryptionKey", "Version": "2023-07-01"}, {}, {}),
            "GetHlsDecryptionKey": ApiInfo("GET", "/", {"Action": "GetHlsDecryptionKey", "Version": "2020-08-01"}, {}, {}),
            "DescribeDrmDataKey": ApiInfo("GET", "/", {"Action": "DescribeDrmDataKey", "Version": "2023-07-01"}, {}, {}),
            "GetPlayInfoWithLiveTimeShiftScene": ApiInfo("GET", "/", {"Action": "GetPlayInfoWithLiveTimeShiftScene", "Version": "2021-11-01"}, {}, {}),
            # 上传
            "UploadMediaByUrl": ApiInfo("GET", "/", {"Action": "UploadMediaByUrl", "Version": "2020-08-01"}, {}, {}),
            "QueryUploadTaskInfo": ApiInfo("GET", "/", {"Action": "QueryUploadTaskInfo", "Version": "2020-08-01"}, {}, {}),
            "ApplyUploadInfo": ApiInfo("GET", "/", {"Action": "ApplyUploadInfo", "Version": "2022-01-01"}, {}, {}),
            "CommitUploadInfo": ApiInfo("GET", "/", {"Action": "CommitUploadInfo", "Version": "2022-01-01"}, {}, {}),
            # 媒资
            "UpdateMediaInfo": ApiInfo("GET", "/", {"Action": "UpdateMediaInfo", "Version": "2020-08-01"}, {}, {}),
            "UpdateMediaPublishStatus": ApiInfo("GET", "/", {"Action": "UpdateMediaPublishStatus", "Version": "2020-08-01"}, {}, {}),
            "UpdateMediaStorageClass": ApiInfo("GET", "/", {"Action": "UpdateMediaStorageClass", "Version": "2022-12-01"}, {}, {}),
            "GetInnerAuditURLs": ApiInfo("POST", "/", {"Action": "GetInnerAuditURLs", "Version": "2023-07-01"}, {}, {}),
            "GetAdAuditResultByVid": ApiInfo("POST", "/", {"Action": "GetAdAuditResultByVid", "Version": "2023-07-01"}, {}, {}),
            "GetMediaInfos": ApiInfo("GET", "/", {"Action": "GetMediaInfos", "Version": "2022-12-01"}, {}, {}),
            "GetMediaInfos20230701": ApiInfo("GET", "/", {"Action": "GetMediaInfos", "Version": "2023-07-01"}, {}, {}),
            "GetRecommendedPoster": ApiInfo("GET", "/", {"Action": "GetRecommendedPoster", "Version": "2020-08-01"}, {}, {}),
            "DeleteMedia": ApiInfo("GET", "/", {"Action": "DeleteMedia", "Version": "2020-08-01"}, {}, {}),
            "DeleteTranscodes": ApiInfo("GET", "/", {"Action": "DeleteTranscodes", "Version": "2020-08-01"}, {}, {}),
            "DeleteMediaTosFile": ApiInfo("POST", "/", {"Action": "DeleteMediaTosFile", "Version": "2022-12-01"}, {}, {}),
            "GetFileInfos": ApiInfo("GET", "/", {"Action": "GetFileInfos", "Version": "2023-07-01"}, {}, {}),
            "GetMediaList": ApiInfo("GET", "/", {"Action": "GetMediaList", "Version": "2022-12-01"}, {}, {}),
            "DeleteMaterial": ApiInfo("GET", "/", {"Action": "DeleteMaterial", "Version": "2023-07-01"}, {}, {}),
            "GetSubtitleInfoList": ApiInfo("GET", "/", {"Action": "GetSubtitleInfoList", "Version": "2020-08-01"}, {}, {}),
            "UpdateSubtitleStatus": ApiInfo("GET", "/", {"Action": "UpdateSubtitleStatus", "Version": "2020-08-01"}, {}, {}),
            "UpdateSubtitleInfo": ApiInfo("GET", "/", {"Action": "UpdateSubtitleInfo", "Version": "2020-08-01"}, {}, {}),
            "GetAuditFramesForAudit": ApiInfo("GET", "/", {"Action": "GetAuditFramesForAudit", "Version": "2021-11-01"}, {}, {}),
            "GetMLFramesForAudit": ApiInfo("GET", "/", {"Action": "GetMLFramesForAudit", "Version": "2021-11-01"}, {}, {}),
            "GetBetterFramesForAudit": ApiInfo("GET", "/", {"Action": "GetBetterFramesForAudit", "Version": "2021-11-01"}, {}, {}),
            "GetAudioInfoForAudit": ApiInfo("GET", "/", {"Action": "GetAudioInfoForAudit", "Version": "2021-11-01"}, {}, {}),
            "GetAutomaticSpeechRecognitionForAudit": ApiInfo("GET", "/", {"Action": "GetAutomaticSpeechRecognitionForAudit", "Version": "2021-11-01"}, {}, {}),
            "GetAudioEventDetectionForAudit": ApiInfo("GET", "/", {"Action": "GetAudioEventDetectionForAudit", "Version": "2021-11-01"}, {}, {}),
            "CreateVideoClassification": ApiInfo("GET", "/", {"Action": "CreateVideoClassification", "Version": "2021-01-01"}, {}, {}),
            "UpdateVideoClassification": ApiInfo("GET", "/", {"Action": "UpdateVideoClassification", "Version": "2021-01-01"}, {}, {}),
            "DeleteVideoClassification": ApiInfo("GET", "/", {"Action": "DeleteVideoClassification", "Version": "2021-01-01"}, {}, {}),
            "ListVideoClassifications": ApiInfo("GET", "/", {"Action": "ListVideoClassifications", "Version": "2021-01-01"}, {}, {}),
            "ListSnapshots": ApiInfo("GET", "/", {"Action": "ListSnapshots", "Version": "2021-01-01"}, {}, {}),
            "ExtractMediaMetaTask": ApiInfo("GET", "/", {"Action": "ExtractMediaMetaTask", "Version": "2022-01-01"}, {}, {}),
            #Object
            "SubmitBlockObjectTasks": ApiInfo("POST", "/",{"Action": "SubmitBlockObjectTasks", "Version": "2023-07-01"},{}, {}),
            "ListBlockObjectTasks": ApiInfo("POST", "/",{"Action": "ListBlockObjectTasks", "Version": "2023-07-01"},{}, {}),
            # 转码
            "StartWorkflow": ApiInfo("GET", "/", {"Action": "StartWorkflow", "Version": "2020-08-01"}, {}, {}),
            "RetrieveTranscodeResult": ApiInfo("GET", "/", {"Action": "RetrieveTranscodeResult", "Version": "2020-08-01"}, {}, {}),
            "GetWorkflowExecution": ApiInfo("GET", "/", {"Action": "GetWorkflowExecution", "Version": "2020-08-01"}, {}, {}),
            "GetWorkflowExecutionResult": ApiInfo("GET", "/", {"Action": "GetWorkflowExecutionResult", "Version": "2022-12-01"}, {}, {}),
            "GetTaskTemplate": ApiInfo("GET", "/", {"Action": "GetTaskTemplate", "Version": "2023-07-01"}, {},{}),
            "CreateTaskTemplate": ApiInfo("POST", "/", {"Action": "CreateTaskTemplate", "Version": "2023-07-01"}, {}, {}),
            "UpdateTaskTemplate": ApiInfo("POST", "/", {"Action": "UpdateTaskTemplate", "Version": "2023-07-01"}, {}, {}),
            "ListTaskTemplate": ApiInfo("GET", "/", {"Action": "ListTaskTemplate", "Version": "2023-07-01"}, {}, {}),
            "DeleteTaskTemplate": ApiInfo("POST", "/", {"Action": "DeleteTaskTemplate", "Version": "2023-07-01"}, {}, {}),
            "GetWorkflowTemplate": ApiInfo("GET", "/", {"Action": "GetWorkflowTemplate", "Version": "2023-07-01"}, {}, {}),
            "CreateWorkflowTemplate": ApiInfo("POST", "/", {"Action": "CreateWorkflowTemplate", "Version": "2023-07-01"}, {}, {}),
            "UpdateWorkflowTemplate": ApiInfo("POST", "/", {"Action": "UpdateWorkflowTemplate", "Version": "2023-07-01"}, {}, {}),
            "ListWorkflowTemplate": ApiInfo("GET", "/", {"Action": "ListWorkflowTemplate", "Version": "2023-07-01"}, {}, {}),
            "DeleteWorkflowTemplate": ApiInfo("POST", "/", {"Action": "DeleteWorkflowTemplate", "Version": "2023-07-01"}, {},{}),
            "GetWatermarkTemplate": ApiInfo("GET", "/", {"Action": "GetWatermarkTemplate", "Version": "2023-07-01"}, {}, {}),
            "CreateWatermarkTemplate": ApiInfo("POST", "/", {"Action": "CreateWatermarkTemplate", "Version": "2023-07-01"}, {}, {}),
            "UpdateWatermarkTemplate": ApiInfo("POST", "/", {"Action": "UpdateWatermarkTemplate", "Version": "2023-07-01"}, {}, {}),
            "ListWatermarkTemplate": ApiInfo("GET", "/", {"Action": "ListWatermarkTemplate", "Version": "2023-07-01"}, {}, {}),
            "DeleteWatermarkTemplate": ApiInfo("POST", "/", {"Action": "DeleteWatermarkTemplate", "Version": "2023-07-01"}, {}, {}),
            # 空间管理
            "DeleteSpace": ApiInfo("GET", "/", {"Action": "DeleteSpace", "Version": "2023-07-01"}, {}, {}),
            "CreateSpace": ApiInfo("GET", "/", {"Action": "CreateSpace", "Version": "2021-01-01"}, {}, {}),
            "ListSpace": ApiInfo("GET", "/", {"Action": "ListSpace", "Version": "2021-01-01"}, {}, {}),
            "GetSpaceDetail": ApiInfo("GET", "/", {"Action": "GetSpaceDetail", "Version": "2022-01-01"}, {}, {}),
            "UpdateSpace": ApiInfo("GET", "/", {"Action": "UpdateSpace", "Version": "2021-01-01"}, {}, {}),
            "UpdateSpaceUploadConfig": ApiInfo("GET", "/", {"Action": "UpdateSpaceUploadConfig", "Version": "2022-01-01"}, {}, {}),
            "DescribeVodSpaceStorageData": ApiInfo("GET", "/", {"Action": "DescribeVodSpaceStorageData", "Version": "2023-07-01"}, {}, {}),
            "DescribeUploadSpaceConfig": ApiInfo("GET", "/", {"Action": "DescribeUploadSpaceConfig", "Version": "2023-07-01"}, {}, {}),
            "UpdateUploadSpaceConfig": ApiInfo("POST", "/", {"Action": "UpdateUploadSpaceConfig", "Version": "2023-07-01"}, {}, {}),
            # 分发加速
            "AddDomainToScheduler": ApiInfo("GET", "/", {"Action": "AddDomainToScheduler", "Version": "2023-07-01"}, {}, {}),
            "RemoveDomainFromScheduler": ApiInfo("GET", "/", {"Action": "RemoveDomainFromScheduler", "Version": "2023-07-01"}, {}, {}),
            "UpdateDomainPlayRule": ApiInfo("GET", "/", {"Action": "UpdateDomainPlayRule", "Version": "2023-07-01"}, {}, {}),
            "StartDomain": ApiInfo("GET", "/", {"Action": "StartDomain", "Version": "2023-07-01"}, {}, {}),
            "StopDomain": ApiInfo("GET", "/", {"Action": "StopDomain", "Version": "2023-07-01"}, {}, {}),
            "DeleteDomain": ApiInfo("GET", "/", {"Action": "DeleteDomain", "Version": "2023-07-01"}, {}, {}),
            "ListDomain": ApiInfo("GET", "/", {"Action": "ListDomain", "Version": "2023-01-01"}, {}, {}),
            "CreateCdnRefreshTask": ApiInfo("GET", "/", {"Action": "CreateCdnRefreshTask", "Version": "2021-01-01"}, {}, {}),
            "CreateCdnPreloadTask": ApiInfo("GET", "/", {"Action": "CreateCdnPreloadTask", "Version": "2021-01-01"}, {}, {}),
            "ListCdnTasks": ApiInfo("GET", "/", {"Action": "ListCdnTasks", "Version": "2022-01-01"}, {}, {}),
            "ListCdnAccessLog": ApiInfo("GET", "/", {"Action": "ListCdnAccessLog", "Version": "2022-01-01"}, {}, {}),
            "ListCdnTopAccessUrl": ApiInfo("GET", "/", {"Action": "ListCdnTopAccessUrl", "Version": "2022-01-01"}, {}, {}),
            "ListCdnTopAccess": ApiInfo("GET", "/", {"Action": "ListCdnTopAccess", "Version": "2023-07-01"}, {}, {}),
            "DescribeVodDomainBandwidthData": ApiInfo("GET", "/", {"Action": "DescribeVodDomainBandwidthData", "Version": "2023-07-01"}, {}, {}),
            "DescribeVodDomainTrafficData": ApiInfo("GET", "/", {"Action": "DescribeVodDomainTrafficData", "Version": "2023-07-01"}, {}, {}),
            "ListCdnUsageData": ApiInfo("GET", "/", {"Action": "ListCdnUsageData", "Version": "2022-12-01"}, {}, {}),
            "ListCdnStatusData": ApiInfo("GET", "/", {"Action": "ListCdnStatusData", "Version": "2022-01-01"}, {}, {}),
            "DescribeIpInfo": ApiInfo("GET", "/", {"Action": "DescribeIpInfo", "Version": "2022-01-01"}, {}, {}),
            "ListCdnPvData": ApiInfo("GET", "/", {"Action": "ListCdnPvData", "Version": "2022-01-01"}, {}, {}),
            "SubmitBlockTasks": ApiInfo("POST", "/", {"Action": "SubmitBlockTasks", "Version": "2022-01-01"}, {}, {}),
            "GetContentBlockTasks": ApiInfo("POST", "/", {"Action": "GetContentBlockTasks", "Version": "2022-01-01"}, {}, {}),
            "ListFileMetaInfosByFileNames": ApiInfo("POST", "/", {"Action": "ListFileMetaInfosByFileNames", "Version": "2023-07-01"}, {}, {}),
            "CreateDomain": ApiInfo("GET", "/", {"Action": "CreateDomain", "Version": "2023-02-01"}, {}, {}),
            "UpdateDomainExpire": ApiInfo("GET", "/", {"Action": "UpdateDomainExpire", "Version": "2023-02-01"}, {}, {}),
            "UpdateDomainAuthConfig": ApiInfo("GET", "/", {"Action": "UpdateDomainAuthConfig", "Version": "2023-02-01"}, {}, {}),
            "AddOrUpdateCertificate": ApiInfo("POST", "/",{"Action": "AddOrUpdateCertificate", "Version": "2023-07-01"}, {}, {}),
            "UpdateDomainUrlAuthConfig": ApiInfo("GET", "/", {"Action": "UpdateDomainUrlAuthConfig", "Version": "2023-07-01"}, {}, {}),
            "UpdateDomainConfig": ApiInfo("GET", "/", {"Action": "UpdateDomainConfig", "Version": "2023-07-01"}, {}, {}),
            "DescribeDomainConfig": ApiInfo("GET", "/", {"Action": "DescribeDomainConfig", "Version": "2023-07-01"}, {}, {}),
            "VerifyDomainOwner": ApiInfo("GET", "/", {"Action": "VerifyDomainOwner", "Version": "2023-07-01"}, {}, {}),
            "DescribeDomainVerifyContent": ApiInfo("GET", "/", {"Action": "DescribeDomainVerifyContent", "Version": "2023-07-01"}, {}, {}),
            # 回调管理
            "AddCallbackSubscription": ApiInfo("GET", "/", {"Action": "AddCallbackSubscription", "Version": "2021-12-01"}, {}, {}),
            "SetCallbackEvent": ApiInfo("GET", "/", {"Action": "SetCallbackEvent", "Version": "2022-01-01"}, {}, {}),
            # 视频编辑
            "SubmitDirectEditTaskAsync": ApiInfo("POST", "/",{"Action": "SubmitDirectEditTaskAsync", "Version": "2018-01-01"}, {},{}),
            "SubmitDirectEditTaskSync": ApiInfo("POST", "/",{"Action": "SubmitDirectEditTaskSync", "Version": "2018-01-01"}, {},{}),
            "GetDirectEditResult": ApiInfo("POST", "/", {"Action": "GetDirectEditResult", "Version": "2018-01-01"}, {}, {}),
            "GetDirectEditProgress": ApiInfo("GET", "/", {"Action": "GetDirectEditProgress", "Version": "2018-01-01"}, {}, {}),
            "CancelDirectEditTask": ApiInfo("POST", "/", {"Action": "CancelDirectEditTask", "Version": "2018-01-01"}, {}, {}),
            # 计量计费
            "DescribeVodSpaceTranscodeData": ApiInfo("GET", "/", {"Action": "DescribeVodSpaceTranscodeData", "Version": "2023-07-01"}, {}, {}),
            "DescribeVodSpaceAIStatisData": ApiInfo("GET", "/", {"Action": "DescribeVodSpaceAIStatisData", "Version": "2023-07-01"}, {}, {}),
            "DescribeVodSpaceSubtitleStatisData": ApiInfo("GET", "/", {"Action": "DescribeVodSpaceSubtitleStatisData", "Version": "2023-07-01"}, {}, {}),
            "DescribeVodSpaceDetectStatisData": ApiInfo("GET", "/", {"Action": "DescribeVodSpaceDetectStatisData", "Version": "2023-07-01"}, {}, {}),
            "DescribeVodSnapshotData": ApiInfo("GET", "/", {"Action": "DescribeVodSnapshotData", "Version": "2023-07-01"}, {}, {}),
            "DescribeVodSpaceWorkflowDetailData": ApiInfo("GET", "/", {"Action": "DescribeVodSpaceWorkflowDetailData", "Version": "2023-07-01"}, {}, {}),
            "DescribeVodSpaceEditDetailData": ApiInfo("GET", "/", {"Action": "DescribeVodSpaceEditDetailData", "Version": "2023-07-01"}, {}, {}),
            "DescribeVodEnhanceImageData": ApiInfo("GET", "/", {"Action": "DescribeVodEnhanceImageData", "Version": "2023-07-01"}, {}, {}),
            "DescribeVodSpaceEditStatisData": ApiInfo("GET", "/", {"Action": "DescribeVodSpaceEditStatisData", "Version": "2023-07-01"}, {}, {}),
            "DescribeVodPlayedStatisData": ApiInfo("GET", "/", {"Action": "DescribeVodPlayedStatisData", "Version": "2023-07-01"}, {}, {}),
            "DescribeVodMostPlayedStatisData": ApiInfo("GET", "/", {"Action": "DescribeVodMostPlayedStatisData", "Version": "2023-07-01"}, {}, {}),
            "DescribeVodRealtimeMediaData": ApiInfo("GET", "/", {"Action": "DescribeVodRealtimeMediaData", "Version": "2023-07-01"}, {}, {}),
            "DescribeVodRealtimeMediaDetailData": ApiInfo("GET", "/", {"Action": "DescribeVodRealtimeMediaDetailData", "Version": "2023-07-01"}, {}, {}),
            "DescribeVodVidTrafficFileLog": ApiInfo("GET", "/", {"Action": "DescribeVodVidTrafficFileLog", "Version": "2023-07-01"}, {}, {})
        }
        return api_info

    @staticmethod
    def crc32(file_path):
        prev = 0
        for eachLine in open(file_path, "rb"):
            prev = crc32(eachLine, prev)
        return prev & 0xFFFFFFFF
