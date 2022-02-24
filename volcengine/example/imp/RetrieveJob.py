# coding:utf-8
from __future__ import print_function

from volcengine.imp.ImpService import ImpService
from volcengine.imp.models.business.imp_common_pb2 import InputPath
from volcengine.imp.models.request.request_imp_pb2 import *

if __name__ == '__main__':
    imp_service = ImpService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    imp_service.set_ak('your ak')
    imp_service.set_sk('your sk')

    # RetrieveJob
    try:
        req = ImpRetrieveJobRequest()
        req.JobIds.extend(['your JobId1', 'your JobId2'])
        resp = imp_service.retrieve_job(req)
    except Exception:
        raise
    else:
        print("resp:\n ", resp)
        if resp.ResponseMetadata.Error.Code == '':
            print("Result:\n ", resp.Result)
        else:
            print(resp.ResponseMetadata.Error)
