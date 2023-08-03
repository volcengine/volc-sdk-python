# coding:utf-8
from __future__ import print_function

from volcengine.imagex.ImageXService import ImageXService

if __name__ == '__main__':
    imagex_service = ImageXService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    imagex_service.set_ak('ak')
    imagex_service.set_sk('sk')

    # service id list allowed to do upload, set to empty if no restriction
    service_ids = ['imagex service id']

    resp = imagex_service.get_upload_auth(service_ids)
    print(resp)
