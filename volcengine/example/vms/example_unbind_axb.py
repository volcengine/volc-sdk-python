# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    unbind_axb_form = {
        "NumberPoolNo": "NP161156328504091435",
        "SubId": "S16328999093159b70bc71",
    }
    print(vms_service.unbind_axb(unbind_axb_form))
