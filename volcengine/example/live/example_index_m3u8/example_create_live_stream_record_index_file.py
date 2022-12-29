# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.request.request_live_pb2 import CreateLiveStreamRecordIndexFilesRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    req = CreateLiveStreamRecordIndexFilesRequest()
    req.Domain = 'your domain'
    req.App = 'your app'
    req.Stream = 'your stream'
    req.StartTime = '2022-12-22T19:35:00Z'
    req.EndTime = '2022-12-22T19:40:05Z'
    req.OutputBucket = "your bucket"
    print(req)
    resp = live_service.create_live_stream_record_index_files(req)
    print(resp)
