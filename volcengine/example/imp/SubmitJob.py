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

    # SubmitJob
    try:
        req = ImpSubmitJobRequest()
        req.InputPath.Type = 'VOD'
        req.InputPath.VodSpaceName = 'your space'
        req.InputPath.FileId = 'your vid'
        req.TemplateId = 'your template id'
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

