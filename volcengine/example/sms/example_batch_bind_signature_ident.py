# coding:utf-8
from __future__ import print_function

import json

from volcengine.sms.SmsService import SmsService
from volcengine.const.Const import *

if __name__ == "__main__":
    # cn
    sms_service = SmsService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    sms_service.set_ak("ak")
    sms_service.set_sk("sk")
    # It is recommended to use this domain name with a CDN.
    sms_service.set_host("sms-api.volcengineapi.com")

    body = {"subAccount": "cYyUq453", "signatures": ["签名1", "签名2"], "id": 123}

    resp = sms_service.batch_bind_signature_ident(body)
    # {
    #     "ResponseMetadata": {
    #         "RequestId": "202404252055144D6C4FB9957172CF8034",
    #         "Action": "BatchBindSignatureIdent",
    #         "Version": "2021-01-11",
    #         "Service": "volcSMS",
    #         "Region": "cn-north-1"
    #     },
    #     "Result": {
    #         "msg": "success",
    #     }
    # }
    print(resp)
