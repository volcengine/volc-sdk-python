from volcengine.livesaas.LivesaasService import LivesaasService

if __name__ == '__main__':
    livesaasService = LivesaasService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    livesaasService.set_ak('AK')
    livesaasService.set_sk('SK')

    params = {
        "ActivityId": 1,
        "IsNeedTotalCount": "True",
        "PageNo": 1,
        "PageItemCount": 10,
        "Name": "",
        "Vid": ""
    }

    resp = livesaasService.list_medias_api(params)
    # resp = await livesaasService.async_list_medias_api(params)
    print(resp)
