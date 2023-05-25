# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    upgrade_ax_to_axb_form = {
        "NumberPoolNo": "NP161156328504091435",
        "SubId": "S163290034831599ce523b",
        "PhoneNoB": "13700000002",
        "UserData": "this is my user data",
    }
    print(vms_service.upgrade_ax_to_axb(upgrade_ax_to_axb_form))
