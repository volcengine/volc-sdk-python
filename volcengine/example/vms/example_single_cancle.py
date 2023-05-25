# coding:utf-8

from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    params = {
        "SingleOpenId": "9b39e17fb12444c78f20d6551469a6e0"
    }

    print(vms_service.single_cancel(params))