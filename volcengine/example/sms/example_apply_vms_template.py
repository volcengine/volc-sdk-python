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
    file_base64_string = to_base64_str("媒体文件路径")
    body = {
        "subAccount": "subAccount",
        "name": "SDK测试",
        "theme": "SDK测试视频短信",
        "signature": "签名",
        "channelType": "CN_VMS",
        "contents": [
            {
                "sourceType": SOURCE_TYPE_TEXT,
                "content": "火山引擎，做企业好的伙伴"
            },
            {
                # choose the midea type
                "sourceType": SOURCE_TYPE_IMAGE_GIF,
                "content": file_base64_string
            }
        ]
    }

    resp = sms_service.apply_vms_template(body)
    print(resp)
