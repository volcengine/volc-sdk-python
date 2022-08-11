# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodDescribeVodDomainBandwidthDataRequest

if __name__ == '__main__':
    vod_service = VodService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('your ak')
    vod_service.set_sk('your sk')
    try:
        req = VodDescribeVodDomainBandwidthDataRequest()
        req.DomainList = ""
        req.StartTime = ""
        req.EndTime = ""
        req.Aggregation = 0
        req.BandwidthType = ""
        req.Area = ""
        resp = vod_service.describe_vod_domain_bandwidth_data(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code != '':
            print(resp.ResponseMetadata.Error)
