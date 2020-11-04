# coding:utf-8
from __future__ import print_function

from volc.iam.IamService import IamService

if __name__ == '__main__':
    iam_service = IamService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    iam_service.set_ak('***REMOVED***')
    iam_service.set_sk('TWpjd1pqRTRaak5rT0RSak5EUmpNR0UzWXpNMVpUSTFZakF4T0RkaU9EYw==')
    iam_service.set_host('volcengineapi-boe.byted.org')

    params = dict()
    params['Limit'] = 5
    params['Offset'] = 0

    resp = iam_service.list_users(params)
    print(resp)
