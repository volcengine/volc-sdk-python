# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.live_requests import GeneratePushURLRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    req = GeneratePushURLRequest()
    req.Vhost = ''
    req.App = ''
    req.Stream = ''
    req.ValidDuration = 0
    req.ExpiredTime = ''

    print(req)
    resp = live_service.generate_push_u_r_l(req)
    print(resp)