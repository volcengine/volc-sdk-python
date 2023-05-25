# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    bind_axn_form = {
        "NumberPoolNo": "NP162981168404095092",
        "PhoneNoA": "13700000001",
        "PhoneNoB": "13700000002",
        "PhoneNoX": "13700000005",
        "ExpireTime": "1632920195",
        "UserData": "this is my user data",
    }
    print(vms_service.bind_axn(bind_axn_form))
