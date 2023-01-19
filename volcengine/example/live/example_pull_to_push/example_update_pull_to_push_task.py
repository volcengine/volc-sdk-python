# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.live_requests import UpdatePullToPushTaskRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')

    req = UpdatePullToPushTaskRequest()
    req.Title = ''
    req.Type = 1
    req.CycleMode = -1
    req.StartTime = 0
    req.EndTime = 0
    req.TaskId = ''
    req.DstAddr = ''
    req.SrcAddr = ''
    req.SrcAddrS = []
    req.SrcAddrS.extend([''])

    print(req)
    resp = live_service.update_pull_to_push_task(req)
    print(resp)