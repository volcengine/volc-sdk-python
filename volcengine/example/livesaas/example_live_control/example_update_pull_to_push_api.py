from volcengine.livesaas.LivesaasService import LivesaasService

if __name__ == '__main__':
    livesaasService = LivesaasService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    livesaasService.set_ak('AK')
    livesaasService.set_sk('SK')

    body = {
        'ActivityId': 1,
        'LineId': 0,
        'PullStreamUrl': "",
        'PullStreamStatus': 1,
        'PullStreamMode': 0,
        'PullStreamLineId': 0,
        'PullStreamMainBackupMode': 0
    }

    resp = livesaasService.update_pull_to_push_api(body)
    # resp = await livesaasService.async_update_pull_to_push_api(body)
    print(resp)
