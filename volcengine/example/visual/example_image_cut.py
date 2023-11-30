# coding:utf-8
from __future__ import print_function

import time

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')

    params = dict()

    form = {
        "image_url": "https://xxx",
        "width": 100,
        "height": 120,
        "cut_method": "gauss_padding_reserve_score"
    }

    resp = visual_service.image_cut(form)
    print(resp)
