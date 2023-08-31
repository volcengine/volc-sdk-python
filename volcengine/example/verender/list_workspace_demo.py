import verender_init


def list_workspace_demo():
    v = verender_init.get_verender_instance()

    params = {
        "PageNum": 1,
        "PageSize": 10
    }
    resp = v.list_workspace(params)
    print(resp)