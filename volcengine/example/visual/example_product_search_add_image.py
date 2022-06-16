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
        "category_id": 1,
        "url": "https://xxx",
        "custom_content": "custom",
        "int_attr": 1,
        "str_attr": "str",
        "crop": True,
        # "region": {
        #     'x1': 1,
        #     'x2': 2,
        #     'y1': 3,
        #     'y2': 4,
        # }
    }

    resp = visual_service.product_search_add_image(params)
    print(resp)
