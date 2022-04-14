
from volcengine.business_security.RiskDetectionService import RiskDetectService

if __name__ == '__main__':
    riskDetector = RiskDetectService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    riskDetector.set_ak('AK')
    riskDetector.set_sk('SK')

    params = dict()
    req = {
         'AppId': 222572,
         'Service': "account_risk",
         'Parameters': '{"operate_time":1609818934, "mobile": "12312341234"}'
    }

    resp = riskDetector.risk_detect(params, req)

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

    params = dict()
    req = {
         'AppId': 5461,
         'Service': "account_risk",
         'Parameters': '{"operate_time":1609818934, "mobile_sha1": "d6e94212f0655d2ce19d047169365a67a1db85bf"}'
    }

    resp = riskDetector.account_risk(params, req)

    params = dict()
    req = {
        'AppId': 5461,
        'Service': "mobile_status",
        'Parameters': '{"operate_time":1609818934, "mobile": ""}'
    }

    mobileResp = riskDetector.mobile_status(params, req)

    print(mobileResp)

    params = dict()
    req = {
        'AppId': 5461,
        'Service': "idcard_two_element_verify",
        'Parameters': '{"operate_time":1609818934, "idcard_no": "", "idcard_name":""}'
    }

    idcardTwoElementResp = riskDetector.element_verify(params, req)

    print(idcardTwoElementResp)

    params = dict()
    req = {
        'AppId': 5461,
        'Service': "mobile_address",
        'Parameters': '{"operate_time":1609818934, "mobile": ""}'
    }

    mobileStatusV2Resp = riskDetector.mobile_status_v2(params, req)

    print(mobileStatusV2Resp)

    params = dict()
    req = {
        'AppId': 5461,
        'Service': "mobile_two_element_verify",
        'Parameters': '{"operate_time":1609818934, "mobile": "", "idcard_name": ""}'
    }

    elementV2resp = riskDetector.element_verify_v2(params, req)

    print(elementV2resp)