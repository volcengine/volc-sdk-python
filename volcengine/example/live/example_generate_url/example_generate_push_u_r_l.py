# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.request_live_pb2 import GeneratePushURLRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    req = GeneratePushURLRequest()
    req.Vhost = 'Vhost'
    req.App = 'App'
    req.Stream = 'Stream'
    req.ValidDuration = 'ValidDuration'
    req.ExpiredTime = '2022-11-24T00:00:00+08:00'

    print(req)
    resp = live_service.generate_push_u_r_l(req)
    print(resp)