import verender_init


def create_render_job_demo(v):
    v = verender_init.get_verender_instance()

    workspace_id = 1993
    params = {
        "WorkspaceId": workspace_id,
    }

    # upload file
    src = "D:\\car-studio\\Studio_Top.ma"
    des = "D:\\car-studio\\Studio_Top.ma"
    isp = "ct"
    obj = v.upload_file(workspace_id, src, des, isp)

    # get render setting
    user = v.get_current_user()
    p = {
        "AccountId": user["AccountId"],
        "UserId": user["UserId"],
        "WorkspaceId": workspace_id,
        "CheckUserId": False,
        "WithDeleted": True,
        "Id": 368
    }
    rs = v.get_render_setting(params=p)

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
    resp = v.create_render_job(params=params, body=body)
    print(resp)