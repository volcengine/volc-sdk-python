# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('AK')
    visual_service.set_sk('SK')

    form = {
        # "binary_data_base64": [""],
        "image_urls": [
            "https://"],
        "req_key": "entity_seg",
        "return_url": True,
        "max_entity": 20,
        "return_format": 0,
        "refine_mask": 0
    }

    resp = visual_service.entity_segment(form)
    print(resp)
