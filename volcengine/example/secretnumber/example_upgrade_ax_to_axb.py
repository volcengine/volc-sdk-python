# coding:utf-8
from volcengine.secretnumber.SecretNumberService import SecretNumberService

if __name__ == '__main__':
    secretNumberService = SecretNumberService()

    secretNumberService.set_ak("")
    secretNumberService.set_sk("")

    upgrade_ax_to_axb_form = {
        "NumberPoolNo": "NP161156328504091435",
        "SubId": "S163290034831599ce523b",
        "PhoneNoB": "13700000002",
        "UserData": "this is my user data",
    }
    print(secretNumberService.upgrade_ax_to_axb(upgrade_ax_to_axb_form))
