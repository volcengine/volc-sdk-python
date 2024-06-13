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
        "Domain": "ga.test.top",
        "OriginPolicy": [
            {
                "Priority": 1,
                "Match": {
                    "Value": [
                        "/hotel"
                    ]
                },
                "SplitClients": {
                    "Policy": "mmh2",
                    "HashVal": "${http_deviceid}",
                    "Splits": [
                        {
                            "DC": "accinstance-BTqmpvDufFSxNeyiu7vxYd",
                            "Weight": 11
                        },
                        {
                            "DC": "accinstance-SkDwncUQWnfTi7AdnvjvHa",
                            "Weight": 14
                        }
                    ]
                }
            },
            {
                "Priority": 2,
                "Match": {
                    "Value": [
                        "/",
                        "/tool"
                    ]
                },
                "SplitClients": {
                    "Policy": "random-rr",
                    "HashVal": "",
                    "Splits": [
                        {
                            "DC": "accinstance-BTqmpvDufFSxNeyiu7vxYd",
                            "Weight": 29
                        },
                        {
                            "DC": "accinstance-SkDwncUQWnfTi7AdnvjvHa",
                            "Weight": 4
                        }
                    ]
                }
            }
        ]
    }
    resp = svc.update_ga_origin_policy(body)
    print(resp)