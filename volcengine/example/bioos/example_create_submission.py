# coding:utf-8
from __future__ import print_function

from volcengine.bioos.BioOsService import BioOsService

import json


if __name__ == '__main__':
    # set endpoint/region here if the default value is unsatisfied
    bioos_service = BioOsService(endpoint='endpoint', region='region')

    # call below method if you don't set ak and sk in $HOME/.volc/config
    bioos_service.set_ak('ak')
    bioos_service.set_sk('sk')

    params = {
        'ClusterID': 'cluster_id',
        'WorkspaceID': 'workspace_id',
        'WorkflowID': 'workflow_id',
        'Name': 'submission_name',
        'Description': 'submission_description',
        'DataModelID': 'data_model_id',
        'DataModelRowIDs': ['your-sample-3-id'],
        'Inputs': json.dumps({
            'testname.hello.name': 'this.name1'
        }),
        'ExposedOptions': {'ReadFromCache': True},
        'Outputs': json.dumps({
            'testname.hello.response': 'this.response1'
        }),
    }

    resp = bioos_service.create_submission(params)
    print(resp)
