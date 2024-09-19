# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodGetAllPlayInfoRequest

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
        req = VodGetAllPlayInfoRequest()
        req.Vids = 'your Vids'
        req.Formats = 'your Formats'
        req.Codecs = 'your Codecs'
        req.Definitions = 'your Definitions'
        req.FileTypes = 'your FileTypes'
        req.LogoTypes = 'your LogoTypes'
        req.NeedEncryptStream = 'your NeedEncryptStream'
        req.Ssl = 'your Ssl'
        req.NeedThumbs = 'your NeedThumbs'
        req.NeedBarrageMask = 'your NeedBarrageMask'
        req.CdnType = 'your CdnType'
        req.UnionInfo = 'your UnionInfo'
        req.PlayScene = 'your PlayScene'
        req.DrmExpireTimestamp = 'your DrmExpireTimestamp'
        req.HDRType = 'your HDRType'
        req.KeyFrameAlignmentVersion = 'your KeyFrameAlignmentVersion'
        req.UserAction = 'your UserAction'
        req.Quality = 'your Quality'
        resp = vod_service.get_all_play_info(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result)
        else:
            print(resp.ResponseMetadata.Error)
    print('*' * 100)
