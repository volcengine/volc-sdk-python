import verender_init


def list_cell_spec_demo():
    v = verender_init.get_verender_instance()

    params = {
        "WorkspaceId": 735
    }
    resp = v.list_cell_spec(params=params)
    print(resp)