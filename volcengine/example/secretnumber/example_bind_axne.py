# coding:utf-8
from volcengine.secretnumber.SecretNumberService import SecretNumberService

if __name__ == '__main__':
    secretNumberService = SecretNumberService()

    secretNumberService.set_ak("")
    secretNumberService.set_sk("")

    bind_axne_form = {
        "NumberPoolNo": "NP167091934402820309",
        "PhoneNoA": "13700000017",
        "PhoneNoB": "13700000018",
        "UserData": "this is my user data",
        "CityCode": "010",
        "ExpireTime":"1673071556",
    }
    print(secretNumberService.bind_axne(bind_axne_form))
