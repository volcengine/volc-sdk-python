# coding:utf-8
from __future__ import print_function

from volcengine.vod.VodService import VodService
from volcengine.vod.models.business.vod_workflow_pb2 import WorkflowParams
from volcengine.vod.models.request.request_vod_pb2 import VodStartWorkflowRequest

if __name__ == '__main__':
    vod_service = VodService()
    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    vod_service.set_ak('your ak')
    vod_service.set_sk('your sk')
    try:
        req = VodStartWorkflowRequest()
        req.Vid = 'your vid'
        req.TemplateId = 'your template id'
        req.Input.MergeFrom(WorkflowParams())
        req.Priority = 0
        req.CallbackArgs = 'your callback args'
        resp = vod_service.start_workflow(req)
    except Exception:
        raise
    else:
        print(resp)
        if resp.ResponseMetadata.Error.Code == '':
            print(resp.Result)
        else:
            print(resp.ResponseMetadata.Error)

