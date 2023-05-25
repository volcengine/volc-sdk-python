# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    query_subscription_form = {
        "NumberPoolNo": "NP161156328504091435",
        "SubId": "S16329001153159fa121d9",
    }
    print(vms_service.query_subscription(query_subscription_form))
