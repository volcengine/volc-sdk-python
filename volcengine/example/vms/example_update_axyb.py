# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    update_axyb_form = {
        "NumberPoolNo": "NP167091934402820309",
        "SubId": "S1672985491953460b641f",
        "UpdateType": "UpdatePhoneNoA",
        "PhoneNoA": "18900000001",
    }
    print(vms_service.update_axyb(update_axyb_form))
