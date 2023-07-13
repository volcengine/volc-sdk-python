import json

from volcengine.dts.dts_service import DtsService

if __name__ == '__main__':
    access_key = 'your_ak_here'
    secret_key = 'your_sk_here'
    task_name = 'task_name_str'
    task_type = 'task_type_here'
    region_str = 'region_str_here'

    dts_service = DtsService(region=region_str)

    dts_service.set_ak(access_key)
    dts_service.set_sk(secret_key)

    params = {}
    body = {
        'TaskName': task_name,
        'TaskType': task_type,
        'ChargeConfig': {
            'ChargeType': 'PostPaid',
            'OneStep': True
        },
        'SrcConfig': {
            'EndpointType': 'Public_Redis',
            'PublicRedisSettings': {
                'Host': 'IP_str_here',
                'Port': 6379,
                'Username': 'default',
                'Password': 'redis_password_here',
                'RegionSettings': {
                    'Region': region_str
                }
            }
        },
        'DestConfig': {
            'EndpointType': 'Volc_Redis',
            'VolcRedisSettings': {
                'DBInstanceId': 'redis-instanceID',
                'Username': 'default',
                'Password': 'redis_password_here',
                'RegionSettings': {
                    'Region': region_str
                }
            }
        },
        'SolutionSettings': {
            'SolutionType': 'Redis2Redis',
            'Redis2RedisSettings': {
                'ObjectMappings': [
                    {
                        "DestObjName": "0",
                        "ObjectType": "Database",
                        "SrcObjName": "0"
                    },
                    {
                        "DestObjName": "6",
                        "ObjectType": "Database",
                        "SrcObjName": "6"
                    }
                ],
                'FullTransmissionSettings': {
                    'EnableFull': True
                },
                'IncrTransmissionSettings': {
                    'EnableIncr': True
                },
                'ErrorBehaviorSettings': {
                    'MaxRetrySeconds': 7200
                }
            }
        }
    }
    resp = dts_service.modify_transmission_task(params, body)
    print(json.dumps(resp, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':')))
