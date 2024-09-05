# coding:utf-8
import json
import threading
import aiohttp

from .common import EnumEncoder
from .Point import Point
from .Collection import Collection
from .exception import ERRCODE_EXCEPTION, VikingKnowledgeBaseException
from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo
from volcengine.auth.SignerV4 import SignerV4


class VikingKnowledgeBaseService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(VikingKnowledgeBaseService, "_instance"):
            with VikingKnowledgeBaseService._instance_lock:
                if not hasattr(VikingKnowledgeBaseService, "_instance"):
                    VikingKnowledgeBaseService._instance = object.__new__(cls)
        return VikingKnowledgeBaseService._instance

    def __init__(self, host="api-knowledgebase.mlp.cn-beijing.volces.com", region="cn-beijing", ak="", sk="", sts_token="", scheme='http',
                 connection_timeout=30, socket_timeout=30):
        self.service_info = VikingKnowledgeBaseService.get_service_info(host, region, scheme, connection_timeout, socket_timeout)
        self.api_info = VikingKnowledgeBaseService.get_api_info()
        super(VikingKnowledgeBaseService, self).__init__(self.service_info, self.api_info)
        if ak:
            self.set_ak(ak)
        if sk:
            self.set_sk(sk)
        if sts_token:
            self.set_session_token(session_token=sts_token)
        try:
            self.get_body("Ping", {}, json.dumps({}))
        except Exception as e:
            raise VikingKnowledgeBaseException(1000028, "missed", "host or region is incorrect".format(str(e))) from None

    def setHeader(self, header):
        api_info = VikingKnowledgeBaseService.get_api_info()
        for key in api_info:
            for item in header:
                api_info[key].header[item] = header[item]
        self.api_info = api_info

    @staticmethod
    def get_service_info(host, region, scheme, connection_timeout, socket_timeout):
        service_info = ServiceInfo(host, {"Host": host},
                                   Credentials('', '', 'air', region), connection_timeout, socket_timeout,
                                   scheme=scheme)
        return service_info

    @staticmethod 
    def get_api_info():
        api_info = {
            # Collection
            "CreateCollection":     ApiInfo("POST", "/api/knowledge/collection/create", {}, {},
                                        {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "GetCollection":        ApiInfo("POST", "/api/knowledge/collection/info", {}, {},
                                        {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "DropCollection":       ApiInfo("POST", "/api/knowledge/collection/delete", {}, {},
                                        {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "ListCollections":      ApiInfo("POST", "/api/knowledge/collection/list", {}, {},
                                        {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "UpdateCollection":     ApiInfo("POST", "/api/knowledge/collection/update", {}, {},
                                        {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "SearchCollection":     ApiInfo("POST", "/api/knowledge/collection/search", {}, {},
                                        {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "SearchAndGenerate":    ApiInfo("POST", "/api/knowledge/collection/search_and_generate", {}, {},
                                        {'Accept': 'application/json', 'Content-Type': 'application/json'}),        

            # Doc
            "AddDoc":               ApiInfo("POST", "/api/knowledge/doc/add", {}, {},
                                        {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "DeleteDoc":            ApiInfo("POST", "/api/knowledge/doc/delete", {}, {},
                                        {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "GetDocInfo":           ApiInfo("POST", "/api/knowledge/doc/info", {}, {},
                                        {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "ListDocs":             ApiInfo("POST", "/api/knowledge/doc/list", {}, {},
                                        {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "UpdateDocMeta":        ApiInfo("POST", "/api/knowledge/doc/update_meta", {}, {},
                                        {'Accept': 'application/json', 'Content-Type': 'application/json'}), 

            # Point
            "GetPointInfo":           ApiInfo("POST", "/api/knowledge/point/info", {}, {},
                                        {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            "ListPoints":             ApiInfo("POST", "/api/knowledge/point/list", {}, {},
                                        {'Accept': 'application/json', 'Content-Type': 'application/json'}),
            
            # Service
            "Ping":                   ApiInfo("GET", "/ping", {}, {},
                                        {'Accept': 'application/json', 'Content-Type': 'application/json'}),
        }
        return api_info

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

    def get_body_exception(self, api, params, body):
        try:
            res = self.get_body(api, params, body)
        except Exception as e:
            try:
                res_json = json.loads(e.args[0].decode("utf-8"))
            except:
                raise VikingKnowledgeBaseException(1000028, "missed", "json load res error, res:{}".format(str(e))) from None
            code = res_json.get("code", 1000028)
            request_id = res_json.get("request_id", 1000028)
            message = res_json.get("message", None)
            raise ERRCODE_EXCEPTION.get(code, VikingKnowledgeBaseException)(code, request_id, message) from None
        if res == '':
            raise VikingKnowledgeBaseException(1000028, "missed",
                                    "empty response due to unknown error, please contact customer service") from None
        return res
    
    def get_exception(self, api, params):
        try:
            res = self.get(api, params)
        except Exception as e:
            try:
                res_json = json.loads(e.args[0].decode("utf-8"))
            except:
                raise VikingKnowledgeBaseException(1000028, "missed", "json load res error, res:{}".format(str(e))) from None
            code = res_json.get("code", 1000028)
            request_id = res_json.get("request_id", 1000028)
            message = res_json.get("message", None)
            raise ERRCODE_EXCEPTION.get(code, VikingKnowledgeBaseException)(code, request_id, message) from None
        if res == '':
            raise VikingKnowledgeBaseException(1000028, "missed",
                                    "empty response due to unknown error, please contact customer service") from None
        return res
    
    def json_exception(self, api, params, body):
        try:
            res = self.json(api, params, body)
        except Exception as e:
            try:
                res_json = json.loads(e.args[0].decode("utf-8"))
            except:
                raise VikingKnowledgeBaseException(1000028, "missed", "json load res error, res:{}".format(str(e))) from None
            code = res_json.get("code", 1000028)
            request_id = res_json.get("request_id", 1000028)
            message = res_json.get("message", None)
            raise ERRCODE_EXCEPTION.get(code, VikingKnowledgeBaseException)(code, request_id, message) from None
        if res == '':
            raise VikingKnowledgeBaseException(1000028, "missed",
                                    "empty response due to unknown error, please contact customer service") from None
        return res

    async def async_json_exception(self, api, params, body):
        try:
            res = await self.async_json(api, params, body)
        except Exception as e:
            try:
                res_json = json.loads(e.args[0].decode("utf-8"))
            except:
                raise VikingKnowledgeBaseException(1000028, "missed", "json load res error, res:{}".format(str(e))) from None
            code = res_json.get("code", 1000028)
            request_id = res_json.get("request_id", 1000028)
            message = res_json.get("message", None)
            raise ERRCODE_EXCEPTION.get(code, VikingKnowledgeBaseException)(code, request_id, message) from None
        if res == '':
            raise VikingKnowledgeBaseException(1000028, "missed",
                                    "empty response due to unknown error, please contact customer service") from None
        return res

    def create_collection(self, collection_name, index=None, description="", preprocessing=None, project="default", data_type="unstructured_data", table_config=None):
        params = {"name": collection_name, "description": description, "index": index, 
                  "preprocessing": preprocessing, "project": project, "data_type": data_type}
        if table_config is not None:
            params["table_config"] = table_config
        res = self.json_exception("CreateCollection", {}, json.dumps(params, cls=EnumEncoder))
        data = json.loads(res)["data"]
        params["resource_id"] = data["resource_id"]
        if index is not None and index.get("index_config") is not None:
            fields = index["index_config"].get("fields")
            if fields is not None:
                assert isinstance(fields, list)
                params["fields"] = fields
        return Collection(self, collection_name, params)

    async def async_create_collection(self, collection_name, index=None, description="", preprocessing=None, project="default", data_type="unstructured_data", table_config=None):
        params = {"name": collection_name, "description": description, "index": index, 
                  "preprocessing": preprocessing, "project": project, "data_type": data_type}
        if table_config is not None:
            params["table_config"] = table_config
        res = await self.async_json_exception("CreateCollection", {}, json.dumps(params, cls=EnumEncoder))
        data = json.loads(res)["data"]
        params["resource_id"] = data["resource_id"]
        if index is not None and index.get("index_config") is not None:
            fields = index["index_config"]["fields"]
            assert isinstance(fields, list)
            params["fields"] = fields
        return Collection(self, collection_name, params)

    def get_collection(self, collection_name, project="default", resource_id=None):
        params = {"name": collection_name, "project": project}
        if resource_id != None:
            params["resource_id"] = resource_id
        res = self.json_exception("GetCollection", {}, json.dumps(params))
        data = json.loads(res)["data"]
        now_index_list = data["pipeline_list"][0]["index_list"][0]
        fields = now_index_list["index_config"]["fields"]
        data["fields"] = fields

        return Collection(self, collection_name, data)

    async def async_get_collection(self, collection_name, project="default", resource_id=None):
        params = {"name": collection_name, "project": project}
        if resource_id != None:
            params["resource_id"] = resource_id
        res = await self.async_json_exception("GetCollection", {}, json.dumps(params))
        data = json.loads(res)["data"]
        now_index_list = data["pipeline_list"][0]["index_list"][0]
        fields = now_index_list["index_config"]["fields"]
        data["fields"] = fields

        return Collection(self, collection_name, data)

    def drop_collection(self, collection_name, project="default", resource_id=None):
        params = {"name": collection_name, "project":project}
        if resource_id != None:
            params["resource_id"] = resource_id
        self.json_exception("DropCollection", {}, json.dumps(params))

    async def async_drop_collection(self, collection_name, project="default", resource_id=None):
        params = {"name": collection_name, "project":project}
        if resource_id != None:
            params["resource_id"] = resource_id
        await self.async_json_exception("DropCollection", {}, json.dumps(params))

    def list_collections(self, project=None, brief=False):
        params = {"brief": brief}
        if project is not None:
            params["project"] = project
        res = self.json_exception("ListCollections", {}, json.dumps(params))
        collection_list = json.loads(res)["data"]["collection_list"]
        collections = []
        for collection in collection_list:
            now_index_list = collection["pipeline_list"][0]["index_list"][0]
            fields = now_index_list["index_config"]["fields"]
            collection["fields"] = fields
            collections.append(Collection(self, collection["collection_name"], collection))

        return collections

    async def async_list_collections(self, project=None, brief=False):
        params = {"brief": brief}
        if project is not None:
            params["project"] = project
        res = await self.async_json_exception("ListCollections", {}, json.dumps(params))
        collection_list = json.loads(res)["data"]["collection_list"]
        collections = []
        for collection in collection_list:
            now_index_list = collection["pipeline_list"][0]["index_list"][0]
            fields = now_index_list["index_config"]["fields"]
            collection["fields"] = fields
            collections.append(Collection(self, collection["collection_name"], collection))

        return collections

    def update_collection(self, collection_name, description=None, cpu_quota=None, project="default", resource_id=None):
        params = {"name": collection_name, "project":project}
        if resource_id != None:
            params["resource_id"] = resource_id
        if description  != None:
            params["description"] = description
        if cpu_quota    != None:
            params["cpu_quota"] = cpu_quota

        self.json_exception("UpdateCollection", {}, json.dumps(params))

    async def async_update_collection(self, collection_name, description=None, cpu_quota=None, project="default", resource_id=None):
        params = {"name": collection_name, "project":project}
        if resource_id != None:
            params["resource_id"] = resource_id
        if description  != None:
            params["description"] = description
        if cpu_quota    != None:
            params["cpu_quota"] = cpu_quota

        await self.async_json_exception("UpdateCollection", {}, json.dumps(params))

    def search_collection(self, collection_name, query, query_param=None, limit=10, dense_weight=0.5, rerank_switch=False, project="default", resource_id=None, retrieve_count= None):
        params = {"name": collection_name, 
                  "query": query,
                  "limit": limit,
                  "dense_weight": dense_weight,
                  "rerank_switch": rerank_switch,
                  "project": project
                  }
        if resource_id != None:
            params["resource_id"] = resource_id
        if query_param != None:
            params["query_param"] = query_param
        if retrieve_count != None:
            params["retrieve_count"] = retrieve_count
        res = self.json_exception("SearchCollection", {}, json.dumps(params))
        data = json.loads(res)["data"]
        results = data.get("result_list")
        points = []
        if results is not None:
            for result in results:
                result['collection_name'] = collection_name
                result['project'] = project
                if resource_id is not None :
                    result['resource_id'] = resource_id
                points.append(Point(result))
        return points
    
    async def async_search_collection(self, collection_name, query, query_param=None, limit=10, dense_weight=0.5, rerank_switch=False, project="default", resource_id=None, retrieve_count= None):
        params = {"name": collection_name, 
                  "query": query,
                  "limit": limit,
                  "dense_weight": dense_weight,
                  "rerank_switch": rerank_switch,
                  "project": project
                  }
        if resource_id != None:
            params["resource_id"] = resource_id
        if query_param != None:
            params["query_param"] = query_param
        if retrieve_count != None:
            params["retrieve_count"] = retrieve_count
        res = await self.async_json_exception("SearchCollection", {}, json.dumps(params))
        data = json.loads(res)["data"]
        results = data.get("result_list")
        points = []
        if results is not None:
            for result in results:
                result['collection_name'] = collection_name
                result['project'] = project
                if resource_id is not None :
                    result['resource_id'] = resource_id
                points.append(Point(result))
        return points
    
    def search_and_generate(self, collection_name, query, query_param=None, retrieve_param=None, llm_param=None, project="default", resource_id=None):
        params = {"name": collection_name, 
                  "query": query,
                  "project": project
                  }
        
        if resource_id != None:
            params["resource_id"] = resource_id
        if query_param != None:
            params["query_param"] = query_param
        if retrieve_param != None:
            params["retrieve_param"] = retrieve_param
        if llm_param != None:
            params["llm_param"] = llm_param
            
        res = self.json_exception("SearchAndGenerate", {}, json.dumps(params))
        data = json.loads(res)["data"]
        results = data.get("result_list")
        points = []
        if results is not None:
            for result in results:
                result['collection_name'] = collection_name
                points.append(Point(result))
        ret = {
            "collection_name": data.get("collection_name"),
            "count": data.get("count"),
            "generated_answer": data.get("generated_answer"),
            "prompt": data.get("prompt"),
            "usage": data.get("usage"),
            "refs": points
        }
        
        return ret
    
    async def async_search_and_generate(self, collection_name, query, query_param=None, retrieve_param=None, llm_param=None, project="default", resource_id=None):
        params = {"name": collection_name, 
                  "query": query,
                  "project": project
                  }
        
        if resource_id != None:
            params["resource_id"] = resource_id
        if query_param != None:
            params["query_param"] = query_param
        if retrieve_param != None:
            params["retrieve_param"] = retrieve_param
        if llm_param != None:
            params["llm_param"] = llm_param
            
        res = await self.async_json_exception("SearchAndGenerate", {}, json.dumps(params))
        data = json.loads(res)["data"]
        results = data.get("result_list")
        points = []
        if results is not None:
            for result in results:
                result['collection_name'] = collection_name
                points.append(Point(result))
        ret = {
            "collection_name": data.get("collection_name"),
            "count": data.get("count"),
            "generated_answer": data.get("generated_answer"),
            "prompt": data.get("prompt"),
            "usage": data.get("usage"),
            "refs": points
        }
        
        return ret
    
    