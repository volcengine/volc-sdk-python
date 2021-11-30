
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

    resp = riskDetector.async_video_risk(params, req)
    print resp

    params = {
        'AppId': 3332,
        'Service': "video_risk",
        'DataId': "123"
    }
    req = dict()

    resp1 = riskDetector.video_result(params, req)
    print resp1

    params = dict()
    req = {
        'AppId': 3332,
        'Service': "image_content_risk",
        'Parameters': "{\"operate_time\": 1617960951, \"ip\": \"127.0.0.9\", \"did\":1357924680, \"url\": \"https://image.uc.cn/s/wemedia/s/upload/2021/Wfmt7d1f82edu22/c2ea0890c3045dad785944b01dd87540.png\", \"data_id\": \"123\", \"account_id\": \"2000000409\"}"
    }

    resp2 = riskDetector.image_content_risk(params, req)

    reqImage = {
        'AppId': 3332,
        'Service': "image_content_risk",
        'Parameters': "{\"operate_time\": 1617960951, \"ip\": \"127.0.0.9\", \"did\":1357924680, \"url\": \"https://image.uc.cn/s/wemedia/s/upload/2021/Wfmt7d1f82edu22/c2ea0890c3045dad785944b01dd87540.png\", \"data_id\": \"image123\", \"account_id\": \"2000000409\"}"
    }

    resp3 = riskDetector.async_image_risk(params, req)
    print resp3

    params = {
        'AppId': 3332,
        'Service': "image_content_risk",
        'DataId': "image123"
    }
    req = dict()

    resp4 = riskDetector.video_result(params, req)
    print resp4

