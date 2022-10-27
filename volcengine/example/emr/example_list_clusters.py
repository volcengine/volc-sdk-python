# coding:utf-8
from __future__ import print_function

import json

from volcengine.emr.EMRService import EMRService

if __name__ == '__main__':
    emr_service = EMRService(region="cn-beijing")

    # call the following methods explicitly if you dont set ak and sk in $HOME/.volc/config
    # emr_service.set_ak(testAk)
    # emr_service.set_sk(testSk)

    params = {}
    resp = emr_service.list_clusters(params)
    print(json.dumps(resp, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':')))
