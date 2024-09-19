# coding:utf-8
from __future__ import print_function

import json

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodSubmitDirectEditTaskSyncRequest

if __name__ == '__main__':
    # Create a VOD instance in the specified region.
    # vod_service = VodService('cn-north-1')
    vod_service = VodService()

    # Configure your Access Key ID (AK) and Secret Access Key (SK) in the environment variables or in the local ~/.volc/config file. For detailed instructions, see https://www.volcengine.com/docs/4/65646.
    # The SDK will automatically fetch the AK and SK from the environment variables or the ~/.volc/config file as needed.
    # During testing, you may use the following code snippet. However, do not store the AK and SK directly in your project code to prevent potential leakage and safeguard the security of all resources associated with your account.
    # vod_service.set_ak('your ak')
    # vod_service.set_sk('your sk')

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
