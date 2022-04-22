# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodUpdateSpaceUploadConfigRequest

if __name__ == '__main__':
    vod_service = VodService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('your ak')
    vod_service.set_sk('your sk')
    try:
        req = VodUpdateSpaceUploadConfigRequest()
        req.SpaceName = 'your space name'
        req.ConfigKey = 'your config key'
        req.ConfigValue = 'your config value'
        resp = vod_service.update_space_upload_config(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code != '':
            print(resp.ResponseMetadata.Error)
