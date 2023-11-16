# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')
    form = {
        "req_key":"face_compare",
        "image_urls":[
            "http://xxx",
            "http://xxx"
        ]
        }
    resp = visual_service.face_compare(form)
    print(resp)
