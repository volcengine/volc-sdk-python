# coding:utf-8
from random import random
from .Task import Task
import json
import re
import threading
import time

import aiohttp

from .Index import Index
from .common import *
from .Collection import Collection
from .exception import ERRCODE_EXCEPTION, VikingDBException
from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo
from volcengine.auth.SignerV4 import SignerV4
from typing import Union, List


class VikingDBService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(VikingDBService, "_instance"):
            with VikingDBService._instance_lock:
                if not hasattr(VikingDBService, "_instance"):
                    VikingDBService._instance = object.__new__(cls)
        return VikingDBService._instance

    def __init__(self, host="api-vikingdb.volces.com", region="cn-north-1", ak="", sk="", scheme='http',
                 connection_timeout=30, socket_timeout=30, proxy=None):
        self.service_info = VikingDBService.get_service_info(host, region, scheme, connection_timeout, socket_timeout, ak, sk)
        self.api_info = VikingDBService.get_api_info()
        super(VikingDBService, self).__init__(self.service_info, self.api_info)
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

        try:
            res = self.get_body("Ping", {}, json.dumps({}))
        except Exception as e:
            raise VikingDBException(1000028, "missed", "host or region is incorrect".format(str(e))) from None

    def setHeader(self, header):
        api_info = VikingDBService.get_api_info()
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
            "DeleteData": ApiInfo("POST", "/api/collection/del_data", {}, {},
                                  {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "FetchData": ApiInfo("GET", "/api/collection/fetch_data", {}, {},
                                 {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "FetchIndexData": ApiInfo("GET", "/api/index/fetch_data", {}, {},
                                      {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "SearchIndex": ApiInfo("POST", "/api/index/search", {}, {},
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
            
    def _retry_request(self, api, params, body, remaining_retries=3):
        try: 
            method = self.api_info[api].method
            if method == "GET":
                res = self.get_body(api, params, body)
            else:
                res = self.json(api, params, body)
        except Exception as e:
            try:
                res_json = json.loads(e.args[0].decode("utf-8"))
            except:
                raise VikingDBException(1000028, "missed", "json load res error, res:{}".format(str(e))) from None
            code = res_json.get("code", 1000028)
            request_id = res_json.get("request_id", 1000028)
            message = res_json.get("message", None)
            if code == 1000029 and remaining_retries > 0:
                remaining_retries  = remaining_retries - 1
                timeout = self._calculate_retry_timeout(remaining_retries)
                time.sleep(timeout)
                return self._retry_request(api, params, body, remaining_retries)
            else:
                raise ERRCODE_EXCEPTION.get(code, VikingDBException)(code, request_id, message) from None
        if res == '':
            raise VikingDBException(1000028, "missed",
                                    "empty response due to unknown error, please contact customer service") from None
        return res
    
    def _calculate_retry_timeout(self, remaining_retries):
        nb_retries = MAX_RETRIES - remaining_retries
        sleep_seconds = min(INITIAL_RETRY_DELAY * pow(2.0, nb_retries), MAX_RETRY_DELAY)
        jitter = 1 - 0.25 * random()
        timeout = sleep_seconds * jitter
        return timeout if timeout >= 0 else 0

    def create_collection(self, collection_name, fields, description=""):
        """
        create a collection.

        :param collection_name: The name of the collection.
        :type collection_name: str
        :param fields: The custom fields of the collection.
        :type fields: list[Field]
        :param description: The description of the collection.
        :type description: str
        :rtype: Collection
        """
        params = {"collection_name": collection_name, "description": description}
        assert isinstance(fields, list)
        primary_key = None
        _fields = []
        for field in fields:
            assert isinstance(field, Field)
            if field.is_primary_key:
                primary_key = field.field_name
            _field = {
                "field_name": field.field_name,
                "field_type": field.field_type.value,
            }
            if field.default_val is not None:
                _field["default_val"] = field.default_val
            if field.dim is not None:
                _field["dim"] = field.dim
            if field.pipeline_name is not None:
                _field["pipeline_name"] = field.pipeline_name
            _fields.append(_field)
        if primary_key:
            params["primary_key"] = primary_key
        else:
            params["primary_key"] = "__AUTO_ID__"
        params["fields"] = _fields
        # print(params)
        self.json_exception("CreateCollection", {}, json.dumps(params))
        return Collection(collection_name, fields, self, primary_key, description=description)

    async def async_create_collection(self, collection_name, fields, description=""):
        params = {"collection_name": collection_name, "description": description}
        assert isinstance(fields, list)
        primary_key = None
        _fields = []
        for field in fields:
            assert isinstance(field, Field)
            if field.is_primary_key:
                primary_key = field.field_name
            _field = {
                "field_name": field.field_name,
                "field_type": field.field_type.value,
            }
            if field.default_val is not None:
                _field["default_val"] = field.default_val
            if field.dim is not None:
                _field["dim"] = field.dim
            if field.pipeline_name is not None:
                _field["pipeline_name"] = field.pipeline_name
            _fields.append(_field)
        if primary_key:
            params["primary_key"] = primary_key
        else:
            params["primary_key"] = "__AUTO_ID__"
        params["fields"] = _fields
        # print(params)
        await self.async_json_exception("CreateCollection", {}, json.dumps(params))
        return Collection(collection_name, fields, self, primary_key, description=description)

    def get_collection(self, collection_name):
        """
        get a collection

        :param collection_name: The name of the collection.
        :type collection_name: str
        :rtype: Collection
        """
        params = {"collection_name": collection_name}
        res = self._retry_request("GetCollection", {}, json.dumps(params))
        res = json.loads(res)
        description = ""
        stat = None
        fields = []
        indexes = []
        create_time = None
        update_time = None
        update_person = None
        # print(res)
        if "fields" in res["data"]:
            # fields 应该是list<Field>，这里是json array
            # print(res["data"]["fields"])
            for item in res["data"]["fields"]:
                field_name = None
                field_type = None
                default_val = None
                dim = None
                is_primary_key = False
                pipeline_name = None
                # print(item)
                if "field_name" in item:
                    field_name = item["field_name"]
                if "field_type" in item:
                    field_type = item["field_type"]
                if "default_val" in item:
                    default_val = item["default_val"]
                if "dim" in item:
                    dim = item["dim"]
                if "primary_key" in res["data"]:
                    if res["data"]["primary_key"] == field_name:
                        is_primary_key = True
                if "pipeline_name" in item:
                    pipeline_name = item["pipeline_name"]
                # print(field_name, field_type, default_val, dim, is_primary_key, pipeline_name)
                field = Field(field_name, field_type, default_val=default_val, dim=dim,
                              is_primary_key=is_primary_key, pipeline_name=pipeline_name)
                fields.append(field)
        if "description" in res["data"]:
            description = res["data"]["description"]
        if "indexes" in res["data"]:
            # print(res["data"]["indexes"]) 返回的是index_name
            for item in res["data"]["indexes"]:
                # print(item)
                index = self.get_index(collection_name, item)
                indexes.append(index)
        if "stat" in res["data"]:
            stat = res["data"]["stat"]
        if "create_time" in res["data"]:
            create_time = res["data"]["create_time"]
        if "update_time" in res["data"]:
            update_time = res["data"]["update_time"]
        if "update_person" in res["data"]:
            update_person = res["data"]["update_person"]
        # print(description, fields, indexes, stat, res["data"]["primary_key"])
        collection = Collection(collection_name, fields, self, res["data"]["primary_key"], indexes=indexes, stat=stat,
                                description=description, create_time=create_time, update_time=update_time,
                                update_person=update_person)
        return collection

    async def async_get_collection(self, collection_name):
        params = {"collection_name": collection_name}
        res = await self.async_get_body_exception("GetCollection", {}, json.dumps(params))
        res = json.loads(res)
        if "data" not in res:
            raise VikingDBException(1000028, "missed", "data format error, please contact us")
        return self.package_collection(collection_name, res["data"])

    def package_collection(self, collection_name, res):
        description = ""
        stat = None
        fields = []
        indexes = []
        create_time = None
        update_time = None
        update_person = None
        if "fields" in res:
            for item in res["fields"]:
                field_name = None
                field_type = None
                default_val = None
                dim = None
                is_primary_key = False
                pipeline_name = None
                # print(item)
                if "field_name" in item:
                    field_name = item["field_name"]
                if "field_type" in item:
                    field_type = item["field_type"]
                if "default_val" in item:
                    default_val = item["default_val"]
                if "dim" in item:
                    dim = item["dim"]
                if "primary_key" in res:
                    if res["primary_key"] == field_name:
                        is_primary_key = True
                if "pipeline_name" in item:
                    pipeline_name = item["pipeline_name"]
                # print(field_name, field_type, default_val, dim, is_primary_key, pipeline_name)
                field = Field(field_name, field_type, default_val=default_val, dim=dim,
                              is_primary_key=is_primary_key, pipeline_name=pipeline_name)
                fields.append(field)
        if "description" in res:
            description = res["description"]
        if "indexes" in res:
            for item in res["indexes"]:
                # print(item)
                index = self.get_index(collection_name, item)
                indexes.append(index)
        if "stat" in res:
            stat = res["stat"]
        if "create_time" in res:
            create_time = res["create_time"]
        if "update_time" in res:
            update_time = res["update_time"]
        if "update_person" in res:
            update_person = res["update_person"]
        # print(description, fields, indexes, stat, res["primary_key"])
        collection = Collection(collection_name, fields, self, res["primary_key"], indexes=indexes, stat=stat,
                                description=description, create_time=create_time, update_time=update_time,
                                update_person=update_person)
        return collection

    def drop_collection(self, collection_name):
        """
        drop a collection

        :param collection_name: The name of the collection.
        :type collection_name: str
        :rtype: None
        """
        params = {"collection_name": collection_name}
        self.json_exception("DropCollection", {}, json.dumps(params))
        # res = self.json("DropCollection", {}, json.dumps(params))

    async def async_drop_collection(self, collection_name):
        params = {"collection_name": collection_name}
        await self.async_json_exception("DropCollection", {}, json.dumps(params))

    def list_collections(self):
        """
        list collections

        :rtype: list[Collection]
        """
        res = self.get_exception("ListCollections", {})
        res = json.loads(res)
        collections = []
        for indexItem in res["data"]:
            # print(indexItem)
            description = None
            collection_name = None
            stat = None
            fields = []
            indexes = []
            create_time = None
            update_time = None
            update_person = None
            # print(res)
            if "fields" in indexItem:
                # print(indexItem)
                for item in indexItem["fields"]:
                    field_name = None
                    field_type = None
                    default_val = None
                    dim = None
                    is_primary_key = False
                    pipeline_name = None
                    # print(item)
                    if "field_name" in item:
                        field_name = item["field_name"]
                    if "field_type" in item:
                        field_type = item["field_type"]
                    if "default_val" in item:
                        default_val = item["default_val"]
                    if "dim" in item:
                        dim = item["dim"]
                    if "primary_key" in indexItem:
                        if indexItem["primary_key"] == field_name:
                            is_primary_key = True
                    if "pipeline_name" in item:
                        pipeline_name = item["pipeline_name"]
                    # print(field_name, field_type, default_val, dim, is_primary_key, pipeline_name)
                    field = Field(field_name, field_type, default_val=default_val, dim=dim,
                                  is_primary_key=is_primary_key, pipeline_name=pipeline_name)
                    fields.append(field)
            if "collection_name" in indexItem:
                collection_name = indexItem["collection_name"]
            if "description" in indexItem:
                description = indexItem["description"]
            if "indexes" in indexItem:
                # print(res["data"]["indexes"]) 返回的是index_name
                for item in indexItem["indexes"]:
                    # print(item)
                    index = self.get_index(collection_name, item)
                    indexes.append(index)
            if "stat" in indexItem:
                stat = indexItem["stat"]
            if "create_time" in indexItem:
                create_time = indexItem["create_time"]
            if "update_time" in indexItem:
                update_time = indexItem["update_time"]
            if "update_person" in indexItem:
                update_person = indexItem["update_person"]
            # print(description, fields, indexes, stat, indexItem["primary_key"], create_time, update_time, update_person)
            collection = Collection(collection_name, fields, self, indexItem["primary_key"], indexes=indexes,
                                    stat=stat,
                                    description=description, create_time=create_time, update_time=update_time,
                                    update_person=update_person)
            collections.append(collection)
        return collections

    async def async_list_collections(self):
        res = await self.async_get_body_exception("ListCollections", {}, json.dumps({}))
        res = json.loads(res)
        collections = []
        if "data" not in res:
            raise VikingDBException(1000028, "missed", "data format error, please contact us")
        for indexItem in res["data"]:
            collection = self.package_collection(indexItem["collection_name"], indexItem)
            collections.append(collection)
        return collections

    def create_index(self, collection_name, index_name, vector_index=None, cpu_quota=2, description="", partition_by="",
                     scalar_index=None, shard_count=None, shard_policy=None):
        """
        create an index.

        :param collection_name: The name of the collection.
        :type collection_name: str
        :param index_name: The name of the index.
        :type index_name: str
        :param vector_index: determine vector index
        :type vector_index: VectorIndexParams or None
        :param cpu_quota: CPU quota
        :type cpu_quota: int
        :param description: The description of the index.
        :type description: str
        :param partition_by: partition_by sub-indexing partition.
        :type partition_by: str
        :param scalar_index: determine index type.
        :type scalar_index: list or None
        :param shard_count: shard count.
        :type shard_count: int
        :rtype: Index
        """
        # print(vector_index.dic())
        params = {
            "collection_name": collection_name,
            "index_name": index_name,
            "cpu_quota": cpu_quota,
            "description": description,
            "partition_by": partition_by,
        }
        if vector_index is not None:
            params["vector_index"] = vector_index.dic()  # vector_index 类型应该是VectorIndexParams，而非json
        if scalar_index is not None:
            params["scalar_index"] = scalar_index
        if shard_count is not None:
            params["shard_count"] = shard_count
        if shard_policy is not None:
            params["shard_policy"] = shard_policy.value
        # print(params)
        res = self.json_exception("CreateIndex", {}, json.dumps(params))
        # print(res)
        index = Index(collection_name, index_name, vector_index, scalar_index, None, self, description=description,
                      cpu_quota=cpu_quota, partition_by=partition_by)
        return index

    async def async_create_index(self, collection_name, index_name, vector_index=None, cpu_quota=2, description="",
                                 partition_by="", scalar_index=None, shard_count=None,  shard_policy=None):
        params = {
            "collection_name": collection_name,
            "index_name": index_name,
            "cpu_quota": cpu_quota,
            "description": description,
            "partition_by": partition_by,
        }
        if vector_index is not None:
            params["vector_index"] = vector_index.dic()  # vector_index 类型应该是VectorIndexParams，而非json
        if scalar_index is not None:
            params["scalar_index"] = scalar_index
        if shard_count is not None:
            params["shard_count"] = shard_count
        if shard_policy is not None:
            params["shard_policy"] = shard_policy.value
        # print(params)
        res = await self.async_json_exception("CreateIndex", {}, json.dumps(params))
        # print(res)
        index = Index(collection_name, index_name, vector_index, scalar_index, None, self, description=description,
                      cpu_quota=cpu_quota, partition_by=partition_by)
        return index

    def get_index(self, collection_name, index_name):
        """
        get an index

        :param collection_name: The name of the collection.
        :type collection_name: str
        :param index_name: The name of the index.
        :type index_name: str
        :rtype: Index
        """
        params = {
            "collection_name": collection_name,
            "index_name": index_name,
        }
        res = self._retry_request("GetIndex", {}, json.dumps(params))
        res = json.loads(res)
        vector_index = scalar_index = partition_by = status = None
        cpu_quota = 2
        description = ""
        shard_count = shard_policy = index_cost = create_time = update_time = update_person = None
        # print(res["data"])
        if "vector_index" in res["data"]:
            vector_index = res["data"]["vector_index"]
        # if "scalar_index" in res["data"]:
        #     scalar_index = res["data"]["scalar_index"]
        if "range_index" in res["data"]:
            scalar_index = res["data"]["range_index"]
        if "enum_index" in res["data"]:
            if scalar_index is not None:
                scalar_index = set(scalar_index + res["data"]["enum_index"])
            else:
                scalar_index = res["data"]["enum_index"]
        if "description" in res["data"]:
            description = res["data"]["description"]
        if "cpu_quota" in res["data"]:
            cpu_quota = res["data"]["cpu_quota"]
        if "partition_by" in res["data"]:
            partition_by = res["data"]["partition_by"]
        if "status" in res["data"]:
            status = res["data"]["status"]
        if "create_time" in res["data"]:
            create_time = res["data"]["create_time"]
        if "update_time" in res["data"]:
            update_time = res["data"]["update_time"]
        if "update_person" in res["data"]:
            update_person = res["data"]["update_person"]
        if "index_cost" in res["data"]:
            index_cost = res["data"]["index_cost"]
        if "shard_count" in res["data"]:
            shard_count = res["data"]["shard_count"]
        if "shard_policy" in res["data"]:
            shard_policy = res["data"]["shard_policy"]
        # print(collection_name, index_name, vector_index, scalar_index, description, cpu_quota, partition_by, status)
        index = Index(collection_name, index_name, vector_index, scalar_index, status, self, description=description,
                      cpu_quota=cpu_quota, partition_by=partition_by, create_time=create_time, update_time=update_time,
                      update_person=update_person, index_cost=index_cost, shard_count=shard_count, shard_policy=shard_policy)
        return index

    async def async_get_index(self, collection_name, index_name):
        params = {
            "collection_name": collection_name,
            "index_name": index_name,
        }
        res = await self.async_get_body_exception("GetIndex", {}, json.dumps(params))
        res = json.loads(res)
        if "data" not in res:
            raise VikingDBException(1000028, "missed", "data format error, please contact us")
        return self.package_index(collection_name, index_name, res["data"])

    def package_index(self, collection_name, index_name, res):
        vector_index = scalar_index = partition_by = status = None
        cpu_quota = 2
        description = ""
        shard_count = shard_policy = index_cost = create_time = update_time = update_person = None
        if "vector_index" in res:
            vector_index = res["vector_index"]
        if "range_index" in res:
            scalar_index = res["range_index"]
        if "enum_index" in res:
            if scalar_index is not None:
                scalar_index = set(scalar_index + res["enum_index"])
            else:
                scalar_index = res["enum_index"]
        if "description" in res:
            description = res["description"]
        if "cpu_quota" in res:
            cpu_quota = res["cpu_quota"]
        if "partition_by" in res:
            partition_by = res["partition_by"]
        if "status" in res:
            status = res["status"]
        if "create_time" in res:
            create_time = res["create_time"]
        if "update_time" in res:
            update_time = res["update_time"]
        if "update_person" in res:
            update_person = res["update_person"]
        if "index_cost" in res:
            index_cost = res["index_cost"]
        if "shard_count" in res:
            shard_count = res["shard_count"]
        if "shard_policy" in res:
            shard_policy = res["shard_policy"]
        # print(collection_name, index_name, vector_index, scalar_index, description, cpu_quota, partition_by, status)
        index = Index(collection_name, index_name, vector_index, scalar_index, status, self, description=description,
                      cpu_quota=cpu_quota, partition_by=partition_by, create_time=create_time, update_time=update_time,
                      update_person=update_person, index_cost=index_cost, shard_count=shard_count, shard_policy=shard_policy)
        return index

    def drop_index(self, collection_name, index_name):
        """
        drop an index

        :param collection_name: The name of the collection.
        :type collection_name: str
        :param index_name: The name of the index.
        :type index_name: str
        :rtype: None
        """
        params = {
            "collection_name": collection_name,
            "index_name": index_name,
        }
        # res = self.json("DropIndex", {}, json.dumps(params))
        self.json_exception("DropIndex", {}, json.dumps(params))

    async def async_drop_index(self, collection_name, index_name):
        params = {
            "collection_name": collection_name,
            "index_name": index_name,
        }
        await self.async_json_exception("DropIndex", {}, json.dumps(params))

    def list_indexes(self, collection_name):
        """
        list indexes

        :rtype: list[Index]
        """
        params = {
            "collection_name": collection_name,
        }
        # res = self.get("ListIndexes", params)
        res = self.get_exception("ListIndexes", params)
        res = json.loads(res)
        indexes = []
        for item in res["data"]:
            # print(item)
            vector_index = scalar_index = partition_by = status = None
            cpu_quota = 2
            description = index_name = ""
            shard_count = shard_policy = index_cost = create_time = update_time = update_person = None
            if "index_name" in item:
                index_name = item["index_name"]
            if "vector_index" in item:
                vector_index = item["vector_index"]
            # if "scalar_index" in item:
            #     scalar_index = item["scalar_index"]
            if "range_index" in item:
                scalar_index = item["range_index"]
            if "enum_index" in item:
                if scalar_index is not None:
                    scalar_index = set(scalar_index + item["enum_index"])
                else:
                    scalar_index = item["enum_index"]
            if "description" in item:
                description = item["description"]
            if "cpu_quota" in item:
                cpu_quota = item["cpu_quota"]
            if "partition_by" in item:
                partition_by = item["partition_by"]
            if "status" in item:
                status = item["status"]
            if "create_time" in item:
                create_time = item["create_time"]
            if "update_time" in item:
                update_time = item["update_time"]
            if "update_person" in item:
                update_person = item["update_person"]
            if "index_cost" in item:
                index_cost = item["index_cost"]
            if "shard_count" in item:
                shard_count = item["shard_count"]
            if "shard_policy" in item:
                shard_policy = item["shard_policy"]
            # print(collection_name, index_name, vector_index, scalar_index, description, cpu_quota, partition_by, status)
            index = Index(collection_name, index_name, vector_index, scalar_index, status, self,
                          description=description,
                          cpu_quota=cpu_quota, partition_by=partition_by, create_time=create_time,
                          update_time=update_time, update_person=update_person, index_cost=index_cost,
                          shard_count=shard_count, shard_policy=shard_policy)
            indexes.append(index)
        # print(indexes)
        return indexes

    async def async_list_indexes(self, collection_name):
        params = {
            "collection_name": collection_name,
        }
        # res = self.get("ListIndexes", params)
        res = await self.async_get_body_exception("ListIndexes", {}, json.dumps(params))
        res = json.loads(res)
        indexes = []
        if "data" not in res:
            raise VikingDBException(1000028, "missed", "data format error, please contact us")
        for item in res["data"]:
            index = self.package_index(collection_name, item["index_name"], item)
            indexes.append(index)
        # print(indexes)
        return indexes

    def embedding(self, emb_model, raw_data: Union[RawData, List[RawData]]):
        """
        request embedding service to extract features from text, images, etc.

        :param emb_model: The name of the collection.
        :type emb_model: EmbModel
        :param raw_data: The name of the collection.
        :type raw_data: RawData or list[RawData]
        :rtype: list or list[list]
        """
        model = {"model_name": emb_model.model_name, "params": emb_model.params}
        data = []
        if isinstance(raw_data, RawData):
            param = {"data_type": raw_data.data_type, "text": raw_data.text}
            data.append(param)
        elif isinstance(raw_data, List):
            for item in raw_data:
                param = {"data_type": item.data_type, "text": item.text}
                data.append(param)
        params = {"model": model, "data": data}
        res = self.json_exception("Embedding", {}, json.dumps(params))
        res = json.loads(res)
        # print(res["data"])
        if isinstance(raw_data, RawData):
            # print(res["data"][0])
            return res["data"][0]
        else:
            # for item in res["data"]:
            #     print("=====")
            # print(res["data"])
            return res["data"]

    async def async_embedding(self, emb_model, raw_data: Union[RawData, List[RawData]]):
        model = {"model_name": emb_model.model_name, "params": emb_model.params}
        data = []
        if isinstance(raw_data, RawData):
            param = {"data_type": raw_data.data_type, "text": raw_data.text}
            data.append(param)
        elif isinstance(raw_data, List):
            for item in raw_data:
                param = {"data_type": item.data_type, "text": item.text}
                data.append(param)
        params = {"model": model, "data": data}
        res = await self.async_json_exception("Embedding", {}, json.dumps(params))
        res = json.loads(res)
        # print(res["data"])
        if isinstance(raw_data, RawData):
            # print(res["data"][0])
            return res["data"][0]
        else:
            return res["data"]

    def update_collection(self, collection_name, fields, description=None):
        _fields = []
        for field in fields:
            assert isinstance(field, Field)
            _field = {
                "field_name": field.field_name,
                "field_type": field.field_type.value,
            }
            if field.default_val is not None:
                _field["default_val"] = field.default_val
            if field.dim is not None:
                _field["dim"] = field.dim
            if field.pipeline_name is not None:
                _field["pipeline_name"] = field.pipeline_name
            _fields.append(_field)
        params = {
            "collection_name": collection_name,
            "fields": _fields
        }
        if description != None:
            params["description"] = description
        # print(params)
        res = self.json_exception("UpdateCollection", {}, json.dumps(params))

    async def async_update_collection(self, collection_name, fields, description=None):
        _fields = []
        for field in fields:
            assert isinstance(field, Field)
            _field = {
                "field_name": field.field_name,
                "field_type": field.field_type.value,
            }
            if field.default_val is not None:
                _field["default_val"] = field.default_val
            if field.dim is not None:
                _field["dim"] = field.dim
            if field.pipeline_name is not None:
                _field["pipeline_name"] = field.pipeline_name
            _fields.append(_field)
        params = {
            "collection_name": collection_name,
            "fields": _fields
        }
        if description != None:
            params["description"] = description
        # print(params)
        res = await self.async_json_exception("UpdateCollection", {}, json.dumps(params))

    def update_index(self, collection_name, index_name, description=None, cpu_quota=None, scalar_index=None,
                     shard_count=None):
        params = {
            "collection_name": collection_name,
            "index_name": index_name,
        }
        if description is not None:
            params["description"] = description
        if cpu_quota is not None:
            params["cpu_quota"] = cpu_quota
        if scalar_index is not None:
            params["scalar_index"] = scalar_index
        if shard_count is not None:
            params["shard_count"] = shard_count
        res = self.json_exception("UpdateIndex", {}, json.dumps(params))

    async def async_update_index(self, collection_name, index_name, description=None, cpu_quota=None, scalar_index=None,
                                 shard_count=None):
        params = {
            "collection_name": collection_name,
            "index_name": index_name,
        }
        if description is not None:
            params["description"] = description
        if cpu_quota is not None:
            params["cpu_quota"] = cpu_quota
        if scalar_index is not None:
            params["scalar_index"] = scalar_index
        if shard_count is not None:
            params["shard_count"] = shard_count
        res = await self.async_json_exception("UpdateIndex", {}, json.dumps(params))

    def list_embeddings(self, model_name=""):
        params = {"model_name": model_name}
        res = self.get_body_exception("ListEmbeddings", {}, json.dumps(params))
        print(res)
        pass

    def rerank(self, query, content, title=""):
        params = {
            "query": query,
            "content": content,
            "title": title
        }
        res = self.json_exception("Rerank", {}, json.dumps(params))
        res = json.loads(res)
        return res["data"]

    async def async_rerank(self, query, content, title=""):
        params = {
            "query": query,
            "content": content,
            "title": title
        }
        res = await self.async_json_exception("Rerank", {}, json.dumps(params))
        res = json.loads(res)
        return res["data"]

    def batch_rerank(self, datas):
        params = {
            "datas": datas,
        }
        res = self.json_exception("BatchRerank", {}, json.dumps(params))
        res = json.loads(res)
        return res["data"]

    async def async_batch_rerank(self, datas):
        params = {
            "datas": datas,
        }
        res = await self.async_json_exception("BatchRerank", {}, json.dumps(params))
        res = json.loads(res)
        return res["data"]

    def embedding_v2(self, emb_model, raw_data: Union[RawData, List[RawData]]):
        """
        request embedding service to extract features from text, images, etc.

        :param emb_model: The name of the collection.
        :type emb_model: EmbModel
        :param raw_data: The name of the collection.
        :type raw_data: RawData or list[RawData]
        :rtype: list or list[list]
        """
        model = {"model_name": emb_model.model_name, "params": emb_model.params}
        data = []
        if isinstance(raw_data, RawData):
            param = {"data_type": raw_data.data_type}
            if raw_data.text != "":
                param["text"] = raw_data.text
            if raw_data.image != "":
                param["image"] = raw_data.image
            data.append(param)
        elif isinstance(raw_data, List):
            for item in raw_data:
                param = {"data_type": item.data_type}
                if item.text != "":
                    param["text"] = item.text
                if item.image != "":
                    param["image"] = item.image
                data.append(param)
        params = {"model": model, "data": data}
        res = self.json_exception("EmbeddingV2", {}, json.dumps(params))
        res = json.loads(res)
        # print(res["data"])

        return res["data"]

    async def async_embedding_v2(self, emb_model, raw_data: Union[RawData, List[RawData]]):
        model = {"model_name": emb_model.model_name, "params": emb_model.params}
        data = []
        if isinstance(raw_data, RawData):
            param = {"data_type": raw_data.data_type}
            if raw_data.text != "":
                param["text"] = raw_data.text
            if raw_data.image != "":
                param["image"] = raw_data.image
            data.append(param)
        elif isinstance(raw_data, List):
            for item in raw_data:
                param = {"data_type": item.data_type}
                if item.text != "":
                    param["text"] = item.text
                if item.image != "":
                    param["image"] = item.image
                data.append(param)
        params = {"model": model, "data": data}
        res = await self.async_json_exception("EmbeddingV2", {}, json.dumps(params))
        res = json.loads(res)
        # print(res["data"])

        return res["data"]
    
    def package_task(self, res_data):
        collection_name = ""
        create_time = ""
        process_info = None
        task_id = ""
        task_params = None
        task_status = ""
        task_type = ""
        update_person = ""
        update_time = ""
        if "collection_name" in res_data:
            collection_name = res_data["collection_name"]
        if "create_time" in res_data:
            create_time = res_data["create_time"]
        if "process_info" in res_data:
            process_info = res_data["process_info"]
        if "task_id" in res_data:
            task_id = res_data["task_id"]
        if "task_params" in res_data:
            task_params = res_data["task_params"]
        if "task_status" in res_data:
            task_status = res_data["task_status"]
        if "task_type" in res_data:
            task_type = res_data["task_type"]
        if "update_person" in res_data:
            update_person = res_data["update_person"]
        if "update_time" in res_data:
            update_time = res_data["update_time"]
        # print(collection_name, create_time, process_info, task_id, task_params, task_status, task_type, update_person, update_time)
        return Task(collection_name, create_time, process_info, task_id, task_params, task_status, task_type, update_person, update_time)

    
    def create_task(self, task_type, task_params):
        params = {"task_type": task_type.value, "task_params": task_params}
        res = self.json_exception("CreateTask", {}, json.dumps(params))
        res = json.loads(res)
        if "data" in res:
            if "task_id" in res["data"]:
                return res["data"]["task_id"]
        return ""
    
    def get_task(self, task_id):
        params = {"task_id": task_id}
        res = self.json_exception("GetTask", {}, json.dumps(params))
        res = json.loads(res)
        if "data" in res:
            return self.package_task(res["data"])
        else: 
            return None
    
    def list_tasks(self):
        res = self.json_exception("ListTask", {}, json.dumps({}))
        res = json.loads(res)
        tasks = []
        if "data" in res:
            for item in res["data"]:
                tasks.append(self.package_task(item))
        return tasks
    
    def drop_task(self, task_id):
        params = {"task_id": task_id}
        res = self.json_exception("DropTask", {}, json.dumps(params))
