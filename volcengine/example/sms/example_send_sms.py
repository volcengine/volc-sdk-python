# coding:utf-8
from __future__ import print_function

import json

from volcengine.sms.SmsService import SmsService

if __name__ == '__main__':
    sms_service = SmsService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    sms_service.set_ak('ak')
    sms_service.set_sk('sk')
    # sms_service.set_host('host')

    body = {
        "SmsAccount": "smsAccount",
        "Sign": "sign",
        "TemplateID": "ST_xxx",
        "TemplateParam": {"code": "1234"},
        "PhoneNumbers": "188xxxxxxxx",
        "Tag": "tag",
    }

    body = json.dumps(body)
    resp = sms_service.send_sms(body)
    print(resp)
