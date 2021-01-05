import json
import os
import time
from zlib import crc32

from retry import retry
from volcengine.Policy import Statement, Policy
from volcengine.models.vod.request.request_vod_pb2 import VodCommitUploadInfoRequest, VodApplyUploadInfoRequest
from volcengine.vod.VodService import VodService
from volcengine.vod.VodUploadService import VodUploadService

MinChunkSize = 1024 * 1024 * 20
LargeFileSize = 1024 * 1024 * 1024


class VodUploadServiceWrapper(VodUploadService):
    def upload_media(self, request):
        oid, session_key, avg_speed = self.upload_tob(request.SpaceName, request.FilePath)

        req = VodCommitUploadInfoRequest()
        req.SpaceName = request.SpaceName
        req.SessionKey = session_key
        req.Functions = request.Functions
        req.CallbackArgs = request.CallbackArgs

        resp = self.commit_upload_info(req)
        if resp.ResponseMetadata.Error.Code != '':
            print(resp.ResponseMetadata.RequestId)
            raise Exception(resp.ResponseMetadata.Error)
        return resp

    def upload_tob(self, space_name, file_path):
        if not os.path.isfile(file_path):
            raise Exception("no such file on file path")

        apply_req = VodApplyUploadInfoRequest()
        apply_req.SpaceName = space_name
        resp = self.apply_upload_info(apply_req)
        if resp.ResponseMetadata.Error.Code != '':
            print(resp.ResponseMetadata.RequestId)
            raise Exception(resp.ResponseMetadata.Error)

        upload_address = resp.Result.Data.UploadAddress
        oid = upload_address.StoreInfos[0].StoreUri
        session_key = upload_address.SessionKey
        auth = upload_address.StoreInfos[0].Auth
        host = upload_address.UploadHosts[0]

        start = time.time()
        file_size = os.path.getsize(file_path)
        if file_size < MinChunkSize:
            self.direct_upload(host, oid, auth, file_path)
        elif file_size > LargeFileSize:
            self.chunk_upload(file_path, host, oid, auth, file_size, True)
        else:
            self.chunk_upload(file_path, host, oid, auth, file_size, False)
        cost = (time.time() - start) * 1000
        file_size = os.path.getsize(file_path)
        avg_speed = float(file_size) / float(cost)

        return oid, session_key, avg_speed

    @retry(tries=3, delay=1, backoff=2)
    def direct_upload(self, host, oid, auth, file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
            check_sum = crc32(data) & 0xFFFFFFFF
        check_sum = "%08x" % check_sum
        url = 'http://{}/{}'.format(host, oid)
        headers = {'Content-CRC32': check_sum, 'Authorization': auth}
        upload_status, resp = self.put(url, file_path, headers)
        if not upload_status:
            raise Exception("direct upload error")
        resp = json.loads(resp)
        if resp.get('success') is None or resp['success'] != 0:
            raise Exception("direct upload error")

    def chunk_upload(self, file_path, host, oid, auth, size, is_large_file):
        upload_id = self.init_upload_part(host, oid, auth, is_large_file)
        n = size // MinChunkSize
        last_num = n - 1
        parts = []
        with open(file_path, 'rb') as f:
            for i in range(0, last_num):
                data = f.read(MinChunkSize)
                part = self.upload_part(host, oid, auth, upload_id, i, data, is_large_file)
                parts.append(part)
            data = f.read()
            part = self.upload_part(host, oid, auth, upload_id, last_num, data, is_large_file)
            parts.append(part)
        return self.upload_merge_part(host, oid, auth, upload_id, parts, is_large_file)

    @retry(tries=3, delay=1, backoff=2)
    def init_upload_part(self, host, oid, auth, is_large_file):
        url = 'http://{}/{}?uploads'.format(host, oid)
        headers = {'Authorization': auth}
        if is_large_file:
            headers['X-Storage-Mode'] = 'gateway'
        upload_status, resp = self.put_data(url, None, headers)
        resp = json.loads(resp)
        if not upload_status:
            raise Exception("init upload error")
        if resp.get('success') is None or resp['success'] != 0:
            raise Exception("init upload error")
        return resp['payload']['uploadID']

    @retry(tries=3, delay=1, backoff=2)
    def upload_part(self, host, oid, auth, upload_id, part_number, data, is_large_file):
        url = 'http://{}/{}?partNumber={}&uploadID={}'.format(host, oid,
                                                              part_number, upload_id)
        check_sum = crc32(data) & 0xFFFFFFFF
        check_sum = "%08x" % check_sum
        headers = {'Content-CRC32': check_sum, 'Authorization': auth}
        if is_large_file:
            headers['X-Storage-Mode'] = 'gateway'
        upload_status, resp = self.put_data(url, data, headers)
        if not upload_status:
            raise Exception(url + json.dumps(resp))
        resp = json.loads(resp)
        if resp.get('success') is None or resp['success'] != 0:
            raise Exception("upload part error")
        return check_sum

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
    def upload_merge_part(self, host, oid, auth, upload_id, check_sum_list, is_large_file):
        url = 'http://{}/{}?uploadID={}'.format(host, oid, upload_id)
        data = self.generate_merge_body(check_sum_list)
        headers = {'Authorization': auth}
        if is_large_file:
            headers['X-Storage-Mode'] = 'gateway'
        upload_status, resp = self.put_data(url, data, headers)
        resp = json.loads(resp)
        if not upload_status:
            raise Exception("init upload error")
        if resp.get('success') is None or resp['success'] != 0:
            raise Exception("init upload error")

    def get_upload_sts2_with_expired_time(self, expired_time):
        actions = ["vod:ApplyUploadInfo", "vod:CommitUploadInfo"]
        resources = []
        statement = Statement.new_allow_statement(actions, resources)
        inline_policy = Policy([statement])
        return self.sign_sts2(inline_policy, expired_time)

    def get_upload_sts2(self):
        return self.get_upload_sts2_with_expired_time(60 * 60)
