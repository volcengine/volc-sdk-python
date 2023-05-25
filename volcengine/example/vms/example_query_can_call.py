# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    query_call_call_form = {
        "CustomerNumberList": "188xxxx1647",
        "BusinessLineId": "200000001",
        "CallType": 1,
    }
    print(vms_service.query_call_call(query_call_call_form))
