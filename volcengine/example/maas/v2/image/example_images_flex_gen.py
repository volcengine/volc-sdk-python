import os
import base64
from volcengine.maas.v2 import MaasService
from volcengine.maas import MaasException


def test_images_flex_gen(maas, endpoint_id, req):
    try:
        resp = maas.images.flex_gen(endpoint_id, req)
        print(resp)
    except MaasException as e:
        print(e)


if __name__ == '__main__':
    maas = MaasService('maas-api.ml-platform-cn-beijing.volces.com', 'cn-beijing')

    maas.set_ak(os.getenv("VOLC_ACCESSKEY"))
    maas.set_sk(os.getenv("VOLC_SECRETKEY"))

    with open("{YOUR_CONTROL_PICTURE_PATH}", "rb") as file:
        controlImage = base64.b64encode(file.read()).decode('utf-8')

    req = {
        "prompt": "(sfw:1.0),(masterpiece,best quality,ultra highres),(realistic:1.15),(3D:1.0)",
        "negative_prompt": "(embedding:EasyNegative:0.9),(embedding:badhandv4:1.3),terrible,injured,(nsfw:1.0),(nude:1.0)",
        "control_image_list": [controlImage],
        "strength": 0.75,
        "height": 512,
        "width": 512,
        "num_inference_steps": 20,
    }

    endpoint_id = "{YOUR_ENDPOINT_ID}"
    test_images_flex_gen(maas, endpoint_id, req)
