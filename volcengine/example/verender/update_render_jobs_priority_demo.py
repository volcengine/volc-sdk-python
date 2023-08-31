import verender_init


def update_render_jobs_priority_demo(v):
    v = verender_init.get_verender_instance()
    params = {
        "WorkspaceId": 1993
    }
    body = {
        "JobIds": [
            "r90ea40ecbd",
            "r041853ab30"
        ],
        "Priority": 10
    }
    resp = v.update_render_jobs_priority(params=params, body=body)
    print(resp)