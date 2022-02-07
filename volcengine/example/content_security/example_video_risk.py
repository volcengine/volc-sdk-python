# coding=utf-8
from volcengine.content_security.ContentSecurityService import ContentSecurityService

if __name__ == '__main__':
    riskDetector = ContentSecurityService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    riskDetector.set_ak('AK')
    riskDetector.set_sk('SK')

    params = dict()
    req = {
         'AppId': 3332,
         'Service': "video_risk",
         'Parameters': "{\"operate_time\": 1617960951, \"ip\": \"127.0.0.9\", \"did\":1357924680, \"url\": \"\", \"data_id\": \"123\", \"account_id\": \"2000000409\"}"
    }

    resp = riskDetector.async_video_risk(params, req)
    print resp

    params = {
        'AppId': 3332,
        'Service': "video_risk",
        'DataId': "test123321"
    }
    req = dict()

    resp1 = riskDetector.video_result(params, req)
    print resp1

    params = dict()
    req = {
        'AppId': 3332,
        'Service': "image_content_risk",
        'Parameters': "{\"operate_time\": 1642130700, \"url\": \"\", \"data_id\": \"test12345\", \"account_id\": \"2000001223\"}"
    }

    resp2 = riskDetector.image_content_risk(params, req)
    print resp2

    reqImage = {
        'AppId': 3332,
        'Service': "image_content_risk",
        'Parameters': "{\"operate_time\": 1617960951, \"ip\": \"127.0.0.9\", \"did\":1357924680, \"url\": \"\", \"data_id\": \"image123\", \"account_id\": \"2000000409\"}"
    }

    resp3 = riskDetector.async_image_risk(params, reqImage)
    print resp3

    params = {
        'AppId': 3332,
        'Service': "image_content_risk",
        'DataId': "123image"
    }
    req = dict()

    resp4 = riskDetector.image_result(params, req)
    print resp4

    params = dict()
    reqText = {
        'AppId': 5461,
        'Service': "text_risk",
        'Parameters': "{\"operate_time\": 1617960951, \"text\": \"加我微信看一些小黄片\", \"account_id\": \"2000000409\"}"
    }

    resp5 = riskDetector.text_risk(params, reqText)
    print resp5

    params = dict()
    reqCreateCustomContentsReq = {
        'app_id': 5461,
        'name': "test_7",
        'decision': "PASS",
        'description': "test"
    }

    resp = riskDetector.create_custom_contents(params, reqCreateCustomContentsReq)
    print resp

    params = dict()
    reqUploadCustomContentsReq = {
        'app_id': 5461,
        'name': "test_7",
        'modify_type': 1,
        'contents': ["1", "2", "3", "5"],
    }

    resp = riskDetector.upload_custom_contents(params, reqUploadCustomContentsReq)
    print resp
