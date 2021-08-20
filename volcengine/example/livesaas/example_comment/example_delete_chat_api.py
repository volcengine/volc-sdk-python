from volcengine.livesaas.LivesaasService import LivesaasService

if __name__ == '__main__':
    livesaasService = LivesaasService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    livesaasService.set_ak('AK')
    livesaasService.set_sk('SK')

    body = {
        "ActivityId": 1,
        "ChatId": 1
    }

    resp = livesaasService.delete_chat_api(body)
    # resp = await livesaasService.async_delete_chat_api(body)
    print(resp)
