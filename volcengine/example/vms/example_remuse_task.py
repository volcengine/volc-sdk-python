# coding:utf-8

from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    pause_task_param = {
       "TaskOpenId": "ecb1be9b71974916a529b936702783cb",
    }

    print(vms_service.resume_task(pause_task_param))
