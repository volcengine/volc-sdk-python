# coding:utf-8

from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    delete_resource_param = {
       "ResourceKey": "4bb4b9b137264148998de1c227e9f652",
    }

    print(vms_service.delete_resource(delete_resource_param))
