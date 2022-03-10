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
        "status": 1,
        "SuffixName": "",
        "Preset": "",
        "FPS": 60,
    }
    resp = live_service.update_transcode_preset(body)
    print(resp)
