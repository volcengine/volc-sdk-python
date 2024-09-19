# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodGetMediaInfosRequest, VodGetRecommendedPosterRequest, \
    VodUpdateMediaPublishStatusRequest, VodUpdateMediaInfoRequest, VodDeleteMediaRequest, VodDeleteTranscodesRequest, \
    VodGetMediaListRequest, VodCreateVideoClassificationRequest, VodUpdateVideoClassificationRequest, \
    VodDeleteVideoClassificationRequest, VodListVideoClassificationsRequest, VodListSnapshotsRequest, \
    VodUpdateMediaStorageClassRequest, VodExtractMediaMetaTaskRequest

if __name__ == '__main__':
    # Create a VOD instance in the specified region.
    # vod_service = VodService('cn-north-1')
    vod_service = VodService()

    # Configure your Access Key ID (AK) and Secret Access Key (SK) in the environment variables or in the local ~/.volc/config file. For detailed instructions, see https://www.volcengine.com/docs/4/65646.
    # The SDK will automatically fetch the AK and SK from the environment variables or the ~/.volc/config file as needed.
    # During testing, you may use the following code snippet. However, do not store the AK and SK directly in your project code to prevent potential leakage and safeguard the security of all resources associated with your account.
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
        req4 = VodUpdateMediaInfoRequest()
        req4.Vid = 'vid'
        req4.Title.value = 'title'
        req4.Description.value = 'description'
        req4.Tags.value = 'tag1,tag2'
        req4.ClassificationId.value = 0
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
        req7.ClassificationId = 1
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

    try:
        req8 = VodCreateVideoClassificationRequest()
        req8.SpaceName = 'your space'
        req8.Level = 1
        req8.ParentId = 0
        req8.Classification = 'your classification'
        resp8 = vod_service.create_video_classification(req8)
    except Exception:
        raise
    else:
        print(resp8)
        if resp8.ResponseMetadata.Error.Code == '':
            print(resp8.Result)
        else:
            print(resp8.ResponseMetadata.Error)

    print('*' * 100)

    try:
        req9 = VodUpdateVideoClassificationRequest()
        req9.SpaceName = 'your space'
        req9.ClassificationId = 0
        req9.Classification = 'your classification'
        resp9 = vod_service.update_video_classification(req9)
    except Exception:
        raise
    else:
        print(resp9)
        if resp9.ResponseMetadata.Error.Code == '':
            print(resp9.Result)
        else:
            print(resp9.ResponseMetadata.Error)

    print('*' * 100)

    try:
        req10 = VodDeleteVideoClassificationRequest()
        req10.SpaceName = 'your space'
        req10.ClassificationId = 0
        resp10 = vod_service.delete_video_classification(req10)
    except Exception:
        raise
    else:
        print(resp10)
        if resp10.ResponseMetadata.Error.Code == '':
            print(resp10.Result)
        else:
            print(resp10.ResponseMetadata.Error)

    print('*' * 100)

    try:
        req11 = VodListVideoClassificationsRequest()
        req11.SpaceName = 'your space'
        req11.ClassificationId = 0
        resp11 = vod_service.list_video_classifications(req11)
    except Exception:
        raise
    else:
        print(resp11)
        if resp11.ResponseMetadata.Error.Code == '':
            print(resp11.Result)
        else:
            print(resp11.ResponseMetadata.Error)

    print('*' * 100)

    try:
        req12 = VodListSnapshotsRequest()
        req12.Vid = "your vid"
        resp12 = vod_service.list_snapshots(req12)
    except Exception:
        raise
    else:
        print(resp12)
        if resp12.ResponseMetadata.Error.Code == '':
            print(resp12.Result)
        else:
            print(resp12.ResponseMetadata.Error)

    try:
        vids = "vid1"
        fileIds = "fileid1"
        req13 = VodUpdateMediaStorageClassRequest()
        req13.Vids = vids
        req13.FileIds = fileIds
        req13.StorageClass = "your storage class"
        req13.CallbackArgs = "your callbackargs"
        resp13 = vod_service.update_media_storage_class(req13)
    except Exception:
        raise
    else:
        print(resp13)
        if resp13.ResponseMetadata.Error.Code == '':
            print(resp13.Result)
        else:
            print(resp13.ResponseMetadata.Error)

    print('*' * 100)

    try:
        req14 = VodExtractMediaMetaTaskRequest()
        req14.Vid = "vid"
        resp14 = vod_service.extract_media_meta_task(req14)
    except Exception:
        raise
    else:
        print(resp14)
        if resp14.ResponseMetadata.Error.Code == '':
            print(resp14.Result)
        else:
            print(resp14.ResponseMetadata.Error)

    print('*' * 100)
