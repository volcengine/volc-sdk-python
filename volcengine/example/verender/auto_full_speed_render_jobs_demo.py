import verender_init


def auto_full_speed_render_jobs_demo():
    v = verender_init.get_verender_instance()
    params = {
        "WorkspaceId": 19931
    }

    body = {
        "JobIds": [
            "r377a81d87e"
        ]
    }
    resp = v.auto_full_speed_render_jobs(params, body)
    print(resp)