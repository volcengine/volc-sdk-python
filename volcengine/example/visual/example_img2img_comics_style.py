# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('AK')
    visual_service.set_sk('SK')

    form = {
        "req_key": "img2img_comic_style",
        "binary_data_base64":[],
        "image_urls": [
            "https://xxx"
        ],
        "sub_req_key": "img2img_comic_style_marvel",
        "return_url": True,
        "logo_info": {
            "add_logo": True,
            "position": 2,
            "language": 0,
            "opacity": 1.0
        }
    }
    resp = visual_service.img2img_comics_style(form)
    print(resp)
