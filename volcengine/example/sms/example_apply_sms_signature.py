# coding:utf-8
from __future__ import print_function

import base64
import json

from volcengine.const.Const import *
from volcengine.sms.SmsService import SmsService

if __name__ == '__main__':
    # base64 encode func
    def to_base64_str(file):
        with open(file, 'rb') as fileObj:
            image_data = fileObj.read()
            return base64.b64encode(image_data).decode('utf-8')

    # cn
    sms_service = SmsService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    sms_service.set_ak('ak')
    sms_service.set_sk('sk')
    # sms_service.set_host('host')

    body = {
        "SubAccount": "subAccount",
        "Content": "content",
        "Desc": "description",
        "Source": "公司名称/公司缩写",
        "Domain": "网站域名",
        "UploadFileList": [{
            "FileType": DOC_TYPE_THREE_IN_ONE,
            "FileContent": to_base64_str("图片.jpg"),
            "FileSuffix": "jpg"
        }],
        "Purpose": SIGN_PURPOSE_FOR_OWN,
        "SignatureIdentificationID": 12
    }

    resp = sms_service.apply_sms_signature(body)
    print(resp)
