# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.request_live_pb2 import DescribeRelaySourceRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    req = DescribeRelaySourceRequest()
    req.Vhost = 'Vhost'
    print(req)
    resp = live_service.describe_relay_source_v2(req)
    print(resp)

