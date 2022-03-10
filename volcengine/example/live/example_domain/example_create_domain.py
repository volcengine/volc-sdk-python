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
        # "Domain": "push-rtmp-testpython.xxx.xx",
        "Domain": "pull-rtmp-testpython.xxx.xx",
        # "Type": "push",
        "Type": "pull-flv",
    }
    resp = live_service.create_domain(body)
    print(resp)
