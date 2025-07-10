# coding:utf-8
from .Task import Task
import json
import threading

from .Index import Index
from .common import *
from .Collection import Collection
from .ServiceBase import VikingDBServiceBase
from .exception import ERRCODE_EXCEPTION, VikingDBException
from typing import Union, List


class VikingDBService(VikingDBServiceBase):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(VikingDBService, "_instance"):
            with VikingDBService._instance_lock:
                if not hasattr(VikingDBService, "_instance"):
                    VikingDBService._instance = object.__new__(cls)
        return VikingDBService._instance

    def __init__(self, host="api-vikingdb.volces.com", region="cn-north-1", ak="", sk="", scheme='http',
                 connection_timeout=30, socket_timeout=30, proxy=None, retry_option=None):
        """
        :param retry_option: retry option.
        :type retry_option: RetryOption
        """
        super(VikingDBService, self).__init__(
            host, region, ak, sk, scheme, connection_timeout, socket_timeout, proxy, retry_option)

    def create_collection(self, collection_name, fields, description="", vectorize=None, project="default"):
        """
        create a collection.

        :param collection_name: The name of the collection.
        :type collection_name: str
        :param fields: The custom fields of the collection.
        :type fields: list[Field]
        :param description: The description of the collection.
        :type description: str
        :param vectorize: vectorize for multi-modal data.
        :type vectorize: list[VectorizeTuple]
        :param project: The name of the project.
        :type project: str
        :rtype: Collection
        """
        params = {"collection_name": collection_name, "description": description, "project": project}
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
        if vectorize is not None:
            assert isinstance(vectorize, list) and all(isinstance(item, VectorizeTuple) for item in vectorize)
            params["vectorize"] = [convert_vectorize_tuple_to_dict(v) for v in vectorize]
        self.json_exception("CreateCollection", {}, json.dumps(params))
        return Collection(collection_name, fields, self, primary_key, description=description, retry_option=self.retry_option, vectorize=vectorize)

    async def async_create_collection(self, collection_name, fields, description="", vectorize=None):
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
        if vectorize is not None:
            assert isinstance(vectorize, list) and all(isinstance(item, VectorizeTuple) for item in vectorize)
            params["vectorize"] = [convert_vectorize_tuple_to_dict(v) for v in vectorize]
        await self.async_json_exception("CreateCollection", {}, json.dumps(params))
        return Collection(collection_name, fields, self, primary_key, description=description, retry_option=self.retry_option, vectorize=vectorize)

    def get_collection(self, collection_name, retry=True):
        """
        get a collection

        :param collection_name: The name of the collection.
        :type collection_name: str
        :rtype: Collection
        :param retry: Whether to retry when QuotaLimiterException occurs.
        :type retry: bool
        """
        params = {"collection_name": collection_name}
        remaining = self.retry_option.new_remaining(retry)
        res = self._retry_request("GetCollection", {}, json.dumps(params), remaining, self.retry_option)
        res = json.loads(res)
        description = ""
        stat = None
        fields = []
        indexes = []
        create_time = None
        update_time = None
        update_person = None
        vectorize = None
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
        if "vectorize" in res["data"]:
            vectorize_dict_list = res["data"]["vectorize"]
            vectorize = [convert_dict_to_vectorize_tuple(v_dict) for v_dict in vectorize_dict_list]
        collection = Collection(collection_name, fields, self, res["data"]["primary_key"], indexes=indexes, stat=stat,
                                description=description, create_time=create_time, update_time=update_time,
                                update_person=update_person, retry_option=self.retry_option, vectorize=vectorize)
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
        vectorize = None
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
        if "vectorize" in res:
            vectorize_dict_list = res["vectorize"]
            vectorize = [convert_dict_to_vectorize_tuple(v_dict) for v_dict in vectorize_dict_list]
        # print(description, fields, indexes, stat, res["primary_key"])
        collection = Collection(collection_name, fields, self, res["primary_key"], indexes=indexes, stat=stat,
                                description=description, create_time=create_time, update_time=update_time,
                                update_person=update_person, retry_option=self.retry_option, vectorize=vectorize)
        return collection

    def drop_collection(self, collection_name, retry=True):
        """
        drop a collection

        :param collection_name: The name of the collection.
        :type collection_name: str
        :rtype: None
        :param retry: Whether to retry when QuotaLimiterException occurs.
        :type retry: bool
        """
        remaining = self.retry_option.new_remaining(retry)
        params = {"collection_name": collection_name}
        self._retry_request("DropCollection", {}, json.dumps(params), remaining, self.retry_option)
        # res = self.json("DropCollection", {}, json.dumps(params))

    async def async_drop_collection(self, collection_name):
        params = {"collection_name": collection_name}
        await self.async_json_exception("DropCollection", {}, json.dumps(params))

    def list_collections(self, project=""):
        """
        list collections

        :param project: The name of the project.
        :type project: str
        :rtype: list[Collection]
        """
        params = {
            "project": project
        }
        res = self.get_body_exception("ListCollections", {}, json.dumps(params))
        res = json.loads(res)
        collections = []
        for indexItem in res["data"]:
            description = None
            collection_name = None
            stat = None
            fields = []
            indexes = []
            create_time = None
            update_time = None
            update_person = None
            vectorize = None
            if "fields" in indexItem:
                for item in indexItem["fields"]:
                    field_name = None
                    field_type = None
                    default_val = None
                    dim = None
                    is_primary_key = False
                    pipeline_name = None
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
            if "vectorize" in indexItem:
                vectorize_dict_list = indexItem["vectorize"]
                vectorize = [convert_dict_to_vectorize_tuple(v_dict) for v_dict in vectorize_dict_list]
            # print(description, fields, indexes, stat, indexItem["primary_key"], create_time, update_time, update_person)
            collection = Collection(collection_name, fields, self, indexItem["primary_key"], indexes=indexes,
                                    stat=stat,
                                    description=description, create_time=create_time, update_time=update_time,
                                    update_person=update_person, retry_option=self.retry_option, vectorize=vectorize)
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
                      cpu_quota=cpu_quota, partition_by=partition_by, retry_option=self.retry_option)
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
                      cpu_quota=cpu_quota, partition_by=partition_by, retry_option=self.retry_option)
        return index

    def get_index(self, collection_name, index_name, retry=True):
        """
        get an index

        :param collection_name: The name of the collection.
        :type collection_name: str
        :param index_name: The name of the index.
        :type index_name: str
        :rtype: Index
        :param retry: Whether to retry when QuotaLimiterException occurs.
        :type retry: bool
        """
        params = {
            "collection_name": collection_name,
            "index_name": index_name,
        }
        remaining = self.retry_option.new_remaining(retry)
        res = self._retry_request("GetIndex", {}, json.dumps(params), remaining, self.retry_option)
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
                      update_person=update_person, index_cost=index_cost, shard_count=shard_count, shard_policy=shard_policy,
                      retry_option=self.retry_option)
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
                      update_person=update_person, index_cost=index_cost, shard_count=shard_count, shard_policy=shard_policy,
                      retry_option=self.retry_option)
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
                          shard_count=shard_count, shard_policy=shard_policy, retry_option=self.retry_option)
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

    def embedding(self, emb_model, raw_data: Union[RawData, List[RawData]], retry=True):
        """
        request embedding service to extract features from text, images, etc.

        :param emb_model: The name of the collection.
        :type emb_model: EmbModel
        :param raw_data: The name of the collection.
        :type raw_data: RawData or list[RawData]
        :rtype: list or list[list]
        :param retry: Whether to retry when QuotaLimiterException occurs.
        :type retry: bool
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
        remaining = self.retry_option.new_remaining(retry)
        res = self._retry_request("Embedding", {}, json.dumps(params), remaining, self.retry_option)
        res = json.loads(res)
        # print(res["data"])
        if isinstance(raw_data, RawData):
            return res["data"][0]
        else:
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

    def embedding_v2(self, emb_model, raw_data: Union[RawData, List[RawData]], retry=True):
        """
        request embedding service to extract features from text, images, etc.

        :param emb_model: The name of the collection.
        :type emb_model: EmbModel
        :param raw_data: The name of the collection.
        :type raw_data: RawData or list[RawData]
        :rtype: list or list[list]
        :param retry: Whether to retry when QuotaLimiterException occurs.
        :type retry: bool
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
        remaining = self.retry_option.new_remaining(retry)
        res = self._retry_request("EmbeddingV2", {}, json.dumps(params), remaining, self.retry_option)
        res = json.loads(res)
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

    def update_task(self, task_id, task_status):
        params = {
            "task_id": task_id,
            "task_status": task_status.value
        }
        res = self.json_exception("UpdateTask", {}, json.dumps(params))
