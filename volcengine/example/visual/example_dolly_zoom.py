# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('sk')
    visual_service.set_sk('sk')

    form = {
        "image_url":"https://xxx",
        "video_type":0,
        "device_type":0,
        "video_length":2.5
    }

    resp = visual_service.dolly_zoom(form)
    print(resp)
