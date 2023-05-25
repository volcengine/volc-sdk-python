# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    unbind_axne_form = {
        "NumberPoolNo": "NP167091934402820309",
        "SubId": "S16729852979534c6e4719",
    }
    print(vms_service.unbind_axne(unbind_axne_form))
