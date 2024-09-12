# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodGetFileInfosRequest
if __name__ == '__main__':
    vod_service = VodService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('ak')
    vod_service.set_sk('sk')

    try:
        req20 = VodGetFileInfosRequest()
        req20.SpaceName = "SpaceName"
        # url encode
        req20.EncodedFileNames = "EncodedFileNames"
        # non-required param
        req20.BucketName = "BucketName"
        req20.NeedDownloadUrl = True
        req20.DownloadUrlNetworkType = "NetworkType"
        req20.DownloadUrlExpire = 3600
        resp = vod_service.get_file_infos(req20)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result)
        else:
            print(resp.ResponseMetadata.Error)
    print('*' * 100)