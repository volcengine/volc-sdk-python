# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    form = {
        "Name": "testsipv1",
        "ServiceType": 100,
        "SubServiceType": 101
    }
    print(vms_service.create_number_pool(form))
