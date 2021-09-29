# coding:utf-8
from volcengine.secretnumber.SecretNumberService import SecretNumberService

if __name__ == '__main__':
    secretNumberService = SecretNumberService()

    secretNumberService.set_ak("")
    secretNumberService.set_sk("")

    query_subscription_for_list_form = {
        "NumberPoolNo": "NP161156328504091435",
        "PhoneNoX": "13700000003",
        "Status": 1,
        "Offset": 0,
        "Limit": 20,
    }
    print(secretNumberService.query_subscription_for_list(query_subscription_for_list_form))
