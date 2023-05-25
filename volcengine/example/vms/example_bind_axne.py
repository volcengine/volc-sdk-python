# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    bind_axne_form = {
        "NumberPoolNo": "NP167091934402820309",
        "PhoneNoA": "13700000017",
        "PhoneNoB": "13700000018",
        "UserData": "this is my user data",
        "CityCode": "010",
        "ExpireTime":"1673071556",
    }
    print(vms_service.bind_axne(bind_axne_form))
