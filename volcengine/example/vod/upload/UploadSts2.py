# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService

if __name__ == '__main__':
    vod_service = VodService()

    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('your ak')
    vod_service.set_sk('your sk')
    sts2 = vod_service.get_upload_sts2_with_expired_time(60 * 60)
    print(sts2)

    sts2 = vod_service.get_upload_sts2()
    print(sts2)
