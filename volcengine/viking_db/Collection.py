# coding:utf-8
import json
from typing import Union, List
from volcengine.viking_db.common import Data, RetryOption


class Collection(object):
    def __init__(self, collection_name, fields, viking_db_service, primary_key, indexes=None, stat=None,
                 description="", create_time=None, update_time=None, update_person=None, retry_option=None, vectorize=None):
        """
        :param collection_name: the name of VikingDB collection.
        :type collection_name: str
        :param fields: fields(schema) defination, including field_name, field_type, default_val, and dim or pipeline_name for embedding related field
        :type fields: list[Field]
        :param viking_db_service: VikingDBService instance.
        :type viking_db_service: VikingDBService
        :param primary_key: field_name of primary key in collection, or "__AUTO_ID__" to use auto int64 id.
        :type primary_key: str
        :param retry_option: retry option.
        :type retry_option: RetryOption
        """
        self.collection_name = collection_name
        self.fields = fields
        self.viking_db_service = viking_db_service
        self.primary_key = primary_key
        self.vectorize = vectorize
        if indexes is not None:
            self.indexes = indexes
        else:
            self.indexes = []
        if stat is not None:
            self.stat = stat
        else:
            self.stat = {}
        self.description = description
        if create_time is not None:
            self.create_time = create_time
        if update_time is not None:
            self.update_time = update_time
        if update_person is not None:
            self.update_person = update_person
        self._is_client = False
        self.retry_option = retry_option if retry_option else RetryOption()

    def upsert_data(self, data: Union[Data, List[Data]], async_upsert=False, retry=True):
        """
        Insert and overwrite data in fields within a collection

        :param data: The data you want to insert or overwrite.
        :type data: Data or list[Data]
        :rtype: None
        :param async_upsert: Whether to use async upsert, if enabled, writing will be faster but the data will not be updated in index immediately but after next round of index building finished.
        :type async_upsert: bool
        :param retry: Whether to retry when QuotaLimiterException occurs.
        :type retry: bool
        """
        remaining = self.retry_option.new_remaining(retry)
        if isinstance(data, Data):
            fields_arr = [data.fields]
            ttl = 0
            if data.TTL is not None:
                ttl = data.TTL
            params = {"collection_name": self.collection_name, "fields": fields_arr, "ttl": ttl}
            if async_upsert:
                params["async"]=True
            # print(params)
            res = self.viking_db_service._retry_request("UpsertData", {}, json.dumps(params), remaining, self.retry_option)
        elif isinstance(data, list):
            fields_arr = []
            ttl = 0
            record = {}
            for item in data:
                if item.TTL in record:
                    fields = record[item.TTL]
                    fields.append(item.fields)
                    record[item.TTL] = fields
                else:
                    record[item.TTL] = [item.fields]
            for item in record:
                params = {"collection_name": self.collection_name, "fields": record[item], "ttl": item}
                if async_upsert:
                    params["async"]=True
                res = self.viking_db_service._retry_request("UpsertData", {}, json.dumps(params), remaining, self.retry_option)

    def update_data(self, data: Union[Data, List[Data]], retry=True):
        """
        Update data in fields within a collection

        :param data: The data field you want to update. must contain primary key
        :type data: Data or list[Data]
        :param retry: Whether to retry when QuotaLimiterException occurs.
        :type retry: bool
        """
        remaining = self.retry_option.new_remaining(retry)
        if isinstance(data, Data):
            fields_arr = [data.fields]
            ttl = 0
            if data.TTL is not None:
                ttl = data.TTL
            params = {"collection_name": self.collection_name, "fields": fields_arr, "ttl": ttl}
            res = self.viking_db_service._retry_request("UpdateData", {}, json.dumps(params), remaining, self.retry_option)
        elif isinstance(data, list):
            fields_arr = []
            ttl = 0
            record = {}
            for item in data:
                if item.TTL in record:
                    fields = record[item.TTL]
                    fields.append(item.fields)
                    record[item.TTL] = fields
                else:
                    record[item.TTL] = [item.fields]
            for item in record:
                params = {"collection_name": self.collection_name, "fields": record[item], "ttl": item}
                res = self.viking_db_service._retry_request("UpdateData", {}, json.dumps(params), remaining, self.retry_option)

    async def async_upsert_data(self, data: Union[Data, List[Data]], async_upsert=False):
        if isinstance(data, Data):
            fields_arr = [data.fields]
            ttl = 0
            if data.TTL is not None:
                ttl = data.TTL
            params = {"collection_name": self.collection_name, "fields": fields_arr, "ttl": ttl}
            if async_upsert:
                params["async"]=True
            # print(params)
            res = await self.viking_db_service.async_json_exception("UpsertData", {}, json.dumps(params))
        elif isinstance(data, list):
            fields_arr = []
            ttl = 0
            record = {}
            for item in data:
                if item.TTL in record:
                    fields = record[item.TTL]
                    fields.append(item.fields)
                    record[item.TTL] = fields
                else:
                    record[item.TTL] = [item.fields]
            for item in record:
                params = {"collection_name": self.collection_name, "fields": record[item], "ttl": item}
                if async_upsert:
                    params["async"]=True
                res = await self.viking_db_service.async_json_exception("UpsertData", {}, json.dumps(params))

    def delete_data(self, id: Union[str, List[str], int, List[int]], retry=True):
        """
        delete data in fields within a collection

        :param id: The data id you want to delete.
        :type id: str or list[str] or int or list[int]
        :param retry: Whether to retry when QuotaLimiterException occurs.
        :type retry: bool
        """
        remaining = self.retry_option.new_remaining(retry)
        if isinstance(id, str) or isinstance(id, int):
            params = {"collection_name": self.collection_name, "primary_keys": id}
            res = self.viking_db_service._retry_request("DeleteData", {}, json.dumps(params), remaining, self.retry_option)
            return res
        elif isinstance(id, List):
            params = {"collection_name": self.collection_name, "primary_keys": id}
            res = self.viking_db_service._retry_request("DeleteData", {}, json.dumps(params), remaining, self.retry_option)
            return res

    async def async_delete_data(self, id: Union[str, List[str], int, List[int]]):
        if isinstance(id, str) or isinstance(id, int):
            params = {"collection_name": self.collection_name, "primary_keys": id}
            await self.viking_db_service.async_json_exception("DeleteData", {}, json.dumps(params))
        elif isinstance(id, List):
            params = {"collection_name": self.collection_name, "primary_keys": id}
            await self.viking_db_service.async_json_exception("DeleteData", {}, json.dumps(params))

    def delete_all_data(self):
        """
        delete all the data of a collection
        """
        params = {"collection_name": self.collection_name, "del_all": True}
        self.viking_db_service.json_exception("DeleteData", {}, json.dumps(params))

    async def async_delete_all_data(self):
        params = {"collection_name": self.collection_name, "del_all": True}
        await self.viking_db_service.async_json_exception("DeleteData", {}, json.dumps(params))


    def fetch_data(self, id: Union[str, List[str], int, List[int]], retry=True):
        """
        Query single or multiple data records in a specified Collection based on primary key

        :param id: the primary key.
        :type id: str or list[str] or int or list[int]
        :rtype: Data or list[Data]
        :param retry: Whether to retry when QuotaLimiterException occurs.
        :type retry: bool
        """
        remaining = self.retry_option.new_remaining(retry)
        if isinstance(id, str) or isinstance(id, int):
            params = {"collection_name": self.collection_name, "primary_keys": id}
            res = self.viking_db_service._retry_request("FetchData", {}, json.dumps(params), remaining, self.retry_option)
            # res是一个列表,只有一个元素
            res = json.loads(res)
            data = Data(res["data"][0], id=id, timestamp=None)
            return data
        elif isinstance(id, List):
            params = {"collection_name": self.collection_name, "primary_keys": id}
            if self._is_client:
                params['replace_primay'] = True
            res = self.viking_db_service._retry_request("FetchData", {}, json.dumps(params), remaining, self.retry_option)
            res = json.loads(res)
            datas = []
            for item in res["data"]:
                data = Data(item, id=item[self.primary_key], timestamp=None)
                datas.append(data)
            return datas

    async def async_fetch_data(self, id: Union[str, List[str], int, List[int]]):
        if isinstance(id, str) or isinstance(id, int):
            params = {"collection_name": self.collection_name, "primary_keys": id}
            # print(params)
            res = await self.viking_db_service.async_get_body_exception("FetchData", {}, json.dumps(params))
            # print(res)
            # res是一个列表,只有一个元素
            res = json.loads(res)
            # print(res["data"][0])
            data = Data(res["data"][0], id=id, timestamp=None)
            return data
        elif isinstance(id, List):
            params = {"collection_name": self.collection_name, "primary_keys": id}
            if self._is_client:
                params['replace_primay'] = True
            res = await self.viking_db_service.async_get_body_exception("FetchData", {}, json.dumps(params))
            res = json.loads(res)
            # print(res["data"],self.primary_key)
            datas = []
            for item in res["data"]:
                # print(item)
                data = Data(item, id=item[self.primary_key], timestamp=None)
                datas.append(data)
                # print(data.id,data.fields)
            return datas
