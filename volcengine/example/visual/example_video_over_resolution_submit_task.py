# coding:utf-8
from __future__ import print_function

import time

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')

    form = {
        "output_resolution": "output_resolution",
        "video_url": ""
    }

    resp = visual_service.video_over_resolution_submit_task(form)
    print(resp)
