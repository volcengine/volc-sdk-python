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
        "service_choice":0,
        "do_risk":False
    }

    resp = visual_service.emoticon_edit(form)
    print(resp)
