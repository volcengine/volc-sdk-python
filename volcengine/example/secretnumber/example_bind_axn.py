# coding:utf-8
from volcengine.secretnumber.SecretNumberService import SecretNumberService

if __name__ == '__main__':
    secretNumberService = SecretNumberService()

    secretNumberService.set_ak("")
    secretNumberService.set_sk("")

    bind_axn_form = {
        "NumberPoolNo": "NP162981168404095092",
        "PhoneNoA": "13700000001",
        "PhoneNoB": "13700000002",
        "PhoneNoX": "13700000005",
        "ExpireTime": "1632920195",
        "UserData": "this is my user data",
    }
    print(secretNumberService.bind_axn(bind_axn_form))
