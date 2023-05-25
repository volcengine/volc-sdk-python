# coding:utf-8

from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    create_task_body = {
        "Name": "你好",
        "Resource": "9b39e17fb12444c78f20d6551469a6f0",
        "Type": 0,
        "NumberPoolNo": "NP162213338604093530",
        "Concurrency": 2,
        "PhoneList": [
            {
                "Phone": "your phone",
            }
        ],
        "StartTime": "2022-03-01 00:00:00",
        "EndTime": "2022-03-12 01:30:00",
        "SelectNumberRule": 5,
    }

    print(vms_service.create_task(create_task_body))
