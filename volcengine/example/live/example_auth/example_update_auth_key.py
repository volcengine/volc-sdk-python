# coding:utf-8

from volcengine.live.LiveService import LiveService

if __name__ == '__main__':
    live_service = LiveService()
    ak = ""
    sk = ""
    live_service.set_ak(ak)
    live_service.set_sk(sk)
    body = {
        "Domain": "domain",
        "SceneType": "push",
        "AuthDetailList": [
            {
                "EncryptionAlgorithm": "md5",
                "SecretKey": "xx",
            },
        ],
    }
    resp = live_service.update_auth_key(body)
    print(resp)
