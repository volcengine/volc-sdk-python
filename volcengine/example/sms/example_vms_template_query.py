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
        "TemplateId": "templateId"
    }

    resp = sms_service.get_vms_template_status(body)
    print(resp)
