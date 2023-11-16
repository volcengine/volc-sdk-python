# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')

    form = {
        "hair_type": "0",
        "image_url":"https://xxx",
        "do_risk":False
    }

    resp = visual_service.hair_style(form)
    print(resp)
