# coding:utf-8
from volcengine.vms.NumberPoolService import NumberPoolService

if __name__ == '__main__':
    numberPoolService = NumberPoolService()

    numberPoolService.set_ak("your ak")
    numberPoolService.set_sk("your sk")

    form = {
        "Name": "testsipv2",
        "ServiceType": 100,
        "SubServiceType": 101,
        "NumberPoolNo":"todo"
    }
    print(numberPoolService.update_number_pool(form))
