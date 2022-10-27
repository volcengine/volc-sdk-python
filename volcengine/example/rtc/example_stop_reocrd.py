# coding:utf-8
from __future__ import print_function

import json

from volcengine.example.rtc.RtcService import RtcService

if __name__ == '__main__':
    # using your own AK and SK
    AK = 'Your_AK'
    SK = 'Your_SK'

    # Firstly , init an RTCService Class
    rtc_service = RtcService()

    # Then , Set your AK and SK
    rtc_service.set_ak(AK)
    rtc_service.set_sk(SK)

    # You can using this API now ! Here are some Examples
    body = dict()
    body['AppId'] = 'Your_AppId'
    body['BusinessId'] = 'Your_BusinessId'
    body['RoomId'] = 'Your_RoomId'
    body['TaskId'] = 'Your_TaskId'

    body = json.dumps(body)
    resp = rtc_service.stop_record(body)
    print(resp)

