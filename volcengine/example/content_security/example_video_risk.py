# coding=utf-8
from volcengine.content_security.ContentSecurityService import ContentSecurityService

if __name__ == '__main__':
    riskDetector = ContentSecurityService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    riskDetector.set_ak('')
    riskDetector.set_sk('')

    params = dict()
    req = {
         'AppId': 0,
         'Service': "",
         'Parameters': '{}'
    }

    resp = riskDetector.async_video_risk(params, req)