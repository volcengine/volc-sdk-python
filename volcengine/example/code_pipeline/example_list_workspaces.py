# coding:utf-8
from __future__ import print_function

from volcengine.code_pipeline.CodePipelineService import CodePipelineService

if __name__ == '__main__':
    cp_service = CodePipelineService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    cp_service.set_ak('ak')
    cp_service.set_sk('sk')

    params = {}
    body = {}

    resp = cp_service.list_workspaces(params, body)
    print(resp)
