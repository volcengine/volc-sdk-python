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

    body = {
        "purpose": 1,
        "materialName": "名称",
        "businessInfo": {
            "businessCertificateType": 1,
            "businessCertificate": {
                "fileContent": "data:image/jpg;base64,IPV*****************************************************************CYII=",
                "fileSuffix": "jpg",
                "fileType": 1,
                "fileUrl": "https://url",
            },
            "businessCertificateName": "xx公司",
            "unifiedSocialCreditIdentifier": "Zf6m",
            "businessCertificateValidityPeriodStart": "2024-01-12",
            "businessCertificateValidityPeriodEnd": "2024-01-12",
            "legalPersonName": "陈xx",
        },
        "operatorPerson": {
            "certificateType": 0,
            "personCertificate": [
                {
                    "fileContent": "data:image/jpg;base64,IPV*****************************************************************CYII=",
                    "fileSuffix": "jpg",
                    "fileType": 8,
                    "fileUrl": "https://url",
                },
                {
                    "fileContent": "data:image/jpg;base64,IPV*****************************************************************CYII=",
                    "fileSuffix": "jpg",
                    "fileType": 9,
                    "fileUrl": "https://url",
                },
            ],
            "personName": "陈xx",
            "personIDCard": "41000000000",
            "personMobile": "13800000",
        },
        "responsiblePersonInfo": {
            "certificateType": 0,
            "personCertificate": [
                {
                    "fileContent": "data:image/jpg;base64,IPV*****************************************************************CYII=",
                    "fileSuffix": "jpg",
                    "fileType": 10,
                    "fileUrl": "https://url",
                },
                {
                    "fileContent": "data:image/jpg;base64,IPV*****************************************************************CYII=",
                    "fileSuffix": "jpg",
                    "fileType": 11,
                    "fileUrl": "https://url",
                },
            ],
            "personName": "陈xx",
            "personIDCard": "41000000000",
            "personMobile": "13800000",
        },
    }

    resp = sms_service.apply_signature_ident(body)
    # {
    #     "ResponseMetadata": {
    #         "RequestId": "202404252055144D6C4FB9957172CF8034",
    #         "Action": "BatchBindSignatureIdent",
    #         "Version": "2021-01-11",
    #         "Service": "volcSMS",
    #         "Region": "cn-north-1"
    #     },
    #     "Result": {
    #         "id": 17,
    #     }
    # }
    print(resp)
