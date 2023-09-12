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

    query = {
        "ebs_id": "disk-t9p44586fn6cbs9",
        "with_attachment_info": "true",
    }

    resp = svc.get_ebs_instance(query)
    print(resp)
