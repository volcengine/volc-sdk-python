# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.request_live_pb2 import DescribeDenyConfigRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    req = DescribeDenyConfigRequest()
    req.Vhost = 'vhost'
    req.Domain = 'domain'
    print(req)
    resp = live_service.describe_deny_config(req)
    print(resp)

