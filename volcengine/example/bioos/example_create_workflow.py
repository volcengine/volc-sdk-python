# coding:utf-8
from __future__ import print_function

from volcengine.bioos.BioOsService import BioOsService

if __name__ == '__main__':
    # set endpoint/region here if the default value is unsatisfied
    bioos_service = BioOsService(endpoint='endpoint', region='region')

    # call below method if you don't set ak and sk in $HOME/.volc/config
    bioos_service.set_ak('ak')
    bioos_service.set_sk('sk')

    params = {
        'WorkspaceID': 'workspace_id',
        'Name': 'workflow_name',
        'Description': 'workflow_description',
        'Language': 'WDL',
        'Source': 'http://foo.git',
        'Tag': 'baz',
        'MainWorkflowPath': 'aaa/bbb.wdl',
    }

    resp = bioos_service.create_workflow(params)
    print(resp)
