# coding:utf-8
import json

from volcengine.live.LiveService import LiveService

if __name__ == '__main__':
    live_service = LiveService()
    ak = ""
    sk = ""
    live_service.set_ak(ak)
    live_service.set_sk(sk)
    body = {
        "PresetList": ["Preset1", "Preset2"],
    }
    resp = live_service.list_common_trans_preset_detail(body)
    print(resp)
