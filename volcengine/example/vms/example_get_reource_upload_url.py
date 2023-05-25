# coding:utf-8

from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    body = {
       "FileName": "ecb1be9b71974916a529b936702783cb.mp3",
    }

    print(vms_service.get_resource_upload_url(body))
