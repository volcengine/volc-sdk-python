# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')

    form = {
        "image_url":"https://xxx",
        "refine":0,
        "return_foreground_image":0
    }

    resp = visual_service.human_segment(form)
    print(resp)
