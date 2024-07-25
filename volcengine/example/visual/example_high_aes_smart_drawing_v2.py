# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('AK')
    visual_service.set_sk('SK')

    form = {
        "req_key": "img2img_photoverse_executive_ID_photo",
        # "binary_data_base64":[],
        "return_url":True,
        "image_urls": ["https://"],
        "beautify_info":{
            "whitening":1.0,
            "dermabrasion":1.0
        },
        "logo_info": {
            "add_logo": False,
            "position": 0,
            "language": 0,
            "opacity": 0.3
        }
    }
    resp = visual_service.high_aes_smart_drawing_v2(form)
    print(resp)
