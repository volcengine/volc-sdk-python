# coding:utf-8
from __future__ import print_function

import json

from volcengine.util.Functions import Function
from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodCommitUploadInfoRequest

if __name__ == '__main__':
    # Create a VOD instance in the specified region.
    # vod_service = VodService('cn-north-1')
    vod_service = VodService()

    # Configure your Access Key ID (AK) and Secret Access Key (SK) in the environment variables or in the local ~/.volc/config file. For detailed instructions, see https://www.volcengine.com/docs/4/65646.
    # The SDK will automatically fetch the AK and SK from the environment variables or the ~/.volc/config file as needed.
    # During testing, you may use the following code snippet. However, do not store the AK and SK directly in your project code to prevent potential leakage and safeguard the security of all resources associated with your account.
    # vod_service.set_ak('your ak')
    # vod_service.set_sk('your sk')

    space_name = 'your space'
    session = ''
    try:
        req = VodCommitUploadInfoRequest()
        req.SpaceName = space_name
        req.SessionKey = session
        get_meta_function = Function.get_meta_func()
        snapshot_function = Function.get_snapshot_func(2.3)
        req.Functions = json.dumps([get_meta_function, snapshot_function])
        resp = vod_service.commit_upload_info(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result.Data)
            print(resp.Result.Data.Vid)
            print(resp.Result.Data.PosterUri)
            print(resp.Result.Data.SourceInfo.Height)
            print(resp.Result.Data.SourceInfo.Width)
        else:
            print(resp.ResponseMetadata.Error)
            print(resp.ResponseMetadata.RequestId)
