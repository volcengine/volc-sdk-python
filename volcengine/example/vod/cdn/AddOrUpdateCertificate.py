# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import AddOrUpdateCertificateV2Request

if __name__ == '__main__':
    vod_service = VodService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('your ak')
    vod_service.set_sk('your sk')
    try:
        req = AddOrUpdateCertificateV2Request()
        req.SpaceName = 'your space name'
        req.Domain = 'your domain'
        req.DomainType = 'your DomainType'
        req.CertificateId = 'your CertificateId'
        req.HttpsStatus = 'your HttpsStatus'
        resp = vod_service.add_or_update_certificate(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code != '':
            print(resp.ResponseMetadata.Error)
