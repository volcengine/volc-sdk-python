# coding:utf-8
from __future__ import print_function

from volcengine.models.vod.request.request_vod_pb2 import *
from volcengine.vod.VodService import VodService

if __name__ == '__main__':

    vod_service = VodService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    # vod_service.set_ak('ak')
    # vod_service.set_sk('sk')
    try:
        vid = 'your vid'
        req = VodGetPlayInfoRequest()
        req.Vid = vid
        resp = vod_service.get_play_auth_token(req)
    except Exception:
        raise
    else:
        print(resp)
    print('*' * 100)
