# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')

    # 高美感通用v1.1-图生图
    # form = {
    #         "req_key": "high_aes_i2i",
    #         "prompt": "千军万马",
    #         "strength": 0.5,
    #         "seed": -1,
    #         "scale": 7.5,
    #         "ddim_steps": 20,
    #         "binary_data_base64": [""],
    #         "logo_info": {
    #             "add_logo": False,
    #             "position": 0,
    #             "language": 0,
    #             "opacity": 0.3
    #         }
    #     }



    #  高美感通用v1.2-文生图
    # form ={
    #
    #     "req_key": "high_aes_t2i",
    #     "prompt": "千军万马",
    #     "seed": -1,
    #     "scale": 5.5,
    #     "ddim_steps": 25,
    #     "width": 512,
    #     "height": 512,
    #     "logo_info": {
    #
    #         "add_logo": False,
    #         "position": 0,
    #         "language": 0,
    #         "opacity": 0.3
    #     }
    #
    # }

    # 高美感动漫v1.3-文生图/图生图
    # form = {
    #     "req_key": "high_aes",
    #     "prompt": "千军万马",
    #     "model_version": "anime_v1.3",
    #     "strength": 0.7,
    #     "seed": -1,
    #     "scale": 7,
    #     "ddim_steps": 20,
    #     "width": 1024,
    #     "height": 1024,
    #     "logo_info": {
    #         "add_logo": False,
    #         "position": 0,
    #         "language": 0,
    #         "opacity": 0.3
    #     },
    #     # "binary_data_base64": [""]       #源图片，仅支持单图输入，图生图必选该字段
    #
    # }

    # 高美感通用V1.3-文生图
    form = {
        "req_key": "high_aes",
        "prompt": "千军万马",
        "model_version": "general_v1.3",
        "seed": -1,
        "scale": 3.5,
        "ddim_steps": 25,
        "width": 512,
        "height": 512,
        "use_sr": False,
        "sr_seed": -1,
        "logo_info": {
            "add_logo": False,
            "position": 0,
            "language": 0,
            "opacity": 0.3
        }
    }

    resp = visual_service.high_aes_smart_drawing(form)
    print(resp)
