# coding:utf-8
from __future__ import print_function
from volcengine.imagex.ImageXService import ImageXService

if __name__ == '__main__':
    imagex_service = ImageXService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    imagex_service.set_ak('ak')
    imagex_service.set_sk('sk')

    req1 = {
        'ServiceId': 'imagex service id',
        'Url': 'image uri',
        # 'Async': True,
    }
    resp1 = imagex_service.fetch_image_url(req1)
    print(resp1)

    if 'TaskId' not in resp1:
        exit()

    req2 = {
        'ServiceId': req1['ServiceId'],
        'Id': resp1['TaskId'],
    }
    resp2 = imagex_service.get_url_fetch_task(req2)
    print(resp2)
