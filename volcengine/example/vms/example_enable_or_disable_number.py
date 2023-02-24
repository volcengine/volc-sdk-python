# coding:utf-8
from volcengine.vms.NumberPoolService import NumberPoolService

if __name__ == '__main__':
    numberPoolService = NumberPoolService()

    numberPoolService.set_ak("your ak")
    numberPoolService.set_sk("your sk")

    form = {
        "NumberList": "xxx",
        "EnableCode": 2
    }
    print(numberPoolService.enable_or_disable_number(form))
