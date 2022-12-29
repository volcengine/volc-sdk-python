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

    body = [
        {
            "Domain": "www.test.com",
            "StrategyType": "wrr",
            "Origin": {
                "Origins": [
                    {
                        "Name": "1.1.1.2",
                        "Weight": 1
                    }
                ],
                "OriginType": "IP",
                "OriginProtocolType": "http",
            },
            "Cache": {
                "Enable": False,
            },
            "EnableFailOver": False,
        }
    ]

    resp = svc.create_domain(body)
    print(resp)
