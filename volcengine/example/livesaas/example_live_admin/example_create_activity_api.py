from volcengine.livesaas.LivesaasService import LivesaasService

if __name__ == '__main__':
    livesaasService = LivesaasService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    livesaasService.set_ak('AK')
    livesaasService.set_sk('SK')

    body = {
        'Name': "test",
        'LiveTime': 1628067360,
        'CoverImage': "",
        'IsReplayAutoOnlineEnable': 1,
        'IsWatermark': 0,
        'ProtectModeCode': "",
        'ViewUrlPath': "",
        'TemplateId': 0
    }

    resp = livesaasService.create_activity_api(body)
    # resp = await livesaasService.async_create_activity_api(body)
    print(resp)
