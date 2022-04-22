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
        "Domain": "",
        "App": "",
        "RefererInfoList":
            [
                {
                    "Key": "asd",
                    "Type": "xx",
                    "Value": "sad",
                    "Priority": 0,
                },
            ]
    }
    resp = live_service.update_referer(body)
    print(resp)
