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

    query = {"instance_type": "veEN.C1.large", "cloud_disk_type": "CloudSSD"}

    resp = svc.list_available_resource_info(query)
    print(resp)
