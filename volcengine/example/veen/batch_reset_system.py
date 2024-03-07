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
        "instance_identities": ["veen26301302623093022820", "testing-veen23323035425312030023"],
        "image_identity": "image7ajpdaodf7",
        "clear_data_disk": False,
    }

    resp = svc.batch_reset_system(body)
    print(resp)
