import verender_init


def update_render_setting_demo():
    v = verender_init.get_verender_instance()

    user = v.get_current_user()
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

    resp = v.update_render_setting(params=params, body=body)
    print(resp)