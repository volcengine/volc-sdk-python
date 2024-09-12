# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('AK')
    visual_service.set_sk('SK')

    form = {
        "req_key": "img2img_rev_animated_style",
        # "binary_data_base64":[],
        "image_urls": [
            "https://"],
        "prompt": "",
        "strength": 0.8,
        "seed": -1,
        "scale": 8,
        "ddim_steps": 20,
        "lora_multipers": {'shanzhagaoSomeSortOf_v1Epoch10': 0.6, 'Moxin_10': 0.5, 'Colorwater_v4': 0.3},
        "clip_skip": 1,
        "canny_weight": 1,
        "sampler_name": "DPM++ 2M Karras",
        "id_scale": 0,
        "return_url": True,
        "logo_info": {
            "add_logo": False,
            "position": 0,
            "language": 0,
            "opacity": 0.3
        }

    }

    resp = visual_service.img2img_create_rev_animated(form)
    print(resp)
