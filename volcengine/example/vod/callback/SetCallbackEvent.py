# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodSetCallbackEventRequest

if __name__ == '__main__':
    vod_service = VodService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('your ak')
    vod_service.set_sk('your sk')
    try:
        req = VodSetCallbackEventRequest()
        req.SpaceName = 'your space name'
        # AuthEnabled 1: enable;0: disable
        req.AuthEnabled = '1'
        req.PrivateKey = 'your private key'
        resp = vod_service.set_callback_event(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code != '':
            print(resp.ResponseMetadata.Error)
            