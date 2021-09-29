# coding:utf-8
from volcengine.secretnumber.SecretNumberService import SecretNumberService

if __name__ == '__main__':
    secretNumberService = SecretNumberService()

    secretNumberService.set_ak("")
    secretNumberService.set_sk("")

    update_axb_form = {
        "NumberPoolNo": "NP161156328504091435",
        "SubId": "S1632900399315954ffbfd",
        "UpdateType": "updateExpireTime",
        "ExpireTime": "1632923795",
    }
    print(secretNumberService.update_axb(update_axb_form))
