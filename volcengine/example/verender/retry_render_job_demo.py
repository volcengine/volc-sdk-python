import verender_init


def retry_render_job_demo():
    v = verender_init.get_verender_instance()
    params = {
        "WorkspaceId": 1993,
        "RenderJobId": "r5ad3829bef"
    }
    body = {
        "JobId": "r5ad3829bef",
        "AllFailedFrames": True,
        "CustomFrames": [
            {
                "LayerIndex": 0,
                "FrameIndexes": "1-5"
            }
        ]
    }

    resp = v.retry_render_job(params=params, body=body)
    print(resp)