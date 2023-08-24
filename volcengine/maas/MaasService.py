# coding:utf-8
import json
import copy

from google.protobuf.json_format import Parse

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo
from volcengine.auth.SignerV4 import SignerV4

from .ka_mgr import *
from .sse_decoder import SSEDecoder
from .models.api.api_pb2 import ChatResp, CertResp
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
            "cert": ApiInfo("POST", "/api/v1/cert", {}, {}, {}),
        }
        return api_info

    def chat(self, req, is_secret=False):
        self._validate()
        try:
            req['stream'] = False
            if is_secret:
                key, nonce, req = self.encrypt_chat_request(req)
            res = self.json("chat", {}, json.dumps(req))
            if res == '':
                raise new_client_sdk_request_error("empty response")
            resp = Parse(res, ChatResp(), True)
            if is_secret:
                self.decrypt_chat_response(key, nonce, resp)
        except Exception as e:
            try:
                resp = Parse(str(e.args[0], encoding='utf-8'), ChatResp(), True)
            except Exception:
                raise new_client_sdk_request_error(str(e))
            else:
                raise MaasException(resp.error.code_n, resp.error.code, resp.error.message)
        else:
            return resp

    def _validate(self):
        if self.service_info.credentials is None or \
            self.service_info.credentials.sk is None or \
            self.service_info.credentials.ak is None:
            raise new_client_sdk_request_error("no valid credential")

    def stream_chat(self, req, is_secret=False):
        self._validate()
        
        try:
            req['stream'] = True
            if is_secret:
                key, nonce, req = self.encrypt_chat_request(req)
            
            if not ("chat" in self.api_info):
                raise new_client_sdk_request_error("no such api")
            api_info = self.api_info["chat"]
            r = self.prepare_request(api_info, {})
            r.headers['Content-Type'] = 'application/json'
            r.body = json.dumps(req)

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
                        if is_secret:
                            self.decrypt_chat_response(key, nonce, res)
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

    def init_cert_by_req(self, req):
        cert_req = {"model": req['model']}
        try:
            resp = self.json("cert", {}, json.dumps(cert_req))
            resp = Parse(resp, CertResp(), True)
            req['model']['endpoint_id'] = resp.model.endpoint_id
            return key_agreement_client(resp.cert)
        except Exception as e:
            raise new_client_sdk_request_error(str(e))

    def encrypt_chat_request(self, req):
        req_c = copy.deepcopy(req)
        
        cert = self.init_cert_by_req(req_c)
        key, nonce, token = cert.generate_ecies_key_pair()
        req_c['crypto_token'] = token
        for i in req_c['messages']:
            if i['content'] != '':
                i['content'] = aes_gcm_encrypt_base64_string(key, nonce, i['content'])
        
        return key, nonce, req_c

    def decrypt_chat_response(self, key, nonce, resp):
        m = resp.choice.message.content
        if m != '':
            resp.choice.message.content = aes_gcm_decrypt_base64_string(key, nonce, m)
        return
