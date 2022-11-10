# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.request_live_pb2 import CreateVQScoreTaskRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('==')
    req = CreateVQScoreTaskRequest()
    req.MainAddr = 'MainAddr'
    req.ContrastAddr = 'ContrastAddr'
    req.FrameInterval = 0
    req.Duration = 0
    req.Algorithm = 'Algorithm'

    print(req)
    resp = live_service.create_v_q_score_task(req)
    print(resp)
    # 7161756940979294477

