# coding:utf-8

from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    batch_append_task = {
        "TaskOpenId": "106d2984fbf0480480cbc8b98d609592",
        "PhoneList": [
            {
                "Phone": "your phone",
            }
        ],
    }

    print(vms_service.batch_append_task(batch_append_task))
