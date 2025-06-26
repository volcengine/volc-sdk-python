# coding:utf-8
from volcengine.live.v20230101.live_service import LiveService

if __name__ == '__main__':
    service = LiveService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    service.set_ak('ak')
    service.set_sk('sk')

    body = {}

    resp = service.describe_high_light_task_by_account_id(body)
    print(resp)
