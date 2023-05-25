# coding:utf-8

from volcengine.vms.VmsService import VmsService

if __name__ == '__main__':
    vms_service = VmsService()

    vms_service.set_ak("your ak")
    vms_service.set_sk("your sk")

    body = {
        "Url": "公网url，使用前需要申请正向代理",
        "Name": "测试文件"
    }

    vms_service.fetch_resource(body)
