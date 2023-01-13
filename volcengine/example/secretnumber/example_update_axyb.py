# coding:utf-8
from volcengine.secretnumber.SecretNumberService import SecretNumberService

if __name__ == '__main__':
    secretNumberService = SecretNumberService()

    secretNumberService.set_ak("")
    secretNumberService.set_sk("")

    update_axyb_form = {
        "NumberPoolNo": "NP167091934402820309",
        "SubId": "S1672985491953460b641f",
        "UpdateType": "UpdatePhoneNoA",
        "PhoneNoA": "18900000001",
    }
    print(secretNumberService.update_axyb(update_axyb_form))
