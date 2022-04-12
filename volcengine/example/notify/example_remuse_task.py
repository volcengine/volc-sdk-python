# coding:utf-8

from volcengine.notify.notify import NotifyService

if __name__ == '__main__':
    notify_service = NotifyService()

    notify_service.set_ak("your ak")
    notify_service.set_sk("your sk")

    pause_task_param = {
       "TaskOpenId": "ecb1be9b71974916a529b936702783cb",
    }

    print(notify_service.resume_task(pause_task_param))
