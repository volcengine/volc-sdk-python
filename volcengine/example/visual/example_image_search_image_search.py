from __future__ import print_function

import time

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')

    form = {
        "url":	"url_1",
        # "image_base64": "img_b64_1",
        "topk": 10
    }

    resp = visual_service.image_search_image_search(form)
    print(resp)
