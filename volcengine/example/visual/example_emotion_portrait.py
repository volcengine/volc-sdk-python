# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('AK')
    visual_service.set_sk('SK')

    form = {
        "req_key": "emotion_portrait",
        "image_urls": [""],
        "target_emotion": "jiuwo"
    }

    resp = visual_service.emotion_portrait(form)
    print(resp)
