# coding:utf-8
import json
import os
import queue
import threading
from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service
from volcengine.const.Const import *
from volcengine.util.Util import *
from volcengine.Policy import *

IMAGEX_SERVICE_NAME = "ImageX"
IMAGEX_API_VERSION = "2018-08-01"

ResourceServiceIdTRN = "trn:ImageX:*:*:ServiceId/%s"
ResourceStoreKeyTRN = "trn:ImageX:*:*:StoreKeys/%s"

UPLOAD_THREADS = 3

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
    # 模板管理
    "CreateImageTemplate":
        ApiInfo("POST", "/", {"Action": "CreateImageTemplate",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    "DeleteImageTemplate":
        ApiInfo("POST", "/", {"Action": "DeleteImageTemplate",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    "PreviewImageTemplate":
        ApiInfo("POST", "/", {"Action": "PreviewImageTemplate",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageTemplate":
        ApiInfo("GET", "/", {"Action": "GetImageTemplate",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetAllImageTemplates":
        ApiInfo("GET", "/", {"Action": "GetAllImageTemplates",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    # 资源管理相关
    "ApplyImageUpload":
        ApiInfo("GET", "/", {"Action": "ApplyImageUpload",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    "CommitImageUpload":
        ApiInfo("POST", "/", {"Action": "CommitImageUpload",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    "DeleteImageUploadFiles":
        ApiInfo("POST", "/", {"Action": "DeleteImageUploadFiles",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    "UpdateImageUploadFiles":
        ApiInfo("POST", "/", {"Action": "UpdateImageUploadFiles",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    "PreviewImageUploadFile":
        ApiInfo("GET", "/", {"Action": "PreviewImageUploadFile",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageUploadFile":
        ApiInfo("GET", "/", {"Action": "GetImageUploadFile",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageUploadFiles":
        ApiInfo("GET", "/", {"Action": "GetImageUploadFiles",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageUpdateFiles":
        ApiInfo("GET", "/", {"Action": "GetImageUpdateFiles",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageOCR":
        ApiInfo("POST", "/", {"Action": "GetImageOCR",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetSegmentImage":
        ApiInfo("POST", "/", {"Action": "GetSegmentImage",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageQuality":
        ApiInfo("POST", "/", {"Action": "GetImageQuality",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageEraseModels":
        ApiInfo("GET", "/", {"Action": "GetImageEraseModels",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageEraseResult":
        ApiInfo("POST", "/", {"Action": "GetImageEraseResult",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageEnhanceResult":
        ApiInfo("POST", "/", {"Action": "GetImageEnhanceResult",
                              "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageBgFillResult":
        ApiInfo("POST", "/", {"Action": "GetImageBgFillResult",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageComicResult":
        ApiInfo("POST", "/", {"Action": "GetImageComicResult",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageSuperResolutionResult":
        ApiInfo("POST", "/", {"Action": "GetImageSuperResolutionResult",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetImageSmartCropResult":
        ApiInfo("POST", "/", {"Action": "GetImageSmartCropResult",
                "Version": IMAGEX_API_VERSION}, {}, {}),
    "GetLicensePlateDetection":
        ApiInfo("POST", "/", {"Action": "GetLicensePlateDetection",
                "Version": IMAGEX_API_VERSION}, {}, {})
}


class Uploader:
    def __init__(self, host, store_infos=[], datas=[]):
        self.host = host
        self.store_infos = store_infos
        self.datas = datas

        self.queue = queue.Queue()
        self.queue_lock = threading.Lock()

        for i in range(len(store_infos)):
            self.queue.put(i)

    def async_upload(self):
        while not self.queue.empty():
            self.queue_lock.acquire()
            if self.queue.empty():
                self.queue_lock.release()
                break
            idx = self.queue.get()
            self.queue_lock.release()
            self.upload_by_host(idx)

    def upload_by_host(self, idx):
        store_info = self.store_infos[idx]
        img_data = self.datas[idx]
        url = 'http://{}/{}'.format(self.host, store_info['StoreUri'])
        check_sum = crc32(img_data) & 0xFFFFFFFF
        check_sum = "%08x" % check_sum
        headers = {'Content-CRC32': check_sum, 'Authorization': store_info['Auth']}
        upload_status, resp = ImageXService().put_data(url, img_data, headers)
        if not upload_status:
            raise Exception('upload by host: upload url %s status false, resp: %s' % (url, resp))


class ImageXService(Service):
    def __init__(self, region=REGION_CN_NORTH1):
        self.service_info = ImageXService.get_service_info(region)
        self.api_info = ImageXService.get_api_info()
        super(ImageXService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(region):
        service_info = service_info_map.get(region, None)
        if not service_info:
            raise Exception('ImageX not support region %s' % region)
        return service_info

    @staticmethod
    def get_api_info():
        return api_info

    # upload
    def apply_upload(self, params):
        res = self.get('ApplyImageUpload', params, doseq=1)
        if res == '':
            raise Exception("ApplyImageUpload: empty response")
        res_json = json.loads(res)
        return res_json

    def commit_upload(self, params, body):
        res = self.json('CommitImageUpload', params, body)
        if res == '':
            raise Exception("CommitImageUpload: empty response")
        res_json = json.loads(res)
        return res_json

    # upload local image file
    def upload_image(self, params, file_paths):
        img_datas = []
        for p in file_paths:
            if not os.path.isfile(p):
                raise Exception("no such file on file path %s" % p)
            in_file = open(p, "rb")
            img_datas.append(in_file.read())
            in_file.close()
        return self.upload_image_data(params, img_datas)

    # upload image data
    def upload_image_data(self, params, img_datas):
        for data in img_datas:
            if not isinstance(data, bytes):
                raise Exception("upload of non-bytes not supported")

        apply_upload_request = {
            'ServiceId': params['ServiceId'],
            'SessionKey': params.get('SessionKey', ''),
            'UploadNum': len(img_datas),
            'StoreKeys': params.get('StoreKeys', []),
        }
        resp = self.apply_upload(apply_upload_request)
        if 'Error' in resp['ResponseMetadata']:
            raise Exception(resp['ResponseMetadata'])

        result = resp['Result']
        reqid = result['RequestId']
        addr = result['UploadAddress']
        if len(addr['UploadHosts']) == 0:
            raise Exception("no upload host found, reqid %s" % reqid)
        elif len(addr['StoreInfos']) != len(img_datas):
            raise Exception("store info len %d != upload num %d, reqid %s" % (
                len(result['StoreInfos']), len(img_datas), reqid))

        session_key = addr['SessionKey']
        host = addr['UploadHosts'][0]
        self.do_upload(img_datas, host, addr['StoreInfos'])

        commit_upload_request = {
            'ServiceId': params['ServiceId'],
        }
        commit_upload_body = {
            'SessionKey': session_key,
            'Functions': params.get('Functions', []),
            'OptionInfos': params.get('OptionInfos', [])
        }
        resp = self.commit_upload(
            commit_upload_request, json.dumps(commit_upload_body))
        if 'Error' in resp['ResponseMetadata']:
            raise Exception(resp['ResponseMetadata'])
        return resp['Result']

    def do_upload(self, img_datas, host, store_infos):
        threads = []
        uploader = Uploader(host, store_infos, img_datas)
        for i in range(UPLOAD_THREADS):
            thread = threading.Thread(target=uploader.async_upload)
            thread.start()
            threads.append(thread)

        for i in range(UPLOAD_THREADS):
            threads[i].join()

    def get_upload_auth_token(self, params):
        apply_token = self.get_sign_url('ApplyImageUpload', params)
        commit_token = self.get_sign_url('CommitImageUpload', params)

        ret = {'Version': 'v1', 'ApplyUploadToken': apply_token,
               'CommitUploadToken': commit_token}
        data = json.dumps(ret)
        if sys.version_info[0] == 3:
            return base64.b64encode(data.encode('utf-8')).decode('utf-8')
        else:
            return base64.b64encode(data.decode('utf-8'))

    def get_upload_auth(self, service_ids, expire=60*60, key_ptn=''):
        apply_res = []
        commit_res = []
        if len(service_ids) == 0:
            apply_res.append(ResourceServiceIdTRN % '*')
            commit_res.append(ResourceServiceIdTRN % '*')
        else:
            for sid in service_ids:
                apply_res.append(ResourceServiceIdTRN % sid)
                commit_res.append(ResourceServiceIdTRN % sid)
        apply_res.append(ResourceStoreKeyTRN % key_ptn)

        inline_policy = Policy([
            Statement.new_allow_statement(
                ['ImageX:ApplyImageUpload'], apply_res),
            Statement.new_allow_statement(
                ['ImageX:CommitImageUpload'], commit_res)
        ])
        return self.sign_sts2(inline_policy, expire)

    def delete_images(self, service_id, uris):
        query = {
            'ServiceId': service_id
        }
        body = {
            'StoreUris': uris
        }
        res = self.json('DeleteImageUploadFiles', query, json.dumps(body))
        if res == '':
            raise Exception("DeleteImageUploadFiles: empty response")
        res_json = json.loads(res)
        if 'Error' in res_json['ResponseMetadata']:
            raise Exception(res_json['ResponseMetadata'])
        return res_json['Result']

    # action=0: refresh
    # action=1: disable
    # action=2: enable
    def update_image_urls(self, service_id, urls, action=0):
        if action < 0 or action > 2:
            raise Exception("update action should be [0,2], %d" % action)

        query = {
            'ServiceId': service_id
        }
        body = {
            'Action': action,
            'ImageUrls': urls
        }
        res = self.json("UpdateImageUploadFiles", query, json.dumps(body))
        if res == '':
            raise Exception("UpdateImageUploadFiles: empty response")
        res_json = json.loads(res)
        if 'Error' in res_json['ResponseMetadata']:
            raise Exception(res_json['ResponseMetadata'])
        return res_json['Result']

    def get_image_info(self, service_id, store_uri):
        query = {
            'ServiceId': service_id,
            'StoreUri': store_uri,
        }
        res = self.get('PreviewImageUploadFile', query)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        if 'Error' in res_json['ResponseMetadata']:
            raise Exception(res_json['ResponseMetadata'])
        return res_json['Result']

    def imagex_get(self, action, params, doseq=0):
        res = self.get(action, params, doseq)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(json.dumps(res))
        return res_json

    def imagex_post(self, action, params, body):
        res = self.json(action, params, body)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(json.dumps(res))
        return res_json

    def get_image_ocr(self, params):
        res = self.post('GetImageOCR', params, {})
        if res == '':
            raise Exception("%s: empty response" % 'GetImageOCR')
        res_json = json.loads(res)
        return res_json

    def get_image_segment(self, params):
        res = self.post('GetSegmentImage', params, {})
        if res == '':
            raise Exception("%s: empty response" % 'GetSegmentImage')
        res_json = json.loads(res)
        return res_json

    def get_image_quality(self, params):
        body = {
            'ImageUrl': params['ImageUrl'],
            'VqType':  params.get('VqType', None)
        }
        res = self.imagex_post('GetImageQuality', params, json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'GetImageQuality')
        res_json = json.loads(res)
        return res_json

    def get_image_erase_models(self, params):
        res = self.imagex_get('GetImageEraseModels', params)
        if res == '':
            raise Exception("%s: empty response" % 'GetImageEraseModels')
        res_json = json.loads(res)
        return res_json

    def get_image_erase_result(self, params):
        body = {
            'ServiceId': params['ServiceId'],
            'StoreUri': params['StoreUri'],
            'Model': params['Model'],
            'BBox': params.get('BBox', None)
        }
        res = self.imagex_post('GetImageEraseResult', params, json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'GetImageEraseResult')
        res_json = json.loads(res)
        return res_json

    def get_image_enhance_result(self, params):
        body = {
            'ServiceId': params['ServiceId'],
            'StoreUri': params['StoreUri'],
            'Model': params['Model'],
            'DisableAr': params.get('DisableAr', None),
            'DisableSharp': params.get('DisableSharp', None),
            'Resolution': params.get('Resolution', None)
        }
        res = self.imagex_post('GetImageEnhanceResult', params, json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'GetImageEnhanceResult')
        res_json = json.loads(res)
        return res_json

    def get_image_bg_fill_result(self, params):
        body = {
            'ServiceId': params['ServiceId'],
            'StoreUri': params['StoreUri'],
            'Model': params['Model'],
            'Top': params.get('Top', None),
            'Bottom': params.get('Bottom', None),
            'Left': params.get('Left', None),
            'Right': params.get('Right', None)
        }
        res = self.imagex_post('GetImageBgFillResult', params, json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'GetImageBgFillResult')
        res_json = json.loads(res)
        return res_json

    def get_image_comic_result(self, params):
        body = {
            'ServiceId': params['ServiceId'],
            'StoreUri': params['StoreUri']
        }
        res = self.imagex_post('GetImageComicResult', params, json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'GetImageComicResult')
        res_json = json.loads(res)
        return res_json

    def get_image_super_resolution_result(self, params):
        body = {
            'ServiceId': params['ServiceId'],
            'StoreUri': params['StoreUri'],
            'Multiple': params.get('Multiple', None)
        }
        res = self.imagex_post('GetImageSuperResolutionResult', params, json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'GetImageSuperResolutionResult')
        res_json = json.loads(res)
        return res_json

    def get_license_plate_detection(self, params):
        body = {
            'ImageUri': params['ImageUri']
        }
        res = self.imagex_post('GetLicensePlateDetection', params, json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'GetLicensePlateDetection')
        res_json = json.loads(res)
        return res_json