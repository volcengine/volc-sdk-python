# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.live_requests import CreatePullToPushTaskRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')

    req = CreatePullToPushTaskRequest()
    req.Title = ''
    req.Type = 0
    req.CycleMode = 0
    req.StartTime = 0
    req.EndTime = 0
    req.DstAddr = ''
    req.SrcAddr = ''
    req.SrcAddrS = []
    req.SrcAddrS.extend([''])
    print(req)
    resp = live_service.create_pull_to_push_task(req)
    print(resp)

