import verender_init


def resume_render_jobs_demo():
    v = verender_init.get_verender_instance()

    params = {
        "WorkspaceId": 1993
    }
    body = {
        "JobIds": [
            "r776bf384a4"
        ]
    }
    resp = v.resume_render_jobs(params=params, body=body)
    print(resp)