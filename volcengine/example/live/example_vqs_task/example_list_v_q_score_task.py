# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.request_live_pb2 import  ListVQScoreTaskRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    req = ListVQScoreTaskRequest()
    req.StartTime = '2022-10-21T00:00:00+08:00'
    req.EndTime = '2022-10-24T00:00:00+08:00'
    req.PageNum = 0
    req.PageSize = 0
    req.Status = 0

    print(req)
    resp = live_service.list_v_q_score_task(req)
    print(resp)
