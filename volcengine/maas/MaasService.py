# coding:utf-8
import sys
import json
import copy

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo
from volcengine.auth.SignerV4 import SignerV4

from .sse_decoder import SSEDecoder
from .exception import MaasException, new_client_sdk_request_error
from .utils import json_to_object


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
            "tokenization": ApiInfo("POST", "/api/v1/tokenization", {}, {}, {}),
            "classification": ApiInfo("POST", "/api/v1/classification", {}, {}, {}),
            "embeddings": ApiInfo("POST", "/api/v1/embeddings", {}, {}, {}),
        }
        return api_info

    def chat(self, req, is_secret=False):
        self._validate(is_secret, req)
        try:
            req['stream'] = False
            if is_secret:
                key, nonce, req = self.encrypt_chat_request(req)
            res = self.json("chat", {}, json.dumps(req).encode("utf-8"))
            if res == '':
                raise new_client_sdk_request_error("empty response", req.get('req_id', None))
            resp = json_to_object(res)
            if is_secret:
                self.decrypt_chat_response(key, nonce, resp)
        except Exception as e:
            try:
                resp = json_to_object(str(e.args[0], encoding='utf-8'))
            except Exception:
                raise new_client_sdk_request_error(str(e), req.get('req_id', None))
            else:
                raise MaasException(resp.error.code_n, resp.error.code, resp.error.message, resp.req_id)
        else:
            return resp

    def _validate(self, is_secret, req):
        if self.service_info.credentials is None or \
            self.service_info.credentials.sk is None or \
            self.service_info.credentials.ak is None:
            raise new_client_sdk_request_error("no valid credential", req.get('req_id', None))

        if is_secret and (sys.version_info < (3, 6)):
            raise new_client_sdk_request_error("For content encryption, python version must be 3.6 or above", req.get('req_id', None))

    def stream_chat(self, req, is_secret=False):
        self._validate(is_secret, req)

        try:
            req['stream'] = True
            if is_secret:
                key, nonce, req = self.encrypt_chat_request(req)

            if not ("chat" in self.api_info):
                raise new_client_sdk_request_error("no such api", req.get('req_id', None))
            api_info = self.api_info["chat"]
            r = self.prepare_request(api_info, {})
            r.headers['Content-Type'] = 'application/json'
            r.body = json.dumps(req).encode("utf-8")

            SignerV4.sign(r, self.service_info.credentials)

            url = r.build()
            res = self.session.post(url, headers=r.headers, data=r.body,
                                    timeout=(self.service_info.connection_timeout, self.service_info.socket_timeout),
                                    stream=True)
            if res.status_code != 200:
                raw = res.text.encode()
                res.close()
                try:
                    resp = json_to_object(str(raw, encoding='utf-8'))
                except Exception:
                    raise new_client_sdk_request_error(raw, req.get('req_id', None))
                else:
                    raise MaasException(resp.error.code_n, resp.error.code, resp.error.message, resp.req_id)

            decoder = SSEDecoder(res)

            def iter():
                for data in decoder.next():
                    if data == b'[DONE]':
                        return

                    try:
                        res = json_to_object(str(data, encoding='utf-8'))
                        if is_secret:
                            self.decrypt_chat_response(key, nonce, res)
                    except:
                        raise
                    else:
                        if res.error is not None and res.error.code_n != 0:
                            raise MaasException(res.error.code_n, res.error.code, res.error.message, res.req_id)
                        yield res

            return iter()
        except MaasException:
            raise
        except Exception as e:
            raise new_client_sdk_request_error(str(e), req.get('req_id', None))

    def tokenize(self, req):
        try:
            res = self.json("tokenization", {}, json.dumps(req).encode("utf-8"))
            if res == '':
                raise new_client_sdk_request_error("empty response", req.get('req_id', None))
            resp = json_to_object(res)
        except Exception as e:
            try:
                resp = json_to_object(str(e.args[0], encoding='utf-8'))
            except Exception:
                raise new_client_sdk_request_error(str(e), req.get('req_id', None))
            else:
                raise MaasException(resp.error.code_n, resp.error.code, resp.error.message, resp.req_id)
        else:
            return resp

    def classification(self, req):
        try:
            res = self.json("classification", {}, json.dumps(req).encode("utf-8"))
            if res == '':
                raise new_client_sdk_request_error("empty response", req.get('req_id', None))
            resp = json_to_object(res)
        except Exception as e:
            try:
                resp = json_to_object(str(e.args[0], encoding='utf-8'))
            except Exception:
                raise new_client_sdk_request_error(str(e), req.get('req_id', None))
            else:
                raise MaasException(resp.error.code_n, resp.error.code, resp.error.message, resp.req_id)
        else:
            return resp

    def embeddings(self, req):
        try:
            res = self.json("embeddings", {}, json.dumps(req).encode("utf-8"))
            if res == '':
                raise new_client_sdk_request_error("empty response", req.get('req_id', None))
            resp = json_to_object(res)
        except Exception as e:
            try:
                resp = json_to_object(str(e.args[0], encoding='utf-8'))
            except Exception:
                raise new_client_sdk_request_error(str(e), req.get('req_id', None))
            else:
                raise MaasException(resp.error.code_n, resp.error.code, resp.error.message, resp.req_id)
        else:
            return resp

    def init_cert_by_req(self, req):
        cert_req = {"model": req['model']}
        try:
            resp = self.json("cert", {}, json.dumps(cert_req).encode("utf-8"))
            resp = json_to_object(resp)
            req['model']['endpoint_id'] = resp.model.endpoint_id
            if resp.cert is None or len(resp.cert) == 0:
                raise new_client_sdk_request_error("No cert found, cannot use secret mode", req.get('req_id', None))
            from .ka_mgr import key_agreement_client
            return key_agreement_client(resp.cert)
        except ImportError:
            raise new_client_sdk_request_error(
                "Please install the cryptography package manually by using pip install cryptography~=38.0", req.get('req_id', None))
        except Exception as e:
            raise new_client_sdk_request_error(str(e), req.get('req_id', None))

    def encrypt_chat_request(self, req):
        req_c = copy.deepcopy(req)
        cert = self.init_cert_by_req(req_c)
        from .ka_mgr import aes_gcm_encrypt_base64_string
        key, nonce, token = cert.generate_ecies_key_pair()
        req_c['crypto_token'] = token
        for i in req_c['messages']:
            if i['content'] != '':
                i['content'] = aes_gcm_encrypt_base64_string(key, nonce, i['content'])

        return key, nonce, req_c

    def decrypt_chat_response(self, key, nonce, resp):
        from .ka_mgr import aes_gcm_decrypt_base64_string
        m = resp.choice.message.content
        if m != '':
            resp.choice.message.content = aes_gcm_decrypt_base64_string(key, nonce, m)
        return
