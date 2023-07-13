# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')

    form = {
        "req_key": "facefusionmovie_standard",
        # "binary_data_base64": ["/9xx"],
        "image_url": 'https://xxxx, https://xxxx',
        "video_url": 'https://xxxx',
        "enable_face_beautify": True,
        # "ref_img_url": "https://xxxx, https://xxxx"
    }

    resp = visual_service.face_fusion_movie(form)
    print(resp)
