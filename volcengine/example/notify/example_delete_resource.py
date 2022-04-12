# coding:utf-8

from volcengine.notify.notify import NotifyService

if __name__ == '__main__':
    notify_service = NotifyService()

    notify_service.set_ak("your ak")
    notify_service.set_sk("your sk")

    delete_resource_param = {
       "ResourceKey": "4bb4b9b137264148998de1c227e9f652",
    }

    print(notify_service.delete_resource(delete_resource_param))
