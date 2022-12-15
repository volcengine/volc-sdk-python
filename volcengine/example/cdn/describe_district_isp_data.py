#  -*- coding: utf-8 -*-
import os
import sys
import datetime

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")

from volcengine.example.cdn import ak, sk
from volcengine.cdn.service import CDNService

if __name__ == '__main__':
    svc = CDNService()
    svc.set_ak(ak)
    svc.set_sk(sk)
    
    now = int(datetime.datetime.now().strftime("%s"))
    body = {
        'StartTime': now - 3600,
        'EndTime': now,
        'Metric': 'bandwidth',
        'Domain': 'example.com',
        'Interval': '5min',
        'Protocol': 'http',
        'IpVersion': 'ipv4'
    }
    
    resp = svc.describe_district_isp_data(body)
    print(resp)
