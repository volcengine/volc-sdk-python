from __future__ import print_function

import time

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')

    params = {
        "category_id": 1,
        "url": "https://xxx",
        "custom_content": "custom",
        "crop": True,
        "filter": '{"op":"must","field":"strAttr","conds":["str"]}'
        # "region": {
        #     'x1': 1,
        #     'x2': 2,
        #     'y1': 3,
        #     'y2': 4,
        # }
    }

    resp = visual_service.product_search_search_image(params)
    print(resp)
