# coding:utf-8
import json
import copy
import time

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo
from volcengine.auth.SignerV4 import SignerV4

from volcengine.maas.sse_decoder import SSEDecoder
from volcengine.maas.exception import MaasException, new_client_sdk_request_error
from volcengine.maas.utils import dict_to_object, json_to_object
from .utils import gen_req_id
from volcengine.maas.v2.audio.audio import Audio
from volcengine.maas.v2.images.images import Images


class MaasService(Service):
    def __init__(self, host, region, connection_timeout=60, socket_timeout=60):
        service_info = MaasService.get_service_info(
            host, region, connection_timeout, socket_timeout
        )
        api_info = MaasService.get_api_info()
        self._setted_apikey = None
        api_info = self.get_api_info()
        super(MaasService, self).__init__(service_info, api_info)

        self.audio = Audio(self)
        self.images = Images(self)

    def set_apikey(self, apikey):
        self._setted_apikey = apikey

    @staticmethod
    def get_service_info(host, region, connection_timeout, socket_timeout):
        service_info = ServiceInfo(
            host,
            {"Accept": "application/json"},
            Credentials("", "", "ml_maas", region),
            connection_timeout,
            socket_timeout,
            "https",
        )
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            "chat": ApiInfo("POST", "/api/v2/endpoint/{endpoint_id}/chat", {}, {}, {}),
            "tokenization": ApiInfo(
                "POST", "/api/v2/endpoint/{endpoint_id}/tokenization", {}, {}, {}
            ),
            "classification": ApiInfo(
                "POST", "/api/v2/endpoint/{endpoint_id}/classification", {}, {}, {}
            ),
            "embeddings": ApiInfo(
                "POST", "/api/v2/endpoint/{endpoint_id}/embeddings", {}, {}, {}
            ),
            "audio.speech": ApiInfo(
                "POST", "/api/v2/endpoint/{endpoint_id}/audio/speech", {}, {}, {}
            ),
            "images.quick_gen": ApiInfo(
                "POST", "/api/v2/endpoint/{endpoint_id}/images/quick-gen", {}, {}, {}
            ),
            "images.flex_gen": ApiInfo(
                "POST", "/api/v2/endpoint/{endpoint_id}/images/flex-gen", {}, {}, {}
            ),
        }
        return api_info

    def chat(self, endpoint_id, req):
        req["stream"] = False
        return self._request(endpoint_id, "chat", req)

    def stream_chat(self, endpoint_id, req):
        req_id = gen_req_id()
        self._validate("chat", req_id)
        apikey = self._setted_apikey

        try:
            req["stream"] = True
            res = self._call(
                endpoint_id, "chat", req_id, {}, json.dumps(req).encode("utf-8"), apikey, stream=True
            )

            decoder = SSEDecoder(res)

            def iter():
                for data in decoder.next():
                    if data == b"[DONE]":
                        return

                    try:
                        res = json_to_object(str(data, encoding="utf-8"), req_id=req_id)
                    except:
                        raise
                    else:
                        if res.error is not None and res.error.code_n != 0:
                            raise MaasException(
                                res.error.code_n,
                                res.error.code,
                                res.error.message,
                                req_id,
                            )
                        yield res

            return iter()
        except MaasException:
            raise
        except Exception as e:
            raise new_client_sdk_request_error(str(e))

    def tokenize(self, endpoint_id, req):
        return self._request(endpoint_id, "tokenization", req)

    def classification(self, endpoint_id, req):
        return self._request(endpoint_id, "classification", req)

    def embeddings(self, endpoint_id, req):
        return self._request(endpoint_id, "embeddings", req)

    def _request(self, endpoint_id, api, req, params={}):
        req_id = gen_req_id()

        self._validate(api, req_id)

        apikey = self._setted_apikey

        try:
            res = self._call(endpoint_id, api, req_id, params, json.dumps(req).encode("utf-8"), apikey)
            resp = dict_to_object(res.json())
            if resp and isinstance(resp, dict):
                resp["req_id"] = req_id
            return resp

        except MaasException as e:
            raise e
        except Exception as e:
            raise new_client_sdk_request_error(str(e), req_id)

    def _validate(self, api, req_id):
        credentials_exist = (
                self.service_info.credentials is not None and
                self.service_info.credentials.sk is not None and
                self.service_info.credentials.ak is not None
        )

        if not self._setted_apikey and not credentials_exist:
            raise new_client_sdk_request_error("no valid credential", req_id)

        if not (api in self.api_info):
            raise new_client_sdk_request_error("no such api", req_id)

    def _call(self, endpoint_id, api, req_id, params, body, apikey=None, stream=False):
        api_info = copy.deepcopy(self.api_info[api])
        api_info.path = api_info.path.format(endpoint_id=endpoint_id)

        r = self.prepare_request(api_info, params)
        r.headers["x-tt-logid"] = req_id
        r.headers["Content-Type"] = "application/json"
        r.body = body

        if apikey is None:
            SignerV4.sign(r, self.service_info.credentials)
        elif apikey is not None:
            r.headers["Authorization"] = "Bearer " + apikey

        url = r.build()
        res = self.session.post(
            url,
            headers=r.headers,
            data=r.body,
            timeout=(
                self.service_info.connection_timeout,
                self.service_info.socket_timeout,
            ),
            stream=stream,
        )

        if res.status_code != 200:
            raw = res.text.encode()
            res.close()
            try:
                resp = json_to_object(str(raw, encoding="utf-8"), req_id=req_id)
            except Exception:
                raise new_client_sdk_request_error(raw, req_id)
            else:
                if resp.error:
                    raise MaasException(
                        resp.error.code_n, resp.error.code, resp.error.message, req_id
                    )
                else:
                    raise new_client_sdk_request_error(resp, req_id)

        return res
