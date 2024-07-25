# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('AK')
    visual_service.set_sk('SK')

    form = {
        "req_key": "i2i_outpainting",
        "binary_data_base64": [
            ""
        ],
        "image_urls": [],
        "custom_prompt": "蓝色海洋",
        "return_url": True,
        "steps": 30,
        "strength": 0.8,
        "scale": 7.0,
        "seed": 0,
        "top": 0.1,
        "bottom": 0.1,
        "left": 1,
        "right": 1,
        "max_height": 1920,
        "max_width": 1920,
        "logo_info": {
            "add_logo": False,
            "position": 0,
            "language": 0,
            "opacity": 0.3
        }
    }
    resp = visual_service.img2img_outpainting(form)
    print(resp)
