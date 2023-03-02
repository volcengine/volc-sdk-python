# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.live_requests import ListVQScoreTaskRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    req = ListVQScoreTaskRequest()
    req.StartTime = ''
    req.EndTime = ''
    # req.PageNum = 0
    # req.PageSize = 0
    req.Status = 0

    print(req)
    resp = live_service.list_v_q_score_task(req)
    print(resp)
