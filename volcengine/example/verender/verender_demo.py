# coding: utf-8

import time

from volcengine.verender.VerenderService import VerenderService


class VerenderDemo:
    def __init__(self, verender):
        self._verender = verender

    def list_workspace_demo(self):
        params = {
            "PageNum": 1,
            "PageSize": 10
        }
        resp = self._verender.list_workspace(params)
        print(resp)

    def get_current_user_demo(self):
        resp = self._verender.get_current_user()
        print(resp)

    def upload_file_demo(self):
        f = self._verender.upload_file(1993, "D:\\tests\\test_upload_file\\test_upload_file.txt", "D:\\tests\\test_upload_file\\test_upload_file.txt")
        print(f.name, f.size, f.mtime, f.md5)

    def upload_folder_demo(self):
        file_info_list = self._verender.upload_folder(1993, "D:\\tests\\test_upload_folder", "D:\\tests\\test_upload_folder")
        print(file_info_list)

    def list_file_demo(self):
        total, file_info_list = self._verender.list_file(1993, "D/tests")
        print(total, file_info_list)

    def stat_file_demo(self):
        f = self._verender.stat_file(1993, "D/tests/test_upload_file/test_upload_file.txt")
        print(f.name, f.size, f.mtime, f.md5)

    def remove_file_demo(self):
        f = self._verender.remove_file(1993, "D/tests/test_upload_file/test_upload_file.txt")
        print(f)

    def download_file_demo(self):
        f = self._verender.download_file(735, "D/tests/test_upload_folder/test_upload_file234", "D:\\tests\\abcd.txt")
        print(f.name, f.size, f.mtime, f.md5)

    def list_cell_spec_demo(self):
        params = {
            "WorkspaceId": 735
        }
        resp = self._verender.list_cell_spec(params=params)
        print(resp)

    def add_render_setting_demo(self):
        user = self._verender.get_current_user()
        params = {
            "WorkspaceId": 1993
        }
        body = {
            "AccountId": user["AccountId"],
            "UserId": user["UserId"],
            "WorkspaceId": 1993,
            "Name": "test-render-setting-2111",
            "Dcc": "maya",
            "DccVersion": "2022.3",
            "Plugins": [
                {
                    "Name": "mtoa",
                    "Version": "5.1.3",
                    "RenderPlugin": True,
                    "NeedLicense": True
                }
            ],
            "RenderLayerMode": "LegacyRenderLayer",
            "ProjectPath": "",
            "FrameOneCell": 1,
            "CellSpecId": 15
        }
        resp = self._verender.add_render_setting(params=params, body=body)
        print(resp)

    def update_render_setting_demo(self):
        user = self._verender.get_current_user()
        params = {
            "WorkspaceId": 1993,
            "RenderSettingId": 360
        }

        body = {
            "AccountId": user["AccountId"],
            "UserId": user["UserId"],
            "WorkspaceId": 1993,
            "Name": "test-render-setting-1",
            "Dcc": "maya",
            "DccVersion": "2022",
            "Plugins": [
                {
                    "Name": "mtoa",
                    "Version": "5.1.2",
                    "RenderPlugin": True,
                    "NeedLicense": True
                }
            ],
            "RenderLayerMode": "LegacyRenderLayer",
            "ProjectPath": "",
            "FrameOneCell": 2,
            "CellSpecId": 9
        }

        resp = self._verender.update_render_setting(params=params, body=body)
        print(resp)

    def delete_render_setting_demo(self):
        params = {
            "WorkspaceId": 1993,
            "RenderSettingId": 361
        }
        resp = self._verender.delete_render_setting(params=params)
        print(resp)

    def list_dcc_demo(self):
        resp = self._verender.list_dcc()
        print(resp)

    def list_account_dcc_plugins_demo(self):
        params = {
            "SpecTemplateId": 15,
            "Dcc": "maya",
            "DccVersion": "2022.3"
        }
        
        resp = self._verender.list_account_dcc_plugin(params=params)
        print(resp)

    def list_render_setting_demo(self):
        user = self._verender.get_current_user()
        params = {
            "AccountId": user["AccountId"],
            "UserId": user["UserId"],
            "WorkspaceId": 1993,
            "Dcc": "maya"
        }
        resp = self._verender.list_render_setting(params=params)
        print(resp)

    def get_render_setting_demo(self):
        user = self._verender.get_current_user()
        params = {
            "AccountId": user["AccountId"],
            "UserId": user["UserId"],
            "WorkspaceId": 1993,
            "Id": 360
        }
        resp = self._verender.get_render_setting(params=params)
        print(resp)

    def create_render_job_demo(self):
        workspace_id = 1993
        params = {
            "WorkspaceId": workspace_id,
        }

        # upload file
        obj = self._verender.upload_file(workspace_id, "D:\\car-studio\\Studio_Top.ma", "D:\\car-studio\\Studio_Top.ma")

        # get render setting
        user = self._verender.get_current_user()
        p = {
            "AccountId": user["AccountId"],
            "UserId": user["UserId"],
            "WorkspaceId": workspace_id,
            "CheckUserId": False,
            "WithDeleted": True,
            "Id": 368
        }
        rs = self._verender.get_render_setting(params=p)

        body = {
            "Title": "test-create-render-job",
            "Description": "volc-sdk-python",
            "Tryout": False,
            "SceneFile": obj.name,
            "TimeoutReminderEachFrame": 86400,
            "TimeoutStopperEachFrame": 86400,
            "LayerConfig": [
                {
                    "LayerIndex": 0,
                    "LayerName": "masterLayer",
                    "Frame": {
                        "Start": 1,
                        "End": 10,
                        "Step": 1
                    },
                    "Resolutions": {
                        "Height": 1080,
                        "Width": 1920
                    },
                    "Cameras": ["文件内设置"],
                    "PluginData": "{}",
                    "Renderer": "mtoa"
                }
            ],
            "RenderSetting": rs,
            "FramesCountEachCell": 8
        }
        resp = self._verender.create_render_job(params=params, body=body)
        print(resp)

    def list_render_job_demo(self):
        params = {
            "WorkspaceId": 1993
        }
        resp = self._verender.list_render_job(params=params)
        print(resp)

    def get_render_job_demo(self):
        params = {
            "WorkspaceId": 1993,
            "RenderJobId": "r776bf384a4"
        }
        resp = self._verender.get_render_job(params=params)
        print(resp)

    def retry_render_job_demo(self):
        params = {
            "WorkspaceId": 1993,
            "RenderJobId": "r5ad3829bef"
        }
        body = {
            "JobId": "r5ad3829bef",
            "AllFailedFrames": True,
            "CustomFrames": [
                {
                    "LayerIndex": 0,
                    "FrameIndexes": "1-5"
                }
            ]
        }
        resp = self._verender.retry_render_job(params=params, body=body)
        print(resp)

    def resume_render_jobs_demo(self):
        params = {
            "WorkspaceId": 1993
        }
        body = {
            "JobIds": [
                "r776bf384a4"
            ]
        }
        resp = self._verender.resume_render_jobs(params=params, body=body)
        print(resp)

    def stop_render_jobs_demo(self):
        params = {
            "WorkspaceId": 1993
        }
        body = {
            "JobIds": [
                "r003ebaa720"
            ]
        }
        resp = self._verender.stop_render_jobs(params=params, body=body)
        print(resp)

    def delete_render_jobs_demo(self):
        params = {
            "WorkspaceId": 1993
        }
        body = {
            "JobIds": [
                "r003ebaa720"
            ]
        }
        resp = self._verender.delete_render_jobs(params=params, body=body)
        print(resp)

    def full_speed_render_jobs_demo(self):
        params = {
            "WorkspaceId": 1993
        }
        body = {
            "JobIds": [
                "r90ea40ecbd",
                "r041853ab30"
            ]
        }
        resp = self._verender.full_speed_render_jobs(params=params, body=body)
        print(resp)

    def auto_full_speed_render_jobs_demo(self):
        params = {
            "WorkspaceId": 19931
        }

        body = {
            "JobIds": [
                "r377a81d87e"
            ]
        }
        resp = self._verender.auto_full_speed_render_jobs(params, body)
        print(resp)

    def update_render_jobs_priority_demo(self):
        params = {
            "WorkspaceId": 1993
        }
        body = {
            "JobIds": [
                "r90ea40ecbd",
                "r041853ab30"
            ],
            "Priority": 10
        }
        resp = self._verender.update_render_jobs_priority(params=params, body=body)
        print(resp)

    def list_job_output_demo(self):
        params = {
            "WorkspaceId": 1802
        }
        body = {}
        resp = self._verender.list_job_output(params=params, body=body)
        print(resp)

    def get_job_output_demo(self):
        params = {
            "WorkspaceId": 1802,
            "JobId": "rf19285eae5"
        }
        body = {}
        resp = self._verender.get_job_output(params=params, body=body)
        print(resp)

    def update_job_output_demo(self):
        params = {
            "WorkspaceId": 1802,
            "JobId": "abc"
        }
        body = {
            "files": [
                "Result/test-create-render-job_rf19285eae5/images/simple.exr.0001"
            ]
        }
        resp = self._verender.update_job_output(params=params, body=body)
        print(resp)


if __name__ == "__main__":
    v = VerenderService()
    v.set_ak("your ak")
    v.set_sk("your sk")

    vd = VerenderDemo(v)

    vd.upload_file_demo()
    vd.upload_folder_demo()
    vd.download_file_demo()
    vd.list_file_demo()
    vd.stat_file_demo()
    vd.remove_file_demo()
    vd.get_current_user_demo()
    vd.list_workspace_demo()
    vd.create_render_job_demo()
    vd.list_render_job_demo()
    vd.get_render_job_demo()
    vd.retry_render_job_demo()
    vd.resume_render_jobs_demo()
    vd.stop_render_jobs_demo()
    vd.delete_render_jobs_demo()
    vd.full_speed_render_jobs_demo()
    vd.update_render_jobs_priority_demo()
    vd.list_job_output_demo()
    vd.get_job_output_demo()
    vd.update_job_output_demo()
    vd.list_cell_spec_demo()
    vd.add_render_setting_demo()
    vd.update_render_setting_demo()
    vd.delete_render_setting_demo()
    vd.list_render_setting_demo()
    vd.get_render_setting_demo()
    vd.list_dcc_demo()
    vd.list_account_dcc_plugins_demo()
