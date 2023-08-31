import verender_init


def update_job_output_demo():
    v = verender_init.get_verender_instance()
    params = {
        "WorkspaceId": 1802,
        "JobId": "abc"
    }

    body = {
        "files": [
            "Result/test-create-render-job_rf19285eae5/images/simple.exr.0001"
        ]
    }
    resp = v.update_job_output(params=params, body=body)
    print(resp)