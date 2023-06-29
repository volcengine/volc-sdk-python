# coding:utf-8
import json
import threading

from google.protobuf.json_format import Parse

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo
from volcengine.auth.SignerV4 import SignerV4

from .sse_decoder import SSEDecoder
from .models.api.api_pb2 import ChatResp


class MaasService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(MaasService, "_instance"):
            with MaasService._instance_lock:
                if not hasattr(MaasService, "_instance"):
                    MaasService._instance = object.__new__(cls)
        return MaasService._instance

    def __init__(self, host, region):
        self.service_info = MaasService.get_service_info(host, region)
        self.api_info = MaasService.get_api_info()
        super(MaasService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(host, region):
        service_info = ServiceInfo(host, {'Accept': 'application/json'},
                                   Credentials('', '', 'ml_maas', region), 30, 30, 'https')
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            "chat": ApiInfo("POST", "/api/v1/chat", {}, {}, {}),
        }
        return api_info

    def chat(self, req):
        try:
            req['stream'] = False
            res = self.json("chat", {}, json.dumps(req))
            if res == '':
                raise Exception("empty response")
            resp = Parse(res, ChatResp(), True)
        except Exception as e:
            try:
                resp = Parse(e.args[0], ChatResp(), True)
            except Exception:
                raise e
            else:
                raise Exception(resp.error.code, resp.error.message, resp.error.code_n)
        else:
            return resp

    def stream_chat(self, req):
        req['stream'] = True
        
        if not ("chat" in self.api_info):
            raise Exception("no such api")
        api_info = self.api_info["chat"]
        r = self.prepare_request(api_info, {})
        r.headers['Content-Type'] = 'application/json'
        r.body = json.dumps(req)

        SignerV4.sign(r, self.service_info.credentials)

        url = r.build()
        resp = self.session.post(url, headers=r.headers, data=r.body,
                                 timeout=(self.service_info.connection_timeout, self.service_info.socket_timeout), 
                                 stream=True)
        if resp.status_code != 200:
            raw = resp.text.encode("utf-8")
            resp.close()
            try:
                resp = Parse(raw, ChatResp(), True)
            except Exception:
                raise Exception(raw)
            else:
                raise Exception(resp.error.code, resp.error.message, resp.error.code_n)

        decoder = SSEDecoder(resp)
        
        def iter():
            for data in decoder.next():
                try:
                    res = Parse(data, ChatResp(), True)
                except:
                    pass
                else:
                    yield res
        
        return iter()
