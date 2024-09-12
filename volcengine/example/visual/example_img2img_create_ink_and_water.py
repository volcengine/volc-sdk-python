# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('AK')
    visual_service.set_sk('SK')

    form = {
        "req_key": "img2img_water_ink_style",
        # "binary_data_base64":[],
        "image_urls": [
            "https://"],
        "prompt": "",
        "sub_prompts": [""],
        "strength": 0.6,
        "seed": -1,
        "scale": 8,
        "ddim_steps": 20,
        "lora_map": {'Cateye_AT45': {'strength_model': 0.2, 'strength_clip': 0.2},'CATSEYEcp001': {'strength_model': 0.2, 'strength_clip': 0.2}},
        "clip_skip": 1,
        "controlnet_weight": 1,
        "sampler_name": "dpmpp_2m",
        "scheduler": "karras",
        "long_resolution": 832,
        "cn_mode": 0,
        "id_weight": 1.0,
        "apply_id_layer": "2,3,4,5,6,7,8,9,10,11,12",
        "tagger_settings": {"switch": False},
        "vae_choice": 1,
        "return_url": True,
        "logo_info": {
            "add_logo": False,
            "position": 0,
            "language": 0,
            "opacity": 0.3
        }
    }
    resp = visual_service.img2img_create_ink_and_water(form)
    print(resp)
