# coding:utf-8
from __future__ import print_function
from volcengine.imagex.v2.imagex_service import ImagexService

if __name__ == '__main__':
    imagex_service = ImagexService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    imagex_service.set_ak('your ak')
    imagex_service.set_sk('your sk')

    query = dict()
    query['ServiceId'] = "xx"

    body = dict()
    body['Scene'] = "license"
    body['StoreUri'] = "xx"

    resp = imagex_service.get_image_ocr_v2(query,body)
    print(resp)
