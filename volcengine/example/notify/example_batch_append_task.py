# coding:utf-8

from volcengine.notify.notify import NotifyService

if __name__ == '__main__':
    notify_service = NotifyService()

    notify_service.set_ak("your ak")
    notify_service.set_sk("your sk")

    batch_append_task = {
        "TaskOpenId": "106d2984fbf0480480cbc8b98d609592",
        "PhoneList": [
            {
                "Phone": "your phone",
            }
        ],
    }

    print(notify_service.batch_append_task(batch_append_task))
