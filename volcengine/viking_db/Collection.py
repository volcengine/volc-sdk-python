# coding:utf-8
import json
from enum import Enum
from collections import namedtuple
from typing import Union, List

from volcengine.viking_db import VikingDBService
from volcengine.viking_db.common import Data


class Collection(object):
    def __init__(self, collection_name, fields, viking_db_service, primary_key, indexes=None, stat=None,
                 description="", create_time=None, update_time=None, update_person=None):
        self.collection_name = collection_name
        self.fields = fields
        self.viking_db_service = viking_db_service
        self.primary_key = primary_key
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
    def upsert_data(self, data: Union[Data, List[Data]]):
        """
        Insert and overwrite data in fields within a collection

        :param data: The data you want to insert or overwrite.
        :type data: Data or list[Data]
        :rtype: None
        """
        if isinstance(data, Data):
            fields_arr = [data.fields]
            ttl = 0
            if data.TTL is not None:
                ttl = data.TTL
            params = {"collection_name": self.collection_name, "fields": fields_arr, "ttl": ttl}
            # print(params)
            res = self.viking_db_service.json_exception("UpsertData", {}, json.dumps(params))
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
                res = self.viking_db_service.json_exception("UpsertData", {}, json.dumps(params))

    async def async_upsert_data(self, data: Union[Data, List[Data]]):
        if isinstance(data, Data):
            fields_arr = [data.fields]
            ttl = 0
            if data.TTL is not None:
                ttl = data.TTL
            params = {"collection_name": self.collection_name, "fields": fields_arr, "ttl": ttl}
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
                res = await self.viking_db_service.async_json_exception("UpsertData", {}, json.dumps(params))


    def delete_data(self, id: Union[str, List[str], int, List[int]]):
        """
        delete data in fields within a collection

        :param id: The data id you want to delete.
        :type id: str or list[str] or int or list[int]
        :rtype: None
        """
        if isinstance(id, str) or isinstance(id, int):
            params = {"collection_name": self.collection_name, "primary_keys": id}
            res = self.viking_db_service.json_exception("DeleteData", {}, json.dumps(params))
            # print(res)
        elif isinstance(id, List):
            params = {"collection_name": self.collection_name, "primary_keys": id}
            res = self.viking_db_service.json_exception("DeleteData", {}, json.dumps(params))
            # print(res,params)

    async def async_delete_data(self, id: Union[str, List[str], int, List[int]]):
        if isinstance(id, str) or isinstance(id, int):
            params = {"collection_name": self.collection_name, "primary_keys": id}
            res = await self.viking_db_service.async_json_exception("DeleteData", {}, json.dumps(params))
            # print(res)
        elif isinstance(id, List):
            params = {"collection_name": self.collection_name, "primary_keys": id}
            res = await self.viking_db_service.async_json_exception("DeleteData", {}, json.dumps(params))
            # print(res,params)

    def fetch_data(self, id: Union[str, List[str], int, List[int]]):
        """
        Query single or multiple data records in a specified Collection based on primary key

        :param id: the primary key.
        :type id: str or list[str] or int or list[int]
        :rtype: Data or list[Data]
        """
        if isinstance(id, str) or isinstance(id, int):
            params = {"collection_name": self.collection_name, "primary_keys": id}
            # print(params)
            res = self.viking_db_service.get_body_exception("FetchData", {}, json.dumps(params))
            # print(res)
            # res是一个列表,只有一个元素
            res = json.loads(res)
            # print(res["data"][0])
            data = Data(res["data"][0], id=id, timestamp=None)
            return data
        elif isinstance(id, List):
            params = {"collection_name": self.collection_name, "primary_keys": id}
            res = self.viking_db_service.get_body_exception("FetchData", {}, json.dumps(params))
            res = json.loads(res)
            # print(res["data"],self.primary_key)
            datas = []
            for item in res["data"]:
                # print(item)
                data = Data(item, id=item[self.primary_key], timestamp=None)
                datas.append(data)
                # print(data.id,data.fields)
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
