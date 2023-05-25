# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    update_axn_form = {
        "NumberPoolNo": "NP162981168404095092",
        "SubId": "S16329006138991e7e1003",
        "UpdateType": "updatePhoneNoB",
        "PhoneNoB": "13700000004",
    }
    print(vms_service.update_axn(update_axn_form))
