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
        "PageNumber": 1,
        "PageSize": 10,
        "Filter": {
            "IDs": ["dataset_id1", "dataset_id2"],
            "ProjectDataTypes": ["data_type"],
            "Categories": ["示例数据"],
            "Keyword": "key",
            "Owner": "ownerName"
        },
        "SortBy": "Name",
        "SortOrder": "Desc"
    },
    resp = bioos_service.list_data_sets(params)
    print(resp)
