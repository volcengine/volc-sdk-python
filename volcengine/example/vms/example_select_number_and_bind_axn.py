# coding:utf-8
from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    select_number_and_bind_axn_form = {
        "NumberPoolNo": "NP167092127702825445",
        "PhoneNoA": "13700000001",
        "PhoneNoB": "13700000002",
        "UserData": "this is my user data",
        "CityCode": "010",
        "ExpireTime": "1673071556",
    }
    print(vms_service.select_number_and_bind_axn(select_number_and_bind_axn_form))
