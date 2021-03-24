
from volcengine.business_security.RiskDetectionService import RiskDetectService

if __name__ == '__main__':
    riskDetector = RiskDetectService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    riskDetector.set_ak('ak')
    riskDetector.set_sk('sk')

    params = dict()
    req = {
         'AppId': 1,
         'Service': "chat",
         'Parameters': '{"uid":123411, "operate_time":1609818934, "chat_text":"a"}'
    }

    resp = riskDetector.risk_detect(params, req)
    print(resp)

    params = dict()
    req = {
        'AppId': 1,
        'Service': "chat",
        'Parameters': '{"uid":123411, "operate_time":1609818934, "chat_text":"a"}'
    }

    asyncResp = riskDetector.async_risk_detect(params, req)
    print(asyncResp)

    params = {
        'AppId': 1,
        'Service': "register",
        'StartTime': 1615535000,
        'EndTime': 1615540603,
        'PageSize': 10,
        'PageNum': 1,
    }

    req = dict()

    resultResp = riskDetector.risk_result(params, req)
    print(resultResp)
