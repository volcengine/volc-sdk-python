# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')
    #Config接口
    # form = {
    #         "req_key":"cert_config_init",
    #         "config_name":"",
    #         "token_api_config":{
    #             "ref_source":"1"
    #         },
    #         "h5_config":{
    #             "redirectUrl":"",
    #             "type":1
    #         }
    #     }

    #ConfigPro接口
    form = {
        "req_key": "cert_config_init",
        "config_name": "",
        #"config_desc":"",
        "token_api_config": {
            "ref_source": "1"
        }
    }

    resp = visual_service.cert_config_init(form)
    print(resp)
