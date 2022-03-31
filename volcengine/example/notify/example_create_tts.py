# coding:utf-8

from volcengine.notify.notify import NotifyService

if __name__ == '__main__':
    notify_service = NotifyService()

    notify_service.set_ak("your ak")
    notify_service.set_sk("your sk")

    body = {
        "Name": "我的tts测试",
        "TtsTemplateContent": "测试文本",
        "Remark": "测试",
        "TtsOption":"{\"loop\":0,\"loop_interval\":0,\"speed\":10,\"volume\":10,\"pitch\":10,\"voice_type\":\"BV001_streaming\",\"lang\":\"ch\",\"voice\":\"other\"}"
    }

    notify_service.create_tts(body)