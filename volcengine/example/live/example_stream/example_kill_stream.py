# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.request_live_pb2 import KillStreamRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    req = KillStreamRequest()
    req.Vhost = 'Vhost'
    req.App = 'App'
    req.Stream = 'Stream'
    print(req)
    resp = live_service.kill_stream(req)
    print(resp)