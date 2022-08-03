#  -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")

from volcengine.example.cdn import ak, sk
from volcengine.cdn.service import CDNService

if __name__ == '__main__':
    svc = CDNService()
    svc.set_ak(ak)
    svc.set_sk(sk)

    body = {
        'Domain': 'example.com',
        'ServiceType': 'web',
        'Origin': [
            {
                'OriginAction': {
                    'OriginLines': [{
                        'OriginType': 'primary',
                        'InstanceType': 'ip',
                        'Address': '1.1.1.1',
                        'HttpPort': '80',
                        'HttpsPort': '443',
                        'Weight': '100'
                    }]
                }
            }
        ],
        'OriginProtocol': 'HTTP'
    }

    resp = svc.add_cdn_domain(body)
    print(resp)
