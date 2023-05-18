# coding:utf-8
from __future__ import print_function

import json

from volcengine.sms.SmsService import SmsService

if __name__ == '__main__':
    # cn
    sms_service = SmsService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    sms_service.set_ak('ak')
    sms_service.set_sk('sk')
    # sms_service.set_host('host')

    body = {
        "SubAccount": "subAccount",
        "Id": "id",
        "IsOrder": True
    }

    resp = sms_service.delete_signature(body)
    print(resp)
