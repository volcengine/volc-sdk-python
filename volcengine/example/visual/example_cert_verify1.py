# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')
    #Verify接口
    # form = {
    #     "req_key":"cert_src_verify",
    #     "byted_token":"",
    #     "video_url":"",
    #     "extra":{
    #         "video_type": "motion"
    #     }
    #     }

    #VerifyPro接口
    form = {
            "req_key":"cert_pro_src_verify",
            "byted_token":"",
            "video_key":"",
            "tos_bucket":"",
            "risk_info":"",
            "extra":{}
            }

    resp = visual_service.cert_verify(form)
    print(resp)
