import os
from volcengine.maas import MaasService, MaasException


def test_classification(maas, req):
    try:
        resp = maas.classification(req)
        print(resp)
    except MaasException as e:
        print(e)


if __name__ == '__main__':
    maas = MaasService('maas-api.ml-platform-cn-beijing.volces.com', 'cn-beijing')

    maas.set_ak(os.getenv("VOLC_ACCESSKEY"))
    maas.set_sk(os.getenv("VOLC_SECRETKEY"))

    # document: "https://www.volcengine.com/docs/82379/1099475"
    # classification
    classificationReq = {
        "model": {
            "name": "${YOUR_MODEL_NAME}"
        },
        "query": "花儿为什么这么香？",
        "labels": ["陈述句", "疑问句", "肯定句"],
    }

    test_classification(maas, classificationReq)

