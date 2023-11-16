# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')

    form = {
        "req_key": "lens_vida_single_pic",
        "image_urls": [
            "https://xxx"
        ],
        "vida_mode": "vida_custom",
        "vida_enable_module": "score_total_ds"
    }

    resp = visual_service.image_score_v2(form)
    print(resp)
