import verender_init


def list_job_output_demo():
    v = verender_init.get_verender_instance()
    params = {
        "WorkspaceId": 1802
    }
    body = {
        "StartTime": "2023-08-01T00:00:00+08:00",
        "EndTime": "2023-08-14T00:00:00+08:00",
        "PageNum": 1,
        "PageSize": 100,
        "Type": "all", # all, image(渲染结果), thumb(缩略图)
        "Status": "all", # all, new(未下载过的记录)
        "OrderType": "asc", # asc, desc
        "OrderField": "created_at", # 暂不支持其他
        "JobIdList": ["job_id1", "job_id2"] # 单次建议不超过10个
    }

    resp = v.list_job_output(params=params, body=body)
    print(resp)