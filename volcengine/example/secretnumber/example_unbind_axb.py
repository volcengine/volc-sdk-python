# coding:utf-8
from volcengine.secretnumber.SecretNumberService import SecretNumberService

if __name__ == '__main__':
    secretNumberService = SecretNumberService()

    secretNumberService.set_ak("")
    secretNumberService.set_sk("")

    unbind_axb_form = {
        "NumberPoolNo": "NP161156328504091435",
        "SubId": "S16328999093159b70bc71",
    }
    print(secretNumberService.unbind_axb(unbind_axb_form))
