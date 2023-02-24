# coding:utf-8
from __future__ import print_function

import json

from volcengine.util.Functions import Function
from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodUploadMediaRequest

if __name__ == '__main__':
    vod_service = VodService()

    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('your ak')
    vod_service.set_sk('your sk')

    space_name = 'your space name'
    file_path = 'your file path'

    get_meta_function = Function.get_meta_func()
    snapshot_function = Function.get_snapshot_func(2.3)

    try:
        req = VodUploadMediaRequest()
        req.SpaceName = space_name
        req.FilePath = file_path
        req.Functions = json.dumps([get_meta_function, snapshot_function])
        req.CallbackArgs = ''
        req.FileName = ''
        req.FileExtension = '.mp4'
        req.StorageClass = 0
        resp = vod_service.upload_media(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result.Data)
            print(resp.Result.Data.Vid)
            print(resp.Result.Data.PosterUri)
            print(resp.Result.Data.SourceInfo.FileName)
            print(resp.Result.Data.SourceInfo.Height)
            print(resp.Result.Data.SourceInfo.Width)
        else:
            print(resp.ResponseMetadata.Error)
            print(resp.ResponseMetadata.RequestId)
