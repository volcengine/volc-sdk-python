from volcengine.livesaas.LivesaasService import LivesaasService

if __name__ == '__main__':
    livesaasService = LivesaasService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    livesaasService.set_ak('AK')
    livesaasService.set_sk('SK')

    body = {
        "ActivityId": 1,
        "LineId": 1,
        "LoopNumber": 1,
        "IsShowProgram": 0,
        "LoopVideo": [{
            "VideoCoverImage": "",
            "VideoName": "test.mp4",
            "VideoVid": "",
            "Index": 1
        }]
    }

    resp = livesaasService.update_loop_video_api(body)
    # resp = await livesaasService.async_update_loop_video_api(body)
    print(resp)
