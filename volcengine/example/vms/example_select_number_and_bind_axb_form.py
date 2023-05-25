# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    select_number_and_bind_axb_form = {
        "NumberPoolNo": "NP161156328504091435",
        "PhoneNoA": "13700000001",
        "PhoneNoB": "13700000002",
        "ExpireTime": "1632920195",
    }
    print(vms_service.select_number_and_bind_axb(select_number_and_bind_axb_form))
