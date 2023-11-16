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
        "type":"3d_cartoon",
        "return_type":1
    }

    resp = visual_service.potrait_effect(form)
    print(resp)
