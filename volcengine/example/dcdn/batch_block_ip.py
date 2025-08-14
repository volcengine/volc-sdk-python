#  -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")

from volcengine.example.dcdn import ak, sk
from volcengine.dcdn.DCDNService import DCDNService

if __name__ == '__main__':
    svc = DCDNService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    svc.set_ak(ak)
    svc.set_sk(sk)

    body = {
        "Domains": [],
        "IPList": [
            "2.2.2.2"
        ],
        "OperatorType": "block",
        "BlockInterval": 1440,
        "UpdateType": "cover",
    }


    resp = svc.batch_block_ip(body)
    print(resp)
