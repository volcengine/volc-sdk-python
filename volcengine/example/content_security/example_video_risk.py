
from volcengine.content_security.ContentSecurityService import ContentSecurityService

if __name__ == '__main__':
    riskDetector = ContentSecurityService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    riskDetector.set_ak('***REMOVED***')
    riskDetector.set_sk('***REMOVED***')

    params = dict()
    req = {
         'AppId': 3332,
         'Service': "video_risk",
         'Parameters': "{\"operate_time\": 1617960951, \"ip\": \"127.0.0.9\", \"did\":1357924680, \"url\": \"http://fc-video-store.vivo.com.cn/fc-author-video-store/V050000000000V_0IkeMgwD.mp4\", \"data_id\": \"123\", \"account_id\": \"2000000409\"}"
    }

    resp = riskDetector.video_risk(params, req)
    print resp

    params = {
        'AppId': 3332,
        'Service': "video_risk",
        'DataId': "123"
    }
    req = dict()

    resp1 = riskDetector.video_result(params, req)
    print resp1
