# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodQueryUploadTaskInfoRequest

if __name__ == '__main__':
    vod_service = VodService()

    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('your ak')
    vod_service.set_sk('your sk')

    jobId = 'url jobId'

    jobIds = [jobId]
    comma = ','
    s = comma.join(jobIds)

    req = VodQueryUploadTaskInfoRequest()
    req.JobIds = s
    try:
        resp = vod_service.query_upload_task_info(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result.Data)
            print(resp.Result.Data.MediaInfoList[0].State)
        else:
            print(resp.ResponseMetadata.Error)
            print(resp.ResponseMetadata.RequestId)
