# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.request_live_pb2 import CreatePullToPushTaskRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    req = CreatePullToPushTaskRequest()
    req.Title = 'Title'
    req.Type = 0
    req.CycleMode = 0

    req.DstAddr = 'DstAddr'
    req.SrcAddr = 'SrcAddr'
    req.SrcAddrS.extend(['SrcAddrS'])

    print(req)
    resp = live_service.create_pull_to_push_task(req)
    print(resp)

