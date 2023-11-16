# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodListFileMetaInfosByFileNamesRequest

if __name__ == '__main__':
    vod_service = VodService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('')
    vod_service.set_sk('')
    try:
        req = VodListFileMetaInfosByFileNamesRequest()
        req.SpaceName = 'spacename'
        req.BucketName = 'bucketname'
        req.FileNameEncodeds = 'a/b/c/d.jpg'
        resp = vod_service.list_file_meta_infos_by_file_names(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result)
        else:
            print(resp.ResponseMetadata.Error)
    print('*' * 100)
