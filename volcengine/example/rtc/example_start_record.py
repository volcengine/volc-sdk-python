# coding:utf-8
from __future__ import print_function

import json

from volcengine.example.rtc.RtcService import RtcService


def set_encode():
    encode = dict()
    encode['VideoWidth'] = 1920
    encode['VideoHeight'] = 1080
    encode['VideoFps'] = 15
    encode['VideoBitrate'] = 4000
    encode['VideoCodec'] = 0
    encode['VideoGop'] = 4
    encode['AudioCodec'] = 0
    encode['AudioProfile'] = 0
    encode['AudioBitrate'] = 64
    encode['AudioSampleRate'] = 48000
    encode['AudioChannels'] = 2
    return encode


def set_layout():
    layout = dict()
    layout['LayoutMode'] = 0
    return layout


def set_control():
    control = dict()
    control['MediaType'] = 0
    control['FrameInterpolationMode'] = 0
    control['MaxIdleTime'] = 180
    control['MaxRecordTime'] = 0
    return control


def set_file_format_config():
    config = dict()
    config['FileFormat'] = ['MP4']
    return config


def set_storage_config():
    config = dict()
    config['Type'] = 0
    config['TosConfig'] = set_tos_config()
    return config


def set_tos_config():
    config = dict()
    config['AccountId'] = 'Your_AccountId'
    config['Region'] = 0
    config['Bucket'] = 'Your_Bucket'
    return config


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
    body['RecordMode'] = 0
    body['Encode'] = set_encode()
    body['Layout'] = set_layout()
    body['Control'] = set_control()
    body['FileFormatConfig'] = set_file_format_config()
    body['StorageConfig'] = set_storage_config()

    body = json.dumps(body)
    resp = rtc_service.start_record(body)
    print(resp)
