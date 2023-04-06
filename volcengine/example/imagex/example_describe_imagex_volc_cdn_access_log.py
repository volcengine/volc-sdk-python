# coding:utf-8
from __future__ import print_function
from volcengine.imagex.ImageXService import ImageXService

if __name__ == '__main__':
    imagex_service = ImageXService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    imagex_service.set_ak('ak')
    imagex_service.set_sk('sk')

    query = {
        'ServiceId': "service id",
    }
    body = {
        'StartTime': 1680500000,
        'EndTime': 1680515000,
        'Domain': "domain",
        'Region': "global",
        'PageNum': 1,
        'PageSize': 10,
    }

    resp = imagex_service.describeImageVolcCdnAccessLog(query, body)
    print(resp)
