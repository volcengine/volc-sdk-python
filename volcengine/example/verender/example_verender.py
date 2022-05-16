#coding: utf-8

import VerenderService


class TestVerenderService(object):
    verender = VerenderService.VerenderService()
    verender.set_ak("Your AK")
    verender.set_sk("Your SK")

    def test_list_workspaces(self):
        #print(self.verender.list_workspaces())
        #print(self.verender.list_workspaces(workspace_id=1))
        print(self.verender.list_workspaces(fuzzy_search_content="test"))

    def test_purchase_workspace(self):
        print(self.verender.purchase_workspace('test-2', '', 150 << 30, 1, 1))

    def test_delete_workspace(self):
        print(self.verender.delete_workspace(400))

    def test_update_workspace(self):
        print(self.verender.update_workspace(1, 'test_update_2', 'update', 200 << 30))

    def test_get_storage_access(self):
        print(self.verender.get_storage_access(1))

    def test_get_workspace_limit(self):
        print(self.verender.get_workspace_limit())

    def test_list_resource_pool(self):
        print(self.verender.list_resource_pools())

    def test_get_workspace_hardware_specifications(self):
        print(self.verender.get_workspace_hardware_specifications(1))

    def test_get_account_statistics(self):
        print(self.verender.get_account_statistics("last_week", workspace_ids=[1,2]))

    def test_get_account_statistic_details(self):
        print(self.verender.get_account_statistic_detail('2022-05-08T00:00:00+08:00', '2022-05-08T23:59:59+08:00', 
            order_by="TotalCost", workspace_ids=[1], user_ids=[0], job_types=["maya_redshift"]))

    def test_download_statistic_details(self):
        self.verender.download_statistic_details('2022-05-08T00:00:00+08:00', '2022-05-08T23:59:59+08:00', '/tmp/abc1.log', job_types=['maya_redshift'])

    def test_get_current_user(self):
        print(self.verender.get_current_user())

    def test_get_job_overall_statistics(self):
        print(self.verender.get_job_overall_statistics())

    def test_create_render_job(self):
        render_job_cfg = {
            'UserName': 'username',
            'Title': 'test-render-job-1',
            'DccTool': 'maya',
            'Renderer': 'redshift',
            'Tryout': False,
            'TryoutFrameNumbers': ['1'],
            'OutputFormat': 'PNG',
            #'PathMapping': {},
            #'MayaProjectPath': '',
            #'Resolutions': [
            #    {
            #        'Width': 1024,
            #        'Height': 768
            #    }
            #],
            #'FrameSettings': {
            #    'Start': 1,
            #    'End': 20,
            #    'Step': 1
            #},
            'Cameras': [
                #'top',
                #'front',
                'side'
            ],
            'Layers': [
                'legacy_layer'
            ],
            'TimeoutReminder': 3600,
            'TimeoutStopper': 7200,
            #'OutputImageTemple': {
            #    'Padding': 4,
            #    'ImageNameTemple': 'template_name',
            #    'SceneName': 'name',
            #    'Extension': 'exr'
            #},
            #'WantedCellSpecs': [
            #    {
            #        'ComputerResourceType': 'CPU',
            #        'ComputerResourceCount': 5
            #    }
            #],
            #'UseLegacyRenderLayers': False
        }

        print(self.verender.create_render_job(1, render_job_cfg, local_scene_file='/local_path/test.ma'))

    def test_list_render_jobs(self):
        print(self.verender.list_render_jobs(1, job_type='maya_redshift', tryout=0, status="Error"))

    def test_get_render_job(self):
        print(self.verender.get_render_job(1, 'job_id'))

    def test_get_frames(self):
        print(self.verender.get_frames(1, "job_id", page_num=1, page_size=60))

    def test_get_frame_layers(self):
        data = {
            'LayerRequests': [
                {
                    'LayerIndex': 0,
                    'PageNum': 1,
                    'PageSize': 10,
                    'Statusess': []
                }
            ]
        }
        print(self.verender.get_layer_frames(1, "job_id", data))

    def test_update_render_job_priority(self):
        print(self.verender.update_render_job_priority(1, "job_id", -5))

    def test_start_render_job(self):
        print(self.verender.start_render_job(1, "job_id"))

    def test_pause_render_job(self):
        print(self.verender.pause_render_job(1, "job_id"))

    def test_stop_render_job(self):
        print(self.verender.stop_render_job(1, "job_id"))

    def test_delete_render_job(self):
        print(self.verender.delete_render_job(1, 'job_id'))

    def test_full_speed_render_job(self):
        print(self.verender.full_speed_render_job(1, "job_id"))

    def test_retry_render_job(self):
        print(self.verender.retry_render_job(1, "job_id"))

    def test_edit_render_job(self):
        print(self.verender.edit_render_job(1, "job_id", "test-render-job-edit-1", "des"))

    def test_pause_jobs(self):
        print(self.verender.pause_jobs(1, ["job_id1", "job_id2", "job_id3"]))

    def test_resume_jobs(self):
        print(self.verender.resume_jobs(1, ["job_id1", "job_id2", "job_id3"]))

    def test_stop_jobs(self):
        print(self.verender.stop_jobs(1, ["job_id1", "job_id2", "job_id3"]))

    def test_delete_jobs(self):
        print(self.verender.delete_jobs(1, ["job_id1", "job_id2", "job_id3"]))

    def test_full_speed_render_jobs(self):
        print(self.verender.full_speed_render_jobs(1, ["job_id1"]))

    def test_list_my_messages(self):
        print(self.verender.list_my_messages())

    def test_mark_message_as_read(self):
        print(self.verender.mark_message_as_read(1))

    def test_batch_mark_messages_as_read(self):
        print(self.verender.batch_mark_messages_as_read([1,2]))

    def test_mark_all_messages_as_read(self):
        print(self.verender.mark_all_messages_as_read())

    def test_delete_message(self):
        print(self.verender.delete_message(1))

    def test_batch_delete_messages(self):
        print(self.verender.batch_delete_messages([1, 2, 3, 4, 5]))

    def test_delete_all_messages(self):
        print(self.verender.delete_all_messages())

    def test_delete_all_read_messages(self):
        print(self.verender.delete_all_read_messages())


if __name__ == "__main__":
    tvs = TestVerenderService()

    #tvs.test_list_workspaces()
    #tvs.test_purchase_workspace()
    #tvs.test_delete_workspace()
    #tvs.test_update_workspace()
    #tvs.test_get_storage_access()
    #tvs.test_get_workspace_limit()
    #tvs.test_list_resource_pool()
    #tvs.test_get_workspace_hardware_specifications()
    #tvs.test_get_account_statistics()
    #tvs.test_get_account_statistic_details()
    #tvs.test_download_statistic_details()
    #tvs.test_get_current_user()
    #tvs.test_get_job_overall_statistics()
    #tvs.test_create_render_job()
    #tvs.test_list_render_jobs()
    #tvs.test_get_render_job()
    #tvs.test_get_frames()
    tvs.test_get_frame_layers()
    #tvs.test_update_render_job_priority()
    #tvs.test_start_render_job()
    #tvs.test_pause_render_job()
    #tvs.test_stop_render_job()
    #tvs.test_delete_render_job()
    #tvs.test_full_speed_render_job()
    #tvs.test_retry_render_job()
    #tvs.test_edit_render_job()
    #tvs.test_pause_jobs()
    #tvs.test_resume_jobs()
    #tvs.test_stop_jobs()
    #tvs.test_delete_jobs()
    #tvs.test_full_speed_render_jobs()
    #tvs.test_list_my_messages()
    #tvs.test_mark_message_as_read()
    #tvs.test_batch_mark_messages_as_read()
    #tvs.test_mark_all_messages_as_read()
    #tvs.test_delete_message()
    #tvs.test_batch_delete_messages()
    #tvs.test_delete_all_messages()
    #tvs.test_delete_all_read_messages()
