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
        'Name': 'file_name',
        'Headers': ['my_entity_id', 'column-1-file-CRAM', 'date'],
        'Rows': [
            ['your-sample-1-id', 'https:test.tos-cn-beijing.volces.com/file1.cram', '01/01/2022'],
            ['your-sample-2-id', 'https:test.tos-cn-beijing.volces.com/file2.cram', '01/01/2022'],
            ['your-sample-3-id', 'https:test.tos-cn-beijing.volces.com/file3.cram', '01/01/2022']
        ],
    }

    resp = bioos_service.create_data_model(params)
    print(resp)
