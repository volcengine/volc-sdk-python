# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodGetPlayInfoWithLiveTimeShiftSceneRequest

if __name__ == '__main__':
    vod_service = VodService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('your ak')
    vod_service.set_sk('your sk')
    try:
        req = VodGetPlayInfoWithLiveTimeShiftSceneRequest()

        req.StoreUris = 'uri1,uri2,uri3'
        req.SpaceName = 'your space name'
        req.Ssl = '0 or 1'
        req.ExpireTimestamp = 'unix timestamp'
        req.NeedComposeBucketName = '0 or 1'
        resp = vod_service.get_play_info_with_live_time_shift_scene(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result.PlayInfoList[0].MainPlayUrl)
        else:
            print(resp.ResponseMetadata.Error)
    print('*' * 100)
