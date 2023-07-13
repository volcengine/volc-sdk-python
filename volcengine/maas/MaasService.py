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
from .exception import MaasException, new_client_sdk_request_error


class MaasService(Service):
    def __init__(self, host, region, connection_timeout=60, socket_timeout=60):
        service_info = MaasService.get_service_info(host, region, connection_timeout, socket_timeout)
        api_info = MaasService.get_api_info()
        super(MaasService, self).__init__(service_info, api_info)

    @staticmethod
    def get_service_info(host, region, connection_timeout, socket_timeout):
        service_info = ServiceInfo(host, {'Accept': 'application/json'},
                                   Credentials('', '', 'ml_maas', region), connection_timeout, socket_timeout, 'https')
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
                raise new_client_sdk_request_error("empty response")
            resp = Parse(res, ChatResp(), True)
        except Exception as e:
            try:
                resp = Parse(str(e.args[0]), ChatResp(), True)
            except Exception:
                raise new_client_sdk_request_error(str(e))
            else:
                raise MaasException(resp.error.code_n, resp.error.code, resp.error.message)
        else:
            return resp

    def stream_chat(self, req):
        try:
            req['stream'] = True
            
            if not ("chat" in self.api_info):
                raise new_client_sdk_request_error("no such api")
            api_info = self.api_info["chat"]
            r = self.prepare_request(api_info, {})
            r.headers['Content-Type'] = 'application/json'
            r.body = json.dumps(req)
            
            if self.service_info.credentials is None or \
                self.service_info.credentials.sk is None or \
                self.service_info.credentials.ak is None:
                raise new_client_sdk_request_error("no valid credential")

            SignerV4.sign(r, self.service_info.credentials)

            url = r.build()
            res = self.session.post(url, headers=r.headers, data=r.body,
                                    timeout=(self.service_info.connection_timeout, self.service_info.socket_timeout), 
                                    stream=True)
            if res.status_code != 200:
                raw = res.text.encode("utf-8")
                res.close()
                try:
                    resp = Parse(raw, ChatResp(), True)
                except Exception:
                    raise new_client_sdk_request_error(raw)
                else:
                    raise MaasException(resp.error.code_n, resp.error.code, resp.error.message)

            decoder = SSEDecoder(res)
            
            def iter():
                for data in decoder.next():
                    try:
                        res = Parse(data, ChatResp(), True)
                    except:
                        pass
                    else:
                        if res.error.code_n != 0:
                            raise MaasException(res.error.code_n, res.error.code, res.error.message)
                        yield res
            
            return iter()
        except MaasException:
            raise
        except Exception as e:
            raise new_client_sdk_request_error(str(e))
