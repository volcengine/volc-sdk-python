# coding:utf-8
import json
import warnings
from typing import Union, List, Dict

from volcengine.viking_db.common import (RetryOption, Data, VectorOrder, ScalarOrder,
                                         AggResult, IndexSortResult, SortResultItem)


class Index(object):
    def __init__(self, collection_name, index_name, vector_index, scalar_index, stat, viking_db_service, description="",
                 cpu_quota=2, partition_by=None, create_time=None, update_time=None, update_person=None,
                 index_cost=None, shard_count=None, shard_policy=None, retry_option=None):
        """
        :param collection_name: the name of VikingDB collection.
        :type collection_name: str
        :param index_name: the name of VikingDB index.
        :type index_name: str
        :param vector_index: ANN vector index information.
        :type vector_index: dict
        :param scalar_index: scalar index information.
        :type scalar_index: set
        :param stat: index status like 'READY'.
        :type stat: str
        :param viking_db_service: VikingDBService instance.
        :type viking_db_service: VikingDBService
        :param description: the description of index.
        :type description: str
        :param cpu_quota: allocated cpu quota of the index.
        :type cpu_quota: int
        :param partition_by: the name of sub-index, if not specified, the sub-index is single default.
        :type partition_by: str
        :param shard_count: the number of shards, by default it's 1.
        :type shard_count: int
        :param shard_policy: the sharding policy of the index, by default it's 'auto'.
        :type shard_policy: str
        :param retry_option: retry option.
        :type retry_option: RetryOption
        """
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
        self.shard_policy = shard_policy
        self.retry_option = retry_option if retry_option else RetryOption()
        # 获取primary_key
        col = self.viking_db_service.get_exception("GetCollection", {"collection_name": self.collection_name})
        col = json.loads(col)
        self.primary_key = col["data"]["primary_key"]

    def search(self, order=None, filter=None, limit=10, output_fields=None, partition="default", dense_weight=None,
               primary_key_in=None, primary_key_not_in=None, post_process_ops=None, post_process_input_limit=None,
               retry=True, filter_pre_ann_limit=-1, filter_pre_ann_ratio=-1.0, **kwargs):
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
        :type: list
        :param dense_weight: the weight of dense vector, the value should be a float in range [0.2, 1.0].
        :type dense_weight: float
        :type primary_key_in: filter data by primary key value, list[int] or list[str]
        :type: list
        :type primary_key_not_in: filter out data by primary key value, list[int] or list[str]
        :type: list
        :type post_process_ops: post process operators
        :type: list[dict]
        :type post_process_input_limit: number of data input to post process operators
        :type: int
        :param retry: whether to retry when the request fails caused by 1000029: QuotaLimiterException.
        :type retry: bool
        """
        if isinstance(order, VectorOrder):
            res = []
            if order.vector is not None:
                res = self.search_by_vector(order.vector, sparse_vectors=order.sparse_vectors, filter=filter, limit=limit,
                                            output_fields=output_fields, partition=partition, dense_weight=dense_weight,
                                            primary_key_in=None, primary_key_not_in=None, post_process_ops=None, post_process_input_limit=None,
                                            retry=retry, filter_pre_ann_limit=filter_pre_ann_limit, filter_pre_ann_ratio=filter_pre_ann_ratio, **kwargs)
            elif order.id is not None:
                res = self.search_by_id(order.id, filter=filter, limit=limit,
                                        output_fields=output_fields, partition=partition, dense_weight=dense_weight,
                                        primary_key_in=None, primary_key_not_in=None, post_process_ops=None, post_process_input_limit=None,
                                        retry=retry, filter_pre_ann_limit=filter_pre_ann_limit, filter_pre_ann_ratio=filter_pre_ann_ratio, **kwargs)
            return res
        elif isinstance(order, ScalarOrder):
            search = {}
            order_by_scalar = {"order": order.order.value, "field_name": order.field_name}
            search = {"order_by_scalar": order_by_scalar, "limit": limit, "partition": partition}
            if output_fields is not None:
                search["output_fields"] = output_fields
            if filter is not None:
                search['filter'] = filter
            if primary_key_in is not None:
                search['primary_key_in'] = primary_key_in
            if primary_key_not_in is not None:
                search['primary_key_not_in'] = primary_key_not_in
            if post_process_ops is not None:
                search['post_process_ops'] = post_process_ops
            if post_process_input_limit is not None:
                search['post_process_input_limit'] = post_process_input_limit
            if filter_pre_ann_limit >= 0:
                search['filter_pre_ann_limit'] = filter_pre_ann_limit
            if filter_pre_ann_ratio >= 0.0:
                search['filter_pre_ann_ratio'] = filter_pre_ann_ratio
            offset = kwargs.get("offset", -1)
            if offset >= 0:
                search['offset'] = offset
            need_search_count = kwargs.get("need_search_count", False)
            if need_search_count:
                search['need_search_count'] = need_search_count
            params = {"collection_name": self.collection_name, "index_name": self.index_name, "search": search}
            # print(params)
            remaining = self.retry_option.new_remaining(retry)
            res = self.viking_db_service._retry_request("SearchIndex", {}, json.dumps(params), remaining, self.retry_option)
            res = json.loads(res)

            datas = []
            # 返回数据是个列表，每个id又对应一个列表，但是这里输入id好像只能传一个值，所以要for两次
            for items in res["data"]:
                for item in items:
                    id = item[self.primary_key]
                    fields = {}
                    if output_fields != [] or output_fields is None:
                        fields = item["fields"]
                    data = Data(fields, id=id, timestamp=None, score=item["score"], dist=item.get('dist', None))
                    datas.append(data)
            extend_info = res.get('extend', {})
            if need_search_count:
                return datas, extend_info
            return datas
        elif order is None:
            search = {"limit": limit, "partition": partition}
            if output_fields is not None:
                search["output_fields"] = output_fields
            if filter is not None:
                search['filter'] = filter
            if primary_key_in is not None:
                search['primary_key_in'] = primary_key_in
            if primary_key_not_in is not None:
                search['primary_key_not_in'] = primary_key_not_in
            if post_process_ops is not None:
                search['post_process_ops'] = post_process_ops
            if post_process_input_limit is not None:
                search['post_process_input_limit'] = post_process_input_limit
            offset = kwargs.get("offset", -1)
            if offset >= 0:
                search['offset'] = offset
            need_search_count = kwargs.get("need_search_count", False)
            if need_search_count:
                search['need_search_count'] = need_search_count
            params = {"collection_name": self.collection_name, "index_name": self.index_name, "search": search}
            remaining = self.retry_option.new_remaining(retry)
            res = self.viking_db_service._retry_request("SearchIndex", {}, json.dumps(params), remaining, self.retry_option)
            res = json.loads(res)

            datas = []
            for items in res["data"]:
                for item in items:
                    id = item[self.primary_key]
                    fields = {}
                    if output_fields != [] or output_fields is None:
                        fields = item["fields"]
                    data = Data(fields, id=id, timestamp=None, score=item["score"], dist=item.get('dist', None))
                    datas.append(data)
            extend_info = res.get('extend', {})
            if need_search_count:
                return datas, extend_info
            return datas

    async def async_search(self, order=None, filter=None, limit=10, output_fields=None, partition="default",
                           dense_weight=None, primary_key_in=None, primary_key_not_in=None, post_process_ops=None, post_process_input_limit=None, **kwargs):
        if isinstance(order, VectorOrder):
            res = []
            if order.vector is not None:
                res = await self.async_search_by_vector(order.vector, sparse_vectors=order.sparse_vectors, filter=filter, limit=limit,
                                                        output_fields=output_fields, partition=partition, dense_weight=dense_weight,
                                                        primary_key_in=None, primary_key_not_in=None,
                                                        post_process_ops=None, post_process_input_limit=None)
            elif order.id is not None:
                res = await self.async_search_by_id(order.id, filter=filter, limit=limit, output_fields=output_fields,
                                                    partition=partition, dense_weight=dense_weight,
                                                    primary_key_in=None, primary_key_not_in=None,
                                                    post_process_ops=None, post_process_input_limit=None)
            return res
        elif isinstance(order, ScalarOrder):
            search = {}
            order_by_scalar = {"order": order.order.value, "field_name": order.field_name}
            search = {"order_by_scalar": order_by_scalar, "limit": limit, "partition": partition}
            if output_fields is not None:
                search["output_fields"] = output_fields
            if filter is not None:
                search['filter'] = filter
            if primary_key_in is not None:
                search['primary_key_in'] = primary_key_in
            if primary_key_not_in is not None:
                search['primary_key_not_in'] = primary_key_not_in
            if post_process_ops is not None:
                search['post_process_ops'] = post_process_ops
            if post_process_input_limit is not None:
                search['post_process_input_limit'] = post_process_input_limit
            offset = kwargs.get("offset", -1)
            if offset >= 0:
                search['offset'] = offset
            need_search_count = kwargs.get("need_search_count", False)
            if need_search_count:
                search['need_search_count'] = need_search_count
            params = {"collection_name": self.collection_name, "index_name": self.index_name, "search": search}
            res = await self.viking_db_service.async_json_exception("SearchIndex", {}, json.dumps(params))
            res = json.loads(res)

            datas = []
            # 返回数据是个列表，每个id又对应一个列表，但是这里输入id好像只能传一个值，所以要for两次
            for items in res["data"]:
                for item in items:
                    id = item[self.primary_key]
                    fields = {}
                    if output_fields != [] or output_fields is None:
                        fields = item["fields"]
                    data = Data(fields, id=id, timestamp=None, score=item["score"], dist=item.get('dist', None))
                    datas.append(data)
            extend_info = res.get('extend', {})
            if need_search_count:
                return datas, extend_info
            return datas
        elif order is None:
            search = {"limit": limit, "partition": partition}
            if output_fields is not None:
                search["output_fields"] = output_fields
            if filter is not None:
                search['filter'] = filter
            if primary_key_in is not None:
                search['primary_key_in'] = primary_key_in
            if primary_key_not_in is not None:
                search['primary_key_not_in'] = primary_key_not_in
            if post_process_ops is not None:
                search['post_process_ops'] = post_process_ops
            if post_process_input_limit is not None:
                search['post_process_input_limit'] = post_process_input_limit
            offset = kwargs.get("offset", -1)
            if offset >= 0:
                search['offset'] = offset
            need_search_count = kwargs.get("need_search_count", False)
            if need_search_count:
                search['need_search_count'] = need_search_count
            params = {"collection_name": self.collection_name, "index_name": self.index_name, "search": search}
            res = await self.viking_db_service.async_json_exception("SearchIndex", {}, json.dumps(params))
            res = json.loads(res)

            datas = []
            for items in res["data"]:
                for item in items:
                    id = item[self.primary_key]
                    fields = {}
                    if output_fields != [] or output_fields is None:
                        fields = item["fields"]
                    data = Data(fields, id=id, timestamp=None, score=item["score"], dist=item.get('dist', None))
                    datas.append(data)
            extend_info = res.get('extend', {})
            if need_search_count:
                return datas, extend_info
            return datas

    def search_by_id(self, id, filter=None, limit=10, output_fields=None, partition="default", dense_weight=None,
                     primary_key_in=None, primary_key_not_in=None, post_process_ops=None, post_process_input_limit=None,
                     retry=True, scale_k=0, filter_pre_ann_limit=-1, filter_pre_ann_ratio=-1.0, **kwargs):
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
        :param dense_weight: the weight of dense vector, the value should be a float in range [0.2, 1.0].
        :type dense_weight: float
        :type primary_key_in: filter data by primary key value, list[int] or list[str]
        :type: list
        :type primary_key_not_in: filter out data by primary key value, list[int] or list[str]
        :type: list
        :type post_process_ops: post process operators
        :type: list[dict]
        :type post_process_input_limit: number of data input to post process operators
        :type: int
        :param retry: whether to retry when the request fails caused by 1000029: QuotaLimiterException.
        :type retry: bool
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
        if primary_key_in is not None:
            search['primary_key_in'] = primary_key_in
        if primary_key_not_in is not None:
            search['primary_key_not_in'] = primary_key_not_in
        if post_process_ops is not None:
            search['post_process_ops'] = post_process_ops
        if post_process_input_limit is not None:
            search['post_process_input_limit'] = post_process_input_limit
        if scale_k > 0:
            search['scale_k'] = scale_k
        if filter_pre_ann_limit >= 0:
            search['filter_pre_ann_limit'] = filter_pre_ann_limit
        if filter_pre_ann_ratio >= 0.0:
            search['filter_pre_ann_ratio'] = filter_pre_ann_ratio
        offset = kwargs.get("offset", -1)
        if offset >= 0:
            search['offset'] = offset
        need_search_count = kwargs.get("need_search_count", False)
        if need_search_count:
            search['need_search_count'] = need_search_count
        params = {"collection_name": self.collection_name, "index_name": self.index_name, "search": search}
        # print(params)
        remaining = self.retry_option.new_remaining(retry)
        res = self.viking_db_service._retry_request("SearchIndex", {}, json.dumps(params), remaining, self.retry_option)
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
        extend_info = res.get('extend', {})
        if need_search_count:
            return datas, extend_info
        return datas

    async def async_search_by_id(self, id, filter=None, limit=10, output_fields=None, partition="default", dense_weight=None,
                                 primary_key_in=None, primary_key_not_in=None, post_process_ops=None, post_process_input_limit=None, **kwargs):
        search = {}
        order_by_id = {"primary_keys": id}
        search = {"order_by_vector": order_by_id, "limit": limit, "partition": partition}
        if output_fields is not None:
            search["output_fields"] = output_fields
        if filter is not None:
            search['filter'] = filter
        if dense_weight is not None:
            search['dense_weight'] = dense_weight
        if primary_key_in is not None:
            search['primary_key_in'] = primary_key_in
        if primary_key_not_in is not None:
            search['primary_key_not_in'] = primary_key_not_in
        if post_process_ops is not None:
            search['post_process_ops'] = post_process_ops
        if post_process_input_limit is not None:
            search['post_process_input_limit'] = post_process_input_limit
        offset = kwargs.get("offset", -1)
        if offset >= 0:
            search['offset'] = offset
        need_search_count = kwargs.get("need_search_count", False)
        if need_search_count:
            search['need_search_count'] = need_search_count
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
        extend_info = res.get('extend', {})
        if need_search_count:
            return datas, extend_info
        return datas

    def search_by_vector(self, vector, sparse_vectors=None, filter=None, limit=10, output_fields=None, partition="default", dense_weight=None,
                         primary_key_in=None, primary_key_not_in=None, post_process_ops=None, post_process_input_limit=None, retry=True, scale_k=0,
                         filter_pre_ann_limit=-1, filter_pre_ann_ratio=-1.0, **kwargs):
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
        :param dense_weight: the weight of dense vector, the value should be a float in range [0.2, 1.0].
        :type dense_weight: float
        :type primary_key_in: filter data by primary key value, list[int] or list[str]
        :type: list
        :type primary_key_not_in: filter out data by primary key value, list[int] or list[str]
        :type: list
        :type post_process_ops: post process operators
        :type: list[dict]
        :type post_process_input_limit: number of data input to post process operators
        :type: int
        :param retry: whether to retry when the request fails caused by 1000029: QuotaLimiterException.
        :type retry: bool
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
        if primary_key_in is not None:
            search['primary_key_in'] = primary_key_in
        if primary_key_not_in is not None:
            search['primary_key_not_in'] = primary_key_not_in
        if post_process_ops is not None:
            search['post_process_ops'] = post_process_ops
        if post_process_input_limit is not None:
            search['post_process_input_limit'] = post_process_input_limit
        if scale_k > 0:
            search['scale_k'] = scale_k
        if filter_pre_ann_limit >= 0:
            search['filter_pre_ann_limit'] = filter_pre_ann_limit
        if filter_pre_ann_ratio >= 0.0:
            search['filter_pre_ann_ratio'] = filter_pre_ann_ratio
        offset = kwargs.get("offset", -1)
        if offset >= 0:
            search['offset'] = offset
        need_search_count = kwargs.get("need_search_count", False)
        if need_search_count:
            search['need_search_count'] = need_search_count
        params = {"collection_name": self.collection_name, "index_name": self.index_name, "search": search}
        remaining = self.retry_option.new_remaining(retry)
        res = self.viking_db_service._retry_request("SearchIndex", {}, json.dumps(params), remaining, self.retry_option)
        res = json.loads(res)

        datas = []
        # 返回数据是个列表，每个vector又对应一个列表，但是这里输入vector好像只能传一个值，所以要for两次
        for items in res["data"]:
            for item in items:
                id = item[self.primary_key]
                fields = {}
                if output_fields != [] or output_fields is None:
                    fields = item["fields"]
                data = Data(fields, id=id, timestamp=None, score=item["score"], dist=item.get('dist', None))
                datas.append(data)
        extend_info = res.get('extend', {})
        if need_search_count:
            return datas, extend_info
        return datas

    async def async_search_by_vector(self, vector, sparse_vectors=None, filter=None, limit=10, output_fields=None, partition="default", dense_weight=None,
                                     primary_key_in=None, primary_key_not_in=None, post_process_ops=None, post_process_input_limit=None, **kwargs):
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
        if primary_key_in is not None:
            search['primary_key_in'] = primary_key_in
        if primary_key_not_in is not None:
            search['primary_key_not_in'] = primary_key_not_in
        if post_process_ops is not None:
            search['post_process_ops'] = post_process_ops
        if post_process_input_limit is not None:
            search['post_process_input_limit'] = post_process_input_limit
        offset = kwargs.get("offset", -1)
        if offset >= 0:
            search['offset'] = offset
        need_search_count = kwargs.get("need_search_count", False)
        if need_search_count:
            search['need_search_count'] = need_search_count
        params = {"collection_name": self.collection_name, "index_name": self.index_name, "search": search}
        res = await self.viking_db_service.async_json_exception("SearchIndex", {}, json.dumps(params))
        res = json.loads(res)

        datas = []
        # 返回数据是个列表，每个vector又对应一个列表，但是这里输入vector好像只能传一个值，所以要for两次
        for items in res["data"]:
            for item in items:
                id = item[self.primary_key]
                fields = {}
                if output_fields != [] or output_fields is None:
                    fields = item["fields"]
                data = Data(fields, id=id, timestamp=None, score=item["score"], dist=item.get('dist', None))
                datas.append(data)
        extend_info = res.get('extend', {})
        if need_search_count:
            return datas, extend_info
        return datas

    def search_with_multi_modal(self, text=None, image=None, filter=None, limit=10, output_fields=None, partition="default", dense_weight=None, need_instruction=None,
                       primary_key_in=None, primary_key_not_in=None, post_process_ops=None, post_process_input_limit=None, retry=True, scale_k=0,
                       filter_pre_ann_limit=-1, filter_pre_ann_ratio=-1.0, **kwargs):
        """
        Search with multi-modal data including type of text and image.

        :param text: the given text.
        :type text: str
        :param image: the given image.
        :type image: str
        :param filter: filter conditions.
        :type filter: dict
        :param limit: number of retrieved results.
        :type limit: int
        :param output_fields: specify the list of scalar fields to be returned.
        :type output_fields: list
        :param partition: the name of sub-index.
        :type partition: int or str or list[int] or list[str]
        :rtype: list
        :param dense_weight: the weight of dense vector, the value should be a float in range [0.2, 1.0].
        :type dense_weight: float
        :type need_instruction: whether need instruction for embedding
        :type: bool
        :type primary_key_in: filter data by primary key value, list[int] or list[str]
        :type: list
        :type primary_key_not_in: filter out data by primary key value, list[int] or list[str]
        :type: list
        :type post_process_ops: post process operators
        :type: list[dict]
        :type post_process_input_limit: number of data input to post process operators
        :type: int
        :param retry: whether to retry when the request fails caused by 1000029: QuotaLimiterException.
        :type retry: bool
        """
        if text is None and image is None:
            raise Exception("not any modal data params exist")
        order_by_raw = {}
        if text is not None:
            order_by_raw["text"] = text
        if image is not None:
            order_by_raw["image"] = image
        search = {"order_by_raw": order_by_raw, "limit": limit, "partition": partition}
        if output_fields is not None:
            search["output_fields"] = output_fields
        if filter is not None:
            search['filter'] = filter
        if dense_weight is not None:
            search['dense_weight'] = dense_weight
        if need_instruction is not None:
            search['need_instruction'] = need_instruction
        if primary_key_in is not None:
            search['primary_key_in'] = primary_key_in
        if primary_key_not_in is not None:
            search['primary_key_not_in'] = primary_key_not_in
        if post_process_ops is not None:
            search['post_process_ops'] = post_process_ops
        if post_process_input_limit is not None:
            search['post_process_input_limit'] = post_process_input_limit
        if scale_k > 0:
            search['scale_k'] = scale_k
        if filter_pre_ann_limit >= 0:
            search['filter_pre_ann_limit'] = filter_pre_ann_limit
        if filter_pre_ann_ratio >= 0.0:
            search['filter_pre_ann_ratio'] = filter_pre_ann_ratio
        offset = kwargs.get("offset", -1)
        if offset >= 0:
            search['offset'] = offset
        need_search_count = kwargs.get("need_search_count", False)
        if need_search_count:
            search['need_search_count'] = need_search_count
        params = {"collection_name": self.collection_name, "index_name": self.index_name, "search": search}
        remaining = self.retry_option.new_remaining(retry)
        res = self.viking_db_service._retry_request("SearchIndex", {}, json.dumps(params), remaining, self.retry_option)
        res = json.loads(res)

        datas = []
        # 返回数据是个列表，每个vector又对应一个列表，但是这里输入vector好像只能传一个值，所以要for两次
        for items in res["data"]:
            for item in items:
                id = item[self.primary_key]
                fields = {}
                if output_fields != [] or output_fields is None:
                    fields = item["fields"]
                text = None
                if "text" in item:
                    text = item["text"]
                data = Data(fields, id=id, timestamp=None, score=item["score"], text=text, dist=item.get('dist', None))
                datas.append(data)
        extend_info = res.get('extend', {})
        if need_search_count:
            return datas, extend_info
        return datas

    async def async_search_with_multi_modal(self, text=None, image=None, filter=None, limit=10, output_fields=None, partition="default", dense_weight=None, need_instruction=None,
                       primary_key_in=None, primary_key_not_in=None, post_process_ops=None, post_process_input_limit=None, scale_k=0, **kwargs):
        if text is None and image is None:
            raise Exception("not any modal data params exist")
        order_by_raw = {}
        if text is not None:
            order_by_raw["text"] = text
        if image is not None:
            order_by_raw["image"] = image
        search = {"order_by_raw": order_by_raw, "limit": limit, "partition": partition}
        if output_fields is not None:
            search["output_fields"] = output_fields
        if filter is not None:
            search['filter'] = filter
        if dense_weight is not None:
            search['dense_weight'] = dense_weight
        if need_instruction is not None:
            search['need_instruction'] = need_instruction
        if primary_key_in is not None:
            search['primary_key_in'] = primary_key_in
        if primary_key_not_in is not None:
            search['primary_key_not_in'] = primary_key_not_in
        if post_process_ops is not None:
            search['post_process_ops'] = post_process_ops
        if post_process_input_limit is not None:
            search['post_process_input_limit'] = post_process_input_limit
        if scale_k > 0:
            search['scale_k'] = scale_k
        offset = kwargs.get("offset", -1)
        if offset >= 0:
            search['offset'] = offset
        need_search_count = kwargs.get("need_search_count", False)
        if need_search_count:
            search['need_search_count'] = need_search_count
        params = {"collection_name": self.collection_name, "index_name": self.index_name, "search": search}
        res = await self.viking_db_service.async_json_exception("SearchIndex", {}, json.dumps(params))
        res = json.loads(res)

        datas = []
        # 返回数据是个列表，每个vector又对应一个列表，但是这里输入vector好像只能传一个值，所以要for两次
        for items in res["data"]:
            for item in items:
                id = item[self.primary_key]
                fields = {}
                if output_fields != [] or output_fields is None:
                    fields = item["fields"]
                text = None
                if "text" in item:
                    text = item["text"]
                data = Data(fields, id=id, timestamp=None, score=item["score"], text=text, dist=item.get('dist', None))
                datas.append(data)
        extend_info = res.get('extend', {})
        if need_search_count:
            return datas, extend_info
        return datas

    def search_by_text(self, text, filter=None, limit=10, output_fields=None, partition="default", dense_weight=None, need_instruction=None,
                       primary_key_in=None, primary_key_not_in=None, post_process_ops=None, post_process_input_limit=None, retry=True, scale_k=0,
                       filter_pre_ann_limit=-1, filter_pre_ann_ratio=-1.0, **kwargs):
        """
        Search for text similar to a given text. (You can use search_with_multi_modal instead.)

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
        :param dense_weight: the weight of dense vector, the value should be a float in range [0.2, 1.0].
        :type dense_weight: float
        :type need_instruction: whether need instruction for embedding
        :type: bool
        :type primary_key_in: filter data by primary key value, list[int] or list[str]
        :type: list
        :type primary_key_not_in: filter out data by primary key value, list[int] or list[str]
        :type: list
        :type post_process_ops: post process operators
        :type: list[dict]
        :type post_process_input_limit: number of data input to post process operators
        :type: int
        :param retry: whether to retry when the request fails caused by 1000029: QuotaLimiterException.
        :type retry: bool
        """
        warnings.warn("search_by_text is deprecated, please use search_with_multi_modal instead", DeprecationWarning)
        order_by_raw = {"text": text.text}
        search = {"order_by_raw": order_by_raw, "limit": limit, "partition": partition}
        if output_fields is not None:
            search["output_fields"] = output_fields
        if filter is not None:
            search['filter'] = filter
        if dense_weight is not None:
            search['dense_weight'] = dense_weight
        if need_instruction is not None:
            search['need_instruction'] = need_instruction
        if primary_key_in is not None:
            search['primary_key_in'] = primary_key_in
        if primary_key_not_in is not None:
            search['primary_key_not_in'] = primary_key_not_in
        if post_process_ops is not None:
            search['post_process_ops'] = post_process_ops
        if post_process_input_limit is not None:
            search['post_process_input_limit'] = post_process_input_limit
        if scale_k > 0:
            search['scale_k'] = scale_k
        if filter_pre_ann_limit >= 0:
            search['filter_pre_ann_limit'] = filter_pre_ann_limit
        if filter_pre_ann_ratio >= 0.0:
            search['filter_pre_ann_ratio'] = filter_pre_ann_ratio
        offset = kwargs.get("offset", -1)
        if offset >= 0:
            search['offset'] = offset
        need_search_count = kwargs.get("need_search_count", False)
        if need_search_count:
            search['need_search_count'] = need_search_count
        params = {"collection_name": self.collection_name, "index_name": self.index_name, "search": search}
        remaining = self.retry_option.new_remaining(retry)
        res = self.viking_db_service._retry_request("SearchIndex", {}, json.dumps(params), remaining, self.retry_option)
        res = json.loads(res)

        datas = []
        # 返回数据是个列表，每个vector又对应一个列表，但是这里输入vector好像只能传一个值，所以要for两次
        for items in res["data"]:
            for item in items:
                id = item[self.primary_key]
                fields = {}
                if output_fields != [] or output_fields is None:
                    fields = item["fields"]
                text = None
                if "text" in item:
                    text = item["text"]
                data = Data(fields, id=id, timestamp=None, score=item["score"], text=text, dist=item.get('dist', None))
                datas.append(data)
        extend_info = res.get('extend', {})
        if need_search_count:
            return datas, extend_info
        return datas

    async def async_search_by_text(self, text, filter=None, limit=10, output_fields=None, partition="default", dense_weight=None, need_instruction=None,
                                   primary_key_in=None, primary_key_not_in=None, post_process_ops=None, post_process_input_limit=None, **kwargs):
        warnings.warn("async_search_by_text is deprecated, please use async_search_with_multi_modal instead", DeprecationWarning)
        order_by_raw = {"text": text.text}
        search = {"order_by_raw": order_by_raw, "limit": limit, "partition": partition}
        if output_fields is not None:
            search["output_fields"] = output_fields
        if filter is not None:
            search['filter'] = filter
        if dense_weight is not None:
            search['dense_weight'] = dense_weight
        if need_instruction is not None:
            search['need_instruction'] = need_instruction
        if primary_key_in is not None:
            search['primary_key_in'] = primary_key_in
        if primary_key_not_in is not None:
            search['primary_key_not_in'] = primary_key_not_in
        if post_process_ops is not None:
            search['post_process_ops'] = post_process_ops
        if post_process_input_limit is not None:
            search['post_process_input_limit'] = post_process_input_limit
        offset = kwargs.get("offset", -1)
        if offset >= 0:
            search['offset'] = offset
        need_search_count = kwargs.get("need_search_count", False)
        if need_search_count:
            search['need_search_count'] = need_search_count
        params = {"collection_name": self.collection_name, "index_name": self.index_name, "search": search}
        res = await self.viking_db_service.async_json_exception("SearchIndex", {}, json.dumps(params))
        res = json.loads(res)

        datas = []
        # 返回数据是个列表，每个vector又对应一个列表，但是这里输入vector好像只能传一个值，所以要for两次
        for items in res["data"]:
            for item in items:
                id = item[self.primary_key]
                fields = {}
                if output_fields != [] or output_fields is None:
                    fields = item["fields"]
                text = None
                if "text" in item:
                    text = item["text"]
                data = Data(fields, id=id, timestamp=None, score=item["score"], text=text, dist=item.get('dist', None))
                datas.append(data)
        extend_info = res.get('extend', {})
        if need_search_count:
            return datas, extend_info
        return datas

    def search_agg(self, agg: Dict[str, any], filter=None, partition="default", retry=True) -> AggResult:
        """
        Search and aggregate the data.

        :param agg: the aggregation operator.
        :type agg: dict
        :param filter: filter conditions.
        :type filter: dict
        :param partition: the name of sub-index.
        :type partition: int or str or list[int] or list[str]
        :rtype: list
        :param retry: whether to retry when the request fails caused by 1000029: QuotaLimiterException.
        :type retry: bool
        """
        params = {"collection_name": self.collection_name, "index_name": self.index_name,
                  "search": {"partition": partition}, "agg": agg}
        if filter is not None:
            params["search"]["filter"] = filter
        remaining = self.retry_option.new_remaining(retry)
        res = self.viking_db_service._retry_request("SearchAgg", {}, json.dumps(params), remaining, self.retry_option)
        res = json.loads(res)
        data = res["data"]
        return AggResult(
            agg_op=data["agg_op"],
            group_by_field=data["group_by_field"],
            agg_result=data["agg_result"],
        )

    async def async_search_agg(self, agg: Dict[str, any], filter=None, partition="default") -> AggResult:
        params = {"collection_name": self.collection_name, "index_name": self.index_name,
                  "search": {"partition": partition}, "agg": agg}
        if filter is not None:
            params["search"]["filter"] = filter
        res = await self.viking_db_service.async_json_exception("SearchAgg", {}, json.dumps(params))
        res = json.loads(res)
        data = res["data"]
        return AggResult(
            agg_op=data["agg_op"],
            group_by_field=data["group_by_field"],
            agg_result=data["agg_result"],
        )

    def sort(self, query_vector: List[float], primary_keys: List, retry=True):
        """
        Index sort: input a query vector and primary key list, get the sorted score list.

        :param query_vector: one query vector.
        :type query_vector: list
        :param primary_keys: primary key list.
        :type primary_keys: list
        :param retry: whether to retry when the request fails caused by 1000029: QuotaLimiterException.
        :type retry: bool
        """
        params = {"collection_name": self.collection_name, "index_name": self.index_name,
                  "sort": {"query_vector": query_vector, "primary_keys": primary_keys}}
        remaining = self.retry_option.new_remaining(retry)
        res = self.viking_db_service._retry_request("IndexSort", {}, json.dumps(params), remaining, self.retry_option)
        res = json.loads(res)
        data = res["data"]
        result_items = []
        for raw_item in data["sort_result"]:
            primary_key = raw_item["primary_key"]
            score = raw_item["score"]
            result_items.append(SortResultItem(primary_key=primary_key, score=score))
        return IndexSortResult(sort_result=result_items, primary_key_not_exist=data["primary_key_not_exist"])

    def fetch_data(self, id: Union[str, List[str], int, List[int]], output_fields=None, partition="", retry=True):
        """
        Fetch data by primary key (id).
        this method is much faster than Collection.fetch_data() due to indexed.
        :param text: the given primary key or keys.
        :type text: str or int or list[str] or list[int]
        :param output_fields: specify the list of scalar fields to be returned.
        :type output_fields: list
        :param partition: the name of sub-index.
        :type partition: int or str or list[int] or list[str]
        :param retry: whether to retry when the request fails caused by 1000029: QuotaLimiterException.
        :type retry: bool
        """
        params = {}
        if isinstance(id, str) or isinstance(id, int):
            params = {"collection_name": self.collection_name, "index_name": self.index_name,
                      "primary_keys": id}
            if output_fields is not None:
                params["output_fields"] = output_fields
            if partition != "":
                params["partition"] = partition
            remaining = self.retry_option.new_remaining(retry)
            res = self.viking_db_service._retry_request("FetchIndexData", {}, json.dumps(params), remaining, self.retry_option)
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
            remaining = self.retry_option.new_remaining(retry)
            res = self.viking_db_service._retry_request("FetchIndexData", {}, json.dumps(params), remaining, self.retry_option)
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
