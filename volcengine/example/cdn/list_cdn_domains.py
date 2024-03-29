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
        'ServiceType': 'web',
        'PageNum': 1,
        'PageSize': 100
    }

    resp = svc.list_cdn_domains(body)
    print(resp)
    
    # use method GET 
    resp = svc.list_cdn_domains(body, svc.use_get())
    print(resp)
