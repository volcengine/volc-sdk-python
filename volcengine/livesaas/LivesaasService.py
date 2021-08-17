# coding:utf-8
import json
import os

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service
from volcengine.const.Const import *
from volcengine.Policy import *
import aiohttp
from volcengine.auth.SignerV4 import SignerV4

LIVESAAS_SERVICE_NAME = "livesaas"
LIVESAAS_API_VERSION = "2020-06-01"

service_info_map = {
    REGION_CN_NORTH1: ServiceInfo(
        "livesaas.volcengineapi.com",
        {'Accept': 'application/json'},
        Credentials('', '', LIVESAAS_SERVICE_NAME, REGION_CN_NORTH1),
        5, 5, "https"),
}

api_info = {
    # 直播间管理类接口
    "CreateActivityAPI":
        ApiInfo("POST", "/", {"Action": "CreateActivityAPI", "Version": LIVESAAS_API_VERSION}, {}, {}),
    "DeleteActivityAPI":
        ApiInfo("POST", "/", {"Action": "DeleteActivityAPI", "Version": LIVESAAS_API_VERSION}, {}, {}),
    "ListActivityAPI":
        ApiInfo("GET", "/", {"Action": "ListActivityAPI", "Version": LIVESAAS_API_VERSION}, {}, {}),
    # 直播控制类接口
    "UpdateActivityStatusAPI":
        ApiInfo("POST", "/", {"Action": "UpdateActivityStatusAPI", "Version": LIVESAAS_API_VERSION}, {}, {}),
    "UpdatePullToPushAPI":
        ApiInfo("POST", "/", {"Action": "UpdatePullToPushAPI", "Version": LIVESAAS_API_VERSION}, {}, {}),
    "GetActivityAPI":
        ApiInfo("GET", "/", {"Action": "GetActivityAPI", "Version": LIVESAAS_API_VERSION}, {}, {}),
    "GetStreamsAPI":
        ApiInfo("GET", "/", {"Action": "GetStreamsAPI", "Version": LIVESAAS_API_VERSION}, {}, {}),
    "UpdateActivityBasicConfigAPI":
        ApiInfo("POST", "/", {"Action": "UpdateActivityBasicConfigAPI", "Version": LIVESAAS_API_VERSION}, {}, {}),
    "GetActivityBasicConfigAPI":
        ApiInfo("GET", "/", {"Action": "GetActivityBasicConfigAPI", "Version": LIVESAAS_API_VERSION}, {}, {}),
    "UpdateLoopVideoAPI":
        ApiInfo("POST", "/", {"Action": "UpdateLoopVideoAPI", "Version": LIVESAAS_API_VERSION}, {}, {}),
    "UpdateLoopVideoStatusAPI":
        ApiInfo("POST", "/", {"Action": "UpdateLoopVideoStatusAPI", "Version": LIVESAAS_API_VERSION}, {}, {}),
    # 回放管理类接口
    "UploadReplayAPI":
        ApiInfo("POST", "/", {"Action": "UploadReplayAPI", "Version": LIVESAAS_API_VERSION}, {}, {}),
    "UpdateMediaOnlineStatusAPI":
        ApiInfo("POST", "/", {"Action": "UpdateMediaOnlineStatusAPI", "Version": LIVESAAS_API_VERSION}, {}, {}),
    "ListMediasAPI":
        ApiInfo("GET", "/", {"Action": "ListMediasAPI", "Version": LIVESAAS_API_VERSION}, {}, {}),
    # 评论类接口
    "PresenterChatAPI":
        ApiInfo("POST", "/", {"Action": "PresenterChatAPI", "Version": LIVESAAS_API_VERSION}, {}, {}),
    "DeleteChatAPI":
        ApiInfo("POST", "/", {"Action": "DeleteChatAPI", "Version": LIVESAAS_API_VERSION}, {}, {}),
    # 客户端SDK类接口
    "GetSDKTokenAPI":
        ApiInfo("POST", "/", {"Action": "GetSDKTokenAPI", "Version": LIVESAAS_API_VERSION}, {}, {}),
}


class LivesaasService(Service):
    def __init__(self, region=REGION_CN_NORTH1):
        self.service_info = LivesaasService.get_service_info(region)
        self.api_info = LivesaasService.get_api_info()
        super(LivesaasService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(region):
        service_info = service_info_map.get(region, None)
        if not service_info:
            raise Exception('LivesaasService not support region %s' % region)
        return service_info

    @staticmethod
    def get_api_info():
        return api_info

    async def async_json(self, api, params, body):
        if not (api in self.api_info):
            raise Exception("no such api")
        api_info = self.api_info[api]
        r = self.prepare_request(api_info, params)
        r.headers['Content-Type'] = 'application/json'
        r.body = body
        timeout = aiohttp.ClientTimeout(connect=self.service_info.connection_timeout, sock_connect=self.service_info.socket_timeout)

        SignerV4.sign(r, self.service_info.credentials)

        url = r.build()
        async with aiohttp.request("POST", url, headers=r.headers, data=r.body, timeout=timeout) as r:
            resp = await r.text(encoding="utf-8")
            if r.status == 200:
                return resp
            else:
                raise Exception(resp)

    async def async_get(self, api, params):
        if not (api in self.api_info):
            raise Exception("no such api")
        api_info = self.api_info[api]
        r = self.prepare_request(api_info, params)
        timeout = aiohttp.ClientTimeout(connect=self.service_info.connection_timeout, sock_connect=self.service_info.socket_timeout)

        SignerV4.sign(r, self.service_info.credentials)

        url = r.build()
        async with aiohttp.request("GET", url, headers=r.headers, timeout=timeout) as r:
            resp = await r.text(encoding="utf-8")
            if r.status == 200:
                return resp
            else:
                raise Exception(resp)

    # ========================= 直播间管理类接口 =========================
    # CreateActivityAPI
    def create_activity_api(self, body):
        res = self.json('CreateActivityAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("CreateActivityAPI: empty response")
        res_json = json.loads(res)
        return res_json

    async def async_create_activity_api(self, body):
        res = await self.async_json('CreateActivityAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("CreateActivityAPI: empty response")
        res_json = json.loads(res)
        return res_json

    # DeleteActivityAPI
    def delete_activity_api(self, body):
        res = self.json('DeleteActivityAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("DeleteActivityAPI: empty response")
        res_json = json.loads(res)
        return res_json

    async def async_delete_activity_api(self, body):
        res = await self.async_json('DeleteActivityAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("DeleteActivityAPI: empty response")
        res_json = json.loads(res)
        return res_json

    # ListActivityAPI
    def list_activity_api(self, params):
        res = self.get('ListActivityAPI', params)
        if res == '':
            raise Exception("ListActivityAPI: empty response")
        res_json = json.loads(res)
        return res_json

    async def async_list_activity_api(self, params):
        res = await self.async_get('ListActivityAPI', params)
        if res == '':
            raise Exception("ListActivityAPI: empty response")
        res_json = json.loads(res)
        return res_json

    # ========================= 直播间控制类接口 =========================
    # UpdateActivityStatusAPI
    def update_activity_status_api(self, body):
        res = self.json('UpdateActivityStatusAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("UpdateActivityStatusAPI: empty response")
        res_json = json.loads(res)
        return res_json

    async def async_update_activity_status_api(self, body):
        res = await self.async_json('UpdateActivityStatusAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("UpdateActivityStatusAPI: empty response")
        res_json = json.loads(res)
        return res_json

    # UpdatePullToPushAPI
    def update_pull_to_push_api(self, body):
        res = self.json('UpdatePullToPushAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("UpdatePullToPushAPI: empty response")
        res_json = json.loads(res)
        return res_json

    async def async_update_pull_to_push_api(self, body):
        res = await self.async_json('UpdatePullToPushAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("UpdatePullToPushAPI: empty response")
        res_json = json.loads(res)
        return res_json

    # GetActivityAPI
    def get_activity_api(self, params):
        res = self.get('GetActivityAPI', params)
        if res == '':
            raise Exception("GetActivityAPI: empty response")
        res_json = json.loads(res)
        return res_json

    async def async_get_activity_api(self, params):
        res = await self.async_get('GetActivityAPI', params)
        if res == '':
            raise Exception("GetActivityAPI: empty response")
        res_json = json.loads(res)
        return res_json

    # GetStreamsAPI
    def get_streams_api(self, params):
        res = self.get('GetStreamsAPI', params)
        if res == '':
            raise Exception("GetStreamsAPI: empty response")
        res_json = json.loads(res)
        return res_json

    async def async_get_streams_api(self, params):
        res = await self.async_get('GetStreamsAPI', params)
        if res == '':
            raise Exception("GetStreamsAPI: empty response")
        res_json = json.loads(res)
        return res_json

    # UpdateActivityBasicConfigAPI
    def update_activity_basic_config_api(self, body):
        res = self.json('UpdateActivityBasicConfigAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("UpdateActivityBasicConfigAPI: empty response")
        res_json = json.loads(res)
        return res_json

    async def async_update_activity_basic_config_api(self, body):
        res = await self.async_json('UpdateActivityBasicConfigAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("UpdateActivityBasicConfigAPI: empty response")
        res_json = json.loads(res)
        return res_json

    # GetActivityBasicConfigAPI
    def get_activity_basic_config_api(self, params):
        res = self.get('GetActivityBasicConfigAPI', params)
        if res == '':
            raise Exception("GetActivityBasicConfigAPI: empty response")
        res_json = json.loads(res)
        return res_json

    async def async_get_activity_basic_config_api(self, params):
        res = await self.async_get('GetActivityBasicConfigAPI', params)
        if res == '':
            raise Exception("GetActivityBasicConfigAPI: empty response")
        res_json = json.loads(res)
        return res_json

    # UpdateLoopVideoAPI
    def update_loop_video_api(self, body):
        res = self.json('UpdateLoopVideoAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("UpdateLoopVideoAPI: empty response")
        res_json = json.loads(res)
        return res_json

    async def async_update_loop_video_api(self, body):
        res = await self.async_json('UpdateLoopVideoAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("UpdateLoopVideoAPI: empty response")
        res_json = json.loads(res)
        return res_json

    # UpdateLoopVideoStatusAPI
    def update_loop_video_status_api(self, body):
        res = self.json('UpdateLoopVideoStatusAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("UpdateLoopVideoStatusAPI: empty response")
        res_json = json.loads(res)
        return res_json

    async def async_update_loop_video_status_api(self, body):
        res = await self.async_json('UpdateLoopVideoStatusAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("UpdateLoopVideoStatusAPI: empty response")
        res_json = json.loads(res)
        return res_json

    # ========================= 回放管理类接口 =========================
    # UploadReplayAPI
    def upload_replay_api(self, body):
        res = self.json('UploadReplayAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("UploadReplayAPI: empty response")
        res_json = json.loads(res)
        return res_json

    async def async_upload_replay_api(self, body):
        res = await self.async_json('UploadReplayAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("UploadReplayAPI: empty response")
        res_json = json.loads(res)
        return res_json

    # UpdateMediaOnlineStatusAPI
    def update_media_online_status_api(self, body):
        res = self.json('UpdateMediaOnlineStatusAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("UpdateMediaOnlineStatusAPI: empty response")
        res_json = json.loads(res)
        return res_json

    async def async_update_media_online_status_api(self, body):
        res = await self.async_json('UpdateMediaOnlineStatusAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("UpdateMediaOnlineStatusAPI: empty response")
        res_json = json.loads(res)
        return res_json

    # ListMediasAPI
    def list_medias_api(self, params):
        res = self.get('ListMediasAPI', params)
        if res == '':
            raise Exception("ListMediasAPI: empty response")
        res_json = json.loads(res)
        return res_json

    async def async_list_medias_api(self, params):
        res = await self.async_get('ListMediasAPI', params)
        if res == '':
            raise Exception("ListMediasAPI: empty response")
        res_json = json.loads(res)
        return res_json

    # ========================= 评论类接口 =========================
    # PresenterChatAPI
    def presenter_chat_api(self, body):
        res = self.json('PresenterChatAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("PresenterChatAPI: empty response")
        res_json = json.loads(res)
        return res_json

    async def async_presenter_chat_api(self, body):
        res = await self.async_json('PresenterChatAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("PresenterChatAPI: empty response")
        res_json = json.loads(res)
        return res_json

    # DeleteChatAPI
    def delete_chat_api(self, body):
        res = self.json('DeleteChatAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("DeleteChatAPI: empty response")
        res_json = json.loads(res)
        return res_json

    async def async_delete_chat_api(self, body):
        res = await self.async_json('DeleteChatAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("DeleteChatAPI: empty response")
        res_json = json.loads(res)
        return res_json

    # ========================= 客户端SDK类接口 =========================
    # GetSDKTokenAPI
    def get_sdk_token_api(self, body):
        res = self.json('GetSDKTokenAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("GetSDKTokenAPI: empty response")
        res_json = json.loads(res)
        return res_json

    async def async_get_sdk_token_api(self, body):
        res = await self.async_json('GetSDKTokenAPI', dict(), json.dumps(body))
        if res == '':
            raise Exception("GetSDKTokenAPI: empty response")
        res_json = json.loads(res)
        return res_json