# coding:utf-8
from volcengine.vms.risk import RiskService

if __name__ == '__main__':
    riskService = RiskService()

    RiskService.set_ak("")
    RiskService.set_sk("")

    query_call_call_form = {
        "CustomerNumberList": "188xxxx1647",
        "BusinessLineId": "200000001",
        "CallType": 1,
    }
    print(RiskService.query_call_call(query_call_call_form))
