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
        "Vhost": "",
        "App": "",
        "Status": 1,
        "Interval": 5,
        "Bucket": "",
        "SnapshotFormat": "jpeg",
        "SnapshotObject": "xx/xx",
        "StorageDir": "/xx",
    }
    resp = live_service.create_snapshot_preset(body)
    print(resp)
