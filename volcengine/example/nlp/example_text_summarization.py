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
        "title": "汽车",
        "text": "例如会让部件磨损大，使得寿命降低，而且还带来动力降低，油耗越来越高，抖动大等。以前一箱油能跑380公里的，如今却只能跑到350了，无疑也增加了开车成本。",
        "max_len": 5
    }

    resp = nlp_service.text_summarization(form)
    print(resp)
