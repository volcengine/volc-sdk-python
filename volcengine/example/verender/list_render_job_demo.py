import verender_init


def list_render_job_demo():
    v = verender_init.get_verender_instance()
    params = {
        "WorkspaceId": 1993
    }
    resp = v.list_render_job(params=params)
    print(resp)