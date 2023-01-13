# coding:utf-8
from volcengine.secretnumber.SecretNumberService import SecretNumberService

if __name__ == '__main__':
    secretNumberService = SecretNumberService()

    secretNumberService.set_ak("")
    secretNumberService.set_sk("")

    unbind_axyb_form = {
        "NumberPoolNo": "NP166375725010908111",
        "SubId": "S16729852979534c6e4719",
    }
    print(secretNumberService.unbind_axyb(unbind_axyb_form))
