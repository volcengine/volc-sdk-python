# coding:utf-8

from volcengine.notify.notify import NotifyService

if __name__ == '__main__':
    notify_service = NotifyService()

    notify_service.set_ak("your ak")
    notify_service.set_sk("your sk")

    body = {
       "FileName": "ecb1be9b71974916a529b936702783cb.mp3",
    }

    print(notify_service.commit_resource_upload(body))
