# coding:utf-8
from volcengine.secretnumber.SecretNumberService import SecretNumberService

if __name__ == '__main__':
    secretNumberService = SecretNumberService()

    secretNumberService.set_ak("")
    secretNumberService.set_sk("")

    bind_axb_form = {
        "NumberPoolNo": "NP161156328504091435",
        "PhoneNoA": "13700000001",
        "PhoneNoB": "13700000002",
        "PhoneNoX": "13700000003",
        "ExpireTime": "1632920195",
        "UserData": "this is my user data",
    }
    print(secretNumberService.bind_axb(bind_axb_form))
