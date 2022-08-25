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
        "Bucket": "bb",
        "Interval": 8.9,
        "StorageStrategy": 1,
        "CallbackDetailList": [{"URL": "http://xx", "CallbackType": "http"}],
        "Label": ["301"]
    }
    resp = live_service.create_snapshot_audit_preset(body)
    print(resp)
