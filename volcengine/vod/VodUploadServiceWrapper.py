import os
import time

from volcengine.Policy import Statement, Policy
from volcengine.models.vod.request.request_vod_pb2 import VodCommitUploadInfoRequest, VodApplyUploadInfoRequest
from volcengine.vod.VodService import VodService
from volcengine.vod.VodUploadService import VodUploadService


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
        check_sum = hex(VodService.crc32(file_path))[2:]

        apply_req = VodApplyUploadInfoRequest()
        apply_req.SpaceName = space_name
        resp = self.apply_upload_info(apply_req)
        if resp.ResponseMetadata.Error.Code != '':
            print(resp.ResponseMetadata.RequestId)
            raise Exception(resp.ResponseMetadata.Error)

        # # TODO 1G以上文件增加Header
        upload_address = resp.Result.Data.UploadAddress
        oid = upload_address.StoreInfos[0].StoreUri
        session_key = upload_address.SessionKey
        auth = upload_address.StoreInfos[0].Auth
        host = upload_address.UploadHosts[0]
        url = 'http://{}/{}'.format(host, oid)
        headers = {'Content-CRC32': check_sum, 'Authorization': auth}
        start = time.time()

        upload_status = False
        for i in range(3):
            upload_status, resp = self.put(url, file_path, headers)
            if upload_status:
                break
            else:
                print(resp)
        if not upload_status:
            raise Exception("upload error")

        cost = (time.time() - start) * 1000
        file_size = os.path.getsize(file_path)
        avg_speed = float(file_size) / float(cost)

        return oid, session_key, avg_speed

    def get_upload_sts2_with_expired_time(self, expired_time):
        actions = ["vod:ApplyUploadInfo", "vod:CommitUploadInfo"]
        resources = []
        statement = Statement.new_allow_statement(actions, resources)
        inline_policy = Policy([statement])
        return self.sign_sts2(inline_policy, expired_time)

    def get_upload_sts2(self):
        return self.get_upload_sts2_with_expired_time(60 * 60)
