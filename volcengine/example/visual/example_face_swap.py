# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')
    #2.0版本
    # form = {
    #     "image_url":"",
    #     "template_url":"",
    #     "action_id":"faceswap",
    #     "version":"2.0",
    #     "do_risk":False,
    #     "source_similarity":"1"
    # }

    # 2.1版本
    form = {
        "template_url":"",
        "action_id":"faceswap",
        "version":"2.1",
        "do_risk":False,
        "type":"l2r",
        "merge_infos":'[{"image_url":"https://xxx","location":1,"template_location":1}]'
    }

    resp = visual_service.face_swap(form)
    print(resp)
