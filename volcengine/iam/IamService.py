# coding:utf-8
import json
import threading

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo


class IamService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(IamService, "_instance"):
            with IamService._instance_lock:
                if not hasattr(IamService, "_instance"):
                    IamService._instance = object.__new__(cls)
        return IamService._instance

    def __init__(self):
        self.service_info = IamService.get_service_info()
        self.api_info = IamService.get_api_info()
        super(IamService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info():
        service_info = ServiceInfo("iam.volcengineapi.com", {'Accept': 'application/json'},
                                   Credentials('', '', 'iam', 'cn-north-1'), 5, 5)
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            # Access Key
            "CreateAccessKey": ApiInfo("GET", "/", {"Action": "CreateAccessKey", "Version": "2018-01-01"}, {}, {}),
            "DeleteAccessKey": ApiInfo("GET", "/", {"Action": "DeleteAccessKey", "Version": "2018-01-01"}, {}, {}),
            "ListAccessKeys": ApiInfo("GET", "/", {"Action": "ListAccessKeys", "Version": "2018-01-01"}, {}, {}),
            "UpdateAccessKey": ApiInfo("GET", "/", {"Action": "UpdateAccessKey", "Version": "2018-01-01"}, {}, {}),
            # User
            "CreateUser": ApiInfo("GET", "/", {"Action": "CreateUser", "Version": "2018-01-01"}, {}, {}),
            "GetUser": ApiInfo("GET", "/", {"Action": "GetUser", "Version": "2018-01-01"}, {}, {}),
            "UpdateUser": ApiInfo("GET", "/", {"Action": "UpdateUser", "Version": "2018-01-01"}, {}, {}),
            "ListUsers": ApiInfo("GET", "/", {"Action": "ListUsers", "Version": "2018-01-01"}, {}, {}),
            "DeleteUser": ApiInfo("GET", "/", {"Action": "DeleteUser", "Version": "2018-01-01"}, {}, {}),
            "CreateLoginProfile": ApiInfo("GET", "/", {"Action": "CreateLoginProfile", "Version": "2018-01-01"}, {}, {}),
            "GetLoginProfile": ApiInfo("GET", "/", {"Action": "GetLoginProfile", "Version": "2018-01-01"}, {}, {}),
            "UpdateLoginProfile": ApiInfo("GET", "/", {"Action": "UpdateLoginProfile", "Version": "2018-01-01"}, {}, {}),
            "DeleteLoginProfile": ApiInfo("GET", "/", {"Action": "DeleteLoginProfile", "Version": "2018-01-01"}, {}, {}),
            # Role
            "CreateRole": ApiInfo("GET", "/", {"Action": "CreateRole", "Version": "2018-01-01"}, {}, {}),
            "GetRole": ApiInfo("GET", "/", {"Action": "GetRole", "Version": "2018-01-01"}, {}, {}),
            "UpdateRole": ApiInfo("GET", "/", {"Action": "UpdateRole", "Version": "2018-01-01"}, {}, {}),
            "ListRoles": ApiInfo("GET", "/", {"Action": "ListRoles", "Version": "2018-01-01"}, {}, {}),
            "DeleteRole": ApiInfo("GET", "/", {"Action": "DeleteRole", "Version": "2018-01-01"}, {}, {}),
            "CreateServiceLinkedRole": ApiInfo("GET", "/", {"Action": "CreateServiceLinkedRole", "Version": "2018-01-01"}, {}, {}),
            # Identity Provider
            "CreateSAMLProvider": ApiInfo("POST", "/", {"Action": "CreateSAMLProvider", "Version": "2018-01-01"}, {}, {}),
            "GetSAMLProvider": ApiInfo("GET", "/", {"Action": "GetSAMLProvider", "Version": "2018-01-01"}, {}, {}),
            "UpdateSAMLProvider": ApiInfo("POST", "/", {"Action": "UpdateSAMLProvider", "Version": "2018-01-01"}, {}, {}),
            "ListSAMLProviders": ApiInfo("GET", "/", {"Action": "ListSAMLProviders", "Version": "2018-01-01"}, {}, {}),
            "DeleteSAMLProvider": ApiInfo("GET", "/", {"Action": "DeleteSAMLProvider", "Version": "2018-01-01"}, {}, {}),
            # Policy
            "CreatePolicy": ApiInfo("GET", "/", {"Action": "CreatePolicy", "Version": "2018-01-01"}, {}, {}),
            "GetPolicy": ApiInfo("GET", "/", {"Action": "GetPolicy", "Version": "2018-01-01"}, {}, {}),
            "ListPolicies": ApiInfo("GET", "/", {"Action": "ListPolicies", "Version": "2018-01-01"}, {}, {}),
            "UpdatePolicy": ApiInfo("GET", "/", {"Action": "UpdatePolicy", "Version": "2018-01-01"}, {}, {}),
            "DeletePolicy": ApiInfo("GET", "/", {"Action": "DeletePolicy", "Version": "2018-01-01"}, {}, {}),
            "AttachUserPolicy": ApiInfo("GET", "/", {"Action": "AttachUserPolicy", "Version": "2018-01-01"}, {}, {}),
            "DetachUserPolicy": ApiInfo("GET", "/", {"Action": "DetachUserPolicy", "Version": "2018-01-01"}, {}, {}),
            "ListAttachedUserPolicies": ApiInfo("GET", "/", {"Action": "ListAttachedUserPolicies", "Version": "2018-01-01"}, {}, {}),
            "AttachRolePolicy": ApiInfo("GET", "/", {"Action": "AttachRolePolicy", "Version": "2018-01-01"}, {}, {}),
            "DetachRolePolicy": ApiInfo("GET", "/", {"Action": "DetachRolePolicy", "Version": "2018-01-01"}, {}, {}),
            "ListAttachedRolePolicies": ApiInfo("GET", "/", {"Action": "ListAttachedRolePolicies", "Version": "2018-01-01"}, {}, {}),
            "ListEntitiesForPolicy": ApiInfo("GET", "/", {"Action": "ListEntitiesForPolicy", "Version": "2018-01-01"}, {}, {}),
        }
        return api_info

    # Access Key

    def create_access_key(self, params):
        res = self.get("CreateAccessKey", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def delete_access_key(self, params):
        res = self.get("DeleteAccessKey", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def list_access_keys(self, params):
        res = self.get("ListAccessKeys", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def update_access_key(self, params):
        res = self.get("UpdateAccessKey", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    # User

    def create_user(self, params):
        res = self.get("CreateUser", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def get_user(self, params):
        res = self.get("GetUser", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def update_user(self, params):
        res = self.get("UpdateUser", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def list_users(self, params):
        res = self.get("ListUsers", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
    
    def delete_user(self, params):
        res = self.get("DeleteUser", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def create_login_profile(self, params):
        res = self.get("CreateLoginProfile", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def get_login_profile(self, params):
        res = self.get("GetLoginProfile", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def update_login_profile(self, params):
        res = self.get("UpdateLoginProfile", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def delete_login_profile(self, params):
        res = self.get("DeleteLoginProfile", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    # Role

    def create_role(self, params):
        res = self.get("CreateRole", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def get_role(self, params):
        res = self.get("GetRole", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def update_role(self, params):
        res = self.get("UpdateRole", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def list_roles(self, params):
        res = self.get("ListRoles", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def delete_role(self, params):
        res = self.get("DeleteRole", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
    
    def create_service_linked_role(self, params):
        res = self.get("CreateServiceLinkedRole", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    # Identity Provider

    def create_saml_provider(self, params):
        res = self.post("CreateSAMLProvider", {}, params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def get_saml_provider(self, params):
        res = self.get("GetSAMLProvider", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def update_saml_provider(self, params):
        res = self.post("UpdateSAMLProvider", {}, params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def list_saml_providers(self, params):
        res = self.get("ListSAMLProviders", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def delete_saml_provider(self, params):
        res = self.get("DeleteSAMLProvider", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    # Policy

    def create_policy(self, params):
        res = self.get("CreatePolicy", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def get_policy(self, params):
        res = self.get("GetPolicy", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def list_policies(self, params):
        res = self.get("ListPolicies", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def update_policy(self, params):
        res = self.get("UpdatePolicy", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def delete_policy(self, params):
        res = self.get("DeletePolicy", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def attach_user_policy(self, params):
        res = self.get("AttachUserPolicy", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def detach_user_policy(self, params):
        res = self.get("DetachUserPolicy", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def list_attached_user_policies(self, params):
        res = self.get("ListAttachedUserPolicies", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def attach_role_policy(self, params):
        res = self.get("AttachRolePolicy", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def detach_role_policy(self, params):
        res = self.get("DetachRolePolicy", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def list_attached_role_policies(self, params):
        res = self.get("ListAttachedRolePolicies", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def list_entities_for_policy(self, params):
        res = self.get("ListEntitiesForPolicy", params)
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
