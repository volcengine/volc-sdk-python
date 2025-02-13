# coding:utf-8
from __future__ import print_function

from volcengine.imp.ImpService import ImpService
from volcengine.imp.models.business.imp_common_pb2 import *
from volcengine.imp.models.request.request_imp_pb2 import *

if __name__ == '__main__':
    imp_service = ImpService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    imp_service.set_ak('your ak')
    imp_service.set_sk('your sk')

    # SubmitJob by Job
    try:
        req = ImpSubmitJobRequest()
        req.InputPath.Type = 'VOD'
        req.InputPath.VodSpaceName = 'your vod space'
        req.InputPath.FileId = 'your vid'
        req.OutputPath.Type = 'VOD'
        req.OutputPath.VodSpaceName = 'your vod space'
        req.Job.TranscodeVideo.Container = 'your container'
        req.Job.TranscodeVideo.Video.Codec = 'your video codec'
        req.Job.TranscodeVideo.Audio.Codec = 'your audio codec'
        req.CallbackArgs = 'your callback args'

        resp = imp_service.submit_job(req)
    except Exception:
        raise
    else:
        print("resp:\n ", resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result)
        else:
            print(resp.ResponseMetadata.Error)

