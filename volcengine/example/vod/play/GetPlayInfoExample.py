# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodGetPlayInfoRequest

if __name__ == '__main__':
    vod_service = VodService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    # vod_service.set_ak('ak')
    # vod_service.set_sk('sk')
    try:
        vid = 'your vid'
        req = VodGetPlayInfoRequest()
        req.Vid = vid
        req.Ssl = '1'
        resp = vod_service.get_play_info(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result.PlayInfoList[0].MainPlayUrl)
        else:
            print(resp.ResponseMetadata.Error)
    print('*' * 100)
