# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    unbind_axn_form = {
        "NumberPoolNo": "NP162981168404095092",
        "SubId": "S16329006138991e7e1003",
    }
    print(vms_service.unbind_axn(unbind_axn_form))
