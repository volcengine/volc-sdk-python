# coding:utf-8
from __future__ import print_function

from volcengine.image_registry.ImageRegistryService import ImageRegistryService

if __name__ == '__main__':
    registry = ImageRegistryService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    registry.set_ak('ak')
    registry.set_sk('sk')

    params = {}
    body = {}

    resp = registry.list_namespace_basic(params, body)
    print(resp)
