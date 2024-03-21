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
    tag = dict()
    # tag 字段如下，可选择所需字段传入
    # upload_policy_dict = {
    #     "FileSizeUpLimit": "xxx",
    #     "FileSizeBottomLimit": "xxx",
    #     "ContentTypeBlackList":[
    #         "xxx"
    #     ],
    #     "ContentTypeWhiteList":[
    #         "xxx"
    #     ]
    # }
    # policy_str = json.dumps(upload_policy_dict)
    #
    # tag = {
    #     "UploadOverwrite": "true",
    #     "UploadPolicy": policy_str,
    # }
    resp = imagex_service.get_upload_auth(service_ids, tag=tag)
    print(resp)
