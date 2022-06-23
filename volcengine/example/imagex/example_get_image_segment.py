# coding:utf-8
from __future__ import print_function
from volcengine.imagex.ImageXService import ImageXService

if __name__ == '__main__':
    imagex_service = ImageXService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    imagex_service.set_ak('your ak')
    imagex_service.set_sk('your sk')

    params = dict()
    params['ServiceId'] = 'xx'
    params['Class'] = 'class'
    params['Refine'] = True
    params['StoreUri'] = 'store uri'
    params['OutFormat'] = 'out format'
    params['TransBg'] = True
    params['Color'] = {
        'Color': "color",
        'Size': 0
    }

    resp = imagex_service.get_image_segment(params)
    print(resp)