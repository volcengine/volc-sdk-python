# coding:utf-8

from volcengine.notify.notify import NotifyService

if __name__ == '__main__':
    notify_service = NotifyService()

    notify_service.set_ak("your ak")
    notify_service.set_sk("your sk")

    body = {
       "Type": 0,
       "Keyword":"0f299353da3343e58373132b9e3b75d4"
    }

    print(notify_service.query_open_get_resource(body))
