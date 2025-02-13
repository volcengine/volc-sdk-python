# coding:utf-8
import json
import time
import requests
import aiohttp

from .common import *
from .exception import ERRCODE_EXCEPTION, VikingDBException
from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo
from volcengine.auth.SignerV4 import SignerV4


class VikingDBServiceBase(Service):
    def __init__(self, host="api-vikingdb.volces.com", region="cn-north-1", ak="", sk="", scheme='http',
                 connection_timeout=30, socket_timeout=30, proxy=None, retry_option=None):
        """
        :param retry_option: retry option.
        :type retry_option: RetryOption
        """
        self.service_info = VikingDBServiceBase.get_service_info(host, region, scheme, connection_timeout, socket_timeout, ak, sk)
        self.api_info = VikingDBServiceBase.get_api_info()
        super(VikingDBServiceBase, self).__init__(self.service_info, self.api_info)
        if ak:
            self.set_ak(ak)
        if sk:
            self.set_sk(sk)

        if proxy is not None:
            if "http:" in proxy:
                self.session.proxies.update({
                    'http': proxy,
                })
            if "https:" in proxy:
                self.session.proxies.update({
                    'https': proxy,
                })
        self.retry_option = retry_option if retry_option else RetryOption()
        try:
            res = self.get_body("Ping", {}, json.dumps({}))
        except Exception as e:
            raise VikingDBException(1000028, "missed", "host or region is incorrect".format(str(e))) from None

    def setHeader(self, header):
        api_info = VikingDBServiceBase.get_api_info()
        for key in api_info:
            for item in header:
                api_info[key].header[item] = header[item]
        self.api_info = api_info

    @staticmethod
    def get_service_info(host, region, scheme, connection_timeout, socket_timeout, ak, sk):
        service_info = ServiceInfo(host, {"Host": host},
                                   Credentials(ak, sk, 'air', region), connection_timeout, socket_timeout,
                                   scheme=scheme)
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            # Collection
            "CreateCollection": ApiInfo("POST", "/api/collection/create", {}, {},
                                        {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "GetCollection": ApiInfo("GET", "/api/collection/info", {}, {},
                                     {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "DropCollection": ApiInfo("POST", "/api/collection/drop", {}, {},
                                      {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "ListCollections": ApiInfo("GET", "/api/collection/list", {}, {},
                                       {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            # Index
            "CreateIndex": ApiInfo("POST", "/api/index/create", {}, {},
                                   {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "GetIndex": ApiInfo("GET", "/api/index/info", {}, {},
                                {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "DropIndex": ApiInfo("POST", "/api/index/drop", {}, {},
                                 {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "ListIndexes": ApiInfo("GET", "/api/index/list", {}, {},
                                   {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "UpsertData": ApiInfo("POST", "/api/collection/upsert_data", {}, {},
                                  {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "UpdateData": ApiInfo("POST", "/api/collection/update_data", {}, {},
                                  {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "DeleteData": ApiInfo("POST", "/api/collection/del_data", {}, {},
                                  {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "FetchData": ApiInfo("GET", "/api/collection/fetch_data", {}, {},
                                 {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "FetchIndexData": ApiInfo("GET", "/api/index/fetch_data", {}, {},
                                      {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "SearchIndex": ApiInfo("POST", "/api/index/search", {}, {},
                                   {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "SearchAgg": ApiInfo("POST", "/api/index/search/agg", {}, {},
                                   {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "IndexSort": ApiInfo("POST", "/api/index/sort", {}, {},
                                 {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "Embedding": ApiInfo("POST", "/api/data/embedding", {}, {},
                                 {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "ListEmbeddings": ApiInfo("GET", "/api/data/list_embedding_models", {}, {},
                                      {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "UpdateCollection": ApiInfo("POST", "/api/collection/update", {}, {},
                                        {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "UpdateIndex": ApiInfo("POST", "/api/index/update", {}, {},
                                   {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "Rerank": ApiInfo("POST", "/api/index/rerank", {}, {},
                              {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "BatchRerank": ApiInfo("POST", "/api/index/batch_rerank", {}, {},
                                   {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "Ping": ApiInfo("GET", "/api/viking_db/data/ping", {}, {},
                            {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "EmbeddingV2": ApiInfo("POST", "/api/data/embedding/version/2", {}, {},
                                   {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "CreateTask": ApiInfo("POST", "/api/task/create", {}, {},
                                   {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "GetTask": ApiInfo("POST", "/api/task/info", {}, {},
                                   {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "ListTask": ApiInfo("POST", "/api/task/list", {}, {},
                                   {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "DropTask": ApiInfo("POST", "/api/task/drop", {}, {},
                                   {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "UpdateTask": ApiInfo("POST", "/api/task/update", {}, {},
                                   {'Accept': 'application/json', 'Content-Type': 'application/json'}),                                    
        }
        return api_info

    # get参数放在body里面
    def get_body(self, api, params, body):
        if not (api in self.api_info):
            raise Exception("no such api")
        api_info = self.api_info[api]
        r = self.prepare_request(api_info, params)
        r.headers['Content-Type'] = 'application/json'
        r.body = body

        SignerV4.sign(r, self.service_info.credentials)

        url = r.build()
        resp = self.session.get(url, headers=r.headers, data=r.body,
                                timeout=(self.service_info.connection_timeout, self.service_info.socket_timeout))
        if resp.status_code == 200:
            return json.dumps(resp.json())
        else:
            raise Exception(resp.text.encode("utf-8"))

    async def async_json(self, api, params, body):
        if not (api in self.api_info):
            raise Exception("no such api")
        api_info = self.api_info[api]
        r = self.prepare_request(api_info, params)
        r.headers['Content-Type'] = 'application/json'
        r.body = body

        SignerV4.sign(r, self.service_info.credentials)
        timeout = aiohttp.ClientTimeout(connect=self.service_info.connection_timeout,
                                        sock_connect=self.service_info.socket_timeout)
        url = r.build()
        async with aiohttp.request("POST", url, headers=r.headers, data=r.body, timeout=timeout) as r:
            resp = await r.text(encoding="utf-8")
            if r.status == 200:
                return resp
            else:
                raise Exception(resp)

    # get参数放在body里面，异常处理
    def get_body_exception(self, api, params, body):
        # res = self.get_body(api, params, body)
        # if res == '':
        #     raise VikingDBException(1000028, "missed",
        #                             "empty response due to unknown error, please contact customer service")
        # return res
        try:
            res = self.get_body(api, params, body)
        except requests.Timeout as e:
            raise e
        except Exception as e:
            try:
                res_json = json.loads(e.args[0].decode("utf-8"))
            except:
                raise VikingDBException(1000028, "missed", "json load res error, res:{}".format(str(e))) from None
            code = res_json.get("code", 1000028)
            request_id = res_json.get("request_id", 1000028)
            message = res_json.get("message", None)
            raise ERRCODE_EXCEPTION.get(code, VikingDBException)(code, request_id, message) from None
        if res == '':
            raise VikingDBException(1000028, "missed",
                                    "empty response due to unknown error, please contact customer service") from None
        return res

    # get参数放在url里面，异常处理
    def get_exception(self, api, params):
        try:
            res = self.get(api, params)
        except requests.Timeout as e:
            raise e
        except Exception as e:
            try:
                res_json = json.loads(e.args[0])
            except:
                raise VikingDBException(1000028, "missed", "json load res error, res:{}".format(str(e))) from None
            code = res_json.get("code", 1000028)
            request_id = res_json.get("request_id", 1000028)
            message = res_json.get("message", None)
            raise ERRCODE_EXCEPTION.get(code, VikingDBException)(code, request_id, message) from None
        if res == '':
            raise VikingDBException(1000028, "missed",
                                    "empty response due to unknown error, please contact customer service") from None
        return res

    # post异常处理
    def json_exception(self, api, params, body):
        # res = self.json(api, params, body)
        # if res == '':
        #     raise VikingDBException(1000028, "missed",
        #                             "empty response due to unknown error, please contact customer service")
        # return res
        try:
            res = self.json(api, params, body)
        except requests.Timeout as e:
            raise e
        except Exception as e:
            try:
                res_json = json.loads(e.args[0].decode("utf-8"))
            except:
                raise VikingDBException(1000028, "missed", "json load res error, res:{}".format(str(e))) from None
            code = res_json.get("code", 1000028)
            request_id = res_json.get("request_id", 1000028)
            message = res_json.get("message", None)
            raise ERRCODE_EXCEPTION.get(code, VikingDBException)(code, request_id, message) from None
        if res == '':
            raise VikingDBException(1000028, "missed",
                                    "empty response due to unknown error, please contact customer service") from None
        return res

    async def async_json_exception(self, api, params, body):
        try:
            res = await self.async_json(api, params, body)
        except requests.Timeout as e:
            raise e
        except Exception as e:
            try:
                res_json = json.loads(e.args[0].decode("utf-8"))
            except:
                raise VikingDBException(1000028, "missed", "json load res error, res:{}".format(str(e))) from None
            code = res_json.get("code", 1000028)
            request_id = res_json.get("request_id", 1000028)
            message = res_json.get("message", None)
            raise ERRCODE_EXCEPTION.get(code, VikingDBException)(code, request_id, message) from None
        if res == '':
            raise VikingDBException(1000028, "missed",
                                    "empty response due to unknown error, please contact customer service") from None
        return res

    async def async_get_body_exception(self, api, params, body):
        try:
            res = await self.async_get_body(api, params, body)
        except requests.Timeout as e:
            raise e
        except Exception as e:
            try:
                res_json = json.loads(e.args[0].decode("utf-8"))
            except:
                raise VikingDBException(1000028, "missed", "json load res error, res:{}".format(str(e))) from None
            code = res_json.get("code", 1000028)
            request_id = res_json.get("request_id", 1000028)
            message = res_json.get("message", None)
            raise ERRCODE_EXCEPTION.get(code, VikingDBException)(code, request_id, message) from None
        if res == '':
            raise VikingDBException(1000028, "missed",
                                    "empty response due to unknown error, please contact customer service") from None
        return res

    async def async_get_body(self, api, params, body):
        if not (api in self.api_info):
            raise Exception("no such api")
        api_info = self.api_info[api]
        r = self.prepare_request(api_info, params)
        r.headers['Content-Type'] = 'application/json'
        r.body = body

        SignerV4.sign(r, self.service_info.credentials)
        timeout = aiohttp.ClientTimeout(connect=self.service_info.connection_timeout,
                                        sock_connect=self.service_info.socket_timeout)
        url = r.build()

        async with aiohttp.request("GET", url, headers=r.headers, data=r.body, timeout=timeout) as r:
            resp = await r.text(encoding="utf-8")
            if r.status == 200:
                return resp
            else:
                raise Exception(resp)
            
    def _retry_request(self, api, params, body, remaining=None, retry_option=None):
        try: 
            method = self.api_info[api].method
            if method == "GET":
                res = self.get_body(api, params, body)
            else:
                res = self.json(api, params, body)
        except requests.Timeout as e:
            if remaining and remaining.has_remaining():
                timeout = retry_option.calculate_retry_timeout(remaining)
                time.sleep(timeout)
            else:
                raise e
            return self._retry_request(api, params, body, remaining, retry_option)
        except Exception as e:
            err_msg = "request exception: {}".format(e)
            try:
                res_json = json.loads(e.args[0].decode("utf-8"))
            except:
                raise VikingDBException(1000028, "missed",
                                        "res json load error: {}, due to last error: {}".format(str(e), err_msg)) from None
            code = res_json.get("code", 1000028)
            request_id = res_json.get("request_id", 1000028)
            message = res_json.get("message", None)
            if code == 1000029 and remaining and remaining.has_remaining():
                timeout = retry_option.calculate_retry_timeout(remaining)
                time.sleep(timeout)
                return self._retry_request(api, params, body, remaining, retry_option)
            else:
                raise ERRCODE_EXCEPTION.get(code, VikingDBException)(code, request_id, message) from None
        if res == '':
            raise VikingDBException(1000028, "missed",
                                    "empty response due to unknown error, please contact customer service") from None
        return res
