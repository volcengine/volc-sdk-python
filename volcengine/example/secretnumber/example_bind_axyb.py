# coding:utf-8
from volcengine.secretnumber.SecretNumberService import SecretNumberService

if __name__ == '__main__':
    secretNumberService = SecretNumberService()

    secretNumberService.set_ak("")
    secretNumberService.set_sk("")

    bind_axyb_form = {
        "NumberPoolNo": "NP166375725010908111",
        "PhoneNoA": "13700000017",
        "CityCode": "010",
        "UserData": "this is my user data",
        "ExpireTime": "1673071556",
        "YbEnableDuration": 600,
        "NumberPoolNoY": "NP166265127202826653"
    }
    print(secretNumberService.bind_axyb(bind_axyb_form))
