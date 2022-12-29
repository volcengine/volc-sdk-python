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
        "StartTime": "2022-12-15 00:00:00",
        "EndTime": "2022-12-15 18:59:00",
        "Domains": ["www.test.com"],
        "Metrics": ["all"],
        "Interval": 300,
    }

    resp = svc.describe_origin_statistics(body)
    print(resp)
