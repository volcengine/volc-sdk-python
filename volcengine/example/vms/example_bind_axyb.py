# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    bind_axyb_form = {
        "NumberPoolNo": "NP166375725010908111",
        "PhoneNoA": "13700000017",
        "CityCode": "010",
        "UserData": "this is my user data",
        "ExpireTime": "1673071556",
        "YbEnableDuration": 600,
        "NumberPoolNoY": "NP166265127202826653"
    }
    print(vms_service.bind_axyb(bind_axyb_form))
