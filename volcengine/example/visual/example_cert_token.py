# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('')
    visual_service.set_sk('')

    #Token接口
    # form = {
    #         "req_key":"cert_token",
    #         "sts_token":"",
    #         "liveness_type":"motion",
    #         "ref_source":"1",
    #         "idcard_name":"",
    #         "idcard_no":""
    #     }
    #TokenPro接口
    form = {
        "req_key": "cert_pro_token",
        "sts_token": "",
        "ref_source": "1",
        "idcard_name": "",
        "idcard_no": ""
    }
    resp = visual_service.cert_token(form)
    print(resp)
