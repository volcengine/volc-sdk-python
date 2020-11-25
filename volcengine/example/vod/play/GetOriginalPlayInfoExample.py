# coding:utf-8
from __future__ import print_function

from volcengine.models.vod.request.request_vod_pb2 import *
from volcengine.vod.VodPlayService import VodPlayService

if __name__ == '__main__':
    vod_service = VodPlayService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    # vod_service.set_ak('ak')
    # vod_service.set_sk('sk')
    try:
        vid = 'v0c2c369007abu04ru8riko30uo9n73g'
        req2 = VodGetOriginalPlayInfoRequest()
        req2.Vid = vid
        req2.Ssl = '1'
        resp2 = vod_service.get_original_play_info(req2)
    except Exception:
        raise
    else:
        print(resp2)
        if resp2.ResponseMetadata.Error.Code == '':
            print(resp2.Result.MainPlayUrl)
        else:
            print(resp2.ResponseMetadata.Error)

    print('*' * 100)