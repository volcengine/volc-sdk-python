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
            "Domain": "111.soultrial.top",
            "ProbeSetting": {
                "Host": "soultrial.top",
                "Url": "/jpg",
                "Switch": "on",
                "UnhealthyStatusList": [
                    "4xx"
                ]
            }
        },
        {
            "Domain": "222.soultrial.top",
            "ProbeSetting": {
                "Host": "222.soultrial.to",
                "Url": "/text",
                "Switch": "on",
                "UnhealthyStatusList": [
                    "5xx"
                ]
            }
        }
    ]
    

    resp = svc.update_domain_probe_setting(body)
    print(resp)
