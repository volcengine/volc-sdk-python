# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodUpdateDomainConfigRequest
from volcengine.vod.models.business.vod_cdn_pb2 import VodDomainConfig

if __name__ == '__main__':
    vod_service = VodService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('your ak')
    vod_service.set_sk('your sk')
    try:
        req = VodUpdateDomainConfigRequest()
        req.SpaceName = 'your space name'
        req.DomainType = 'your domain type'
        req.Domain = 'your domain'
        config = VodDomainConfig()
        req.Config.CopyFrom(config)
        resp = vod_service.update_domain_config(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code != '':
            print(resp.ResponseMetadata.Error)