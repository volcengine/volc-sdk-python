import os
from volcengine.maas.v2 import MaasService
from volcengine.maas import MaasException


def test_tokenize(maas, endpoint_id, req):
    try:
        resp = maas.tokenize(endpoint_id, req)
        print(resp)
    except MaasException as e:
        print(e)


if __name__ == '__main__':
    maas = MaasService('maas-api.ml-platform-cn-beijing.volces.com', 'cn-beijing')

    maas.set_ak(os.getenv("VOLC_ACCESSKEY"))
    maas.set_sk(os.getenv("VOLC_SECRETKEY"))

    # document: "https://www.volcengine.com/docs/82379/1099475"
    # tokenize
    tokenizeReq = {
        "text": "花儿为什么这么香？",
    }

    endpoint_id = "{YOUR_ENDPOINT_ID}"
    test_tokenize(maas, endpoint_id, tokenizeReq)
