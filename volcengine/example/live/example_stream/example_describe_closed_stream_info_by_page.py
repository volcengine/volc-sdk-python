# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.request_live_pb2 import DescribeClosedStreamInfoByPageRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    req = DescribeClosedStreamInfoByPageRequest()
    req.Vhost = 'Vhost'
    req.PageNum = 0
    req.PageSize = 0
    print(req)
    resp = live_service.describe_closed_stream_info_by_page(req)
    print(resp)

