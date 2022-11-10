# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.request_live_pb2 import DescribeForbiddenStreamInfoByPageRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    req = DescribeForbiddenStreamInfoByPageRequest()
    req.PageNum = 0
    req.PageSize = 0
    req.App = 'App'
    req.Stream = 'Stream'
    print(req)
    resp = live_service.describe_forbidden_stream_info_by_page(req)
    print(resp)

