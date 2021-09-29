# coding:utf-8
from volcengine.secretnumber.SecretNumberService import SecretNumberService

if __name__ == '__main__':
    secretNumberService = SecretNumberService()

    secretNumberService.set_ak("")
    secretNumberService.set_sk("")

    update_axn_form = {
        "NumberPoolNo": "NP162981168404095092",
        "SubId": "S16329006138991e7e1003",
        "UpdateType": "updatePhoneNoB",
        "PhoneNoB": "13700000004",
    }
    print(secretNumberService.update_axn(update_axn_form))
