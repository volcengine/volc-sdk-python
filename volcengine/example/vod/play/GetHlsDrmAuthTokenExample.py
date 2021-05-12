# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService

if __name__ == '__main__':

    vod_service = VodService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('your ak')
    vod_service.set_sk('your sk')
    try:
        expireSeconds = 60000
        resp = vod_service.get_sha1_hls_drm_auth_token(expireSeconds)
    except Exception:
        raise
    else:
        print(resp)
    print('*' * 100)
