import json
import threading
import redo

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo
from requests import exceptions


class ImageRegistryService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(ImageRegistryService, "_instance"):
            with ImageRegistryService._instance_lock:
                if not hasattr(ImageRegistryService, "_instance"):
                    ImageRegistryService._instance = object.__new__(cls)
        return ImageRegistryService._instance

    def __init__(self):
        self.service_info = ImageRegistryService.get_service_info()
        self.api_info = ImageRegistryService.get_api_info()
        super(ImageRegistryService, self).__init__(
            self.service_info, self.api_info)

    @staticmethod
    def get_service_info():
        service_info = ServiceInfo("open.volcengineapi.com", {'Accept': 'application/json'},
                                   Credentials('', '', 'cr', 'cn-north-1'), 5, 5)
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            "DeleteNamespaceBasic": ApiInfo(
                "POST", "/", {"Action": "DeleteNamespaceBasic", "Version": "2021-03-03"}, {}, {}),
            "CreateNamespaceBasic": ApiInfo(
                "POST", "/", {"Action": "CreateNamespaceBasic", "Version": "2021-03-03"}, {}, {}),
            "ValidateNamespaceBasic": ApiInfo(
                "POST", "/", {"Action": "ValidateNamespaceBasic", "Version": "2021-03-03"}, {}, {}),
            "GetNamespaceBasic": ApiInfo(
                "POST", "/", {"Action": "GetNamespaceBasic", "Version": "2021-03-03"}, {}, {}),
            "ListNamespacesBasic": ApiInfo(
                "POST", "/", {"Action": "ListNamespacesBasic", "Version": "2021-03-03"}, {}, {}),
            "ValidateRepositoryBasic": ApiInfo(
                "POST", "/", {"Action": "ValidateRepositoryBasic", "Version": "2021-03-03"}, {}, {}),
            "DeleteRepositoryBasic": ApiInfo(
                "POST", "/", {"Action": "DeleteRepositoryBasic", "Version": "2021-03-03"}, {}, {}),
            "CreateRepositoryBasic": ApiInfo(
                "POST", "/", {"Action": "CreateRepositoryBasic", "Version": "2021-03-03"}, {}, {}),
            "UpdateRepositoryBasic": ApiInfo(
                "POST", "/", {"Action": "UpdateRepositoryBasic", "Version": "2021-03-03"}, {}, {}),
            "GetRepositoryBasic": ApiInfo(
                "POST", "/", {"Action": "GetRepositoryBasic", "Version": "2021-03-03"}, {}, {}),
            "ListRepositoriesBasic": ApiInfo(
                "POST", "/", {"Action": "ListRepositoriesBasic", "Version": "2021-03-03"}, {}, {}),
            "DeleteTagBasic": ApiInfo(
                "POST", "/", {"Action": "DeleteTagBasic", "Version": "2021-03-03"}, {}, {}),
            "ListTagsBasic": ApiInfo(
                "POST", "/", {"Action": "ListTagsBasic", "Version": "2021-03-03"}, {}, {}),
            "GetTagBasic": ApiInfo(
                "POST", "/", {"Action": "GetTagBasic", "Version": "2021-03-03"}, {}, {}),
            "GetTagAdditionBasic": ApiInfo(
                "POST", "/", {"Action": "GetTagAdditionBasic", "Version": "2021-03-03"}, {}, {})}

        return api_info

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def delete_namespace_basic(self, params, body):
        res = self.json("DeleteNamespaceBasic", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def create_namespace_basic(self, params, body):
        res = self.json("CreateNamespaceBasic", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def validate_namespace_basic(self, params, body):
        res = self.json("ValidateNamespaceBasic", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def get_namespace_basic(self, params, body):
        res = self.json("GetNamespaceBasic", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def list_namespaces_basic(self, params, body):
        res = self.json("ListNamespacesBasic", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def validate_repository_basic(self, params, body):
        res = self.json("ValidateRepositoryBasic", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def delete_repository_basic(self, params, body):
        res = self.json("DeleteRepositoryBasic", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def create_repository_basic(self, params, body):
        res = self.json("CreateRepositoryBasic", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def update_repository_basic(self, params, body):
        res = self.json("UpdateRepositoryBasic", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def get_repository_basic(self, params, body):
        res = self.json("GetRepositoryBasic", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def list_repositories_basic(self, params, body):
        res = self.json("ListRepositoriesBasic", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def delete_tag_basic(self, params, body):
        res = self.json("DeleteTagBasic", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def list_tags_basic(self, params, body):
        res = self.json("ListTagsBasic", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def get_tag_basic(self, params, body):
        res = self.json("GetTagBasic", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @ redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2, retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def get_tag_addition_basic(self, params, body):
        res = self.json("GetTagAdditionBasic", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
