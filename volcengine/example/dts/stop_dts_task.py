import json

from volcengine.dts.dts_service import DtsService

if __name__ == '__main__':
    access_key = 'your_ak_here'
    secret_key = 'your_sk_here'
    region_str = 'region_str_here'
    task_id_str = 'task_id_str'

    dts_service = DtsService(region=region_str)

    dts_service.set_ak(access_key)
    dts_service.set_sk(secret_key)

    params = {}
    body = {
        'TaskId': task_id_str
    }

    resp = dts_service.stop_transmission_task(params, body)
    print(json.dumps(resp, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':')))
