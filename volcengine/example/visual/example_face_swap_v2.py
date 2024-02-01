# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('')
    visual_service.set_sk('')

    form = {
        # 注意3.0版本req_key传faceswap | | 3.3版本req_key传face_swap3_3
        "req_key": "faceswap",
        "image_urls": [
            "https://xxx",
            "https://xxx",
            "https://xxx"
        ],
        "face_type": "area",
        "merge_infos": [
            {
                "location": 1,
                "template_location": 1
            },
            {
                "location": 1,
                "template_location": 2
            }
        ]
        # "logo_info":{
        #     "add_logo":True,
        #     "position":2,
        #     "language":0,
        #     "opacity":1.0
        # },
        # "do_risk":False,
        # "source_similarity":"1"
    }
    resp = visual_service.face_swap_v2(form)
    print(resp)
