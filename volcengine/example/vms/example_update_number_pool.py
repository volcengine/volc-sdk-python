# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    form = {
        "Name": "testsipv2",
        "ServiceType": 100,
        "SubServiceType": 101,
        "NumberPoolNo": "todo"
    }
    print(vms_service.update_number_pool(form))
