# coding:utf-8
from __future__ import print_function

import json

from volcengine.const.Const import REGION_AP_SINGAPORE1, AREA_OVERSEAS
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
    # sms_service.set_host('host')¬

    param = {
        "subAccount": "subAccount",
        "signature": "sign",
        "pageIndex": 1,
        "pageSize": 10
    }

    resp = sms_service.get_signature_and_order_list(param)
    print(resp)
