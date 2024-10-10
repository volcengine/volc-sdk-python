# coding:utf-8
from __future__ import print_function

import json

from volcengine.util.Functions import Function
from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodUploadMediaRequest

if __name__ == '__main__':
    # Create a VOD instance in the specified region.
    # vod_service = VodService('cn-north-1')
    vod_service = VodService()

    # Configure your Access Key ID (AK) and Secret Access Key (SK) in the environment variables or in the local ~/.volc/config file. For detailed instructions, see https://www.volcengine.com/docs/4/65646.
    # The SDK will automatically fetch the AK and SK from the environment variables or the ~/.volc/config file as needed.
    # During testing, you may use the following code snippet. However, do not store the AK and SK directly in your project code to prevent potential leakage and safeguard the security of all resources associated with your account.
    # vod_service.set_ak('your ak')
    # vod_service.set_sk('your sk')

    space_name = 'your space name'
    file_path = 'your file path'

    get_meta_function = Function.get_meta_func()
    snapshot_function = Function.get_snapshot_func(2.3)
    get_start_workflow_func = Function.get_start_workflow_template_func(
        [{"TemplateIds": ["imp template id"], "TemplateType": "imp"},
         {"TemplateIds": ["transcode template id"], "TemplateType": "transcode"}])
    apply_function = Function.get_add_option_info_func("title1", "tag1", "desc1", 0, False)

    try:
        req = VodUploadMediaRequest()
        req.SpaceName = space_name
        req.FilePath = file_path
        req.Functions = json.dumps([get_meta_function, snapshot_function, get_start_workflow_func])
        req.CallbackArgs = ''
        req.FileName = 'hello/vod.mp4'
        req.FileExtension = '.mp4'
        req.StorageClass = 0
        req.UploadHostPrefer = ''
        resp = vod_service.upload_media(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result.Data)
            print(resp.Result.Data.Vid)
            print(resp.Result.Data.PosterUri)
            print(resp.Result.Data.SourceInfo.FileName)
            print(resp.Result.Data.SourceInfo.Height)
            print(resp.Result.Data.SourceInfo.Width)
        else:
            print(resp.ResponseMetadata.Error)
            print(resp.ResponseMetadata.RequestId)
