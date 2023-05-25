# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    bind_yb_for_axyb_form = {
        "NumberPoolNo": "NP166191438910906190",
        "ParentSubId": "S16722126795817211a93e",
        "PhoneNoB": "13500000001",
        "EnableDuration": 360, 
    }
    print(vms_service.bind_yb_for_axyb(bind_yb_for_axyb_form))
