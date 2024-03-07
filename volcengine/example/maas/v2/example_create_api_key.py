import os
from volcengine.maas.v2 import MaasService
from volcengine.maas import MaasException, ChatRole


def test_create_api_key(maas, req):
    try:
        apikey = maas.create_or_refresh_api_key(req)
        print(apikey)
    except MaasException as e:
        print(e)


if __name__ == '__main__':
    maas = MaasService('open.volcengineapi.com', 'cn-beijing')

    maas.set_ak(os.getenv("VOLC_ACCESSKEY"))
    maas.set_sk(os.getenv("VOLC_SECRETKEY"))

    req = {
        "Ttl": 86400,  # seconds
        "EndpointIdList": ["{YOUR_ENDPOINT_ID_LIST}"],
    }

    test_create_api_key(maas, req)
