# coding:utf-8

from volcengine.notify.notify import NotifyService

if __name__ == '__main__':
    notify_service = NotifyService()

    notify_service.set_ak("your ak")
    notify_service.set_sk("your sk")

    update_task_body = {
        "TaskOpenId": "106d2984fbf0480480cbc8b98d609592",
        "Concurrency": 3,
        "StartTime": "2022-03-02 00:00:00",
        "EndTime": "2022-03-13 01:30:00",
        "Recall": 1
    }

    print(notify_service.update_task(update_task_body))
