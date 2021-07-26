#  -*- coding: utf-8 -*-
from __future__ import print_function

from volcengine.nlp.NLPService import NLPService

if __name__ == '__main__':
    nlp_service = NLPService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    nlp_service.set_ak('ak')
    nlp_service.set_sk('sk')

    params = dict()

    body = {
        "content": "好就不见"
    }

    resp = nlp_service.novel_correction(body)
    print(resp)
