import os
from volcengine.maas.v2 import MaasService
from volcengine.maas import MaasException


def test_speech(maas: MaasService, endpoint_id, req, file):
    request_id = ""
    try:
        resp = maas.audio.speech.create(endpoint_id, req)
        request_id = resp.request_id
        resp.stream_to_file(file)
        print(f"request_id: {request_id}")
        print("finish create audio file.")
    except MaasException as e:
        print(f"request_id: {request_id}")
        print(e)


if __name__ == '__main__':
    maas = MaasService('maas-api.ml-platform-cn-beijing.volces.com', 'cn-beijing')

    maas.set_ak(os.getenv("VOLC_ACCESSKEY"))
    maas.set_sk(os.getenv("VOLC_SECRETKEY"))

    req = {
        "input": "你好欢迎光临",
        "voice": "zh_male_rap",
        "response_format": "mp3",
        "speed": 1.0
    }

    endpoint_id = "{YOUR_ENDPOINT_ID}"
    file = "{YOUR_LOCAL_FILE}"
    test_speech(maas, endpoint_id, req, file)

