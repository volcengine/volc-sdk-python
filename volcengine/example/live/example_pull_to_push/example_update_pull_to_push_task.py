# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.request_live_pb2 import  UpdatePullToPushTaskRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    req = UpdatePullToPushTaskRequest()
    req.Title = 'Title'
    req.Type = 0
    req.CycleMode = 0
    req.TaskId = 'TaskId'
    req.DstAddr = 'DstAddr'
    req.SrcAddr = 'SrcAddr'
    req.SrcAddrS.extend(['SrcAddrS'])

    print(req)
    resp = live_service.update_pull_to_push_task(req)
    print(resp)