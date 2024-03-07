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
        "cluster_name": "bdcdn-chdcu",
        "charge_type": "HourUsed",
        "ebs_type": "data",
        "storage_type": "CloudBlockHDD",
        "capacity": "200",
        "number": 1,
        "name": "ebs_test_yx",
        "desc": "test",
        "project": "",
        "delete_with_res": True,
        "res_id": "veen-xxxxx",
    }

    resp = svc.create_ebs_instances(body)
    print(resp)
