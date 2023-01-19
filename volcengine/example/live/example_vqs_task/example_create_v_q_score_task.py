# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.live_requests import CreateVQScoreTaskRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    req = CreateVQScoreTaskRequest()
    req.MainAddr = ''
    req.ContrastAddr = ''
    req.FrameInterval = 0
    req.Duration = 700
    req.Algorithm = ''

    print(req.__dict__)
    resp = live_service.create_v_q_score_task(req)
    print(resp)
