import verender_init


def stop_render_jobs_demo():
    v = verender_init.get_verender_instance()
    params = {
        "WorkspaceId": 1993
    }
    body = {
        "JobIds": [
            "r003ebaa720"
        ]
    }
    resp = v.stop_render_jobs(params=params, body=body)
    print(resp)