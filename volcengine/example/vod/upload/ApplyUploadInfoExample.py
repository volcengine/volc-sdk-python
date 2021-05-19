# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodApplyUploadInfoRequest

if __name__ == '__main__':
    vod_service = VodService()

    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('your ak')
    vod_service.set_sk('your sk')

    space_name = 'your space'

    try:
        req = VodApplyUploadInfoRequest()
        req.SpaceName = space_name

        resp = vod_service.apply_upload_info(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result.Data)
            print(resp.Result.Data.UploadAddress.StoreInfos[0].StoreUri)
            print(resp.Result.Data.UploadAddress.StoreInfos[0].Auth)
            print(resp.Result.Data.UploadAddress.UploadHosts[0])
            print(resp.Result.Data.UploadAddress.SessionKey)
        else:
            print(resp.ResponseMetadata.Error)
            print(resp.ResponseMetadata.RequestId)

