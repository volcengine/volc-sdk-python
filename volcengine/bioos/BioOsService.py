# coding:utf-8
import json
import threading
from urllib.parse import urlparse

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service
from volcengine.const.Const import REGION_CN_NORTH1


class BioOsService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(BioOsService, '_instance'):
            with BioOsService._instance_lock:
                if not hasattr(BioOsService, '_instance'):
                    BioOsService._instance = object.__new__(cls)
        return BioOsService._instance

    def __init__(self, endpoint="https://open.volcengineapi.com", region=REGION_CN_NORTH1):
        self.service_info = BioOsService.get_service_info(endpoint, region)
        self.api_info = BioOsService.get_api_info()
        super(BioOsService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(endpoint, region):
        parsed = urlparse(endpoint)
        scheme, hostname = parsed.scheme, parsed.hostname
        if not scheme or not hostname:
            raise Exception(f"invalid endpoint format: {endpoint}")
        service_info = ServiceInfo(hostname, {'Accept': 'application/json'},
                                   Credentials('', '', 'bio', region), 5, 5, scheme=scheme)
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            'ListWorkspaces':
                ApiInfo('POST', '/', {'Action': 'ListWorkspaces', 'Version': '2021-03-04'}, {}, {}),
            'CreateDataModel':
                ApiInfo('POST', '/', {'Action': 'CreateDataModel', 'Version': '2021-03-04'}, {}, {}),
            'ListDataModels':
                ApiInfo('POST', '/', {'Action': 'ListDataModels', 'Version': '2021-03-04'}, {}, {}),
            'ListDataModelRows':
                ApiInfo('POST', '/', {'Action': 'ListDataModelRows', 'Version': '2021-03-04'}, {}, {}),
            'ListAllDataModelRowIDs':
                ApiInfo('POST', '/', {'Action': 'ListAllDataModelRowIDs', 'Version': '2021-03-04'}, {}, {}),
            'DeleteDataModelRowsAndHeaders':
                ApiInfo('POST', '/', {'Action': 'DeleteDataModelRowsAndHeaders', 'Version': '2021-03-04'}, {}, {}),
            'ListWorkflows':
                ApiInfo('POST', '/', {'Action': 'ListWorkflows', 'Version': '2021-03-04'}, {}, {}),
            'CreateSubmission':
                ApiInfo('POST', '/', {'Action': 'CreateSubmission', 'Version': '2021-03-04'}, {}, {}),
            'ListSubmissions':
                ApiInfo('POST', '/', {'Action': 'ListSubmissions', 'Version': '2021-03-04'}, {}, {}),
            'DeleteSubmission':
                ApiInfo('POST', '/', {'Action': 'DeleteSubmission', 'Version': '2021-03-04'}, {}, {}),
            'ListRuns':
                ApiInfo('POST', '/', {'Action': 'ListRuns', 'Version': '2021-03-04'}, {}, {}),
            'ListTasks':
                ApiInfo('POST', '/', {'Action': 'ListTasks', 'Version': '2021-03-04'}, {}, {}),
            'GetTOSAccess':
                ApiInfo('POST', '/', {'Action': 'GetTOSAccess', 'Version': '2021-03-04'}, {}, {}),
            'ListClustersOfWorkspace':
                ApiInfo('POST', '/', {'Action': 'ListClustersOfWorkspace', 'Version': '2021-03-04'}, {}, {}),
            'CreateWorkflow':
                ApiInfo('POST', '/', {'Action': 'CreateWorkflow', 'Version': '2021-03-04'}, {}, {}),
            'CheckCreateWorkflow':
                ApiInfo('POST', '/', {'Action': 'CheckCreateWorkflow', 'Version': '2021-03-04'}, {}, {}),
            'DeleteWorkflow':
                ApiInfo('POST', '/', {'Action': 'DeleteWorkflow', 'Version': '2021-03-04'}, {}, {}),
        }
        return api_info

    def list_workspaces(self, params):
        return self.__request('ListWorkspaces', params)

    def create_data_model(self, params):
        return self.__request('CreateDataModel', params)

    def list_data_models(self, params):
        return self.__request('ListDataModels', params)

    def list_data_model_rows(self, params):
        return self.__request('ListDataModelRows', params)

    def list_data_model_row_ids(self, params):
        return self.__request('ListAllDataModelRowIDs', params)

    def delete_data_model_rows_and_headers(self, params):
        return self.__request('DeleteDataModelRowsAndHeaders', params)

    def list_workflows(self, params):
        return self.__request('ListWorkflows', params)

    def create_submission(self, params):
        return self.__request('CreateSubmission', params)

    def list_submissions(self, params):
        return self.__request('ListSubmissions', params)

    def delete_submission(self, params):
        return self.__request('DeleteSubmission', params)

    def list_runs(self, params):
        return self.__request('ListRuns', params)

    def list_tasks(self, params):
        return self.__request('ListTasks', params)

    def get_tos_access(self, params):
        return self.__request('GetTOSAccess', params)

    def list_cluster(self, params):
        return self.__request('ListClustersOfWorkspace', params)

    def create_workflow(self, params):
        return self.__request('CreateWorkflow', params)

    def check_workflow(self, params):
        return self.__request("CheckCreateWorkflow", params)

    def delete_workflow(self, params):
        return self.__request("DeleteWorkflow", params)

    def __request(self, action, params):
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception('empty response')
        res_json = json.loads(res)
        return res_json['Result']
