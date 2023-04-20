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
        "regions": "SouthChina,Northwest", 
        "cities": "440300,640100",
        "isps": "CTCC,CMCC_CTCC_CUCC",
        "status": "opening,running",
        "page": 2, 
        "limit": 2, 
        "order_by": 2
    }

    resp = svc.list_instances(query)
    print(resp)
