#  -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from volcengine.example.veen import ak, sk
from volcengine.veen.service import VeenService

if __name__ == "__main__":
    svc = VeenService()
    svc.set_ak(ak)
    svc.set_sk(sk)

    body = {
        "instance_identity": "veen26301302623093022820",
        "secret_type": 2,
        "secret_data": "Abcd1234&"
    }

    resp = svc.reset_login_credential(body)
    print(resp)
