# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    bind_axb_for_axne_form = {
        "NumberPoolNo": "NP167091951102821491",
        "ParentSubId": "S16729859759534216e440",
        "PhoneNoB": "13500000001",
        "EnableDuration": 360, 
    }
    print(vms_service.bind_axb_for_axne(bind_axb_for_axne_form))
