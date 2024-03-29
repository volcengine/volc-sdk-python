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
        "cloud_server_identity": "cloudserver-8fz56vmnzbwcv99",
        "instance_area_nums": [
            {"cluster_name": "bdcdn-ycct", "num": 1}
        ],
    }

    resp = svc.create_instance(body)
    print(resp)
