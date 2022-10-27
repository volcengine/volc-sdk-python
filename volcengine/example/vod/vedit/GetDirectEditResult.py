# coding:utf-8
from __future__ import print_function

import json

from volcengine.vod.VodService import VodService
from volcengine.vod.models.request.request_vod_pb2 import VodGetDirectEditResultRequest

if __name__ == '__main__':
    vod_service = VodService()

    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('ak')
    vod_service.set_sk('sk')
    req = VodGetDirectEditResultRequest()
    req.ReqIds.extend(['your ReqId'])
    resp = vod_service.get_direct_edit_result(req)
    l = json.loads(resp)
    print(json.dumps(l, ensure_ascii=False, indent=4))
    print("****")
