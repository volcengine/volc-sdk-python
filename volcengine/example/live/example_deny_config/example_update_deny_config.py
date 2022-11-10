# coding:utf-8
import json

from volcengine.live.LiveService import LiveService
from volcengine.live.models.business.deny_config_pb2 import DenyConfigDetail
from volcengine.live.models.request.request_live_pb2 import  UpdateDenyConfigRequest

if __name__ == '__main__':
    live_service = LiveService()
    live_service.set_ak('')
    live_service.set_sk('')
    req = UpdateDenyConfigRequest()

    detail = DenyConfigDetail()
    detail.ProType.extend(['ProType'])
    detail.FmtType.extend(['FmtType'])
    detail.AllowList.extend(['AllowList'])
    detail.DenyList.extend(['DenyList'])
    req.Vhost = 'Vhost'
    req.Domain = 'Domain'
    req.DenyConfigList.extend([detail])

    print(req)
    resp = live_service.update_deny_config(req)
    print(resp)