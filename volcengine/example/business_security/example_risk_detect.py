
from volcengine.business_security.RiskDetectionService import RiskDetectService

if __name__ == '__main__':
    riskDetector = RiskDetectService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    riskDetector.set_ak('***REMOVED***')
    riskDetector.set_sk('***REMOVED***')

    # params = dict()
    # req = {
    #      'AppId': 1,
    #      'Service': "chat",
    #      'Parameters': '{"uid":123411, "operate_time":1609818934, "chat_text":"a"}'
    # }
    #
    # resp = riskDetector.risk_detect(params, req)
    # print(resp)
    #
    # params = dict()
    # req = {
    #     'AppId': 1,
    #     'Service': "chat",
    #     'Parameters': '{"uid":123411, "operate_time":1609818934, "chat_text":"a"}'
    # }
    #
    # asyncResp = riskDetector.async_risk_detect(params, req)
    # print(asyncResp)
    #
    # params = {
    #     'AppId': 1,
    #     'Service': "register",
    #     'StartTime': 1615535000,
    #     'EndTime': 1615540603,
    #     'PageSize': 10,
    #     'PageNum': 1,
    # }
    #
    # req = dict()
    #
    # resultResp = riskDetector.risk_result(params, req)

    params = dict()
    req = {
         'AppId': 222572,
         'Service': "account_risk",
         'Parameters': '{"operate_time":1609818934, "mobile": "15959215326"}'
    }

    resp = riskDetector.risk_detect(params, req)

    print resp
    # params = dict()
    # req = {
    #     'AppId': 5461,
    #     'Service': "mobile_status",
    #     'Parameters': '{"operate_time":1609818934, "mobile": ""}'
    # }
    #
    # mobileResp = riskDetector.mobile_status(params, req)

    # print(mobileResp)