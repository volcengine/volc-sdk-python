
from __future__ import print_function

from volcengine.adblocker.AdBlockerService import AdBlockService


if __name__ == '__main__':
    adblocker = AdBlockService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    adblocker.set_ak('ak')
    adblocker.set_sk('sk')

    params = dict()
    req = {
         'app_id': 3332,
         'service': "chat",
         'parameters': '{"uid":123411, "operate_time":1609818934, "chat_text":"a"}'
    }

    resp = adblocker.ad_block(params, req)
    print(resp)
