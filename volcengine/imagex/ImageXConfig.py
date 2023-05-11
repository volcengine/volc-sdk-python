# coding:utf-8
from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.const.Const import *

IMAGEX_SERVICE_NAME = "ImageX"
IMAGEX_API_VERSION = "2018-08-01"

ResourceServiceIdTRN = "trn:ImageX:*:*:ServiceId/%s"
ResourceStoreKeyTRN = "trn:ImageX:*:*:StoreKeys/%s"

UPLOAD_THREADS = 3

MinChunkSize = 1024 * 1024 * 20
LargeFileSize = 1024 * 1024 * 1024

service_info_map = {
    REGION_CN_NORTH1: ServiceInfo(
        "imagex.volcengineapi.com",
        {'Accept': 'application/json'},
        Credentials('', '', IMAGEX_SERVICE_NAME, REGION_CN_NORTH1),
        10, 10, "https"),
    REGION_AP_SINGAPORE1: ServiceInfo(
        "imagex-ap-singapore-1.volcengineapi.com",
        {'Accept': 'application/json'},
        Credentials('', '', IMAGEX_SERVICE_NAME, REGION_AP_SINGAPORE1),
        10, 10, "https"),
    REGION_US_EAST1: ServiceInfo(
        "imagex-us-east-1.volcengineapi.com",
        {'Accept': 'application/json'},
        Credentials('', '', IMAGEX_SERVICE_NAME, REGION_US_EAST1),
        10, 10, "https"),
}

api_info = {
    "GetImageServiceSubscription":
        ApiInfo("GET", "/", {"Action": "GetImageServiceSubscription", "Version": IMAGEX_API_VERSION}, {}, {}),
    "CreateImageService":
        ApiInfo("POST", "/", {"Action": "CreateImageService", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageService":
        ApiInfo("GET", "/", {"Action": "GetImageService", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetAllImageServices":
        ApiInfo("GET", "/", {"Action": "GetAllImageServices", "Version": IMAGEX_API_VERSION}, {}, {}),
    "DeleteImageService":
        ApiInfo("POST", "/", {"Action": "DeleteImageService", "Version": IMAGEX_API_VERSION}, {}, {}),
    "UpdateImageAuthKey":
        ApiInfo("POST", "/", {"Action": "UpdateImageAuthKey", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageAuthKey":
        ApiInfo("GET", "/", {"Action": "GetImageAuthKey", "Version": IMAGEX_API_VERSION}, {}, {}),
    "UpdateImageObjectAccess":
        ApiInfo("POST", "/", {"Action": "UpdateImageObjectAccess", "Version": IMAGEX_API_VERSION}, {}, {}),
    "UpdateImageMirrorConf":
        ApiInfo("POST", "/", {"Action": "UpdateImageMirrorConf", "Version": IMAGEX_API_VERSION}, {}, {}),
    "DelDomain":
        ApiInfo("POST", "/", {"Action": "DelDomain", "Version": IMAGEX_API_VERSION}, {}, {}),

    # 域名管理
    "GetServiceDomains":
        ApiInfo("GET", "/", {"Action": "GetServiceDomains", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetDomainConfig":
        ApiInfo("GET", "/", {"Action": "GetDomainConfig", "Version": IMAGEX_API_VERSION}, {}, {}),
    "SetDefaultDomain":
        ApiInfo("POST", "/", {"Action": "SetDefaultDomain", "Version": IMAGEX_API_VERSION}, {}, {}),
    "UpdateResponseHeader":
        ApiInfo("POST", "/", {"Action": "UpdateResponseHeader", "Version": IMAGEX_API_VERSION}, {}, {}),
    "UpdateRefer":
        ApiInfo("POST", "/", {"Action": "UpdateRefer", "Version": IMAGEX_API_VERSION}, {}, {}),
    "UpdateHttps":
        ApiInfo("POST", "/", {"Action": "UpdateHttps", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetResponseHeaderValidateKeys":
        ApiInfo("GET", "/", {"Action": "GetResponseHeaderValidateKeys", "Version": IMAGEX_API_VERSION}, {}, {}),

    # 模板管理
    "CreateImageTemplate":
        ApiInfo("POST", "/", {"Action": "CreateImageTemplate", "Version": IMAGEX_API_VERSION}, {}, {}),
    "DeleteImageTemplate":
        ApiInfo("POST", "/", {"Action": "DeleteImageTemplate", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageTemplate":
        ApiInfo("GET", "/", {"Action": "GetImageTemplate", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetAllImageTemplates":
        ApiInfo("GET", "/", {"Action": "GetAllImageTemplates", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetTemplatesFromBin":
        ApiInfo("GET", "/", {"Action": "GetTemplatesFromBin", "Version": IMAGEX_API_VERSION}, {}, {}),
    "CreateTemplatesFromBin":
        ApiInfo("POST", "/", {"Action": "CreateTemplatesFromBin", "Version": IMAGEX_API_VERSION}, {}, {}),
    "DeleteTemplatesFromBin":
        ApiInfo("POST", "/", {"Action": "DeleteTemplatesFromBin", "Version": IMAGEX_API_VERSION}, {}, {}),

    # 资源管理相关
    "ApplyImageUpload":
        ApiInfo("GET", "/", {"Action": "ApplyImageUpload", "Version": IMAGEX_API_VERSION}, {}, {}),
    "CommitImageUpload":
        ApiInfo("POST", "/", {"Action": "CommitImageUpload", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageUploadFile":
        ApiInfo("GET", "/", {"Action": "GetImageUploadFile", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageUploadFiles":
        ApiInfo("GET", "/", {"Action": "GetImageUploadFiles", "Version": IMAGEX_API_VERSION}, {}, {}),
    "DeleteImageUploadFiles":
        ApiInfo("POST", "/", {"Action": "DeleteImageUploadFiles", "Version": IMAGEX_API_VERSION}, {}, {}),
    "PreviewImageUploadFile":
        ApiInfo("GET", "/", {"Action": "PreviewImageUploadFile", "Version": IMAGEX_API_VERSION}, {}, {}),
    "CreateImageContentTask":
        ApiInfo("POST", "/", {"Action": "CreateImageContentTask", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageContentTaskDetail":
        ApiInfo("POST", "/", {"Action": "GetImageContentTaskDetail", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageContentBlockList":
        ApiInfo("POST", "/", {"Action": "GetImageContentBlockList", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageUpdateFiles":
        ApiInfo("GET", "/", {"Action": "GetImageUpdateFiles", "Version": IMAGEX_API_VERSION}, {}, {}),
    "FetchImageUrl":
        ApiInfo("POST", "/", {"Action": "FetchImageUrl", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetUrlFetchTask":
        ApiInfo("GET", "/", {"Action": "GetUrlFetchTask", "Version": IMAGEX_API_VERSION}, {}, {}),

    "UpdateServiceName":
        ApiInfo("POST", "/", {"Action": "UpdateServiceName", "Version": IMAGEX_API_VERSION}, {}, {}),
    "UpdateImageStorageTTL":
        ApiInfo("POST", "/", {"Action": "UpdateImageStorageTTL", "Version": IMAGEX_API_VERSION}, {}, {}),
    "DescribeImageVolcCdnAccessLog":
        ApiInfo("POST", "/", {"Action": "DescribeImageVolcCdnAccessLog", "Version": IMAGEX_API_VERSION}, {}, {}),

    # 其他 API
    "GetImageOCRV2":
        ApiInfo("POST", "/", {"Action": "GetImageOCRV2", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageQuality":
        ApiInfo("POST", "/", {"Action": "GetImageQuality", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageEraseModels":
        ApiInfo("GET", "/", {"Action": "GetImageEraseModels", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageEnhanceResult":
        ApiInfo("POST", "/", {"Action": "GetImageEnhanceResult", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageEnhanceResultWithData":
        ApiInfo("POST", "/", {"Action": "GetImageEnhanceResultWithData", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageBgFillResult":
        ApiInfo("POST", "/", {"Action": "GetImageBgFillResult", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageDuplicateDetection":
        ApiInfo("POST", "/", {"Action": "GetImageDuplicateDetection", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetDedupTaskStatus":
        ApiInfo("GET", "/", {"Action": "GetImageDuplicateDetection", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetDenoisingImage":
        ApiInfo("POST", "/", {"Action": "GetDenoisingImage", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetSegmentImage":
        ApiInfo("POST", "/", {"Action": "GetSegmentImage", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageComicResult":
        ApiInfo("POST", "/", {"Action": "GetImageComicResult", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageSuperResolutionResult":
        ApiInfo("POST", "/", {"Action": "GetImageSuperResolutionResult", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageSmartCropResult":
        ApiInfo("POST", "/", {"Action": "GetImageSmartCropResult", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetLicensePlateDetection":
        ApiInfo("POST", "/", {"Action": "GetLicensePlateDetection", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImagePSDetection":
        ApiInfo("POST", "/", {"Action": "GetImagePSDetection", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetPrivateImageType":
        ApiInfo("POST", "/", {"Action": "GetPrivateImageType", "Version": IMAGEX_API_VERSION}, {}, {}),
    "CreateImageHmEmbed":
        ApiInfo("POST", "/", {"Action": "CreateImageHmEmbed", "Version": IMAGEX_API_VERSION}, {}, {}),
    "CreateImageHmExtract":
        ApiInfo("POST", "/", {"Action": "CreateImageHmExtract", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageEraseResult":
        ApiInfo("POST", "/", {"Action": "GetImageEraseResult", "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageStyleResult":
        ApiInfo("POST", "/", {"Action": "GetImageStyleResult", "Version": IMAGEX_API_VERSION}, {}, {}),
}
