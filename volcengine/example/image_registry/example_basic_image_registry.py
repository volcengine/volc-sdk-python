# coding:utf-8
from __future__ import print_function

from volcengine.image_registry.BasicImageRegistryService import BasicImageRegistryService

if __name__ == '__main__':
    registry = BasicImageRegistryService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    registry.set_ak('ak')
    registry.set_sk('sk')

    params = {}
    body = {}

    resp = registry.list_namespaces(params, body)
    print(resp)
