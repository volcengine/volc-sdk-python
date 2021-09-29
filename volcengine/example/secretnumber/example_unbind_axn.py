# coding:utf-8
from volcengine.secretnumber.SecretNumberService import SecretNumberService

if __name__ == '__main__':
    secretNumberService = SecretNumberService()

    secretNumberService.set_ak("")
    secretNumberService.set_sk("")

    unbind_axn_form = {
        "NumberPoolNo": "NP162981168404095092",
        "SubId": "S16329006138991e7e1003",
    }
    print(secretNumberService.unbind_axn(unbind_axn_form))
