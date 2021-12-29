# coding: utf-8
import datetime

from volcengine.auth.SignerV4 import SignerV4
from volcengine.auth.SignParam import SignParam
from volcengine.Credentials import Credentials
from collections import  OrderedDict

if __name__ == '__main__':
    sign = SignerV4()

    param = SignParam()
    param.path = '/'
    param.method = 'GET'
    param.host = 'open.volcengineapi.com'
    param.body = ''
    param.date = datetime.datetime.utcfromtimestamp(1640712206)
    query = OrderedDict()
    query['Action'] = 'ListUsers'
    query['Version'] = '2018-01-01'
    query['Limit'] = '5'
    query['Offset'] = '0'

    param.query = query
    header = OrderedDict()
    header['Host'] = 'open.volcengineapi.com'
    param.header_list = header

    cren = Credentials('ak','sk', 'iam', 'cn-north-1')
    result = sign.sign_only(param, cren)

    print(result)