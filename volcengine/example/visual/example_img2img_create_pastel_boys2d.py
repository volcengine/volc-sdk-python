# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('AK')
    visual_service.set_sk('SK')

    form = {
        "req_key": "img2img_pastel_boys_style",
        # "binary_data_base64": [],
        "image_urls": [
            "https://"],
        "prompt": "good looking,(((pure white statue))),(((only white color in picture))), (((white plaster figure))), (Renaissance), ancient Greek mythological statue, monochromatic realism style, rococo, (((plaster texture))), ((white hair)), 8k, best quality, masterpiece, depth, face light,",
        "strength": 0.6,
        "seed": -1,
        "scale": 8,
        "ddim_steps": 20,
        "lora_multipers": {
        },
        "clip_skip": 1,
        "canny_weight": 0.8,
        "i2i_keep_texture": 1,
        "long_resolution": 704,
        "id_scale": 0,
        "return_url": True,
        "logo_info": {
            "add_logo": False,
            "position": 0,
            "language": 0,
            "opacity": 0.3
        }
    }

    resp = visual_service.img2img_create_pastel_boys2d(form)
    print(resp)
