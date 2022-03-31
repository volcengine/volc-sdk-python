# coding:utf-8

from volcengine.notify.notify import NotifyService

if __name__ == '__main__':
    notify_service = NotifyService()

    notify_service.set_ak("your ak")
    notify_service.set_sk("your sk")

    body = {
        "Url": "公网url，使用前需要申请正向代理",
        "Name": "测试文件"
    }

    notify_service.fetch_resource(body)
