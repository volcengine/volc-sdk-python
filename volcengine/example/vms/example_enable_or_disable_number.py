# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    form = {
        "NumberList": "xxx",
        "EnableCode": 2
    }
    print(vms_service.enable_or_disable_number(form))
