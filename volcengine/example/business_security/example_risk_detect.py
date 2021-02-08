
from volcengine.business_security.RiskDetectionService import RiskDetectService

if __name__ == '__main__':
    riskDetector = RiskDetectService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    riskDetector.set_ak('ak')
    riskDetector.set_sk('sk')

    params = dict()
    req = {
         'app_id': 3332,
         'service': "chat",
         'parameters': '{"uid":123411, "operate_time":1609818934, "chat_text":"a"}'
    }

    resp = riskDetector.risk_detect(params, req)
    print(resp)
