# coding:utf-8
from volcengine.vms.NumberPoolService import NumberPoolService

if __name__ == '__main__':
    numberPoolService = NumberPoolService()

    numberPoolService.set_ak("your ak")
    numberPoolService.set_sk("your sk")

    form = {
        "NumberPoolNo": "xxx",
        "NumberPoolTypeCode": 101,
        "Limit": 5,
        "Offset":0
    }
    print(numberPoolService.number_list(form))
