# coding:utf-8
import json

from volcengine.live.LiveService import LiveService

if __name__ == '__main__':
    live_service = LiveService()
    ak = ""
    sk = ""
    live_service.set_ak(ak)
    live_service.set_sk(sk)
    body = {
        "Vhost": "vhost",
        "App": "app",
        "Status": 1,
        "Bucket": "bb",
        "RecordTob": [
            {
                "Format": "hls",
                "Duration": 100,
                "Splice": -1,
                "RecordObject": "/xx/xx",
            },
        ]
    }
    resp = live_service.create_record_preset(body)
    print(resp)
