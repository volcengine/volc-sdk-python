# coding:utf-8
from __future__ import print_function
from volcengine.imagex.ImageXService import ImageXService

if __name__ == '__main__':
    imagex_service = ImageXService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    imagex_service.set_ak('ak')
    imagex_service.set_sk('sk')

    params = dict()
    params['ServiceId'] = 'service id'
    params['StoreUri'] = 'xx'
    params['Model'] = ''

    resp = imagex_service.get_image_erase_result(params)
    print(resp)
