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
        "strategy": "STATIC_CROPPING",
        "aspect_ratio": 1,
        "crop_size": 1,
        "video_url": ""
    }

    resp = visual_service.video_retargeting_submit_task(form)
    print(resp)

    params = dict()

    params = {
        "task_id": "get from submit_task resp"
    }

    resp = visual_service.video_retargeting_query_task(params)
    print(resp)
