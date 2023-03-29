# coding:utf-8
from __future__ import print_function
from volcengine.imagex.ImageXService import ImageXService

if __name__ == '__main__':
    imagex_service = ImageXService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    imagex_service.set_ak('ak')
    imagex_service.set_sk('sk')

    query = dict()
    query['StartTime'] = "2023-01-21T00:00:00+08:00"
    query['EndTime'] = "2023-01-28T00:00:00+08:00"
    query['Interval'] = "5m"

    resp = imagex_service.describe_imagex_mirror_request_http_code_by_time(query)
    print(resp)
