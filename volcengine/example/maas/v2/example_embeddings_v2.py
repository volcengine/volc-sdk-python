import os
from volcengine.maas.v2 import MaasService
from volcengine.maas import MaasException


def test_embeddings(maas, endpoint_id, req):
    try:
        resp = maas.embeddings(endpoint_id, req)
        print(resp)
    except MaasException as e:
        print(e)


if __name__ == '__main__':
    maas = MaasService('maas-api.ml-platform-cn-beijing.volces.com', 'cn-beijing')

    maas.set_ak(os.getenv("VOLC_ACCESSKEY"))
    maas.set_sk(os.getenv("VOLC_SECRETKEY"))

    # document: "https://www.volcengine.com/docs/82379/1099475"
    # embeddings
    embeddingsReq = {
        "input": [
            "天很蓝",
            "海很深"
        ]
    }

    endpoint_id = "{YOUR_ENDPOINT_ID}"
    test_embeddings(maas, endpoint_id, embeddingsReq)
