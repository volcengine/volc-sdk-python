# coding:utf-8
from volcengine.secretnumber.SecretNumberService import SecretNumberService

if __name__ == '__main__':
    secretNumberService = SecretNumberService()

    secretNumberService.set_ak("")
    secretNumberService.set_sk("")

    unbind_axne_form = {
        "NumberPoolNo": "NP167091934402820309",
        "SubId": "S16729852979534c6e4719",
    }
    print(secretNumberService.unbind_axne(unbind_axne_form))
