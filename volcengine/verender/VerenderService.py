# coding: utf-8
import json
import os.path
import threading

import redo

from requests import exceptions

from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo
from volcengine.ApiInfo import ApiInfo
from volcengine.verender.ftrans import FtransService

SERVICE = "verender"
VERSION = "2021-12-31"
REGION = "cn-north1"
SCHEME = "https"
CONN_TIMEOUT = 5
RECV_TIMEOUT = 5
DEFAULT_PAGE_NUM = 1
DEFAULT_PAGE_SIZE = 10


class FileInfo(object):
    def __init__(self, name, size, mtime, md5=None):
        self.name = name
        self.size = size
        self.mtime = mtime
        self.md5 = md5


class VerenderService(Service):
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(VerenderService, "_instance"):
            with VerenderService._lock:
                if not hasattr(VerenderService, "_instance"):
                    VerenderService._instance = object.__new__(cls)
        return VerenderService._instance

    def __init__(self):
        self.api_info = VerenderService.get_api_info()
        self.service_info = VerenderService.get_service_info()
        super(VerenderService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info():
        service_info = ServiceInfo(
            "open.volcengineapi.com",
            {"Accept": "application/json"},
            Credentials("", "", SERVICE, REGION),
            CONN_TIMEOUT,
            RECV_TIMEOUT,
            SCHEME
        )
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            "ListWorkspace": ApiInfo(
                "GET",
                "/",
                {"Action": "ListWorkspaces", "Version": VERSION},
                {},
                {}
            ),
            "GetStorageAccess": ApiInfo(
                "GET",
                "/",
                {"Action": "GetStorageAccess", "Version": VERSION},
                {},
                {}
            ),
            "ListDccs": ApiInfo(
                "GET",
                "/",
                {"Action": "ListDccs", "Version": VERSION},
                {},
                {}
            ),
            "ListAccountDccPlugins": ApiInfo(
                "GET",
                "/",
                {"Action": "ListAccountDccPlugins", "Version": VERSION},
                {},
                {}
            ),
            "GetCurrentUser": ApiInfo(
                "GET",
                "/",
                {"Action": "GetCurrentUser", "Version": VERSION},
                {},
                {}
            ),
            "CreateRenderJob": ApiInfo(
                "POST",
                "/",
                {"Action": "CreateRenderJob", "Version": VERSION},
                {},
                {}
            ),
            "ListRenderJob": ApiInfo(
                "GET",
                "/",
                {"Action": "ListRenderJobs", "Version": VERSION},
                {},
                {}
            ),
            "GetRenderJob": ApiInfo(
                "GET",
                "/",
                {"Action": "GetRenderJob", "Version": VERSION},
                {},
                {}
            ),
            "RetryRenderJob": ApiInfo(
                "POST",
                "/",
                {"Action": "RetryJob", "Version": VERSION},
                {},
                {}
            ),
            "ResumeRenderJobs": ApiInfo(
                "POST",
                "/",
                {"Action": "ResumeJobs", "Version": VERSION},
                {},
                {}
            ),
            "StopRenderJobs": ApiInfo(
                "POST",
                "/",
                {"Action": "StopJobs", "Version": VERSION},
                {},
                {}
            ),
            "DeleteRenderJobs": ApiInfo(
                "POST",
                "/",
                {"Action": "DeleteJobs", "Version": VERSION},
                {},
                {}
            ),
            "FullSpeedRenderJobs": ApiInfo(
                "POST",
                "/",
                {"Action": "FullSpeedRenderJobs", "Version": VERSION},
                {},
                {}
            ),
            "AutoAllRenderJobs": ApiInfo(
                "POST",
                "/",
                {"Action": "AutoAllRenderJobs", "Version": VERSION},
                {},
                {}
            ),
            "UpdateRenderJobsPriority": ApiInfo(
                "POST",
                "/",
                {"Action": "UpdateRenderJobsPriority", "Version": VERSION},
                {},
                {}
            ),
            "ListJobOutput": ApiInfo(
                "POST",
                "/",
                {"Action": "ListJobOutput", "Version": VERSION},
                {},
                {}
            ),
            "GetJobOutput": ApiInfo(
                "POST",
                "/",
                {"Action": "GetJobOutput", "Version": VERSION},
                {},
                {}
            ),
            "UpdateJobOutput": ApiInfo(
                "POST",
                "/",
                {"Action": "UpdateJobOutput", "Version": VERSION},
                {},
                {}
            ),
            "ListCellSpec": ApiInfo(
                "GET",
                "/",
                {"Action": "ListCellSpecs", "Version": VERSION},
                {},
                {}
            ),
            "AddRenderSetting": ApiInfo(
                "POST",
                "/",
                {"Action": "AddRenderSetting", "Version": VERSION},
                {},
                {}
            ),
            "UpdateRenderSetting": ApiInfo(
                "POST",
                "/",
                {"Action": "UpdateRenderSetting", "Version": VERSION},
                {},
                {}
            ),
            "DeleteRenderSetting": ApiInfo(
                "POST",
                "/",
                {"Action": "DeleteRenderSetting", "Version": VERSION},
                {},
                {}
            ),
            "ListRenderSetting": ApiInfo(
                "GET",
                "/",
                {"Action": "GetRenderSettingList", "Version": VERSION},
                {},
                {}
            ),
            "GetRenderSetting": ApiInfo(
                "GET",
                "/",
                {"Action": "GetRenderSetting", "Version": VERSION},
                {},
                {}
            ),
            "GetPluginList": ApiInfo(
                "GET",
                "/",
                {"Action": "GetPlugins", "Version": VERSION},
                {},
                {}
            )
        }
        return api_info

    @staticmethod
    def _get_ftrans_client(storage):
        addr = storage["ftrans_s10_server"]
        bucket = storage["bucket_name"]
        ftrans_security_token = storage["ftrans_security_token"]
        ftrans_cert_pem = storage["cert_pem"]
        ftrans_key_pem = storage["private_key_pem"]
        ftrans_server_name = storage["ftrans_cert_name"]

        cli = FtransService(bucket, ftrans_security_token, ftrans_server_name, addr, ftrans_cert_pem, ftrans_key_pem)
        return cli

    @redo.retriable(retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout, exceptions.ReadTimeout),
                    sleeptime=0.1, jitter=0.01, attempts=2)
    def _call_json(self, api, params=None, body=None, with_meta=False):
        params = params or {}
        body = body or {}
        body = json.dumps(body)
        resp = self.json(api, params, body)
        if "" == resp:
            raise Exception("empty response")
        resp_json = json.loads(resp)
        if resp_json.get("ResponseMetadata", {}).get("Error", {}).get("CodeN", 0) != 0:
            raise Exception(resp)
        if with_meta:
            result = resp_json
        else:
            result = resp_json.get("Result", "")
        return result

    @redo.retriable(retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout, exceptions.ReadTimeout),
                    sleeptime=0.1, jitter=0.01, attempts=2)
    def _call_get(self, api, params=None, with_meta=False):
        params = params or {}
        resp = self.get(api, params=params)
        if "" == resp:
            raise Exception("empty response")
        resp_json = json.loads(resp)
        if resp_json.get("ResponseMetadata", {}).get("Error", {}).get("CodeN", 0) != 0:
            raise Exception(resp)
        if with_meta:
            result = resp_json
        else:
            result = resp_json.get("Result", "")
        return result

    @redo.retriable(retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout, exceptions.ReadTimeout),
                    sleeptime=0.1, jitter=0.01, attempts=2)
    def _call_post(self, api, params=None, form=None):
        params = params or {}
        form = form or {}
        resp = self.post(api, params=params, form=form)
        if "" == resp:
            raise Exception("empty response")

        return resp

    def list_workspace(self, params=None):
        return self._call_get("ListWorkspace", params=params)

    def get_storage_access(self, params=None):
        return self._call_get("GetStorageAccess", params=params)

    def get_current_user(self):
        return self._call_get("GetCurrentUser", params=None)

    @staticmethod
    def to_slash(src):
        path = os.path.normpath(src)
        new = path.replace(":\\", "/").replace("\\", "/")
        if new[0] == '/':
            return new[1:]
        else:
            return new

    @staticmethod
    def get_des_file_path(filename, src_path, des_path):
        filename = VerenderService.to_slash(filename)
        src_path = VerenderService.to_slash(src_path)
        des_path = VerenderService.to_slash(des_path)

        if src_path[-1] != '/':
            src_path = src_path + "/"

        if des_path[-1] != '/':
            des_path = des_path + "/"

        return des_path + filename[len(src_path):]

    @staticmethod
    def list_dir(dir_name, max_depth=50):
        if max_depth <= 0:
            raise Exception("too deep dir %s" % dir_name)

        local_files = []
        files = os.listdir(dir_name)
        if len(files) == 0:
            local_files.append(dir_name)

        for f in files:
            full_path = os.path.join(dir_name, f)
            if os.path.isfile(full_path):
                local_files.append(full_path)
            else:
                subs = VerenderService.list_dir(full_path, max_depth-1)
                for e in subs:
                    local_files.append(e)

        return local_files

    def upload_file(self, workspace_id, src, des):
        params = {
            "WorkspaceId": workspace_id
        }
        storage = self.get_storage_access(params=params)
        cli = VerenderService._get_ftrans_client(storage)
        des = self.to_slash(des)

        try:
            name, size, mtime, md5 = cli.upload_file(src, des)
            return FileInfo(name, size, mtime, md5)
        except Exception as ex:
            raise ex
        finally:
            cli.clean()

    def upload_folder(self, workspace_id, src_path, des_path):
        params = {
            "WorkspaceId": workspace_id
        }
        storage = self.get_storage_access(params=params)
        cli = VerenderService._get_ftrans_client(storage)

        try:
            local_files = VerenderService.list_dir(src_path)

            file_info_list = []

            for f in local_files:
                des = self.get_des_file_path(f, src_path, des_path)
                info = cli.upload_file(f, des)
                file_info_list.append(info)

            return file_info_list
        except Exception as ex:
            raise ex
        finally:
            cli.clean()

    def download_file(self, workspace_id, src, dst):
        params = {
            "WorkspaceId": workspace_id
        }
        storage = self.get_storage_access(params=params)
        cli = VerenderService._get_ftrans_client(storage)

        try:
            name, size, mtime, md5 = cli.download_file(dst, src)
            return FileInfo(name, size, mtime, md5)
        except Exception as ex:
            raise ex
        finally:
            cli.clean()

    def list_file(self, workspace_id, prefix, filter_in=None, order_type=None, order_field=None,
                  page_num=None, page_size=None):

        params = {
            "WorkspaceId": workspace_id
        }
        storage = self.get_storage_access(params=params)
        cli = VerenderService._get_ftrans_client(storage)
        try:
            resp = cli.list_file(prefix,
                                filter_in=filter_in,
                                order_type=order_type,
                                order_field=order_field,
                                page_num=page_num,
                                page_size=page_size)
            return resp
        except Exception as ex:
            raise ex
        finally:
            cli.clean()

    def stat_file(self, workspace_id, filename):
        params = {
            "WorkspaceId": workspace_id
        }
        storage = self.get_storage_access(params=params)
        cli = self._get_ftrans_client(storage)

        try:
            size, mtime = cli.get_file_size(filename)
            resp = FileInfo(filename, size, mtime)
            return resp
        except Exception as ex:
            raise ex
        finally:
            cli.clean()

    def remove_file(self, workspace_id, filename):
        params = {
            "WorkspaceId": workspace_id
        }
        storage = self.get_storage_access(params=params)
        cli = self._get_ftrans_client(storage)

        try:
            return cli.remove_file(filename)
        except Exception as ex:
            raise ex
        finally:
            cli.clean()

    def list_cell_spec(self, params=None):
        resp = self._call_get("ListCellSpec", params=params)
        return resp

    def create_render_job(self, params, body):
        resp = self._call_json("CreateRenderJob", params=params, body=body)
        return resp

    def list_render_job(self, params):
        resp = self._call_get("ListRenderJob", params=params)
        return resp

    def get_render_job(self, params):
        resp = self._call_get("GetRenderJob", params=params)
        return resp

    def retry_render_job(self, params, body):
        resp = self._call_json("RetryRenderJob", params=params, body=body, with_meta=True)
        return resp

    def auto_full_speed_render_jobs(self, params, body):
        resp = self._call_json("AutoAllRenderJobs", params=params, body=body, with_meta=True)
        return resp

    def resume_render_jobs(self, params, body):
        resp = self._call_json("ResumeRenderJobs", params=params, body=body, with_meta=True)
        return resp

    def stop_render_jobs(self, params, body):
        resp = self._call_json("StopRenderJobs", params=params, body=body, with_meta=True)
        return resp

    def delete_render_jobs(self, params, body):
        resp = self._call_json("DeleteRenderJobs", params=params, body=body, with_meta=True)
        return resp

    def full_speed_render_jobs(self, params, body):
        resp = self._call_json("FullSpeedRenderJobs", params=params, body=body, with_meta=True)
        return resp

    def update_render_jobs_priority(self, params, body):
        resp = self._call_json("UpdateRenderJobsPriority", params=params, body=body, with_meta=True)
        return resp

    def list_job_output(self, params, body=None):
        resp = self._call_json("ListJobOutput", params=params, body=body)
        return resp

    def get_job_output(self, params, body=None):
        resp = self._call_json("GetJobOutput", params=params, body=body)
        return resp

    def update_job_output(self, params, body=None):
        resp = self._call_json("UpdateJobOutput", params=params, body=body, with_meta=True)
        return resp

    def add_render_setting(self, params, body):
        resp = self._call_json("AddRenderSetting", params=params, body=body)
        return resp

    def update_render_setting(self, params, body):
        resp = self._call_json("UpdateRenderSetting", params=params, body=body, with_meta=True)
        return resp

    def delete_render_setting(self, params):
        resp = self._call_json("DeleteRenderSetting", params=params, with_meta=True)
        return resp

    def list_dcc(self):
        resp = self._call_get("ListDccs")
        return resp

    def list_render_setting(self, params):
        resp = self._call_get("ListRenderSetting", params=params)
        return resp

    def get_render_setting(self, params):
        resp = self._call_get("GetRenderSetting", params=params)
        return resp["Settings"][0]

    def list_account_dcc_plugin(self, params):
        resp = self._call_get("ListAccountDccPlugins", params=params)
        return resp