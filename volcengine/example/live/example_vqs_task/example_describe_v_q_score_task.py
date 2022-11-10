# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.request_live_pb2 import DescribeVQScoreTaskRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    req = DescribeVQScoreTaskRequest()
    req.ID = 'ID'

    print(req)
    resp = live_service.describe_v_q_score_task(req)
    print(resp)