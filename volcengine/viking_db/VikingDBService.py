# coding:utf-8
import json
import threading

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

    def __init__(self, host="api-vikingdb.volces.com", region="cn-north-1", ak="", sk="", scheme='http'):
        self.service_info = VikingDBService.get_service_info(host, region, scheme)
        self.api_info = VikingDBService.get_api_info()
        super(VikingDBService, self).__init__(self.service_info, self.api_info)
        if ak:
            self.set_ak(ak)
        if sk:
            self.set_sk(sk)

    @staticmethod
    def get_service_info(host, region, scheme):
        service_info = ServiceInfo(host, {"Host": host},
                                   Credentials('', '', 'air', region), 5, 5, scheme=scheme)
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
                raise VikingDBException(1000028, "missed", "json load res error, res:{}".format(str(e)))
            code = res_json.get("code", 1000028)
            request_id = res_json.get("request_id", 1000028)
            message = res_json.get("message", None)
            raise ERRCODE_EXCEPTION.get(code, VikingDBException)(code, request_id, message)
        if res == '':
            raise VikingDBException(1000028, "missed",
                                    "empty response due to unknown error, please contact customer service")
        return res

    # get参数放在url里面，异常处理
    def get_exception(self, api, params):
        # res = self.get(api, params)
        # if res == '':
        #     raise VikingDBException(1000028, "missed",
        #                             "empty response due to unknown error, please contact customer service")
        # return res
        try:
            res = self.get(api, params)
        except Exception as e:
            try:
                res_json = json.loads(e.args[0].decode("utf-8"))
            except:
                raise VikingDBException(1000028, "missed", "json load res error, res:{}".format(str(e)))
            code = res_json.get("code", 1000028)
            request_id = res_json.get("request_id", 1000028)
            message = res_json.get("message", None)
            raise ERRCODE_EXCEPTION.get(code, VikingDBException)(code, request_id, message)
        if res == '':
            raise VikingDBException(1000028, "missed",
                                    "empty response due to unknown error, please contact customer service")
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
                raise VikingDBException(1000028, "missed", "json load res error, res:{}".format(str(e)))
            code = res_json.get("code", 1000028)
            request_id = res_json.get("request_id", 1000028)
            message = res_json.get("message", None)
            raise ERRCODE_EXCEPTION.get(code, VikingDBException)(code, request_id, message)
        if res == '':
            raise VikingDBException(1000028, "missed",
                                    "empty response due to unknown error, please contact customer service")
        return res

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
        assert primary_key is not None
        params["primary_key"] = primary_key
        params["fields"] = _fields
        # print(params)
        self.json_exception("CreateCollection", {}, json.dumps(params))
        return Collection(collection_name, fields, self, primary_key, description=description)

    def get_collection(self, collection_name):
        """
        get a collection

        :param collection_name: The name of the collection.
        :type collection_name: str
        :rtype: Collection
        """
        params = {"collection_name": collection_name}
        # params不用解析成json格式，否则后续代码无法识别
        res = self.get_exception("GetCollection", params)
        # 转换为字典形式
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
                                description=description, create_time=create_time, update_time=update_time, update_person=update_person)
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

    def list_collections(self):
        """
        list collections

        :rtype: list[Collection]
        """
        res = self.get_exception("ListCollections", {})
        res = json.loads(res)
        collections = []
        for item in res["data"]:
            # print(item)
            collection = self.get_collection(item["collection_name"])
            # print(collection)
            collections.append(collection)
        return collections

    def create_index(self, collection_name, index_name, vector_index=None, cpu_quota=2, description="", partition_by="",
                     scalar_index=None):
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
        # print(params)
        res = self.json_exception("CreateIndex", {}, json.dumps(params))
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
        res = self.get_exception("GetIndex", params)
        res = json.loads(res)
        vector_index = scalar_index = partition_by = status = None
        cpu_quota = 2
        description = ""
        shard_count = index_cost = create_time = update_time = update_person = None
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
        # print(collection_name, index_name, vector_index, scalar_index, description, cpu_quota, partition_by, status)
        index = Index(collection_name, index_name, vector_index, scalar_index, status, self, description=description,
                      cpu_quota=cpu_quota, partition_by=partition_by, create_time=create_time, update_time=update_time,
                      update_person=update_person, index_cost=index_cost, shard_count=shard_count)
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
            shard_count = index_cost = create_time = update_time = update_person = None
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
            # print(collection_name, index_name, vector_index, scalar_index, description, cpu_quota, partition_by, status)
            index = Index(collection_name, index_name, vector_index, scalar_index, status, self,
                          description=description,
                          cpu_quota=cpu_quota, partition_by=partition_by, create_time=create_time,
                          update_time=update_time, update_person=update_person, index_cost=index_cost,
                          shard_count=shard_count)
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

    def list_embeddings(self, model_name=""):
        params = {"model_name": model_name}
        res = self.get_body_exception("ListEmbeddings", {}, json.dumps(params))
        print(res)
        pass
