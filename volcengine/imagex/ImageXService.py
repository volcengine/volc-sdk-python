# coding:utf-8
import json
import os
from six.moves import queue
import threading
from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service
from volcengine.const.Const import *
from volcengine.util.Util import *
from volcengine.Policy import *
from volcengine.imagex.ImageXConfig import *
from retry import retry


class Uploader:
    def __init__(self, imagex_service, host, store_infos=None, file_paths_or_bytes=None):
        if store_infos is None:
            store_infos = []
        if file_paths_or_bytes is None:
            file_paths_or_bytes = []

        self.imagex_service = imagex_service
        self.host = host
        self.store_infos = store_infos
        self.file_paths_or_bytes = file_paths_or_bytes

        self.queue = queue.Queue()
        self.queue_lock = threading.Lock()

        self.successOids = []
        self.results = []

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

            store_info = self.store_infos[idx]
            file_paths_or_bytes = self.file_paths_or_bytes[idx]

            try:
                if isinstance(file_paths_or_bytes, bytes):
                    self.upload_by_host(store_info, file_paths_or_bytes)
                elif isinstance(file_paths_or_bytes, str):
                    file_path = file_paths_or_bytes
                    file_size = os.path.getsize(file_path)
                    data = open(file_path, "rb")
                    if file_size < MinChunkSize:
                        self.upload_by_host(store_info, data.read())
                    elif file_size > LargeFileSize:
                        self.chunk_upload(store_info, data, file_size, True)
                    else:
                        self.chunk_upload(store_info, data, file_size, False)
                    data.close()
                else:
                    raise Exception("Uploader only accept bytes or path data")
                self.successOids.append(store_info['StoreUri'])
                self.results.append({
                    'Uri': store_info['StoreUri'],
                    'UriStatus': 2000,
                })
            except Exception as e:
                self.results.append({
                    'Uri': store_info['StoreUri'],
                    'UriStatus': 2001,
                    'Error': e,
                })

    @retry(tries=3, delay=1, backoff=2)
    def upload_by_host(self, store_info, img_data):
        url = 'https://{}/{}'.format(self.host, store_info['StoreUri'])
        check_sum = crc32(img_data) & 0xFFFFFFFF
        check_sum = "%08x" % check_sum
        headers = {'Content-CRC32': check_sum, 'Authorization': store_info['Auth']}
        upload_status, resp = self.imagex_service.put_data(url, img_data, headers)
        if not upload_status:
            raise Exception('upload by host: upload url %s status false, resp: %s' % (url, resp))

    def chunk_upload(self, store_info, f, size, is_large_file):
        upload_id = self.init_upload_part(store_info, is_large_file)
        n = size // MinChunkSize
        last_num = n - 1
        parts = []
        for i in range(0, last_num):
            data = f.read(MinChunkSize)
            part_number = i
            if is_large_file:
                part_number = i + 1
            part = self.upload_part(store_info, upload_id, part_number, data, is_large_file)
            parts.append(part)
        data = f.read()
        if is_large_file:
            last_num = last_num + 1
        part = self.upload_part(store_info, upload_id, last_num, data, is_large_file)
        parts.append(part)
        return self.upload_merge_part(store_info, upload_id, parts, is_large_file)

    @retry(tries=3, delay=1, backoff=2)
    def init_upload_part(self, store_info, is_large_file):
        url = 'https://{}/{}?uploads'.format(self.host, store_info['StoreUri'])
        headers = {'Authorization': store_info['Auth']}
        if is_large_file:
            headers['X-Storage-Mode'] = 'gateway'
        upload_status, resp = self.imagex_service.put_data(url, None, headers)
        resp = json.loads(resp)
        if not upload_status:
            raise Exception("init upload error")
        if resp.get('success') is None or resp['success'] != 0:
            raise Exception("init upload error")
        return resp['payload']['uploadID']

    @retry(tries=3, delay=1, backoff=2)
    def upload_part(self, store_info, upload_id, part_number, data, is_large_file):
        url = 'https://{}/{}?partNumber={}&uploadID={}'.format(self.host, store_info['StoreUri'], part_number,
                                                               upload_id)
        check_sum = crc32(data) & 0xFFFFFFFF
        check_sum = "%08x" % check_sum
        headers = {'Content-CRC32': check_sum, 'Authorization': store_info['Auth']}
        if is_large_file:
            headers['X-Storage-Mode'] = 'gateway'
        upload_status, resp = self.imagex_service.put_data(url, data, headers)
        if not upload_status:
            raise Exception(url + json.dumps(resp))
        resp = json.loads(resp)
        if resp.get('success') is None or resp['success'] != 0:
            raise Exception("upload part error")
        return check_sum

    # noinspection DuplicatedCode
    @staticmethod
    def generate_merge_body(check_sum_list):
        if len(check_sum_list) == 0:
            raise Exception('crc32 list empty')
        s = []
        for i in range(len(check_sum_list)):
            s.append('{}:{}'.format(i, check_sum_list[i]))
        comma = ','
        return comma.join(s)

    @retry(tries=3, delay=1, backoff=2)
    def upload_merge_part(self, store_info, upload_id, check_sum_list, is_large_file):
        url = 'https://{}/{}?uploadID={}'.format(self.host, store_info['StoreUri'], upload_id)
        data = self.generate_merge_body(check_sum_list)
        headers = {'Authorization': store_info['Auth']}
        if is_large_file:
            headers['X-Storage-Mode'] = 'gateway'
        upload_status, resp = self.imagex_service.put_data(url, data, headers)
        resp = json.loads(resp)
        if not upload_status:
            raise Exception("init upload error")
        if resp.get('success') is None or resp['success'] != 0:
            raise Exception("init upload error")


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
    # noinspection DuplicatedCode
    def upload_image(self, params, file_paths):
        for p in file_paths:
            if not os.path.isfile(p):
                raise Exception("no such file on file path %s" % p)

        apply_upload_request = {
            'ServiceId': params['ServiceId'],
            'SessionKey': params.get('SessionKey', ''),
            'UploadNum': len(file_paths),
            'StoreKeys': params.get('StoreKeys', []),
            'Overwrite': str(params.get('Overwrite', False)),
        }
        resp = self.apply_upload(apply_upload_request)
        if 'Error' in resp['ResponseMetadata']:
            raise Exception(resp['ResponseMetadata'])

        result = resp['Result']
        reqid = result['RequestId']
        addr = result['UploadAddress']
        if len(addr['UploadHosts']) == 0:
            raise Exception("no upload host found, reqid %s" % reqid)
        elif len(addr['StoreInfos']) != len(file_paths):
            raise Exception("store info len %d != upload num %d, reqid %s" % (
                len(result['StoreInfos']), len(file_paths), reqid))

        session_key = addr['SessionKey']
        host = addr['UploadHosts'][0]
        uploader = self.do_upload(file_paths, host, addr['StoreInfos'])
        if len(uploader.successOids) == 0:
            raise Exception("no file uploaded")

        if params.get('SkipCommit', False):
            return {'Results': uploader.results}
        commit_upload_request = {
            'ServiceId': params['ServiceId'],
            'SkipMeta': params.get('SkipMeta', False)
        }
        commit_upload_body = {
            'SessionKey': session_key,
            'SuccessOids': uploader.successOids,
            'Functions': params.get('Functions', []),
            'OptionInfos': params.get('OptionInfos', [])
        }
        resp = self.commit_upload(
            commit_upload_request, json.dumps(commit_upload_body))
        if 'Error' in resp['ResponseMetadata']:
            raise Exception(resp['ResponseMetadata'])
        return resp['Result']

    # upload image data
    # noinspection DuplicatedCode
    def upload_image_data(self, params, img_datas):
        for data in img_datas:
            if not isinstance(data, bytes):
                raise Exception("upload of non-bytes not supported")

        apply_upload_request = {
            'ServiceId': params['ServiceId'],
            'SessionKey': params.get('SessionKey', ''),
            'UploadNum': len(img_datas),
            'StoreKeys': params.get('StoreKeys', []),
            'Overwrite': str(params.get('Overwrite', False)),
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
        uploader = self.do_upload(img_datas, host, addr['StoreInfos'])
        if len(uploader.successOids) == 0:
            raise Exception("no file uploaded")

        if params.get('SkipCommit', False):
            return {'Results': uploader.results}
        commit_upload_request = {
            'ServiceId': params['ServiceId'],
            'SkipMeta': params.get('SkipMeta', False)
        }
        commit_upload_body = {
            'SessionKey': session_key,
            'SuccessOids': uploader.successOids,
            'Functions': params.get('Functions', []),
            'OptionInfos': params.get('OptionInfos', [])
        }
        resp = self.commit_upload(
            commit_upload_request, json.dumps(commit_upload_body))
        if 'Error' in resp['ResponseMetadata']:
            raise Exception(resp['ResponseMetadata'])
        return resp['Result']

    def do_upload(self, file_paths_or_bytes, host, store_infos):
        threads = []
        uploader = Uploader(self, host, store_infos, file_paths_or_bytes)
        for i in range(UPLOAD_THREADS):
            thread = threading.Thread(target=uploader.async_upload)
            thread.start()
            threads.append(thread)
        for i in range(UPLOAD_THREADS):
            threads[i].join()
        return uploader

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

    # tag 字段如下，可选择所需字段传入
    # upload_policy_dict = {
    #     "FileSizeUpLimit": "xxx",
    #     "FileSizeBottomLimit": "xxx",
    #     "ContentTypeBlackList":[
    #         "xxx"
    #     ],
    #     "ContentTypeWhiteList":[
    #         "xxx"
    #     ]
    # }
    # policy_str = json.dumps(upload_policy_dict)
    #
    # tag = {
    #     "UploadOverwrite": "true",
    #     "UploadPolicy": policy_str,
    # }
    def get_upload_auth(self, service_ids, expire=60 * 60, key_ptn='', tag=dict):
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
        for k, v in tag.items():
            inline_policy.statements.append(Statement.new_allow_statement([k], [str(v)]))
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

    def create_image_content_task(self, args):
        query = {
            'ServiceId': args['ServiceId']
        }
        res = self.imagex_post('CreateImageContentTask', query, json.dumps(args))
        if res == '':
            raise Exception("%s: empty response" % 'CreateImageContentTask')
        res_json = json.loads(res)
        return res_json

    def get_image_content_task_detail(self, args):
        query = {
            'ServiceId': args['ServiceId']
        }
        res = self.imagex_post('GetImageContentTaskDetail', query, json.dumps(args))
        if res == '':
            raise Exception("%s: empty response" % 'CreateImageContentTask')
        res_json = json.loads(res)
        return res_json

    def get_image_content_block_list(self, args):
        query = {
            'ServiceId': args['ServiceId']
        }
        res = self.imagex_post('GetImageContentBlockList', query, json.dumps(args))
        if res == '':
            raise Exception("%s: empty response" % 'CreateImageContentTask')
        res_json = json.loads(res)
        return res_json

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

    def imagex_request(self, action, params, body, files):
        res = self.request(action, params, body, files)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(json.dumps(res))
        return res_json

    def fetch_image_url(self, request):
        res = self.imagex_post('FetchImageUrl', request, json.dumps(request))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        if 'Error' in res_json['ResponseMetadata']:
            raise Exception(res_json['ResponseMetadata'])
        return res_json['Result']

    def get_url_fetch_task(self, query):
        res = self.imagex_get('GetUrlFetchTask', query)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        if 'Error' in res_json['ResponseMetadata']:
            raise Exception(res_json['ResponseMetadata'])
        return res_json['Result']

    def update_image_storage_ttl(self, request):
        res = self.imagex_post('UpdateImageStorageTTL', {}, json.dumps(request))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        if 'Error' in res_json['ResponseMetadata']:
            raise Exception(res_json['ResponseMetadata'])
        return res_json['Result']

    def get_image_ocr_v2(self, params):
        query = {
            'ServiceId': params['ServiceId']
        }
        body = {
            'Scene': params['Scene'],
            'StoreUri': params.get('StoreUri', None),
            'ImageUrl': params.get('ImageUrl', None),
            'InstrumentName': params.get('InstrumentName', None)
        }
        res = self.imagex_post('GetImageOCRV2', query, json.dumps(body))
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
            'VqType': params.get('VqType', None)
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

    def get_image_enhance_result_with_data(self, input, data):
        params = {
            "ServiceId": input["ServiceId"]
        }
        res = self.imagex_request('GetImageEnhanceResultWithData', params, body={
            'Input': json.dumps(input),
        }, files={
            'Data': ('img', data),
        })
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

    def get_image_duplicate_detection(self, body):
        query = {
            'ServiceId': body['ServiceId'],
        }
        res = self.imagex_post('GetImageDuplicateDetection', query, json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'GetImageDuplicateDetection')
        res_json = json.loads(res)
        return res_json

    def get_image_duplicate_task_status(self, query):
        res = self.imagex_get('GetDedupTaskStatus', query)
        if res == '':
            raise Exception("%s: empty response" % 'GetDedupTaskStatus')
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

    def get_image_style_result(self, args):
        query = {
            'ServiceId': args['ServiceId'],
        }
        res = self.imagex_post('GetImageStyleResult', query, json.dumps(args))
        if res == '':
            raise Exception("%s: empty response" % 'GetImageStyleResult')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_domain_traffic_data(self, query):
        res = self.imagex_get('DescribeImageXDomainTrafficData', query)
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXDomainTrafficData')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_domain_bandwidth_data(self, query):
        res = self.imagex_get('DescribeImageXDomainBandwidthData', query)
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXDomainBandwidthData')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_bucket_usage(self, query):
        res = self.imagex_get('DescribeImageXBucketUsage', query)
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXBucketUsage')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_request_cnt_usage(self, query):
        res = self.imagex_get('DescribeImageXRequestCntUsage', query)
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXRequestCntUsage')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_base_op_usage(self, query):
        res = self.imagex_get('DescribeImageXBaseOpUsage', query)
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXBaseOpUsage')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_compress_usage(self, query):
        res = self.imagex_get('DescribeImageXCompressUsage', query)
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXCompressUsage')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_edge_request(self, query):
        res = self.imagex_get('DescribeImageXEdgeRequest', query)
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXEdgeRequest')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_hit_rate_traffic_data(self, query):
        res = self.imagex_get('DescribeImageXHitRateTrafficData', query)
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXHitRateTrafficData')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_hit_rate_request_data(self, query):
        res = self.imagex_get('DescribeImageXHitRateRequestData', query)
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXHitRateRequestData')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_cdntop_request_data(self, query):
        res = self.imagex_get('DescribeImageXCDNTopRequestData', query)
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXCDNTopRequestData')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_summary(self, query):
        res = self.imagex_get('DescribeImageXSummary', query)
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXSummary')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_edge_request_bandwidth(self, query):
        res = self.imagex_get('DescribeImageXEdgeRequestBandwidth', query)
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXEdgeRequestBandwidth')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_edge_request_traffic(self, query):
        res = self.imagex_get('DescribeImageXEdgeRequestTraffic', query)
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXEdgeRequestTraffic')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_edge_request_regions(self, query):
        res = self.imagex_get('DescribeImageXEdgeRequestRegions', query)
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXEdgeRequestRegions')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_mirror_request_traffic(self, body):
        res = self.imagex_post('DescribeImageXMirrorRequestTraffic', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXMirrorRequestTraffic')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_mirror_request_bandwidth(self, body):
        res = self.imagex_post('DescribeImageXMirrorRequestBandwidth', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXMirrorRequestBandwidth')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_mirror_request_http_code_by_time(self, body):
        res = self.imagex_post('DescribeImageXMirrorRequestHttpCodeByTime', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXMirrorRequestHttpCodeByTime')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_mirror_request_http_code_overview(self, body):
        res = self.imagex_post('DescribeImageXMirrorRequestHttpCodeOverview', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXMirrorRequestHttpCodeOverview')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_service_quality(self, query):
        res = self.imagex_get('DescribeImageXServiceQuality', query)
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXServiceQuality')
        res_json = json.loads(res)
        return res_json

    def get_imagex_query_apps(self, query):
        res = self.imagex_get('GetImageXQueryApps', query)
        if res == '':
            raise Exception("%s: empty response" % 'GetImageXQueryApps')
        res_json = json.loads(res)
        return res_json

    def get_imagex_query_regions(self, query):
        res = self.imagex_get('GetImageXQueryRegions', query)
        if res == '':
            raise Exception("%s: empty response" % 'GetImageXQueryRegions')
        res_json = json.loads(res)
        return res_json

    def get_imagex_query_dims(self, query):
        res = self.imagex_get('GetImageXQueryDims', query)
        if res == '':
            raise Exception("%s: empty response" % 'GetImageXQueryDims')
        res_json = json.loads(res)
        return res_json

    def get_imagex_query_vals(self, query):
        res = self.imagex_get('GetImageXQueryVals', query)
        if res == '':
            raise Exception("%s: empty response" % 'GetImageXQueryVals')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_upload_success_rate_by_time(self, body):
        res = self.imagex_post('DescribeImageXUploadSuccessRateByTime', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXUploadSuccessRateByTime')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_upload_error_code_all(self, body):
        res = self.imagex_post('DescribeImageXUploadErrorCodeAll', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXUploadErrorCodeAll')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_upload_error_code_by_time(self, body):
        res = self.imagex_post('DescribeImageXUploadErrorCodeByTime', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXUploadErrorCodeByTime')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_upload_count_by_time(self, body):
        res = self.imagex_post('DescribeImageXUploadCountByTime', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXUploadCountByTime')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_upload_file_size(self, body):
        res = self.imagex_post('DescribeImageXUploadFileSize', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXUploadFileSize')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_upload_speed(self, body):
        res = self.imagex_post('DescribeImageXUploadSpeed', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXUploadSpeed')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_upload_duration(self, body):
        res = self.imagex_post('DescribeImageXUploadDuration', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXUploadDuration')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_upload_segment_speed_by_time(self, body):
        res = self.imagex_post('DescribeImageXUploadSegmentSpeedByTime', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXUploadSegmentSpeedByTime')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_cdn_success_rate_by_time(self, body):
        res = self.imagex_post('DescribeImageXCdnSuccessRateByTime', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXCdnSuccessRateByTime')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_cdn_success_rate_all(self, body):
        res = self.imagex_post('DescribeImageXCdnSuccessRateAll', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXCdnSuccessRateAll')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_cdn_error_code_by_time(self, body):
        res = self.imagex_post('DescribeImageXCdnErrorCodeByTime', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXCdnErrorCodeByTime')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_cdn_error_code_all(self, body):
        res = self.imagex_post('DescribeImageXCdnErrorCodeAll', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXCdnErrorCodeAll')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_cdn_duration_detail_by_time(self, body):
        res = self.imagex_post('DescribeImageXCdnDurationDetailByTime', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXCdnDurationDetailByTime')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_cdn_duration_all(self, body):
        res = self.imagex_post('DescribeImageXCdnDurationAll', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXCdnDurationAll')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_cdn_reuse_rate_by_time(self, body):
        res = self.imagex_post('DescribeImageXCdnReuseRateByTime', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXCdnReuseRateByTime')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_cdn_reuse_rate_all(self, body):
        res = self.imagex_post('DescribeImageXCdnReuseRateAll', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXCdnReuseRateAll')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_cdn_protocol_rate_by_time(self, body):
        res = self.imagex_post('DescribeImageXCdnProtocolRateByTime', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXCdnProtocolRateByTime')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_client_error_code_all(self, body):
        res = self.imagex_post('DescribeImageXClientErrorCodeAll', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXClientErrorCodeAll')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_client_error_code_by_time(self, body):
        res = self.imagex_post('DescribeImageXClientErrorCodeByTime', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXClientErrorCodeByTime')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_client_decode_success_rate_by_time(self, body):
        res = self.imagex_post('DescribeImageXClientDecodeSuccessRateByTime', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXClientDecodeSuccessRateByTime')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_client_decode_duration_by_time(self, body):
        res = self.imagex_post('DescribeImageXClientDecodeDurationByTime', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXClientDecodeDurationByTime')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_client_queue_duration_by_time(self, body):
        res = self.imagex_post('DescribeImageXClientQueueDurationByTime', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXClientQueueDurationByTime')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_client_load_duration_all(self, body):
        res = self.imagex_post('DescribeImageXClientLoadDurationAll', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXClientLoadDurationAll')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_client_load_duration(self, body):
        res = self.imagex_post('DescribeImageXClientLoadDuration', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXClientLoadDuration')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_client_failure_rate(self, body):
        res = self.imagex_post('DescribeImageXClientFailureRate', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXClientFailureRate')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_client_sdk_ver_by_time(self, body):
        res = self.imagex_post('DescribeImageXClientSdkVerByTime', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXClientSdkVerByTime')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_client_file_size(self, body):
        res = self.imagex_post('DescribeImageXClientFileSize', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXClientFileSize')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_client_top_file_size(self, body):
        res = self.imagex_post('DescribeImageXClientTopFileSize', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXClientTopFileSize')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_client_count_by_time(self, body):
        res = self.imagex_post('DescribeImageXClientCountByTime', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXClientCountByTime')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_client_score_by_time(self, body):
        res = self.imagex_post('DescribeImageXClientScoreByTime', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXClientScoreByTime')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_client_demotion_rate_by_time(self, body):
        res = self.imagex_post('DescribeImageXClientDemotionRateByTime', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXClientDemotionRateByTime')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_client_top_demotion_url(self, body):
        res = self.imagex_post('DescribeImageXClientTopDemotionURL', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXClientTopDemotionURL')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_client_quality_rate_by_time(self, body):
        res = self.imagex_post('DescribeImageXClientQualityRateByTime', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXClientQualityRateByTime')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_client_top_quality_url(self, body):
        res = self.imagex_post('DescribeImageXClientTopQualityURL', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXClientTopQualityURL')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_sensible_count_by_time(self, body):
        res = self.imagex_post('DescribeImageXSensibleCountByTime', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXSensibleCountByTime')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_sensible_cache_hit_rate_by_time(self, body):
        res = self.imagex_post('DescribeImageXSensibleCacheHitRateByTime', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXSensibleCacheHitRateByTime')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_sensible_top_size_url(self, body):
        res = self.imagex_post('DescribeImageXSensibleTopSizeURL', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXSensibleTopSizeURL')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_sensible_top_ram_url(self, body):
        res = self.imagex_post('DescribeImageXSensibleTopRamURL', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXSensibleTopRamURL')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_sensible_top_resolution_url(self, body):
        res = self.imagex_post('DescribeImageXSensibleTopResolutionURL', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXSensibleTopResolutionURL')
        res_json = json.loads(res)
        return res_json

    def describe_imagex_sensible_top_unknown_url(self, body):
        res = self.imagex_post('DescribeImageXSensibleTopUnknownURL', [], json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageXSensibleTopUnknownURL')
        res_json = json.loads(res)
        return res_json

    def describeImageVolcCdnAccessLog(self, query, body):
        res = self.imagex_post('DescribeImageVolcCdnAccessLog', query, json.dumps(body))
        if res == '':
            raise Exception("%s: empty response" % 'DescribeImageVolcCdnAccessLog')
        res_json = json.loads(res)
        return res_json
