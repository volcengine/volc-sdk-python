# coding:utf-8
from volcengine.secretnumber.SecretNumberService import SecretNumberService

if __name__ == '__main__':
    secretNumberService = SecretNumberService()

    secretNumberService.set_ak("")
    secretNumberService.set_sk("")

    select_number_and_bind_axn_form = {
        "NumberPoolNo": "NP167092127702825445",
        "PhoneNoA": "13700000001",
        "PhoneNoB": "13700000002",
        "UserData": "this is my user data",
        "CityCode": "010",
        "ExpireTime":"1673071556",
    }
    print(secretNumberService.select_number_and_bind_axn(select_number_and_bind_axn_form))
