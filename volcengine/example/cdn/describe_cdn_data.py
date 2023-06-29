#  -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
import datetime

from volcengine.example.cdn import ak, sk
from volcengine.cdn.service import CDNService

if __name__ == '__main__':
    svc = CDNService()
    svc.set_ak(ak)
    svc.set_sk(sk)
    now = int(datetime.datetime.now().strftime("%s"))
    body = {
        'StartTime': now - 86400,
        'EndTime': now,
        'Metric': 'pv',
        'Domain': 'example.com',
        'Interval': '5min',
        'Isp': 'CT',
        'Region': 'BJ',
        'Protocol': 'http',
        'IpVersion': 'ipv4',
        "OnlyTotal": True
    }

    resp = svc.describe_cdn_data(body)
    print(resp)
    
    # use method GET
    resp = svc.describe_cdn_data(body, svc.use_get())
    print(resp)
