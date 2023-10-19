import verender_init


def add_render_setting_demo():
    v = verender_init.get_verender_instance()

    user = v.get_current_user()
    params = {
        "WorkspaceId": 1935
    }
    body = {
        "AccountId": user["AccountId"],
        "UserId": user["UserId"],
        "WorkspaceId": 1935,
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
        "FramesCountOneCell": 1,
        "CellSpecId": 15
    }

    resp = v.add_render_setting(params=params, body=body)
    print(resp)