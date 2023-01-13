# coding:utf-8

from volcengine.notify.notify import NotifyService

if __name__ == '__main__':
    notify_service = NotifyService()

    notify_service.set_ak("your ak")
    notify_service.set_sk("your sk")

    params = {
       "ResourceKey": "1ca08a45a937411ebd78e572cef87086",
       "Name": "123.mp3"
    }

    print(notify_service.open_update_resource(params))
