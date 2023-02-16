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
        'ID': 'workspace_id',
        'Name': 'workspace_name',
        'Description': 'workspace_description',
        'CoverPath': 'template-cover/pic1.png'
    }

    resp = bioos_service.update_workspace(params)
    print(resp)
