# coding:utf-8
from __future__ import print_function

from volcengine.models.vod.request.request_vod_pb2 import *
from volcengine.vod.VodMediaService import VodMediaService

if __name__ == '__main__':
    vod_service = VodMediaService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('your ak')
    vod_service.set_sk('your sk')
    try:
        vids = 'vid1,aaaaaaa'
        req = VodGetMediaInfosRequest()
        req.Vids = vids
        resp = vod_service.get_media_infos(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result)
        else:
            print(resp.ResponseMetadata.Error)
    print('*' * 100)

    try:
        vids = 'vid1,aaaaaaa'
        req2 = VodGetRecommendedPosterRequest()
        req2.Vids = vids
        resp2 = vod_service.get_recommended_poster(req2)
    except Exception:
        raise
    else:
        print(resp2)
        if resp2.ResponseMetadata.Error.Code == '':
            print(resp2.Result)
        else:
            print(resp2.ResponseMetadata.Error)

    print('*' * 100)

    try:
        vid = 'vid'
        req3 = VodUpdateMediaPublishStatusRequest()
        req3.Vid = vid
        req3.Status = 'Unpublished'
        resp3 = vod_service.update_media_publish_status(req3)
    except Exception:
        raise
    else:
        print(resp3)
        if resp3.ResponseMetadata.Error.Code == '':
            print('update media publish status success')
        else:
            print(resp3.ResponseMetadata.Error)

    print('*' * 100)

    try:
        vid = 'vid'
        req4 = VodUpdateMediaInfoRequest()
        req4.Vid = vid
        req4.Tags.value = 'aaa,bbb'
        resp4 = vod_service.update_media_info(req4)
    except Exception:
        raise
    else:
        print(resp4)
        if resp4.ResponseMetadata.Error.Code == '':
            print('update media info success')
        else:
            print(resp4.ResponseMetadata.Error)

    print('*' * 100)
