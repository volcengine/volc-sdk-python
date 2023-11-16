# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')

    form = {
        "mode": 1,
        "refine_mask": 0 ,
        "image_url":"https://xxx",
        "flip_test":1
    }

    resp = visual_service.hair_segment(form)
    print(resp)
