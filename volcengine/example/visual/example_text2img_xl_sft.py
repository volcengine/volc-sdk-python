# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('AK')
    visual_service.set_sk('SK')

    form = {
        "req_key": "t2i_xl_sft",
        "prompt": "少女，光影，瘦，白皙，干净，美丽",
        "width": 1024,
        "height": 1024,
        "seed": -1,
        "ddim_steps": 20,
        "scale":7.0,
        "return_url": True,
        "logo_info": {
            "add_logo": True,
            "position": 2,
            "language": 0,
            "opacity": 1
        }
    }
    resp = visual_service.text2img_xl_sft(form)
    print(resp)
