# coding:utf-8
from __future__ import print_function
from volcengine.imagex.v2.imagex_service import ImagexService

if __name__ == '__main__':
    imagex_service = ImagexService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    imagex_service.set_ak('ak')
    imagex_service.set_sk('sk')

    body = dict()
    body['ServiceId'] = 'service id'
    body['StoreUri'] = 'xx'

    resp = imagex_service.get_image_comic_result(body)
    print(resp)
