# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import DescribeVodMostPlayedStatisDataRequest

if __name__ == '__main__':
    vod_service = VodService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('your ak')
    vod_service.set_sk('your sk')
    try:
        req = DescribeVodMostPlayedStatisDataRequest()
        req.Space = 'your Space'
        req.StartTime = 'your StartTime'
        req.EndTime = 'your EndTime'
        req.OrderType = 'your OrderType'
        req.TopN = 0
        resp = vod_service.describe_vod_most_played_statis_data(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code != '':
            print(resp.ResponseMetadata.Error)
            