# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')

    form = {
        "req_key": "lens_lqir",
        "image_urls": [
            "https://xxx"
        ],
        "resolution_boundary": "540p",
        "enable_hdr": False,
        "enable_wb": False,
        "result_format": 1,
        "jpg_quality": 95,
        "hdr_strength": 1.0
    }

    resp = visual_service.enhance_photo_v2(form)
    print(resp)
