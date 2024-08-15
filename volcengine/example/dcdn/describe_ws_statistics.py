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

    body = {
        "StartTime": "2024-08-09 16:00:00",
        "EndTime":  "2024-08-09 17:00:00",
        "Interval": 300,
        "Domains": [
            "xxxx.test.com"
        ],
        "GroupByDomain": False
    }

    resp = svc.describe_ws_statistics(body)
    print(resp)
