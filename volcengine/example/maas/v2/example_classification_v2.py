import os
from volcengine.maas.v2 import MaasService
from volcengine.maas import MaasException


def test_classification(maas, endpoint_id, req):
    try:
        resp = maas.classification(endpoint_id, req)
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
        "query": "花儿为什么这么香？",
        "labels": ["陈述句", "疑问句", "肯定句"],
    }

    endpoint_id = "{YOUR_ENDPOINT_ID}"
    test_classification(maas, endpoint_id, classificationReq)

