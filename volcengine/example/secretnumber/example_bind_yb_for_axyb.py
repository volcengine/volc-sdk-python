# coding:utf-8
from volcengine.secretnumber.SecretNumberService import SecretNumberService

if __name__ == '__main__':
    secretNumberService = SecretNumberService()

    secretNumberService.set_ak("")
    secretNumberService.set_sk("")

    bind_yb_for_axyb_form = {
        "NumberPoolNo": "NP166191438910906190",
        "ParentSubId": "S16722126795817211a93e",
        "PhoneNoB": "13500000001",
        "EnableDuration": 360, 
    }
    print(secretNumberService.bind_yb_for_axyb(bind_yb_for_axyb_form))
