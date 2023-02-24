# coding:utf-8
from __future__ import print_function
from volcengine.imagex.data.ImageXData import *
from volcengine.imagex.ImageXService import ImageXService

if __name__ == '__main__':
    imagex_service = ImageXService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    imagex_service.set_ak('ak')
    imagex_service.set_sk('sk')

    query = dict()
    query['DataTypes'] = "2xx,3xx,4xx,5xx"
    query['GroupBy'] = "DomainName,DataType"
    query['StartTime'] = "2023-01-21T00:00:00+08:00"
    query['EndTime'] = "2023-01-28T00:00:00+08:00"
    query['Interval'] = "300"

    resp = describe_imagex_edge_request(imagex_service, query)
    print(resp)
