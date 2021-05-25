# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodUrlUploadRequest

if __name__ == '__main__':
    vod_service = VodService()

    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('your ak')
    vod_service.set_sk('your sk')

    space_name = 'your space'
    url = 'url'

    try:
        req = VodUrlUploadRequest()
        req.SpaceName = space_name
        url_set = req.URLSets.add()
        url_set.SourceUrl = url
        resp = vod_service.upload_media_by_url(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result.Data)
            print(resp.Result.Data[0].JobId)
            print(resp.Result.Data[0].SourceUrl)
        else:
            print(resp.ResponseMetadata.Error)
            print(resp.ResponseMetadata.RequestId)
