# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('AK')
    visual_service.set_sk('SK')

    form = {
        "req_key": "img2img_water_paint_style",
        # "binary_data_base64":[],
        "image_urls": [
            "https://"],
        "return_url": True,
    }

    resp = visual_service.img2img_water_color_style(form)
    print(resp)
