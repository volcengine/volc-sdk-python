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
        "DomainList": ["domain1","domain2"],
    }
    # body = json.dumps(body)
    resp = live_service.describe_domain(body)
    print(resp)
