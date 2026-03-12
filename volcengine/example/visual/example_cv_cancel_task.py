# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('Ak')
    visual_service.set_sk('Sk')

    form = {
        "req_key": "xxx",
        "task_id": "123456"
    }
    resp = visual_service.cv_cancel_task(form)
    print(resp)
