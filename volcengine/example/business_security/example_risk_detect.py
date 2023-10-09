
from volcengine.business_security.RiskDetectionService import RiskDetectService

if __name__ == '__main__':
    riskDetector = RiskDetectService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    riskDetector.set_ak('AK')
    riskDetector.set_sk('SK')

    params = dict()
    req = {
         'AppId': 0,
         'Service': "",
         'Parameters': '{}'
    }

    resp = riskDetector.risk_detect(params, req)
