# coding:utf-8

from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    params = {
       "ResourceKey": "1ca08a45a937411ebd78e572cef87086",
       "Name": "123.mp3"
    }

    print(vms_service.open_update_resource(params))
