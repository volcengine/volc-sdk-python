# coding:utf-8
import json
import threading

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service


class RdsPostgreSQL(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(RdsPostgreSQL, "_instance"):
            with RdsPostgreSQL._instance_lock:
                if not hasattr(RdsPostgreSQL, "_instance"):
                    RdsPostgreSQL._instance = object.__new__(cls)
        return RdsPostgreSQL._instance

    def __init__(self, region='cn-north-1'):
        self.service_info = RdsPostgreSQL.get_service_info(region)
        self.api_info = RdsPostgreSQL.get_api_info()
        self.domain_cache = {}
        self.fallback_domain_weights = {}
        self.update_interval = 10
        self.lock = threading.Lock()
        super(RdsPostgreSQL, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(region):
        service_info_map = {
            'cn-north-1': ServiceInfo("open.volcengineapi.com",
                                      {'Accept': 'application/json'},
                                      Credentials('', '', 'rds_postgresql', 'cn-north-1'), 10, 10),
        }
        service_info = service_info_map.get(region, None)
        if not service_info:
            raise Exception('Cant find the region, please check it carefully')

        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            "CreateDBInstance": ApiInfo("POST", "/", {"Action": "CreateDBInstance", "Version": "2018-01-01"}, {}, {}),
            "CreateDBInstanceIPList": ApiInfo("POST", "/", {"Action": "CreateDBInstanceIPList", "Version": "2018-01-01"}, {}, {}),
            "CreateAccount": ApiInfo("POST", "/", {"Action": "CreateAccount", "Version": "2018-01-01"}, {}, {}),
            "ModifyDatabaseOwner": ApiInfo("POST", "/", {"Action": "ModifyDatabaseOwner", "Version": "2018-01-01"}, {}, {}),
            "CreateDatabase": ApiInfo("POST", "/", {"Action": "CreateDatabase", "Version": "2018-01-01"}, {}, {}),
        }
        return api_info

    def common_handler(self, api, form):
        params = dict()
        try:
            res = self.post(api, params, form)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            res = str(e)
            try:
                res_json = json.loads(res)
                return res_json
            except:
                raise Exception(str(e))

    def common_json_handler(self, api, body):
        params = dict()
        try:
            body = json.dumps(body)
            res = self.json(api, params, body)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            res = str(e)
            try:
                res_json = json.loads(res)
                return res_json
            except:
                raise Exception(str(e))

    def create_instance(self, form):
        try:
            return self.common_json_handler("CreateDBInstance", form)
        except Exception as e:
            raise Exception(str(e))

    def create_instance_white_list(self, form):
        try:
            return self.common_json_handler("CreateDBInstanceIPList", form)
        except Exception as e:
            raise Exception(str(e))

    def create_account(self, form):
        try:
            return self.common_json_handler("CreateAccount", form)
        except Exception as e:
            raise Exception(str(e))

    def modify_database_owner(self, form):
        try:
            return self.common_json_handler("ModifyDatabaseOwner", form)
        except Exception as e:
            raise Exception(str(e))

    def create_database(self, form):
        try:
            return self.common_json_handler("CreateDatabase", form)
        except Exception as e:
            raise Exception(str(e))

