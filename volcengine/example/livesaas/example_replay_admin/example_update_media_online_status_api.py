from volcengine.livesaas.LivesaasService import LivesaasService

if __name__ == '__main__':
    livesaasService = LivesaasService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    livesaasService.set_ak('AK')
    livesaasService.set_sk('SK')

    body = {
        "ActivityId": 1,
        "MediaId": 1,
        "OnlineStatus": 2
    }

    resp = livesaasService.update_media_online_status_api(body)
    # resp = await livesaasService.async_update_media_online_status_api(body)
    print(resp)
