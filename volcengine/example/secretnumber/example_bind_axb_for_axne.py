# coding:utf-8
from volcengine.secretnumber.SecretNumberService import SecretNumberService

if __name__ == '__main__':
    secretNumberService = SecretNumberService()

    secretNumberService.set_ak("")
    secretNumberService.set_sk("")

    bind_axb_for_axne_form = {
        "NumberPoolNo": "NP167091951102821491",
        "ParentSubId": "S16729859759534216e440",
        "PhoneNoB": "13500000001",
        "EnableDuration": 360, 
    }
    print(secretNumberService.bind_axb_for_axne(bind_axb_for_axne_form))
