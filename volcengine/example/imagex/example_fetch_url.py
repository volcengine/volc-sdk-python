# coding:utf-8
from __future__ import print_function
from volcengine.imagex.ImageXService import ImageXService

if __name__ == '__main__':
    imagex_service = ImageXService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    imagex_service.set_ak('ak')
    imagex_service.set_sk('sk')

    req = dict()
    req['ServiceId'] = 'imagex service id'
    req['Url'] = 'image uri'

    resp = imagex_service.fetch_image_url(req)
    print(resp)
