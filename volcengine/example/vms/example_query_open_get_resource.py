# coding:utf-8

from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    body = {
       "Type": 0,
       "Keyword": "0f299353da3343e58373132b9e3b75d4"
    }

    print(vms_service.query_open_get_resource(body))
