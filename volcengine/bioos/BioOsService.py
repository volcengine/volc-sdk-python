# coding:utf-8
import json
import threading
from urllib.parse import urlparse

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service


class BioOsService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(BioOsService, '_instance'):
            with BioOsService._instance_lock:
                if not hasattr(BioOsService, '_instance'):
                    BioOsService._instance = object.__new__(cls)
        return BioOsService._instance

    def __init__(self, endpoint='https://open.volcengineapi.com', region='cn-beijing'):
        self.service_info = BioOsService.get_service_info(endpoint, region)
        self.api_info = BioOsService.get_api_info()
        super(BioOsService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(endpoint, region):
        parsed = urlparse(endpoint)
        scheme, hostname = parsed.scheme, parsed.hostname
        if not scheme or not hostname:
            raise Exception(f'invalid endpoint format: {endpoint}')
        service_info = ServiceInfo(hostname, {'Accept': 'application/json'},
                                   Credentials('', '', 'bio', region), 5, 5, scheme=scheme)
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            'CreateWorkspace':
                ApiInfo('POST', '/', {'Action': 'CreateWorkspace', 'Version': '2021-03-04'}, {}, {}),
            'ListWorkspaces':
                ApiInfo('POST', '/', {'Action': 'ListWorkspaces', 'Version': '2021-03-04'}, {}, {}),
            'UpdateWorkspace':
                ApiInfo('POST', '/', {'Action': 'UpdateWorkspace', 'Version': '2021-03-04'}, {}, {}),
            'DeleteWorkspace':
                ApiInfo('POST', '/', {'Action': 'DeleteWorkspace', 'Version': '2021-03-04'}, {}, {}),
            'BindClusterToWorkspace':
                ApiInfo('POST', '/', {'Action': 'BindClusterToWorkspace', 'Version': '2021-03-04'}, {}, {}),
            'UnbindClusterAndWorkspace':
                ApiInfo('POST', '/', {'Action': 'UnbindClusterAndWorkspace', 'Version': '2021-03-04'}, {}, {}),
            'ListClustersOfWorkspace':
                ApiInfo('POST', '/', {'Action': 'ListClustersOfWorkspace', 'Version': '2021-03-04'}, {}, {}),
            'CreateCluster':
                ApiInfo('POST', '/', {'Action': 'CreateCluster', 'Version': '2021-03-04'}, {}, {}),
            'ListClusters':
                ApiInfo('POST', '/', {'Action': 'ListClusters', 'Version': '2021-03-04'}, {}, {}),
            'DeleteCluster':
                ApiInfo('POST', '/', {'Action': 'DeleteCluster', 'Version': '2021-03-04'}, {}, {}),
            'CreateDataModel':
                ApiInfo('POST', '/', {'Action': 'CreateDataModel', 'Version': '2021-03-04'}, {}, {}),
            'ListDataModels':
                ApiInfo('POST', '/', {'Action': 'ListDataModels', 'Version': '2021-03-04'}, {}, {}),
            'ListDataModelRows':
                ApiInfo('POST', '/', {'Action': 'ListDataModelRows', 'Version': '2021-03-04'}, {}, {}),
            'DeleteDataModelRowsAndHeaders':
                ApiInfo('POST', '/', {'Action': 'DeleteDataModelRowsAndHeaders', 'Version': '2021-03-04'}, {}, {}),
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
            'CreateWorkflow':
                ApiInfo('POST', '/', {'Action': 'CreateWorkflow', 'Version': '2021-03-04'}, {}, {}),
            'ListWorkflows':
                ApiInfo('POST', '/', {'Action': 'ListWorkflows', 'Version': '2021-03-04'}, {}, {}),
            'UpdateWorkflow':
                ApiInfo('POST', '/', {'Action': 'UpdateWorkflow', 'Version': '2021-03-04'}, {}, {}),
            'DeleteWorkflow':
                ApiInfo('POST', '/', {'Action': 'DeleteWorkflow', 'Version': '2021-03-04'}, {}, {}),
        }
        return api_info

    def create_workspaces(self, params):
        return self.__request('CreateWorkspace', params)

    def list_workspaces(self, params):
        return self.__request('ListWorkspaces', params)

    def update_workspace(self, params):
        return self.__request('UpdateWorkspace', params)

    def delete_workspace(self, params):
        return self.__request('DeleteWorkspace', params)

    def bind_cluster_to_workspace(self, params):
        return self.__request('BindClusterToWorkspace', params)

    def unbind_cluster_and_workspace(self, params):
        return self.__request('UnbindClusterAndWorkspace', params)

    def list_clusters_of_workspace(self, params):
        return self.__request('ListClustersOfWorkspace', params)

    def create_cluster(self, params):
        return self.__request('CreateCluster', params)

    def list_clusters(self, params):
        return self.__request('ListClusters', params)

    def delete_cluster(self, params):
        return self.__request('DeleteCluster', params)

    def create_data_model(self, params):
        return self.__request('CreateDataModel', params)

    def list_data_models(self, params):
        return self.__request('ListDataModels', params)

    def list_data_model_rows(self, params):
        return self.__request('ListDataModelRows', params)

    def delete_data_model_rows_and_headers(self, params):
        return self.__request('DeleteDataModelRowsAndHeaders', params)

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

    def create_workflow(self, params):
        return self.__request('CreateWorkflow', params)

    def list_workflows(self, params):
        return self.__request('ListWorkflows', params)

    def update_workflow(self, params):
        return self.__request('UpdateWorkflow', params)

    def delete_workflow(self, params):
        return self.__request('DeleteWorkflow', params)

    def __request(self, action, params):
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception('empty response')
        res_json = json.loads(res)
        if 'Result' not in res_json.keys():
            return res_json
        return res_json['Result']
