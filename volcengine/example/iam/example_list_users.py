# coding:utf-8
from __future__ import print_function

from volcengine.iam.IamService import IamService

if __name__ == '__main__':
    iam_service = IamService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    iam_service.set_ak('ak')
    iam_service.set_sk('sk')

    params = dict()
    params['Limit'] = 5
    params['Offset'] = 0

    resp = iam_service.list_users(params)
    print(resp)
