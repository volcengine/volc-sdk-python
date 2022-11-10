# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.request_live_pb2 import RestartPullToPushTaskRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    req = RestartPullToPushTaskRequest()
    req.TaskId = 'TaskId'
    print(req)
    resp = live_service.restart_pull_to_push_task(req)
    print(resp)