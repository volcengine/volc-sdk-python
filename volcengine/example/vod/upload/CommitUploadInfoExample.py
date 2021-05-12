# coding:utf-8
from __future__ import print_function

import json

from volcengine.util.Functions import Function
from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodCommitUploadInfoRequest

if __name__ == '__main__':
    vod_service = VodService()

    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('your ak')
    vod_service.set_sk('your sk')

    space_name = 'your space'
    session = ''
    try:
        req = VodCommitUploadInfoRequest()
        req.SpaceName = space_name
        req.SessionKey = session
        get_meta_function = Function.get_meta_func()
        snapshot_function = Function.get_snapshot_func(2.3)
        req.Functions = json.dumps([get_meta_function, snapshot_function])
        resp = vod_service.commit_upload_info(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result.Data)
            print(resp.Result.Data.Vid)
            print(resp.Result.Data.PosterUri)
            print(resp.Result.Data.SourceInfo.Height)
            print(resp.Result.Data.SourceInfo.Width)
        else:
            print(resp.ResponseMetadata.Error)
            print(resp.ResponseMetadata.RequestId)
