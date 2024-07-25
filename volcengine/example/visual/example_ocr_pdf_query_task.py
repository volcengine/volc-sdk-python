# coding:utf-8
from __future__ import print_function

import json

from six import b

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('AK')
    visual_service.set_sk('SK')

    form = {
        "req_key": "ocr_pdf",
        "task_id": "7394366186341040167"
    }
    resp = visual_service.ocr_pdf_query_task(form)
    print(resp)

    resp_data = resp['data']['resp_data']
    print(eval(f"u'{resp_data}'"))
