# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.live_requests import GeneratePlayURLRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    req = GeneratePlayURLRequest()
    req.Vhost = ''
    req.Domain = ''
    req.App = ''
    req.Stream = ''
    req.Suffix = ''
    req.Type = ''
    req.ValidDuration = 1
    req.ExpiredTime = ''

    print(req)
    resp = live_service.generate_play_u_r_l(req)
    print(resp)