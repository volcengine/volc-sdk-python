# coding:utf-8

from volcengine.notify.notify import NotifyService

if __name__ == '__main__':
    notify_service = NotifyService()

    notify_service.set_ak("your ak")
    notify_service.set_sk("your sk")

    params = {
       "Type": 0,
    }

    print(notify_service.query_usable_resource(params))
