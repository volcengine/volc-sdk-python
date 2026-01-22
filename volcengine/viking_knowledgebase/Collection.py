# coding:utf-8
import json

from .Doc import Doc
from .Point import Point
from .common import Field


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

    def add_doc(self, add_type, doc_id=None, doc_name=None, doc_type=None, description=None, tos_path=None, url=None,
                lark_file=None, meta=None, dedup=None, project="default", resource_id=None, collection_name=None, headers=None):
        params = {"collection_name": self.collection_name, "add_type": add_type, "project":project}
        if resource_id is not None:
            params["resource_id"] = resource_id
        if collection_name is not None:
            params["collection_name"] = collection_name
        if description is not None:
            params["description"] = description
        if dedup is not None:
            params["dedup"] = dedup

        if add_type == "tos" :
            params["tos_path"]  = tos_path
        elif add_type == "url" :
            params["doc_id"]    = doc_id
            params["doc_name"]  = doc_name
            params["doc_type"]  = doc_type
            params["url"]       = url
            if meta is not None:
                params["meta"]  = meta
        elif add_type == "lark" :
            params["doc_type"]  = doc_type
            params["lark_file"] = lark_file
            if doc_id is not None:
                params["doc_id"] = doc_id
            if meta is not None:
                params["meta"]  = meta

        self.viking_knowledgebase_service.json_exception("AddDoc", {}, json.dumps(params), headers=headers)

    async def async_add_doc(self, add_type, doc_id=None, doc_name=None, doc_type=None, description=None, tos_path=None, url=None,
                lark_file=None, meta=None, dedup=None, project="default", resource_id=None, collection_name=None, headers=None):
        params = {"collection_name": self.collection_name, "add_type": add_type, "project":project}
        if resource_id is not None:
            params["resource_id"] = resource_id
        if collection_name is not None:
            params["collection_name"] = collection_name
        if description is not None:
            params["description"] = description
        if dedup is not None:
            params["dedup"] = dedup

        if add_type == "tos" :
            params["tos_path"]  = tos_path
        elif add_type == "url" :
            params["doc_id"]    = doc_id
            params["doc_name"]  = doc_name
            params["doc_type"]  = doc_type
            params["url"]       = url
            if meta is not None:
                params["meta"]  = meta
        elif add_type == "lark" :
            params["doc_type"]  = doc_type
            params["lark_file"] = lark_file
            if doc_id is not None:
                params["doc_id"] = doc_id
            if meta is not None:
                params["meta"]  = meta

        await self.viking_knowledgebase_service.async_json_exception("AddDoc", {}, json.dumps(params), headers=headers)

    def delete_doc(self, doc_id, project="default", resource_id=None, collection_name=None, headers=None):
        params = {"collection_name": self.collection_name, "doc_id": doc_id, "project":project}
        if resource_id is not None:
            params["resource_id"] = resource_id
        if collection_name is not None:
            params["collection_name"] = collection_name
        self.viking_knowledgebase_service.json_exception("DeleteDoc", {}, json.dumps(params), headers=headers)

    async def async_delete_doc(self, doc_id, project="default", resource_id=None, collection_name=None, headers=None):
        params = {"collection_name": self.collection_name, "doc_id": doc_id, "project":project}
        if resource_id is not None:
            params["resource_id"] = resource_id
        if collection_name is not None:
            params["collection_name"] = collection_name
        await self.viking_knowledgebase_service.async_json_exception("DeleteDoc", {}, json.dumps(params), headers=headers)

    def get_doc(self, doc_id, return_token_usage=False, project="default", resource_id=None, collection_name=None, headers=None):
        params = {"collection_name": self.collection_name, "doc_id": doc_id, "project":project}
        if resource_id is not None:
            params["resource_id"] = resource_id
        if collection_name is not None:
            params["collection_name"] = collection_name
        if return_token_usage:
            params["return_token_usage"] = return_token_usage
        res = self.viking_knowledgebase_service.json_exception("GetDocInfo", {}, json.dumps(params), headers=headers)
        data = json.loads(res)["data"]
        data['project'] = project
        if resource_id is not None :
            data['resource_id'] = resource_id
        return Doc(data)

    async def async_get_doc(self, doc_id, return_token_usage=False, project="default", resource_id=None, collection_name=None, headers=None):
        params = {"collection_name": self.collection_name, "doc_id": doc_id, "project":project}
        if resource_id is not None:
            params["resource_id"] = resource_id
        if collection_name is not None:
            params["collection_name"] = collection_name
        if return_token_usage:
            params["return_token_usage"] = return_token_usage
        res = await self.viking_knowledgebase_service.async_json_exception("GetDocInfo", {}, json.dumps(params), headers=headers)
        data = json.loads(res)["data"]
        data['project'] = project
        if resource_id is not None :
            data['resource_id'] = resource_id
        return Doc(data)

    def list_docs(self, offset=0, limit=-1, doc_type=None, return_token_usage=False, project="default", collection_name=None, filter=None, headers=None):
        params = {"collection_name": self.collection_name, "offset": offset, "limit": limit, "doc_type": doc_type, "project":project, "filter": filter}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if return_token_usage:
            params["return_token_usage"] = return_token_usage
        res = self.viking_knowledgebase_service.json_exception("ListDocs", {}, json.dumps(params), headers=headers)
        data = json.loads(res)["data"]
        docs = []
        for item in data["doc_list"]:
            item['project'] = project
            docs.append(Doc(item))
        return docs

    async def async_list_docs(self, offset=0, limit=-1, doc_type=None, return_token_usage=False, project="default", collection_name=None, filter=None, headers=None):
        params = {"collection_name": self.collection_name, "offset": offset, "limit": limit, "doc_type": doc_type, "project":project, "filter": filter}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if return_token_usage:
            params["return_token_usage"] = return_token_usage
        res = await self.viking_knowledgebase_service.async_json_exception("ListDocs", {}, json.dumps(params), headers=headers)
        data = json.loads(res)["data"]
        docs = []
        for item in data["doc_list"]:
            item['project'] = project
            docs.append(Doc(item))
        return docs

    def update_meta(self, doc_id, meta, project="default", resource_id=None, collection_name=None, headers=None):
        params = {"collection_name": self.collection_name, "doc_id": doc_id, "meta": meta, "project":project}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if resource_id is not None:
            params["resource_id"] = resource_id
        self.viking_knowledgebase_service.json_exception("UpdateDocMeta", {}, json.dumps(params), headers=headers)

    async def async_update_meta(self, doc_id, meta, project="default", resource_id=None, collection_name=None, headers=None):
        params = {"collection_name": self.collection_name, "doc_id": doc_id, "meta": meta, "project":project}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if resource_id is not None:
            params["resource_id"] = resource_id
        await self.viking_knowledgebase_service.async_json_exception("UpdateDocMeta", {}, json.dumps(params), headers=headers)

    def update_doc(self, doc_id, doc_name, project="default", resource_id=None, collection_name=None, headers=None):
        params= {"collection_name": self.collection_name, "doc_id": doc_id, "doc_name": doc_name, "project":project}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if resource_id is not None:
            params["resource_id"] = resource_id
        return self.viking_knowledgebase_service.json_exception("UpdateDoc", {}, json.dumps(params), headers=headers)

    async def async_update_doc(self, doc_id, doc_name, project="default", resource_id=None, collection_name=None, headers=None):
        params= {"collection_name": self.collection_name, "doc_id": doc_id, "doc_name": doc_name, "project":project}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if resource_id is not None:
            params["resource_id"] = resource_id
        return await self.viking_knowledgebase_service.async_json_exception("UpdateDoc", {}, json.dumps(params), headers=headers)

    def get_point(self, point_id, get_attachment_link=False, project="default", resource_id=None, collection_name=None, headers=None):
        params = {"collection_name": self.collection_name, "point_id": point_id, "project":project}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if resource_id is not None:
            params["resource_id"] = resource_id
        if get_attachment_link:
            params["get_attachment_link"] = get_attachment_link
        res = self.viking_knowledgebase_service.json_exception("GetPointInfo", {}, json.dumps(params), headers=headers)
        res = json.loads(res)
        res["data"]["project"] = project
        if resource_id is not None :
            res["data"]["resource_id"] = resource_id
        return Point(res["data"])

    async def async_get_point(self, point_id, get_attachment_link=False, project="default", resource_id=None, collection_name=None, headers=None):
        params = {"collection_name": self.collection_name, "point_id": point_id, "project":project}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if resource_id is not None:
            params["resource_id"] = resource_id
        if get_attachment_link:
            params["get_attachment_link"] = get_attachment_link
        res = await self.viking_knowledgebase_service.async_json_exception("GetPointInfo", {}, json.dumps(params), headers=headers)
        res = json.loads(res)
        res["data"]["project"] = project
        if resource_id is not None :
            res["data"]["resource_id"] = resource_id
        return Point(res["data"])

    def list_points(self, offset=0, limit=-1, doc_ids=None, point_ids=None, get_attachment_link=False, project="default", resource_id=None, collection_name=None, headers=None):
        params = {"collection_name": self.collection_name, "offset": offset, "limit": limit, "doc_ids": doc_ids, "project":project, "get_attachment_link": get_attachment_link}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if resource_id is not None:
            params["resource_id"] = resource_id
        if point_ids is not None:
            params["point_ids"] = point_ids
        res = self.viking_knowledgebase_service.json_exception("ListPoints", {}, json.dumps(params), headers=headers)
        point_list = json.loads(res)["data"].get("point_list", [])
        points = []
        for item in point_list:
            item["project"] = project
            points.append(Point(item))
        return points

    async def async_list_points(self, offset=0, limit=-1, doc_ids=None, point_ids=None, get_attachment_link=False, project="default", resource_id=None, collection_name=None, headers=None):
        params = {"collection_name": self.collection_name, "offset": offset, "limit": limit, "doc_ids": doc_ids, "project":project, "get_attachment_link": get_attachment_link}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if resource_id is not None:
            params["resource_id"] = resource_id
        if point_ids is not None:
            params["point_ids"] = point_ids
        res = await self.viking_knowledgebase_service.async_json_exception("ListPoints", {}, json.dumps(params), headers=headers)
        point_list = json.loads(res)["data"].get("point_list", [])
        points = []
        for item in point_list:
            item["project"] = project
            points.append(Point(item))
        return points

    def add_point(self, doc_id, chunk_type, project="default", resource_id=None, collection_name=None, chunk_title=None, content=None, question=None, fields=None, headers=None):
        params= {"collection_name": self.collection_name, "doc_id": doc_id, "project":project, "chunk_type": chunk_type}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if resource_id is not None:
            params["resource_id"] = resource_id
        if chunk_title is not None:
            params["chunk_title"] = chunk_title
        if content is not None:
            params["content"] = content
        if question is not None:
            params["question"] = question
        if fields is not None:
            params["fields"] = fields
        return self.viking_knowledgebase_service.json_exception("AddPoint", {}, json.dumps(params), headers=headers)

    async def async_add_point(self, doc_id, chunk_type, project="default", resource_id=None, collection_name=None, chunk_title=None, content=None, question=None, fields=None, headers=None):
        params= {"collection_name": self.collection_name, "doc_id": doc_id, "project":project, "chunk_type": chunk_type}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if resource_id is not None:
            params["resource_id"] = resource_id
        if chunk_title is not None:
            params["chunk_title"] = chunk_title
        if content is not None:
            params["content"] = content
        if question is not None:
            params["question"] = question
        if fields is not None:
            params["fields"] = fields
        return await self.viking_knowledgebase_service.async_json_exception("AddPoint", {}, json.dumps(params), headers=headers)

    def update_point(self, point_id, project="default", resource_id=None, collection_name=None, chunk_title=None, content=None, question=None, fields=None, headers=None):
        params= {"collection_name": self.collection_name, "point_id": point_id, "project":project}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if resource_id is not None:
            params["resource_id"] = resource_id
        if chunk_title is not None:
            params["chunk_title"] = chunk_title
        if content is not None:
            params["content"] = content
        if question is not None:
            params["question"] = question
        if fields is not None:
            params["fields"] = fields
        return self.viking_knowledgebase_service.json_exception("UpdatePoint", {}, json.dumps(params), headers=headers)

    async def async_update_point(self, point_id, project="default", resource_id=None, collection_name=None, chunk_title=None, content=None, question=None, fields=None, headers=None):
        params= {"collection_name": self.collection_name, "point_id": point_id, "project":project}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if resource_id is not None:
            params["resource_id"] = resource_id
        if chunk_title is not None:
            params["chunk_title"] = chunk_title
        if content is not None:
            params["content"] = content
        if question is not None:
            params["question"] = question
        if fields is not None:
            params["fields"] = fields
        return await self.viking_knowledgebase_service.async_json_exception("UpdatePoint", {}, json.dumps(params), headers=headers)

    def delete_point(self, point_id, project="default", resource_id=None, collection_name=None, headers=None):
        params= {"collection_name": self.collection_name, "point_id": point_id, "project":project}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if resource_id is not None:
            params["resource_id"] = resource_id
        return self.viking_knowledgebase_service.json_exception("DeletePoint", {}, json.dumps(params), headers=headers)

    async def async_delete_point(self, point_id, project="default", resource_id=None, collection_name=None, headers=None):
        params= {"collection_name": self.collection_name, "point_id": point_id, "project":project}
        if collection_name is not None:
            params["collection_name"] = collection_name
        if resource_id is not None:
            params["resource_id"] = resource_id
        return await self.viking_knowledgebase_service.async_json_exception("DeletePoint", {}, json.dumps(params), headers=headers)
