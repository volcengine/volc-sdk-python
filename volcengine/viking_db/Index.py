# coding:utf-8
import json
from typing import Union, List

from volcengine.viking_db.common import Data, VectorOrder, ScalarOrder


class Index(object):
    def __init__(self, collection_name, index_name, vector_index, scalar_index, stat, viking_db_service, description="",
                 cpu_quota=2, partition_by=None, create_time=None, update_time=None, update_person=None,
                 index_cost=None, shard_count=None):
        self.collection_name = collection_name
        self.index_name = index_name
        self.description = description
        self.vector_index = vector_index
        self.scalar_index = scalar_index
        self.stat = stat
        self.viking_db_service = viking_db_service
        self.cpu_quota = cpu_quota
        self.partition_by = partition_by
        self.create_time = create_time
        self.update_time = update_time
        self.update_person = update_person
        self.index_cost = index_cost
        self.shard_count = shard_count
        # 获取primary_key
        col = self.viking_db_service.get_exception("GetCollection", {"collection_name": self.collection_name})
        col = json.loads(col)
        # print(col["data"]["primary_key"])
        self.primary_key = col["data"]["primary_key"]

    def search(self, order=None, filter=None, limit=10, output_fields=None, partition="default", dense_weight=None):
        """
        Search for vectors or scalars similar to a given vector or scalar.

        :param order: the given vector or scalar or None.
        :type order: VectorOrder or ScalarOrder or None
        :param filter: filter conditions.
        :type filter: dict
        :param limit: number of retrieved results.
        :type limit: int
        :param output_fields: specify the list of scalar fields to be returned.
        :type output_fields: list
        :param partition: the name of sub-index.
        :type partition: int or str or list[int] or list[str]
        :rtype: list
        """
        if isinstance(order, VectorOrder):
            res = []
            if order.vector is not None:
                res = self.search_by_vector(order.vector, sparse_vectors=order.sparse_vectors, filter=filter,
                                            limit=limit,
                                            output_fields=output_fields, partition=partition, dense_weight=dense_weight)
            elif order.id is not None:
                res = self.search_by_id(order.id, filter=filter, limit=limit,
                                        output_fields=output_fields, partition=partition, dense_weight=dense_weight)
            return res
        elif isinstance(order, ScalarOrder):
            search = {}
            order_by_scalar = {"order": order.order.value, "field_name": order.field_name}
            search = {"order_by_scalar": order_by_scalar, "limit": limit, "partition": partition}
            if output_fields is not None:
                search["output_fields"] = output_fields
            if filter is not None:
                search['filter'] = filter
            params = {"collection_name": self.collection_name, "index_name": self.index_name, "search": search}
            # print(params)
            res = self.viking_db_service.json_exception("SearchIndex", {}, json.dumps(params))
            res = json.loads(res)
            # print(res["data"])

            datas = []
            # 返回数据是个列表，每个id又对应一个列表，但是这里输入id好像只能传一个值，所以要for两次
            for items in res["data"]:
                for item in items:
                    # print(item)
                    id = item[self.primary_key]
                    fields = {}
                    if output_fields != [] or output_fields is None:
                        fields = item["fields"]
                    # print(id, fields)
                    data = Data(fields, id=id, timestamp=None, score=item["score"], dist=item.get('dist', None))
                    datas.append(data)
                # print("==================")
            return datas
        elif order is None:
            search = {"limit": limit, "partition": partition}
            if output_fields is not None:
                search["output_fields"] = output_fields
            if filter is not None:
                search['filter'] = filter
            params = {"collection_name": self.collection_name, "index_name": self.index_name, "search": search}
            res = self.viking_db_service.json_exception("SearchIndex", {}, json.dumps(params))
            res = json.loads(res)

            datas = []
            # print(res)
            for items in res["data"]:
                for item in items:
                    id = item[self.primary_key]
                    fields = {}
                    if output_fields != [] or output_fields is None:
                        fields = item["fields"]
                    data = Data(fields, id=id, timestamp=None, score=item["score"], dist=item.get('dist', None))
                    datas.append(data)
                # print("==================")
            return datas

    async def async_search(self, order=None, filter=None, limit=10, output_fields=None, partition="default",
                           dense_weight=None):
        if isinstance(order, VectorOrder):
            res = []
            if order.vector is not None:
                res = await self.async_search_by_vector(order.vector, sparse_vectors=order.sparse_vectors,
                                                        filter=filter,
                                                        limit=limit,
                                                        output_fields=output_fields, partition=partition,
                                                        dense_weight=dense_weight)
            elif order.id is not None:
                res = await self.async_search_by_id(order.id, filter=filter, limit=limit,
                                                    output_fields=output_fields, partition=partition,
                                                    dense_weight=dense_weight)
            return res
        elif isinstance(order, ScalarOrder):
            search = {}
            order_by_scalar = {"order": order.order.value, "field_name": order.field_name}
            search = {"order_by_scalar": order_by_scalar, "limit": limit, "partition": partition}
            if output_fields is not None:
                search["output_fields"] = output_fields
            if filter is not None:
                search['filter'] = filter
            params = {"collection_name": self.collection_name, "index_name": self.index_name, "search": search}
            # print(params)
            res = await self.viking_db_service.async_json_exception("SearchIndex", {}, json.dumps(params))
            res = json.loads(res)
            # print(res["data"])

            datas = []
            # 返回数据是个列表，每个id又对应一个列表，但是这里输入id好像只能传一个值，所以要for两次
            for items in res["data"]:
                for item in items:
                    # print(item)
                    id = item[self.primary_key]
                    fields = {}
                    if output_fields != [] or output_fields is None:
                        fields = item["fields"]
                    # print(id, fields)
                    data = Data(fields, id=id, timestamp=None, score=item["score"], dist=item.get('dist', None))
                    datas.append(data)
                # print("==================")
            return datas
        elif order is None:
            search = {"limit": limit, "partition": partition}
            if output_fields is not None:
                search["output_fields"] = output_fields
            if filter is not None:
                search['filter'] = filter
            params = {"collection_name": self.collection_name, "index_name": self.index_name, "search": search}
            res = await self.viking_db_service.async_json_exception("SearchIndex", {}, json.dumps(params))
            res = json.loads(res)

            datas = []
            # print(res)
            for items in res["data"]:
                for item in items:
                    id = item[self.primary_key]
                    fields = {}
                    if output_fields != [] or output_fields is None:
                        fields = item["fields"]
                    data = Data(fields, id=id, timestamp=None, score=item["score"], dist=item.get('dist', None))
                    datas.append(data)
                # print("==================")
            return datas

    def search_by_id(self, id, filter=None, limit=10, output_fields=None, partition="default", dense_weight=None):
        """
        Search for vectors similar to a given vector based on its id.

        :param id: the primary key.
        :type id: str
        :param filter: filter conditions.
        :type filter: dict
        :param limit: number of retrieved results.
        :type limit: int
        :param output_fields: specify the list of scalar fields to be returned.
        :type output_fields: list
        :param partition: the name of sub-index.
        :type partition: int or str or list[int] or list[str]
        :rtype: list
        """
        search = {}
        order_by_id = {"primary_keys": id}
        search = {"order_by_vector": order_by_id, "limit": limit, "partition": partition}
        if output_fields is not None:
            search["output_fields"] = output_fields
        if filter is not None:
            search['filter'] = filter
        if dense_weight is not None:
            search['dense_weight'] = dense_weight
        params = {"collection_name": self.collection_name, "index_name": self.index_name, "search": search}
        # print(params)
        res = self.viking_db_service.json_exception("SearchIndex", {}, json.dumps(params))
        res = json.loads(res)
        # print(res["data"])

        datas = []
        # 返回数据是个列表，每个id又对应一个列表，但是这里输入id好像只能传一个值，所以要for两次
        for items in res["data"]:
            for item in items:
                # print(item)
                id = item[self.primary_key]
                # print(id)
                fields = {}
                if output_fields != [] or output_fields is None:
                    fields = item["fields"]
                # print(id, fields)
                data = Data(fields, id=id, timestamp=None, score=item["score"], dist=item.get('dist', None))
                datas.append(data)
            # print("==================")
        return datas

    async def async_search_by_id(self, id, filter=None, limit=10, output_fields=None, partition="default",
                                 dense_weight=None):
        search = {}
        order_by_id = {"primary_keys": id}
        search = {"order_by_vector": order_by_id, "limit": limit, "partition": partition}
        if output_fields is not None:
            search["output_fields"] = output_fields
        if filter is not None:
            search['filter'] = filter
        if dense_weight is not None:
            search['dense_weight'] = dense_weight
        params = {"collection_name": self.collection_name, "index_name": self.index_name, "search": search}
        # print(params)
        res = await self.viking_db_service.async_json_exception("SearchIndex", {}, json.dumps(params))
        res = json.loads(res)
        # print(res["data"])

        datas = []
        # 返回数据是个列表，每个id又对应一个列表，但是这里输入id好像只能传一个值，所以要for两次
        for items in res["data"]:
            for item in items:
                # print(item)
                id = item[self.primary_key]
                # print(id)
                fields = {}
                if output_fields != [] or output_fields is None:
                    fields = item["fields"]
                # print(id, fields)
                data = Data(fields, id=id, timestamp=None, score=item["score"], dist=item.get('dist', None))
                datas.append(data)
            # print("==================")
        return datas

    def search_by_vector(self, vector, sparse_vectors=None, filter=None, limit=10, output_fields=None,
                         partition="default", dense_weight=None):
        """
        Search for vectors similar to a given vector.

        :param vector: the given vector.
        :type vector: list
        :param filter: filter conditions.
        :type filter: dict
        :param limit: number of retrieved results.
        :type limit: int
        :param output_fields: specify the list of scalar fields to be returned.
        :type output_fields: list
        :param partition: the name of sub-index.
        :type partition: int or str or list[int] or list[str]
        :rtype: list
        """
        # vector是一个向量，不是list，但是数据库要求传入的是个列表
        search = {}
        order_by_vector = {"vectors": [vector]}
        if sparse_vectors is not None:
            order_by_vector['sparse_vectors'] = [sparse_vectors]
        search = {"order_by_vector": order_by_vector, "limit": limit, "partition": partition}
        if output_fields is not None:
            search["output_fields"] = output_fields
        if filter is not None:
            search['filter'] = filter
        if dense_weight is not None:
            search['dense_weight'] = dense_weight
        params = {"collection_name": self.collection_name, "index_name": self.index_name, "search": search}
        # print(params)
        res = self.viking_db_service.json_exception("SearchIndex", {}, json.dumps(params))
        res = json.loads(res)
        # print(res["data"])

        datas = []
        # 返回数据是个列表，每个vector又对应一个列表，但是这里输入vector好像只能传一个值，所以要for两次
        for items in res["data"]:
            for item in items:
                # print(item)
                id = item[self.primary_key]
                fields = {}
                if output_fields != [] or output_fields is None:
                    fields = item["fields"]
                # print(id, fields)
                data = Data(fields, id=id, timestamp=None, score=item["score"], dist=item.get('dist', None))
                datas.append(data)
            # print("==================")
        return datas

    async def async_search_by_vector(self, vector, sparse_vectors=None, filter=None, limit=10, output_fields=None,
                                     partition="default", dense_weight=None):
        # vector是一个向量，不是list，但是数据库要求传入的是个列表
        search = {}
        order_by_vector = {"vectors": [vector]}
        if sparse_vectors is not None:
            order_by_vector['sparse_vectors'] = [sparse_vectors]
        search = {"order_by_vector": order_by_vector, "limit": limit, "partition": partition}
        if output_fields is not None:
            search["output_fields"] = output_fields
        if filter is not None:
            search['filter'] = filter
        if dense_weight is not None:
            search['dense_weight'] = dense_weight
        params = {"collection_name": self.collection_name, "index_name": self.index_name, "search": search}
        # print(params)
        res = await self.viking_db_service.async_json_exception("SearchIndex", {}, json.dumps(params))
        res = json.loads(res)
        # print(res["data"])

        datas = []
        # 返回数据是个列表，每个vector又对应一个列表，但是这里输入vector好像只能传一个值，所以要for两次
        for items in res["data"]:
            for item in items:
                # print(item)
                id = item[self.primary_key]
                fields = {}
                if output_fields != [] or output_fields is None:
                    fields = item["fields"]
                # print(id, fields)
                data = Data(fields, id=id, timestamp=None, score=item["score"], dist=item.get('dist', None))
                datas.append(data)
            # print("==================")
        return datas

    def search_by_text(self, text, filter=None, limit=10, output_fields=None, partition="default", dense_weight=None):
        """
        Search for text similar to a given text.

        :param text: the given text.
        :type text: Text
        :param filter: filter conditions.
        :type filter: dict
        :param limit: number of retrieved results.
        :type limit: int
        :param output_fields: specify the list of scalar fields to be returned.
        :type output_fields: list
        :param partition: the name of sub-index.
        :type partition: int or str or list[int] or list[str]
        :rtype: list
        """
        search = {}
        order_by_raw = {"text": text.text}
        search = {"order_by_raw": order_by_raw, "limit": limit, "partition": partition}
        if output_fields is not None:
            search["output_fields"] = output_fields
        if filter is not None:
            search['filter'] = filter
        if dense_weight is not None:
            search['dense_weight'] = dense_weight
        params = {"collection_name": self.collection_name, "index_name": self.index_name, "search": search}
        res = self.viking_db_service.json_exception("SearchIndex", {}, json.dumps(params))
        res = json.loads(res)
        # print(res["data"])

        datas = []
        # 返回数据是个列表，每个vector又对应一个列表，但是这里输入vector好像只能传一个值，所以要for两次
        for items in res["data"]:
            for item in items:
                # print(item)
                id = item[self.primary_key]
                fields = {}
                if output_fields != [] or output_fields is None:
                    fields = item["fields"]
                # print(id, fields)
                text = None
                if "text" in item:
                    text = item["text"]
                data = Data(fields, id=id, timestamp=None, score=item["score"], text=text, dist=item.get('dist', None))
                datas.append(data)
            # print("==================")
        return datas

    async def async_search_by_text(self, text, filter=None, limit=10, output_fields=None, partition="default",
                                   dense_weight=None):
        search = {}
        order_by_raw = {"text": text.text}
        search = {"order_by_raw": order_by_raw, "limit": limit, "partition": partition}
        if output_fields is not None:
            search["output_fields"] = output_fields
        if filter is not None:
            search['filter'] = filter
        if dense_weight is not None:
            search['dense_weight'] = dense_weight
        params = {"collection_name": self.collection_name, "index_name": self.index_name, "search": search}
        res = await self.viking_db_service.async_json_exception("SearchIndex", {}, json.dumps(params))
        res = json.loads(res)
        # print(res["data"])

        datas = []
        # 返回数据是个列表，每个vector又对应一个列表，但是这里输入vector好像只能传一个值，所以要for两次
        for items in res["data"]:
            for item in items:
                # print(item)
                id = item[self.primary_key]
                fields = {}
                if output_fields != [] or output_fields is None:
                    fields = item["fields"]
                # print(id, fields)
                text = None
                if "text" in item:
                    text = item["text"]
                data = Data(fields, id=id, timestamp=None, score=item["score"], text=text, dist=item.get('dist', None))
                datas.append(data)
            # print("==================")
        return datas

    def fetch_data(self, id: Union[str, List[str], int, List[int]], output_fields=None, partition=""):
        params = {}
        if isinstance(id, str) or isinstance(id, int):
            params = {"collection_name": self.collection_name, "index_name": self.index_name,
                      "primary_keys": id}
            if output_fields is not None:
                params["output_fields"] = output_fields
            if partition != "":
                params["partition"] = partition
            res = self.viking_db_service.get_body_exception("FetchIndexData", {}, json.dumps(params))
            res = json.loads(res)
            # res["data"]是一个list
            # print(res["data"][0]["fields"])
            fields = {}
            if "fields" in res["data"][0]:
                fields = res["data"][0]["fields"]
            data = Data(fields, id=id, timestamp=None)
            return data
        elif isinstance(id, List):
            datas = []
            params = {"collection_name": self.collection_name, "index_name": self.index_name,
                      "primary_keys": id}
            if output_fields is not None:
                params["output_fields"] = output_fields
            if partition != "":
                params["partition"] = partition
            res = self.viking_db_service.get_body_exception("FetchIndexData", {}, json.dumps(params))
            res = json.loads(res)
            # print(res)
            for item in res["data"]:
                # print(item)
                fields = {}
                if "fields" in item:
                    # print(item["fields"])
                    fields = item["fields"]
                data = Data(fields, id=item[self.primary_key], timestamp=None)
                datas.append(data)
            return datas

    async def async_fetch_data(self, id: Union[str, List[str], int, List[int]], output_fields=None, partition=""):
        params = {}
        if isinstance(id, str) or isinstance(id, int):
            params = {"collection_name": self.collection_name, "index_name": self.index_name,
                      "primary_keys": id}
            if output_fields is not None:
                params["output_fields"] = output_fields
            if partition != "":
                params["partition"] = partition
            res = await self.viking_db_service.async_get_body_exception("FetchIndexData", {}, json.dumps(params))
            res = json.loads(res)
            # res["data"]是一个list
            # print(res["data"][0]["fields"])
            fields = {}
            if "fields" in res["data"][0]:
                fields = res["data"][0]["fields"]
            data = Data(fields, id=id, timestamp=None)
            return data
        elif isinstance(id, List):
            datas = []
            params = {"collection_name": self.collection_name, "index_name": self.index_name,
                      "primary_keys": id}
            if output_fields is not None:
                params["output_fields"] = output_fields
            if partition != "":
                params["partition"] = partition
            res = await self.viking_db_service.async_get_body_exception("FetchIndexData", {}, json.dumps(params))
            res = json.loads(res)
            # print(res)
            for item in res["data"]:
                # print(item)
                fields = {}
                if "fields" in item:
                    # print(item["fields"])
                    fields = item["fields"]
                data = Data(fields, id=item[self.primary_key], timestamp=None)
                datas.append(data)
            return datas
