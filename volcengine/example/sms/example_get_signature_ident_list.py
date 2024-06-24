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

    body = {"ids": [1, 23], "pageIndex": 1, "pageSize": 15}

    resp = sms_service.get_signature_ident_list(body)
    # {
    #     "ResponseMetadata": {
    #         "RequestId": "202404252055144D6C4FB9957172CF8034",
    #         "Action": "GetSignatureIdentList",
    #         "Version": "2021-01-11",
    #         "Service": "volcSMS",
    #         "Region": "cn-north-1",
    #     },
    #     "Result": {
    #         "list": [
    #             {
    #                 "id": 953,
    #                 "purpose": 1,
    #                 "materialName": "name",
    #                 "businessCertificateName": "xx公司",
    #                 "operatorPersonName": "陈xx",
    #                 "responsiblePersonName": "陈xx",
    #                 "effectSignatures": ["签名"],
    #             }
    #         ],
    #         "total": 1,
    #     },
    # }
    print(resp)
