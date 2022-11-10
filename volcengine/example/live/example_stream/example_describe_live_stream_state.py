# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.request_live_pb2 import DescribeLiveStreamStateRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    req = DescribeLiveStreamStateRequest()
    req.Vhost = 'Vhost'
    req.App = 'App'
    req.Stream = 'Stream'
    print(req)
    resp = live_service.describe_live_stream_state(req)
    print(resp)

