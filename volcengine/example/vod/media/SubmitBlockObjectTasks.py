# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodSubmitBlockObjectTasksRequest
if __name__ == '__main__':
    vod_service = VodService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    #vod_service.set_ak('ak')
    #vod_service.set_sk('sk')

    try:
        req20 = VodSubmitBlockObjectTasksRequest()
        req20.SpaceName = "SpaceName"
        resp = vod_service.submit_block_object_tasks(req20)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result)
        else:
            print(resp.ResponseMetadata.Error)
    print('*' * 100)