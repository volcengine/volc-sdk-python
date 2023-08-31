import verender_init


def get_job_output_demo():
    v = verender_init.get_verender_instance()
    params = {
        "WorkspaceId": 1802,
        "JobId": "rf19285eae5"
    }

    body = {
        "Layers": {
            "masterLayer": {
                "Frames": [1, 2, 3],
                "IncludeThumb": True,
                "IncludeImage": True
            }
        }
    }

    resp = v.get_job_output(params=params, body=body)
    print(resp)