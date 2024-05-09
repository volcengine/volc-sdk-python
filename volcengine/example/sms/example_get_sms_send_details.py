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
    sms_service.set_host('sms-api.volcengineapi.com')

    body = {
        "subAccount": "subAccount",
        "phoneNumber": "xxxxxx",
        "messageId": "",
        "sendDate": "20240424",
        "pageIndex": 1,
        "pageSize": 15
    }


    resp = sms_service.get_sms_send_details(body)
    # {
    #     "ResponseMetadata": {
    #         "RequestId": "202404252055144D6C4FB9957172CF8034",
    #         "Action": "GetSmsSendDetails",
    #         "Version": "2021-01-11",
    #         "Service": "volcSMS",
    #         "Region": "cn-north-1"
    #     },
    #     "Result": {
    #         "account": "xxxxxxxx",
    #         "sendDetailsResults": [
    #             {
    #                 "status": 3,
    #                 "errorCode": "0",
    #                 "errorMessage": "发送成功",
    #                 "phoneNumber": "152********",
    #                 "signature": "xx",
    #                 "templateID": "xxx",
    #                 "content": "xxxxxx",
    #                 "channelType": "CN_MKT",
    #                 "messageId": "xxxxxxxxxx",
    #                 "msgCount": 1,
    #                 "sendTime": 1713951918107,
    #                 "receiptTime": 1713951925706
    #             }
    #         ],
    #         "subAccount": "xxxxxx",
    #         "total": 1
    #     }
    # }
    print(resp)
