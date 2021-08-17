from volcengine.livesaas.LivesaasService import LivesaasService

if __name__ == '__main__':
    livesaasService = LivesaasService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    livesaasService.set_ak('AK')
    livesaasService.set_sk('SK')

    body = {
        "ActivityId": 1,
        "Mode": 1,
        "Nickname": "", #当Mode为2时为必传
        "UserIdStr": "", #当Mode为2时为必传
    }

    resp = livesaasService.get_sdk_token_api(body)
    # resp = await livesaasService.async_get_sdk_token_api(body)
    print(resp)
