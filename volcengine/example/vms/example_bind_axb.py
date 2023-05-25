# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    bind_axb_form = {
        "NumberPoolNo": "NP161156328504091435",
        "PhoneNoA": "13700000001",
        "PhoneNoB": "13700000002",
        "PhoneNoX": "13700000003",
        "ExpireTime": "1632920195",
        "UserData": "this is my user data",
    }
    print(vms_service.bind_axb(bind_axb_form))
