# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    update_axb_form = {
        "NumberPoolNo": "NP161156328504091435",
        "SubId": "S1632900399315954ffbfd",
        "UpdateType": "updateExpireTime",
        "ExpireTime": "1632923795",
    }
    print(vms_service.update_axb(update_axb_form))
