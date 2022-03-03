#  -*- coding: utf-8 -*-
import datetime

from volcengine.example.cdn import ak, sk
from volcengine.cdn.service import CDNService

if __name__ == '__main__':
    svc = CDNService()
    svc.set_ak(ak)
    svc.set_sk(sk)
    now = int(datetime.datetime.now().strftime("%s"))
    body = {
        'TaskType': 'block_url',
        'StartTime': now - 86400,
        'EndTime': now,
    }
    print(body)

    resp = svc.describe_edge_nrt_data_summary(body)
    print(resp)
