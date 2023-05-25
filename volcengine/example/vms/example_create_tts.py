# coding:utf-8

from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    body = {
        "Name": "我的tts测试",
        "TtsTemplateContent": "测试文本",
        "Remark": "测试",
        "TtsOption":"{\"loop\":0,\"loop_interval\":0,\"speed\":10,\"volume\":10,\"pitch\":10,\"voice_type\":\"BV001_streaming\",\"lang\":\"ch\",\"voice\":\"other\"}"
    }

    vms_service.create_tts(body)