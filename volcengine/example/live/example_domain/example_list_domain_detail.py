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
        "PageNum": 1,
        "PageSize": 10,
    }
    resp = live_service.list_domain_detail(body)
    print(resp)
