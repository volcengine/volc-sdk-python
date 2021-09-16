# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodGetPrivateDrmPlayAuthRequest

if __name__ == '__main__':

    vod_service = VodService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('your ak')
    vod_service.set_sk('your sk')
    try:
        vid = 'your vid'
        req = VodGetPrivateDrmPlayAuthRequest()
        req.Vid = vid
        req.DrmType = 'your drm type'
        req.PlayAuthIds = 'a,b,c (your PlayAuthIds)'
        req.UnionInfo = 'your unionInfo'
        expire = 60  # seconds
        resp = vod_service.get_private_drm_play_auth_token(req, expire)
    except Exception:
        raise
    else:
        print(resp)
    print('*' * 100)
