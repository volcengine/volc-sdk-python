# coding:utf-8

from volcengine.notify.notify import NotifyService

if __name__ == '__main__':
    notify_service = NotifyService()

    notify_service.set_ak("your ak")
    notify_service.set_sk("your sk")

    single_append_body = {
        "List": [
            {
                "Phone": "your phone",
                "Resource": "9b39e17fb12444c78f20d6551469a6f0",
                "NumberPoolNo": "NP162213338604093530",
                "NumberType": 0,
                "TriggerTime": "2022-03-12 19:18:00",
                "Type": 0,
                "SingleOpenId": "9b39e17fb12444c78f20d6551469a6e0"
            }
        ],
    }
    print(notify_service.single_batch_append(single_append_body))
