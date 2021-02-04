# coding:utf-8
from __future__ import print_function

import json

from volcengine.vedit.VEditService import VEditService

if __name__ == '__main__':
    edit_service = VEditService()

    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    # edit_service.set_ak('ak')
    # edit_service.set_sk('sk')

    body = {}
    body["EditParam"] = {
        "Upload": {
            "Uploader": "your uploader",
            "VideoName": "your video name"
        },
        "Output": {
            "Fps": 25,
            "Height": 720,
            "Quality": "medium",
            "Width": 1280
        },
        "Segments": [{
            "BackGround": "0xFFFFFFFF",
            "Duration": 3,
            "Elements": [],
            "Volume": 1
        }],
        "GlobalElements": []
    }
    body["Priority"] = 0
    body["CallbackArgs"] = "your callback args"
    body["CallbackUri"] = "your callback uri"

    body = json.dumps(body)
    resp = edit_service.submit_direct_edit_task_async(body)
    print(resp)

    print("****")

    body = {}
    body["ReqIds"] = ["your req id 1", "your req id 2"]

    body = json.dumps(body)
    resp = edit_service.get_direct_edit_result(body)
    print(resp)
