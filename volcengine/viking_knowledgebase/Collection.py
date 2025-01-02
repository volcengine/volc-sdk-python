# coding:utf-8
from .common import Field
import json
from .Doc import Doc
from .Point import Point

class Collection(object):
    """
    KnowledgeBase Collection
    """
    def __init__(self, viking_knowledgebase_service, collection_name, kwargs=None):
        self.viking_knowledgebase_service      = viking_knowledgebase_service
        self.collection_name        = collection_name
        if kwargs is not None:
            self.description            = kwargs.get("description")
            self.doc_num                = kwargs.get("doc_num")
            self.create_time            = kwargs.get("create_time")
            self.update_time            = kwargs.get("update_time")
            self.creator                = kwargs.get("creator")
            self.pipeline_list          = kwargs.get("pipeline_list")
            self.preprocessing          = kwargs.get("preprocessing")
            self.fields                 = [Field(field) for field in kwargs.get("fields", [])]
            self.project                = kwargs.get("project")
            self.resource_id            = kwargs.get("resource_id")
            self.data_type              = kwargs.get("data_type", "")

    def add_doc(self, add_type, doc_id=None, doc_name=None, doc_type=None, tos_path=None, url=None, meta=None, project="default", resource_id=None, collection_name=None):
        params = {"collection_name": self.collection_name, "add_type": add_type, "project":project}
        if resource_id is not None:
            params["resource_id"] = resource_id
        if collection_name is not None:
            params["collection_name"] = collection_name
        if add_type == "tos" :
            params["tos_path"]  = tos_path

        elif add_type == "url" :
            params["doc_id"]    = doc_id
            params["doc_name"]  = doc_name
            params["doc_type"]  = doc_type
            params["url"]       = url
            if meta is not None: 
                params["meta"]  = meta
        self.viking_knowledgebase_service.json_exception("AddDoc", {}, json.dumps(params))

    async def async_add_doc(self, add_type, doc_id=None, doc_name=None, doc_type=None, tos_path=None, url=None, meta=None, project="default", resource_id=None, collection_name=None):
        params = {"collection_name": self.collection_name, "add_type": add_type, "project":project}
        if resource_id is not None:
            params["resource_id"] = resource_id
        if collection_name is not None:
            params["collection_name"] = collection_name
        if add_type == "tos" :
            params["tos_path"]  = tos_path

        elif add_type == "url" :
            params["doc_id"]    = doc_id
            params["doc_name"]  = doc_name
            params["doc_type"]  = doc_type
            params["url"]       = url
            if meta != None: 
                params["meta"]  = meta
        await self.viking_knowledgebase_service.async_json_exception("AddDoc", {}, json.dumps(params))

    def delete_doc(self, doc_id, project="default", resource_id=None, collection_name=None):
        params = {"collection_name": self.collection_name, "doc_id": doc_id, "project":project}
        if resource_id is not None:
            params["resource_id"] = resource_id
        if collection_name is not None:
            params["collection_name"] = collection_name
        self.viking_knowledgebase_service.json_exception("DeleteDoc", {}, json.dumps(params))
    
    async def async_delete_doc(self, doc_id, project="default", resource_id=None, collection_name=None):
        params = {"collection_name": self.collection_name, "doc_id": doc_id, "project":project}
        if resource_id is not None:
            params["resource_id"] = resource_id
        if collection_name is not None:
            params["collection_name"] = collection_name
        await self.viking_knowledgebase_service.async_json_exception("DeleteDoc", {}, json.dumps(params))

    def get_doc(self, doc_id, project="default", resource_id=None, collection_name=None):
        params = {"collection_name": self.collection_name, "doc_id": doc_id, "project":project}
        if resource_id is not None:
            params["resource_id"] = resource_id
        if collection_name is not None:
            params["collection_name"] = collection_name
        res = self.viking_knowledgebase_service.json_exception("GetDocInfo", {}, json.dumps(params))
        data = json.loads(res)["data"]
        data['project'] = project
        if resource_id is not None :
            data['resource_id'] = resource_id
        return Doc(data)

    async def async_get_doc(self, doc_id, project="default", resource_id=None, collection_name=None):
        params = {"collection_name": self.collection_name, "doc_id": doc_id, "project":project}
        if resource_id is not None:
            params["resource_id"] = resource_id
        if collection_name is not None:
            params["collection_name"] = collection_name
        res = await self.viking_knowledgebase_service.async_json_exception("GetDocInfo", {}, json.dumps(params))
        data = json.loads(res)["data"]
        data['project'] = project
        if resource_id is not None :
            data['resource_id'] = resource_id
        return Doc(data)

    def list_docs(self, offset=0, limit=-1, doc_type=None, project="default", collection_name=None):
        params = {"collection_name": self.collection_name, "offset": offset, "limit": limit, "doc_type": doc_type, "project":project}
        if collection_name is not None:
            params["collection_name"] = collection_name
        res = self.viking_knowledgebase_service.json_exception("ListDocs", {}, json.dumps(params))
        data = json.loads(res)["data"]
        docs = []
        for item in data["doc_list"]:
            item['project'] = project
            docs.append(Doc(item))
        return docs

    async def async_list_docs(self, offset=0, limit=-1, doc_type=None, project="default", collection_name=None):
        params = {"collection_name": self.collection_name, "offset": offset, "limit": limit, "doc_type": doc_type, "project":project}
        if collection_name is not None:
            params["collection_name"] = collection_name
        res = await self.viking_knowledgebase_service.async_json_exception("ListDocs", {}, json.dumps(params))
        data = json.loads(res)["data"]
        docs = []
        for item in data["doc_list"]:
            item['project'] = project
            docs.append(Doc(item))
        return docs

    def update_meta(self, doc_id, meta, project="default", resource_id=None, collection_name=None):
        params = {"collection_name": self.collection_name, "doc_id": doc_id, "meta": meta, "project":project}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if resource_id is not None:
            params["resource_id"] = resource_id
        self.viking_knowledgebase_service.json_exception("UpdateDocMeta", {}, json.dumps(params))
    
    async def async_update_meta(self, doc_id, meta, project="default", resource_id=None, collection_name=None):
        params = {"collection_name": self.collection_name, "doc_id": doc_id, "meta": meta, "project":project}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if resource_id is not None:
            params["resource_id"] = resource_id
        await self.viking_knowledgebase_service.async_json_exception("UpdateDocMeta", {}, json.dumps(params))

    def get_point(self, point_id, project="default", resource_id=None, collection_name=None):
        params = {"collection_name": self.collection_name, "point_id": point_id, "project":project}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if resource_id is not None:
            params["resource_id"] = resource_id
        res = self.viking_knowledgebase_service.json_exception("GetPointInfo", {}, json.dumps(params))
        res = json.loads(res)
        res["data"]["project"] = project
        if resource_id is not None :
            res["data"]["resource_id"] = resource_id
        return Point(res["data"])
    
    async def async_get_point(self, point_id, project="default", resource_id=None, collection_name=None):
        params = {"collection_name": self.collection_name, "point_id": point_id, "project":project}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if resource_id is not None:
            params["resource_id"] = resource_id
        res = await self.viking_knowledgebase_service.async_json_exception("GetPointInfo", {}, json.dumps(params))
        res = json.loads(res)
        res["data"]["project"] = project
        if resource_id is not None :
            res["data"]["resource_id"] = resource_id
        return Point(res["data"])

    def list_points(self, offset=0, limit=-1, doc_ids=None, project="default", resource_id=None, collection_name=None):
        params = {"collection_name": self.collection_name, "offset": offset, "limit": limit, "doc_ids": doc_ids, "project":project}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if resource_id is not None:
            params["resource_id"] = resource_id
        res = self.viking_knowledgebase_service.json_exception("ListPoints", {}, json.dumps(params))
        point_list = json.loads(res)["data"].get("point_list", [])
        points = []
        for item in point_list:
            item["project"] = project
            points.append(Point(item))
        return points 
    
    async def async_list_points(self, offset=0, limit=-1, doc_ids=None, project="default", resource_id=None, collection_name=None):
        params = {"collection_name": self.collection_name, "offset": offset, "limit": limit, "doc_ids": doc_ids, "project":project}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if resource_id is not None:
            params["resource_id"] = resource_id
        res = await self.viking_knowledgebase_service.async_json_exception("ListPoints", {}, json.dumps(params))
        point_list = json.loads(res)["data"].get("point_list", [])
        points = []
        for item in point_list:
            item["project"] = project
            points.append(Point(item))
        return points 