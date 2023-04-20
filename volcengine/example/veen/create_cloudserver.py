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
        "cloudserver_name": "test-sdk",
        "image_id": "imagekhvhgzhna6",
        "spec_name": "veEN.C1.large",
        "storage_config": {
            "system_disk": {"capacity": "40", "storage_type": "CloudBlockSSD"},
            "data_disk_list": [
                {"capacity": "20", "storage_type": "CloudBlockSSD"},
                {"capacity": "40", "storage_type": "CloudBlockSSD"},
            ],
        },
        "network_config": {
            "bandwidth_peak": "200",
            "enable_ipv6": False,
        },
        "secret_config": {"secret_type": 2, "secret_data": "Abcd1234*"},
        "instance_area_nums": [
            {"cluster_name": "bdcdn-ycct", "num": 2}
        ],
        "billing_config": {
            "computing_billing_method": "MonthlyPeak",
            "bandwidth_billing_method": "MonthlyP95",
        },
    }

    resp = svc.create_cloudserver(body)
    print(resp)
