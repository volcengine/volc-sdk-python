import os
from volcengine.maas import MaasService, MaasException


def test_embeddings(maas, req):
    try:
        resp = maas.embeddings(req)
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
        "model": {
            "name": "${YOUR_MODEL_NAME}"
        },
        "input": [
            "天很蓝",
            "海很深"
        ]
    }

    test_embeddings(maas, embeddingsReq)
