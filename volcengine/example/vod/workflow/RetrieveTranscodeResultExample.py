# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodRetrieveTranscodeResultRequest

if __name__ == '__main__':
    vod_service = VodService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('your ak')
    vod_service.set_sk('your sk')
    try:
        req = VodRetrieveTranscodeResultRequest()
        req.Vid = 'your vid'
        req.ResultType = 'your resultType'
        resp = vod_service.retrieve_transcode_result(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result)
        else:
            print(resp.ResponseMetadata.Error)

