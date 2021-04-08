#  -*- coding: utf-8 -*-
from __future__ import print_function

from volcengine.nlp.NLPService import NLPService

if __name__ == '__main__':
    nlp_service = NLPService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    nlp_service.set_ak('ak')
    nlp_service.set_sk('sk')

    params = dict()

    form = {
        "content": "This is a incomplte text test"
    }

    resp = nlp_service.text_correction_en_correct(form)
    print(resp)
