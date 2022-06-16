# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodGetAllPlayInfoRequest

if __name__ == '__main__':
    vod_service = VodService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    # vod_service.set_ak('ak')
    # vod_service.set_sk('sk')
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
