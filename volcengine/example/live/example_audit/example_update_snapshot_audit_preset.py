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
        "PresetName": "presetName",
        "Interval": 5.0,
    }
    resp = live_service.update_snapshot_audit_preset(body)
    print(resp)
