# coding:utf-8
from __future__ import print_function

from volcengine import visual
from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')
    # 设置超时时间，最大30s
    # visual_service.set_connection_timeout(30)

    # # version = 2020-08-26
    # # 参考接口文档query部分 传Action、Version
    # action = ""
    # version = ""
    # visual_service.set_api_info(action, version)
    # # body 参考接口文档 请求Body传参部分
    # form = dict()
    # form["image_base64"] = "image_base64_str"
    # resp = visual_service.cv_form_api(action, form)
    # print(resp)

    # version >= 2022-08-31
    # 参考接口文档query部分 传Action、Version
    action = ""
    version = ""
    visual_service.set_api_info(action, version)
    # body 参考接口文档 请求Body传参部分
    form = {
        "req_key": "xxxx",
        # ...
    }

    resp = visual_service.cv_json_api(action, form)
    print(resp)
