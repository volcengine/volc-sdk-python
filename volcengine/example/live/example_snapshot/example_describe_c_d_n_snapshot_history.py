# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.request_live_pb2 import DescribeCDNSnapshotHistoryRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    req = DescribeCDNSnapshotHistoryRequest()
    req.Vhost = 'Vhost'
    req.App = 'App'
    req.Stream = 'Stream'
    req.DateFrom = '2022-10-16T00:00:00+08:00'
    req.DateTo = '2022-10-21T23:59:59+08:00'
    req.Type = 'Type'
    req.PageNum = 0
    req.PageSize = 0
    print(req)
    resp = live_service.describe_c_d_n_snapshot_history(req)
    print(resp)

