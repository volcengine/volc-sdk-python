# coding:utf-8
from __future__ import print_function
from volcengine.imagex.v2.imagex_service import ImagexService

if __name__ == '__main__':
    imagex_service = ImagexService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    imagex_service.set_ak('ak')
    imagex_service.set_sk('sk')

    params = dict()
    params['ServiceId'] = 'imagex service id'
    params['SkipMeta'] = False
    # params['UploadHost'] = 'upload host'
    params['SkipCommit'] = False
    file_paths = ['image file path 1']
    resp = imagex_service.upload_image(params, file_paths)
    print(resp)

    img_datas = ['image data 1']
    resp = imagex_service.upload_image_data(params, img_datas)
    print(resp)
