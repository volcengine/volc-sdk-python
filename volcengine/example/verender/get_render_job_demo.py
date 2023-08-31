import verender_init


def get_render_job_demo():
    v = verender_init.get_verender_instance()
    params = {
        "WorkspaceId": 1993,
        "RenderJobId": "r776bf384a4"
    }
    resp = v.get_render_job(params=params)
    print(resp)