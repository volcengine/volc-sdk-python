# coding:utf-8
from __future__ import print_function

import json

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodSubmitDirectEditTaskSyncRequest

if __name__ == '__main__':
    vod_service = VodService()

    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('ak')
    vod_service.set_sk('sk')
    req = VodSubmitDirectEditTaskSyncRequest()
    req.Uploader = 'your uploader'
    req.Application = 'SimpleCut'
    editParam = {
            "Source": "your source",
            "Upload": {
                "SpaceName": "your uploader",
                "StorageBind": False
            },
            "CutList": [
                {
                    "StartTime": 9,
                    "EndTime": 78
                },
                {
                    "StartTime":   157,
                    "EndTime": 370
                }
            ]
        }
    req.EditParam = json.dumps(editParam).encode('utf-8')
    resp = vod_service.submit_direct_edit_task_sync(req)
    l = json.loads(resp)
    print(json.dumps(l, ensure_ascii=False, indent=4))
    print("****")
