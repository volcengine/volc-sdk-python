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
        "grade": "junior",
        "question": "My Beloved Teacher",
        "essay": "Sara, who came from Canada is our English Oral teacher. She is loved and respected by many students. What impressed me the most is that she is warm-hearted, generous and easy-going. She always stays optimistic and tries hard to understand every of her student. Besides, she often tells us some interesting stories and jokes in class, so as to make a happy atmosphere for us to study English. She loves teaching so much and has the eagerness to devote her life to Chinese education. Because of her outstanding achievements, she had won lots of rewards, one of which is “Model Teacher”.",
    }

    resp = nlp_service.essay_auto_grade(form)
    print(resp)
