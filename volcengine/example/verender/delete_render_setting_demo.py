import verender_init


def delete_render_setting_demo():
    v = verender_init.get_verender_instance()

    params = {
        "WorkspaceId": 1993,
        "RenderSettingId": 361
    }
    resp = v.delete_render_setting(params=params)
    print(resp)