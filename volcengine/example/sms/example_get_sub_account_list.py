# coding:utf-8
from __future__ import print_function

import json

from volcengine.const.Const import REGION_AP_SINGAPORE1
from volcengine.sms.SmsService import SmsService

if __name__ == '__main__':
    # SmsService is no longer support SG endpoint
    # cn
    sms_service = SmsService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    sms_service.set_ak('ak')
    sms_service.set_sk('sk')
    # sms_service.set_host('host')

    param = {
        "subAccountName": "",
        "pageIndex": 1,
        "pageSize": 1
    }

    resp = sms_service.get_sub_account_list(param)
    print(resp)
