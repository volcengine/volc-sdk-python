import verender_init


def full_speed_render_jobs_demo():
    v = verender_init.get_verender_instance()
    params = {
        "WorkspaceId": 1993
    }
    body = {
        "JobIds": [
            "r90ea40ecbd",
            "r041853ab30"
        ]
    }
    resp = v.full_speed_render_jobs(params=params, body=body)
    print(resp)