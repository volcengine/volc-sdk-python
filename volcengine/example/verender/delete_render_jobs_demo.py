import verender_init


def delete_render_jobs_demo():
    v = verender_init.get_verender_instance()
    params = {
        "WorkspaceId": 1993
    }
    body = {
        "JobIds": [
            "r003ebaa720"
        ]
    }
    resp = v.delete_render_jobs(params=params, body=body)
    print(resp)