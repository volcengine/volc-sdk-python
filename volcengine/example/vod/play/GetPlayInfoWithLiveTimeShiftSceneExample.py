# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodGetPlayInfoWithLiveTimeShiftSceneRequest

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
        req = VodGetPlayInfoWithLiveTimeShiftSceneRequest()

        req.StoreUris = 'uri1,uri2,uri3'
        req.SpaceName = 'your space name'
        req.Ssl = '0 or 1'
        req.ExpireTimestamp = 'unix timestamp'
        req.NeedComposeBucketName = '0 or 1'
        resp = vod_service.get_play_info_with_live_time_shift_scene(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result.PlayInfoList[0].MainPlayUrl)
        else:
            print(resp.ResponseMetadata.Error)
    print('*' * 100)
