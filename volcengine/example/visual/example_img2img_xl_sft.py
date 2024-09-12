# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('AK')
    visual_service.set_sk('SK')

    form = {
        "req_key": "i2i_xl_sft",
        # "binary_data_base64":[],
        "image_urls": [
            "https://xxx"
        ],
        "prompt": "美女",
        "seed": -1,
        "ddim_step": 20,
        "scale": 7.0,
        "controlnet_args": [
            {
                "type": "pose",
                "strength": 0.4,
                "binary_data_index": 0
            }
        ],
        "style_reference_args": {
            "id_weight": 0.2,
            "style_weight": 0.0,
            "binary_data_index": 0
        },
        "return_url": True,
        "logo_info": {
            "add_logo": True,
            "position": 2,
            "language": 0,
            "opacity": 1
        }
    }
    resp = visual_service.img2img_xl_sft(form)
    print(resp)
