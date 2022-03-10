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
        "Domain": "domain",
        "App": "app",
        "Stream": "stream",
    }
    resp = live_service.forbid_stream(body)
    print(resp)
