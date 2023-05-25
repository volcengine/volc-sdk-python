# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    query_subscription_for_list_form = {
        "NumberPoolNo": "NP161156328504091435",
        "PhoneNoX": "13700000003",
        "Status": 1,
        "Offset": 0,
        "Limit": 20,
    }
    print(vms_service.query_subscription_for_list(query_subscription_for_list_form))
