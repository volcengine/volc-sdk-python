# coding:utf-8
from volcengine.secretnumber.SecretNumberService import SecretNumberService

if __name__ == '__main__':
    secretNumberService = SecretNumberService()

    secretNumberService.set_ak("")
    secretNumberService.set_sk("")

    query_subscription_form = {
        "NumberPoolNo": "NP161156328504091435",
        "SubId": "S16329001153159fa121d9",
    }
    print(secretNumberService.query_subscription(query_subscription_form))
