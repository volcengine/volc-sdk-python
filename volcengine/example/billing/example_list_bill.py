# coding:utf-8
from __future__ import print_function

import json

from volcengine.billing.BillingService import BillingService

if __name__ == '__main__':
    testAk = "<Your AK>"
    testSk = "<Your SK>"

    billing_service = BillingService()
    billing_service.set_ak(testAk)
    billing_service.set_sk(testSk)

    params = dict()
    params['BillPeriod'] = '2022-01'
    params['Limit'] = 10
    params['Offset'] = 0
    params['Product'] = ''
    params['BillingMode'] = ''
    params['BillCategoryParent'] = ''
    params['PayStatus'] = ''
    params['IgnoreZero'] = 0
    params['NeedRecordNum'] = 0

    body = {}

    resp = billing_service.list_bill(params, body)
    print(json.dumps(resp, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':')))
