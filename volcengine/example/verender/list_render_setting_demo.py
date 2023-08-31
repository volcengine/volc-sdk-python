import verender_init


def list_render_setting_demo():
    v = verender_init.get_verender_instance()
    user = v.get_current_user()
    params = {
        "AccountId": user["AccountId"],
        "UserId": user["UserId"],
        "WorkspaceId": 1993,
        "Dcc": "maya"
    }
    resp = v.list_render_setting(params=params)
    print(resp)