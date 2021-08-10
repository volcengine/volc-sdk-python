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
            "VideoCoverImage": "tos-cn-v-c1801c/1d8aa8be39484140a7affbce0daa8929",
            "VideoName": "download (3).mp4",
            "VideoVid": "v02a49g10000c45l963c77ubrcg01ffg",
            "Index": 1
        }]
    }

    resp = livesaasService.update_loop_video_api(body)
    print(resp)
