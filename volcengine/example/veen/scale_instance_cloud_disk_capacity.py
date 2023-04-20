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
        "scale_system_cloud_disk_info": {"device_name": "vda", "capacity": "1000"},
        "scale_data_cloud_disk_info_list": [{"device_name": "vdb", "capacity": "1000"}],
        "with_reboot": True,
    }

    resp = svc.scale_instance_cloud_disk_capacity(body)
    print(resp)
