# coding:utf-8
from __future__ import print_function
from volcengine.imagex.v2.imagex_service import ImagexService

if __name__ == '__main__':
    imagex_service = ImagexService()

    imagex_service.set_ak('ak')
    imagex_service.set_sk('sk')

    body = dict()
    body['ServiceId'] = 'service id'
    body['StoreUri'] = 'xx'
    body['Model'] = 0
    body['Top'] = 0.0
    body['Bottom'] = 0.0
    body['Left'] = 0.0
    body['Right'] = 0.0

    resp = imagex_service.get_image_bg_fill_result(body)
    print(resp)
