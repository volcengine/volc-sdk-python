# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('')
    visual_service.set_sk('')

    form = {
        "req_key": "cert_pro_liveness_verify_query",
        "byted_token": "",
        "omit_data": False,
        "omit_image_data": False,
        "omit_video_data": False
    }
    resp = visual_service.cert_pro_liveness_verify_query(form)
    print(resp)
