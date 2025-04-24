# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodUpdateUploadSpaceConfigRequest
from volcengine.vod.models.business.vod_space_pb2 import CustomPosterConfig
from volcengine.vod.models.business.vod_space_pb2 import TranscodeConfig


if __name__ == '__main__':
    # Create a VOD instance in the specified region.
    # vod_service = VodService('cn-north-1')
    vod_service = VodService()

    # Configure your Access Key ID (AK) and Secret Access Key (SK) in the environment variables or in the local ~/.volc/config file. For detailed instructions, see https://www.volcengine.com/docs/4/65646.
    # The SDK will automatically fetch the AK and SK from the environment variables or the ~/.volc/config file as needed.
    # During testing, you may use the following code snippet. However, do not store the AK and SK directly in your project code to prevent potential leakage and safeguard the security of all resources associated with your account.
    # vod_service.set_ak('your ak')
    # vod_service.set_sk('your sk')

    try:
        req = VodUpdateUploadSpaceConfigRequest()
        req.SpaceName = "your SpaceName"
        req.AutoPoster = "your AutoPoster"
        req.CustomPosterConfig.CopyFrom(CustomPosterConfig()) 
        req.GetPosterMode = "your GetPosterMode"
        req.AutoPosterCandidate = "your AutoPosterCandidate"
        req.AutoTranscode = "your AutoTranscode"
        req.TranscodeConfig.CopyFrom(TranscodeConfig()) 
        req.AutoSetVideoStatus = "your AutoSetVideoStatus"
        req.UploadOverwrite = "your UploadOverwrite"
        req.CallbackReturnPlayUrl = "your CallbackReturnPlayUrl"
        req.CallbackReturnRunId = "your CallbackReturnRunId"
        req.GetMetaMode = "your GetMetaMode"
        req.AutoGetArchiveVideoMeta = "your AutoGetArchiveVideoMeta"
        req.AutoGetIAVideoMeta = "your AutoGetIAVideoMeta"
        req.MetaGetMd5 = "your MetaGetMd5"
        
        resp = vod_service.update_upload_space_config(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result)
        else:
            print(resp.ResponseMetadata.Error)
    print('*' * 100)