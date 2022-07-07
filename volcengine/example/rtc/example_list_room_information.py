# coding:utf-8
from __future__ import print_function

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
    params = dict()
    params['AppId'] = 'Your_AppId'
    params['StartTime'] = '2022-07-06T12:00:00+08:00'
    params['EndTime'] = '2022-07-06T14:00:00+08:00'
    # optional params
    # params['RoomId'] = 'Your_RoomId'
    # params['PageNum'] = 'PageNum'
    # params['PageSize'] = 'PageSize'

    resp = rtc_service.list_room_information(params)
    print(resp)
