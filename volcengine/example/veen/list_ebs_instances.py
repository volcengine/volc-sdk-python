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
        "with_attachment_info": "true",
        "res_ids": ["testing2-veen92023710333272539522"],
        "ebs_ids": ["disk-t9p44586fn6cbs9"],
        "ebs_names": ["本地_虚机测试用-3"],
        "regions": ["CentralChina"],
        "cluster_names": ["nbct05-testing3"],
        "status": ["attached"],
        "ebs_type": ["data"],
        "charge_type": ["HourUsed"],
        "fuzzy_veen_external_ip": "172.19.23.230",
        "page_option": {
            "page_no": 1,
            "page_size": 10,
        },
        "order_option": {
            "order_by": "ebs_id",
            "asc": "true",
        },
    }

    resp = svc.list_ebs_instances(query)
    print(resp)
