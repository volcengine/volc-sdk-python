# coding:utf-8
from __future__ import print_function

import json

from volcengine.const.Const import *
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
    sms_service.set_scheme("https")
    # sms_service.set_host('host')

    body = {
        "SubAccount": "subAccount",
        "Content": "content",
        "Desc": "description",
        "Source": "公司名称/公司缩写",
        "Domain": "网站域名"
    }

    resp = sms_service.apply_sms_signature(body)
    print(resp)
