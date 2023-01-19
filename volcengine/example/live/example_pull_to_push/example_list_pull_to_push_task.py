# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.request_live_pb2 import ListPullToPushTaskRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    req = ListPullToPushTaskRequest()
    req.Title = 'Title'
    req.Page = 0
    req.Size = 0
    print(req)
    resp = live_service.list_pull_to_push_task(req)
    print(resp)

