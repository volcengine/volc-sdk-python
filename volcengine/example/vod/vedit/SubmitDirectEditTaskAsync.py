# coding:utf-8
from __future__ import print_function

import json

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodSubmitDirectEditTaskAsyncRequest

if __name__ == '__main__':
    vod_service = VodService()

    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('ak')
    vod_service.set_sk('sk')
    req = VodSubmitDirectEditTaskAsyncRequest()
    req.Uploader = 'your uploader'
    req.Application = 'VideoTrackToB'
    req.Priority = 0
    req.CallbackUri = 'your callback uri'
    req.CallbackArgs = 'your callback args'
    editParam = {
        "Canvas": {
            "Height": 2160,
            "Width": 3840
        },
        "Output": {
            "Alpha": False,
            "Codec": {
                "AudioBitrate": 128,
                "AudioCodec": "aac",
                "Crf": 23,
                "Preset": "slow",
                "VideoCodec": "h264"
            },
            "DisableAudio": False,
            "DisableVideo": False,
            "Fps": 30
        },
        "Track": [
            [
                {
                    "ID": "video1",
                    "Source": "your source",
                    "TargetTime": [
                        0,
                        10000
                    ],
                    "Type": "video"
                }
            ]
        ],
        "Upload": {
            "SpaceName": "your uploader",
            "VideoName": "your video name"
        },
        "Uploader": "your uploader"
    }
    req.EditParam = json.dumps(editParam)
    resp = vod_service.submit_direct_edit_task_async(req)
    l = json.loads(resp)
    print(json.dumps(l, ensure_ascii=False, indent=4))
    print("****")
