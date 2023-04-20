#  -*- coding: utf-8 -*-
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from volcengine.example.veen import ak, sk
from volcengine.veen.service import VeenService

if __name__ == "__main__":
    svc = VeenService()
    svc.set_ak(ak)
    svc.set_sk(sk)

    query = {
        "instance_identity": "veen26301302623093022820",
    }

    resp = svc.get_instance(query)
    print(resp)
