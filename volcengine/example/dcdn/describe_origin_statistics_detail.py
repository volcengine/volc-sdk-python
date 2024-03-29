#  -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")

from volcengine.example.dcdn import ak, sk
from volcengine.dcdn.DCDNService import DCDNService

if __name__ == '__main__':
    svc = DCDNService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    svc.set_ak(ak)
    svc.set_sk(sk)

    params = {
        "StartTime": "2022-08-09 00:00:00",
        "EndTime": "2022-08-09 00:20:11",
        "Domains": [
            "www.test1.com",
            "www.test2.com"
        ],
        "Metrics": [
            "all"
        ],
        "Interval": 300
    }

    resp = svc.describe_origin_statistics_detail(params)
    print(resp)
