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
        "TaskType": ["refresh_url"],
        "TaskStatus": ["running"],
        "Url": "www.test.com",
        "StartTime": "2022-12-15 00:00:00",
        "EndTime": "2022-12-15 18:59:00",
        "Page": 1,
        "PageSize": 100,
        "OrderType": "OpTime_DESC"
    }

    resp = svc.check_purge_prefetch_task(body)
    print(resp)
