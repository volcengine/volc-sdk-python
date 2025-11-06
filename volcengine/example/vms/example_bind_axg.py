# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()
    vms_service.set_ak("ak")
    vms_service.set_sk("sk")

    bind_axg_json = {
        "NumberPoolNo": "NP162981168404095092",
        "PhoneNoA": "13700000001",
        "PhoneNoB": "13700000002",
        "PhoneNoX": "13700000005",
        "ExpireTime": "1632920195",
    }
    print(vms_service.bind_axg(bind_axg_json))
