# coding:utf-8
from __future__ import print_function

from volcengine.models.vod.request.request_vod_pb2 import *
from volcengine.vod.VodPlayServiceWrapper import VodPlayServiceWrapper

if __name__ == '__main__':

    vod_service_wrapper = VodPlayServiceWrapper()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    # vod_service_wrapper.set_ak('ak')
    # vod_service_wrapper.set_sk('sk')
    try:
        vid = 'your vid'
        req3 = VodGetPlayInfoRequest()
        req3.Vid = vid
        resp3 = vod_service_wrapper.get_play_auth_token(req3)
    except Exception:
        raise
    else:
        print(resp3)
    print('*' * 100)
