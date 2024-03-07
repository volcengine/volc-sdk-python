import os
from volcengine.maas.v2 import MaasService
from volcengine.maas import MaasException


def test_images_quick_gen(maas, endpoint_id, req):
    try:
        resp = maas.images.quick_gen(endpoint_id, req)
        print(resp)
    except MaasException as e:
        print(e)


if __name__ == '__main__':
    maas = MaasService('maas-api.ml-platform-cn-beijing.volces.com', 'cn-beijing')

    maas.set_ak(os.getenv("VOLC_ACCESSKEY"))
    maas.set_sk(os.getenv("VOLC_SECRETKEY"))

    with open("", "r") as file:
        controlImage = file.read().encode()

    req = {
        "prompt":          "(sfw:1.0),(masterpiece,best quality,ultra highres),(realistic:1.15),(3D:1.0),8k wallpaper,ultra detailed,beautiful and aesthetic,official art,real,(tech city background:1.3),(depth of field:1.1),(colorful:1),wind,(sky:1.25),chinese (high quality:1.3) ((golden:1.3) dragon:1.3),glowing,(1girl:1.1),portrait,(bright face:1.2),bangs,light smile,hair,(look at viewer1.2),(young:1.0),(big eyes:1),solo,Brilliant,face to viewer,(future architecture:1.1),(milk print hanfu:1.2),(liquid:1.1),(bubble:1.2),pvc texture,(building:1.2),(detailed skin:1.2),(science fiction:1.3),(machinery:1.2),anmuxi,(iridescent film coat:1.3),(iridescent (blue:0.15) film hanfu:1.30),(red lantern:1.3),",
        "negative_prompt": "(embedding:EasyNegative:0.9),(embedding:badhandv4:1.3),terrible,injured,(nsfw:1.0),(nude:1.0),naked,small eyes,Sleepy,big small eyes,(breasts:1.0),lowres,text,log,signature,symbol-shaped pupils,heterochromia,multicolored eyes,no pupils,slit pupils,asymmetrical pupils,asymmetrical eyes,asymmetrical eyebrows,streaked hair,colored inner hair,two-tone hair,multicolored hair,gradient hair,earrings,hair ornaments,asymmetrical breasts,multiple views,reference sheet,simple background,room,indoors,japan,blue arm,(old:1.2),sad,asian face,blue skin,monster,bone,europa,american,(facial tattoo:1),tattoo,(hat:1.1),blue face,blue skin,white lantern,western dargon,Cross-eyed,curls hai,flower on head,skin blemish,tongue out,(sky:1.1),(yellow skin:1.3),white lantern,centre parting,fog,(facepaint:1.2),",
        "control_image":   "",
        "parameters": {
            "seed":                 38,
            "strength":             0.75,
            "num_inference_steps":  20,
        },
    }

    endpoint_id = "{YOUR_ENDPOINT_ID}"
    test_images_quick_gen(maas, endpoint_id, req)
