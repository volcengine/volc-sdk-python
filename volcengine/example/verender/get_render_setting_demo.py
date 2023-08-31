import verender_init


def get_render_setting_demo():
    v = verender_init.get_verender_instance()
    user = v.get_current_user()
    params = {
        "AccountId": user["AccountId"],
        "UserId": user["UserId"],
        "WorkspaceId": 1993,
        "Id": 360
    }

    resp = v.get_render_setting(params=params)
    print(resp)