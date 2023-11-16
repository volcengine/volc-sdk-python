# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')

    form = {
        "req_key": "facefusionmovie_standard_v2",
        "image_url": "https://xxx",
        "video_url": "https://xxx",
        "ref_img_url": "https://xxx",
        "source_similarity": 1,
         "logo_info": {
            "add_logo": True,
            "position": 2,
            "language": 0,
            "opacity": 0.9
        }
    }

    resp = visual_service.face_fusion_movie_submit_task(form)
    print(resp)
