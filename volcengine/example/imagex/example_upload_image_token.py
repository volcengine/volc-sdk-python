# coding:utf-8
from __future__ import print_function

from volcengine.imagex.ImageXService import ImageXService

if __name__ == '__main__':
    imagex_service = ImageXService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    imagex_service.set_ak('ak')
    imagex_service.set_sk('sk')

    params = dict()
    params['ServiceId'] = 'imagex service id'

    resp = imagex_service.get_upload_auth_token(params)
    print(resp)
