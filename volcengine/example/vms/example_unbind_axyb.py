# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    unbind_axyb_form = {
        "NumberPoolNo": "NP166375725010908111",
        "SubId": "S16729852979534c6e4719",
    }
    print(vms_service.unbind_axyb(unbind_axyb_form))
