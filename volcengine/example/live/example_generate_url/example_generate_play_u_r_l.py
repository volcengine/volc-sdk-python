# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.request_live_pb2 import GeneratePlayURLRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    req = GeneratePlayURLRequest()
    req.Vhost = 'Vhost'
    req.Domain = 'Domain'
    req.App = 'App'
    req.Stream = 'Stream'
    req.Type = 'Type'
    req.ValidDuration = "ValidDuration"
    req.ExpiredTime = '2022-11-24T00:00:00+08:00'

    print(req)
    resp = live_service.generate_play_u_r_l(req)
    print(resp)