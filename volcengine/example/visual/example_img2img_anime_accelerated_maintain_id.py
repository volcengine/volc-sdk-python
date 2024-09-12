# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('AK')
    visual_service.set_sk('SK')

    form = {
        "req_key": "img2img_anime_accelerated_maintain_id",
        "positive_prompt": "1girl,beautiful,looking at viewer,portrait,",
        "return_url": True,
        "image_urls": [
            "https://"],
        # "binary_data_base64": [],
        "hyper_switch": True,
        # "seed": -1,
        # "step": 18,
        # "cfg": 4.5,
        # "face_image": "uri://binary_data?index=0",
        # "style_image": "uri://binary_data?index=1",
        # "face_switch": True,
        # "facestyle_switch": True,
        # # "style_switch": False,
        # "width": 1000,
        # "height": 1000,
        # "logo_info": {
        #     "add_logo": True,
        #     "position": 2,
        #     "language": 0,
        #     "opacity": 1
        # }
    }
    resp = visual_service.img2img_anime_accelerated_maintain_id(form)
    print(resp)
