# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodGetPlayInfoWithLiveTimeShiftSceneRequest

if __name__ == '__main__':
    vod_service = VodService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('***REMOVED***')
    vod_service.set_sk('***REMOVED***')
    try:
        req = VodGetPlayInfoWithLiveTimeShiftSceneRequest()
        req.StoreUris = 'tos-cn-v-76d802/5f488325972b4fb2adf935a6b22ac8b1.m3u8'
        req.SpaceName = 'qwe'
        req.Ssl = 0
        req.ExpireTimestamp = 1675216800000
        req.NeedComposeBucketName = 0
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
