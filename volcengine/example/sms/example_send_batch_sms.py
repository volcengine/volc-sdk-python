# coding:utf-8
from __future__ import print_function

import json

from volcengine.const.Const import REGION_AP_SINGAPORE1
from volcengine.sms.SmsService import SmsService

if __name__ == '__main__':
    # oversea
    # sms_service = SmsService(REGION_AP_SINGAPORE1)
    # cn
    sms_service = SmsService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    sms_service.set_ak('ak')
    sms_service.set_sk('sk')
    # sms_service.set_scheme("http")
    # sms_service.set_scheme("https")
    # sms_service.set_host('host')

    body = {
        "SmsAccount": "subAccount",
        "Sign": "signature",
        "From": "BytePlus",
        "TemplateID": "ST_xxx",
        "Messages": [{"TemplateParam": "{\"code\": \"1234\"}", "PhoneNumber": "+65xxxxxxxx"}],
        "Tag": "tag",
    }
    resp = sms_service.send_batch_sms(body)
    print(resp)
