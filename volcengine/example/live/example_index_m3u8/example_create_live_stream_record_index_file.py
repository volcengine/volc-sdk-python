# coding:utf-8
import json

from volcengine.live.LiveService import LiveService

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    body = {
        "Domain": "your domain",
        "App": "your app",
        "Stream": "your stream",
        "StartTime": "2022-12-22T19:35:00Z",
        "EndTime": "2022-12-22T19:40:05Z",
        "OutputBucket": "your bucket"
    }
    resp = live_service.create_live_stream_record_index_files(body)
    print(resp)
