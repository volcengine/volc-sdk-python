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
        "SmsAccount": "subAccount",
        "TemplateID": "templateId",
        # enable TemplateParam if there is template param in your template text content
        # "TemplateParam": "{\"code\": \"111\"}",
        "PhoneNumbers": "188********",
        "Tag": "tag",
    }

    body = json.dumps(body)
    resp = sms_service.send_sms(body)
    print(resp)
