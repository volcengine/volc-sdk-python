# coding:utf-8
from volcengine.secretnumber.SecretNumberService import SecretNumberService

if __name__ == '__main__':
    secretNumberService = SecretNumberService()

    secretNumberService.set_ak("")
    secretNumberService.set_sk("")

    select_number_and_bind_axb_form = {
        "NumberPoolNo": "NP161156328504091435",
        "PhoneNoA": "13700000001",
        "PhoneNoB": "13700000002",
        "ExpireTime": "1632920195",
    }
    print(secretNumberService.select_number_and_bind_axb(select_number_and_bind_axb_form))
