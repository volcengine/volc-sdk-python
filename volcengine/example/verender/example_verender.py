#coding: utf-8

from volcengine.verender.VerenderService import VerenderService

class VerenderExample(object):
    def __init__(self, ak, sk):
        self.verender = VerenderService()
        if ak and sk:
            self.verender.set_ak(ak)
            self.verender.set_sk(sk)

    def list_all_workspace(self):
        resp = self.verender.list_workspaces()
        print(resp)

    def list_one_workspace(self):
        resp = self.verender.list_workspaces(workspace_id=1442)
        print(resp)

    def purchase_one_workspace(self):
        title = "workspace_name"
        description = "workspace_description"
        storage_total = 200 * 1024 * 1024 * 1024

        available_resource_pools = self.verender.list_resource_pools()["Result"]
        resource_pool_id = available_resource_pools[0]["ResourcePoolId"]
        cps_id = available_resource_pools[0]["CpsId"]
        resp = self.verender.purchase_workspace(title, description, storage_total, resource_pool_id, cps_id)
        print(resp)

    def update_one_workspace(self):
        workspace_id = 1532
        title = "new_workspace_name"
        description = "new_workspace_description"
        storage_total = 300 * 1024 * 1024 * 1024
        resp = self.verender.update_workspace(workspace_id, title, description, storage_total)
        print(resp)

    def get_last_day_account_statistics(self):
        resp = self.verender.get_account_statistics("last_day")
        print(resp["Result"])

    def get_last_week_account_statistics(self):
        resp = self.verender.get_account_statistics("last_week")
        print(resp["Result"])

    def get_accout_statistics_by_start_and_end(self):
        start_time = "2022-05-01T00:00:00+08:00"
        end_time = "2022-05-15T00:00:00+08:00"
        resp = self.verender.get_account_statistics("by_day", start_time=start_time, end_time=end_time)
        print(resp)

    def get_all_account_statistic_detail(self):
        start_time = "2022-05-01T00:00:00+08:00"
        end_time = "2022-05-15T00:00:00+08:00"
        resp = self.verender.get_account_statistic_detail(start_time, end_time)
        print(resp["Result"])

    def download_all_statistic_details(self):
        start_time = "2022-05-01T00:00:00+08:00"
        end_time = "2022-05-15T00:00:00+08:00"
        save_file = "/tmp/1.log"
        self.verender.download_statistic_details(start_time, end_time, save_file)

    def download_one_workspace_statistic_details(self):
        start_time = "2022-05-01T00:00:00+08:00"
        end_time = "2022-05-15T00:00:00+08:00"
        save_file = "/tmp/2.log"
        workspace_ids = [1534]
        self.verender.download_statistic_details(start_time, end_time, save_file, workspace_ids=workspace_ids)

    def create_one_render_job(self):
        workspace_id = 1442
        user_info = self.verender.get_current_user()["Result"]
        scene_file = self.verender.upload_file(workspace_id, ["/tmp/test.ma"])[0]
        render_job_cfg = {
            'UserName': user_info['UserName'],
            'Title': 'test-render-job-1',
            'DccTool': 'maya',
            'DccVersion': '',
            'Renderer': 'redshift',
            'RendererVersion': '',
            'SceneFile': scene_file,
            'Tryout': False,
            'TryoutFrames': [1, 2, 3],
            'OutputFormat': 'PNG',
            'Cameras': [
                'front'
            ],
            'Layers': [
                'legacy_layer'
            ]
        }

        resp = self.verender.create_render_job(workspace_id, render_job_cfg)
        print(resp)

    def list_all_render_jobs(self):
        workspace_id = 1442
        resp = self.verender.list_render_jobs(workspace_id)
        print(resp["Result"])

    def list_maya_render_jobs(self):
        workspace_id = 1442
        job_type = "maya_redshift"
        resp = self.verender.list_render_jobs(workspace_id, job_type=job_type)
        print(resp["Result"])

    def get_one_layer_frames(self):
        workspace_id = 1442
        job_id = "r2c311d776e"
        layer_requests = {
            'LayerRequests': [
                {
                    'LayerIndex': 0,
                    'PageNum': 1,
                    'PageSize': 10,
                    'Statuses': []
                }
            ]
        }
        resp = self.verender.get_layer_frames(workspace_id, job_id, layer_requests)
        print(resp)


if __name__ == "__main__":
    v = VerenderExample("Your ak", "Your sk")

    #v.list_all_workspace()
    #v.list_one_workspace()
    #v.purchase_one_workspace()
    #v.update_one_workspace()
    #v.get_last_day_account_statistics()
    #v.get_last_week_account_statistics()
    #v.get_accout_statistics_by_start_and_end()
    #v.get_all_account_statistic_detail()
    #v.download_all_statistic_details()
    #v.download_one_workspace_statistic_details()
    v.create_one_render_job()
    #v.list_all_render_jobs()
    #v.list_maya_render_jobs()
    #v.get_one_layer_frames()