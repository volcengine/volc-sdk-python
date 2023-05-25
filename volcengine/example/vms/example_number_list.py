# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    form = {
        "NumberPoolNo": "xxx",
        "NumberPoolTypeCode": 101,
        "Limit": 5,
        "Offset": 0
    }
    print(vms_service.number_list(form))
