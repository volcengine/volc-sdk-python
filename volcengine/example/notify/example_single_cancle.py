# coding:utf-8

from volcengine.notify.notify import NotifyService

if __name__ == '__main__':
    notify_service = NotifyService()

    notify_service.set_ak("your ak")
    notify_service.set_sk("your sk")

    params = {
        "SingleOpenId": "9b39e17fb12444c78f20d6551469a6e0"
    }

    print(notify_service.single_cancel(params))