# coding:utf-8
from __future__ import print_function

import json

from volcengine.sms.SmsService import SmsService
from volcengine.const.Const import *

if __name__ == '__main__':
    sms_service = SmsService()
    # oversea
    # sms_service = SmsService(REGION_AP_SINGAPORE1)

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

    body = {
        "SmsAccount": "smsAccount",
        "Sign": "sign",
        "TemplateID": "ST_xxx",
        "PhoneNumber": "188xxxxxxxx",
        "CodeType": 6,
        "TryCount": 3,
        "ExpireTime": 240,
        "Scene": "Test"
    }
    body = json.dumps(body)
    resp = sms_service.send_sms_verify_code(body)
    print(resp)

    body = {
        "SmsAccount": "smsAccount",
        "PhoneNumber": "188xxxxxxxx",
        "Scene": "Test",
        "Code": "123456"
    }
    body = json.dumps(body)
    resp = sms_service.check_sms_verify_code(body)
    print(resp)
