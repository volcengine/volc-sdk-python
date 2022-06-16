from __future__ import print_function

import time

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')

    params = {
        "product_id": "test",
        "image_id": "test",
    }

    resp = visual_service.product_search_delete_image(params)
    print(resp)
