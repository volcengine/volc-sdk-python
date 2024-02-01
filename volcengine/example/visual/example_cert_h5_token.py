# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('')
    visual_service.set_sk('')

    form = {

        "req_key":"cert_h5_token",
        "h5_config_id":"",
        "sts_token":"",
        "idcard_name":"",
        "idcard_no":""
}
    resp = visual_service.cert_5_token(form)
    print(resp)
