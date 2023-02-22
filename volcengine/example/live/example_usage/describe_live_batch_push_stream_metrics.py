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
        "StartTime": "2022-12-22T19:35:00+08:00",
        "EndTime": "2022-12-22T19:40:05+08:00",
        "Aggregation": 60
    }
    resp = live_service.describe_live_batch_push_stream_metrics.py(body)
    print(resp)
