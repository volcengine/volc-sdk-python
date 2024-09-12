# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')

    form = {
        "req_key": "img2video3d",
        "image_urls": [
            "https://xxx"
        ],
        "render_spec": {
            "mode": 2,
            "long_side": 960,
            "frame_num": 90,
            "fps": 30,
            "use_flow": -1,
            "speed_shift": [
                0,
                1,
                0.5,
                4,
                0.5,
                4,
                1,
                1
            ]
        }
    }

    resp = visual_service.img2video3d(form)
    print(resp)
