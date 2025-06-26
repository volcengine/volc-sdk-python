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
        "subAccount": "abc",
        "purpose": SIGN_PURPOSE_FOR_OWN,
        "source": SIGN_SOURCE_APP,
        "content": "测试签名",
        "desc": "000000",
        "domain": "000000",
        "signatureIdentificationID": 123,
        "appIcp": {
            "appIcpFilling": "APPICP测试备案",
            "appIcpFileList": [
                {
                    "fileSuffix": "jpg",
                    "fileUrl": "http:",
                    "fileType": DOC_TYPE_APP_ICP_CERTIFICATE
                }
            ]
        },
        "trademark": {
            "trademarkCn": "商标中文",
            "trademarkEn": "english",
            "trademarkNumber": "商标注册号1",
            "trademarkFileList": [
                {
                    "fileSuffix": "jpg",
                    "fileUrl": "http:",
                    "fileType": DOC_TYPE_TRADEMARK_CERTIFICATE
                },
                {
                    "fileSuffix": "jpg",
                    "fileUrl": "http:",
                    "fileType": DOC_TYPE_TRADEMARK_CERTIFICATE
                }
            ]
        }
    }

    resp = sms_service.apply_signature_ident(body)
    print(resp)
