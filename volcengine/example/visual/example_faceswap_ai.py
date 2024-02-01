# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('')
    visual_service.set_sk('')

    form = {
        "req_key": "faceswap_ai",
        "image_urls": [
            "https://xxx",
            "https://xxx"
        ],
        "gpen":0.9,
        "skin":0.9
        # "do_risk":False,
        # "tou_repair":1
    }
    resp = visual_service.faceswap_ai(form)
    print(resp)
