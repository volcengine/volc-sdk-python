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
        "UseWay": "sign",
        "CertName": "",
    }
    resp = live_service.create_cert(body)
    print(resp)
