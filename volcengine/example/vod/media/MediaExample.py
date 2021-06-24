# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodGetMediaInfosRequest, VodGetRecommendedPosterRequest, \
    VodUpdateMediaPublishStatusRequest, VodUpdateMediaInfoRequest, VodDeleteMediaRequest, VodDeleteTranscodesRequest, \
    VodGetSubtitleInfoListRequest, VodUpdateSubtitleStatusRequest, VodUpdateSubtitleInfoRequest, VodGetMediaListRequest

if __name__ == '__main__':
    vod_service = VodService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    # vod_service.set_ak('your ak')
    # vod_service.set_sk('your sk')

    try:
        vids = 'vid1,vid2'
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
        vids = 'vid1,vid2'
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
        status = 'Unpublished'
        req3 = VodUpdateMediaPublishStatusRequest()
        req3.Vid = vid
        req3.Status = status
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
        tags = 'aaa,bbb'
        req4 = VodUpdateMediaInfoRequest()
        req4.Vid = vid
        req4.Tags.value = tags
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

    try:
        vids = 'vid1,vid2'
        callBackArgs = 'CallBackArgs'
        req5 = VodDeleteMediaRequest()
        req5.Vids = vids
        req5.CallbackArgs = callBackArgs
        resp5 = vod_service.delete_media(req5)
    except Exception:
        raise
    else:
        print(resp5)
        if resp5.ResponseMetadata.Error.Code == '':
            print('delete media info success')
        else:
            print(resp5.ResponseMetadata.Error)

    print('*' * 100)

    try:
        vid = 'vid'
        fileIds = 'fileId1,fileId2'
        callBackArgs = 'CallBackArgs'
        req6 = VodDeleteTranscodesRequest()
        req6.Vid = vid
        req6.FileIds = fileIds
        req6.CallbackArgs = callBackArgs
        resp6 = vod_service.delete_transcodes(req6)
    except Exception:
        raise
    else:
        print(resp6)
        if resp6.ResponseMetadata.Error.Code == '':
            print('delete transcodes info success')
        else:
            print(resp6.ResponseMetadata.Error)

    print('*' * 100)

    try:
        req7 = VodGetMediaListRequest()
        req7.SpaceName = 'your space name'
        req7.Vid = 'your vid'
        req7.Status = 'Published'  #Published/Unpublished
        req7.Order = 'Desc'        #Desc/Asc
        req7.StartTime = '1999-01-01T00:00:00Z'
        req7.EndTime = '2021-04-01T00:00:00Z'
        req7.Offset = '0'
        req7.PageSize = '10'
        resp7 = vod_service.get_media_list(req7)
    except Exception:
        raise
    else:
        print(resp7)
        if resp7.ResponseMetadata.Error.Code == '':
            print(resp7.Result)
        else:
            print(resp7.ResponseMetadata.Error)

    print('*' * 100)
