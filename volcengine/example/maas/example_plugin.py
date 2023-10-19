import os
from volcengine.maas import MaasService, MaasException, ChatRole


def test_chat(maas, req):
    try:
        resp = maas.chat(req)
        print(resp)
    except MaasException as e:
        print(e)


if __name__ == "__main__":
    maas = MaasService("maas-api.ml-platform-cn-beijing.volces.com", "cn-beijing")

    maas.set_ak(os.getenv("VOLC_ACCESSKEY"))
    maas.set_sk(os.getenv("VOLC_SECRETKEY"))

    # document: "https://www.volcengine.com/docs/82379/1099475"
    req = {
        "model": {"name": "${YOUR_MODEL_NAME}"},
        "parameters": {"max_new_tokens": 2000, "temperature": 0.8},
        "messages": [
            {"role": ChatRole.USER, "content": "说一说这周发生的新鲜事儿"},
        ],
        "plugins": ["browsing"],
    }

    test_chat(maas, req)
