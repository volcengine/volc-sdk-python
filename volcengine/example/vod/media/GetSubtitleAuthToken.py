# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodGetSubtitleInfoListRequest

if __name__ == '__main__':
    vod_service = VodService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    # vod_service.set_ak('your ak')
    # vod_service.set_sk('your sk')

    try:
        req11 = VodGetSubtitleInfoListRequest()
        req11.Vid = 'vid'

        token = vod_service.get_subtitle_auth_token(req11, 60)
    except Exception:
        raise
    else:
        print(token)

    print('*' * 100)