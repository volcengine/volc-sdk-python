# coding:utf-8
from __future__ import print_function
from volcengine.imagex.ImageXService import ImageXService

if __name__ == '__main__':
    imagex_service = ImageXService()


    imagex_service.set_ak('ak')
    imagex_service.set_sk('sk')

    params = dict()
    params['ServiceId'] = 'service id'
    params['StoreUri'] = 'xx'
    params['Model'] = 0
    params['Top'] = 0.0
    params['Bottom'] = 0.0
    params['Left'] = 0.0
    params['Right'] = 0.0

    resp = imagex_service.get_image_bg_fill_result(params)
    print(resp)
