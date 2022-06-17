#coding: utf-8

import json
import os
import redo
import threading

import minio
from requests import exceptions

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo

ORDER_TYPE_MAP = {
    'ascend': 1,
    'descend': 2
}

ALLOW_FILE_TYPES = [
    'asset',
    'scene_file',
    'client_script'
]


class VerenderService(Service):
    _instance_lock = threading.Lock()
    _version = "2021-12-31"
    _DEFAULT_REGION = "cn-north-1"
    _SERVICE = "verender"

    def __new__(cls, *args, **kwargs):
        if not hasattr(VerenderService, '_instance'):
            with VerenderService._instance_lock:
                if not hasattr(VerenderService, '_instance'):
                    VerenderService._instance = object.__new__(cls)

        return VerenderService._instance

    def __init__(self, ak=None, sk=None):
        if ak and sk:
            self.set_ak(ak)
            self.set_sk(sk)

        self.service_info = VerenderService.get_service_info()
        self.api_info_map = VerenderService.get_api_info()
        super(VerenderService, self).__init__(self.service_info, self.api_info_map)

    @staticmethod
    def get_service_info():
        service_info = ServiceInfo(
            'open.volcengineapi.com',
            {'Accept': 'application/json'},
            Credentials('', '', VerenderService._SERVICE, VerenderService._DEFAULT_REGION),
            5,
            5,
            'https'
        )

        return service_info

    @staticmethod
    def get_api_info():
        api_info_map = {
            'ListWorkspaces': ApiInfo(
                'GET',
                '/',
                {'Action': 'ListWorkspaces', 'Version': VerenderService._version},
                {},
                {}
            ),
            'PurchaseWorkspace': ApiInfo(
                'POST',
                '/',
                {'Action': 'PurchaseWorkspace', 'Version': VerenderService._version},
                {},
                {}
            ),
            'DeleteWorkspace': ApiInfo(
                'POST',
                '/',
                {'Action': 'DeleteWorkspace', 'Version': VerenderService._version},
                {},
                {}
            ),
            'UpdateWorkspace': ApiInfo(
                'POST',
                '/',
                {'Action': 'UpdateWorkspace', 'Version': VerenderService._version},
                {},
                {}
            ),
            'GetStorageAccess': ApiInfo(
                'GET',
                '/',
                {'Action': 'GetStorageAccess', 'Version': VerenderService._version},
                {},
                {}
            ),
            'GetWorkspaceLimit': ApiInfo(
                'GET',
                '/',
                {'Action': 'GetWorkspaceLimit', 'Version': VerenderService._version},
                {},
                {}
            ),
            'ListResourcePools': ApiInfo(
                'GET',
                '/',
                {'Action': 'ListResourcePools', 'Version': VerenderService._version},
                {},
                {}
            ),
            'GetWorkspaceHardwareSpecifications': ApiInfo(
                'GET',
                '/',
                {'Action': 'GetWorkspaceHardwareSpecifications', 'Version': VerenderService._version},
                {},
                {}
            ),
            'GetAccountStatistics': ApiInfo(
                'POST',
                '/',
                {'Action': 'GetAccountStatistics', 'Version': VerenderService._version},
                {},
                {}
            ),
            'GetAccountStatisticDetails': ApiInfo(
                'POST',
                '/',
                {'Action': 'GetAccountStatisticDetails', 'Version': VerenderService._version},
                {},
                {}
            ),
            'DownloadStatisticDetails': ApiInfo(
                'POST',
                '/',
                {'Action': 'DownloadStatisticDetails', 'Version': VerenderService._version},
                {},
                {}
            ),
            'GetCurrentUser': ApiInfo(
                'GET',
                '/',
                {'Action': 'GetCurrentUser', 'Version': VerenderService._version},
                {},
                {}
            ),
            'GetJobOverallStatistics': ApiInfo(
                'GET',
                '/',
                {'Action': 'GetJobOverallStatistics', 'Version': VerenderService._version},
                {},
                {}
            ),
            'CreateRenderJob': ApiInfo(
                'POST',
                '/',
                {'Action': 'CreateRenderJob', 'Version': VerenderService._version},
                {},
                {}
            ),
            'ListRenderJobs': ApiInfo(
                'GET',
                '/',
                {'Action': 'ListRenderJobs', 'Version': VerenderService._version},
                {},
                {}
            ),
            'GetRenderJob': ApiInfo(
                'GET',
                '/',
                {'Action': 'GetRenderJob', 'Version': VerenderService._version},
                {},
                {}
            ),
            'GetFrames': ApiInfo(
                'GET',
                '/',
                {'Action': 'GetFrames', 'Version': VerenderService._version},
                {},
                {}
            ),
            'GetLayerFrames': ApiInfo(
                'POST',
                '/',
                {'Action': 'GetLayerFrames', 'Version': VerenderService._version},
                {},
                {}
            ),
            'UpdateRenderJobPriority': ApiInfo(
                'POST',
                '/',
                {'Action': 'UpdateRenderJobPriority', 'Version': VerenderService._version},
                {},
                {}
            ),
            'StartRenderJob': ApiInfo(
                'POST',
                '/',
                {'Action': 'StartRenderJob', 'Version': VerenderService._version},
                {},
                {}
            ),
            'PauseRenderJob': ApiInfo(
                'POST',
                '/',
                {'Action': 'PauseRenderJob', 'Version': VerenderService._version},
                {},
                {}
            ),
            'StopRenderJob': ApiInfo(
                'POST',
                '/',
                {'Action': 'StopRenderJob', 'Version': VerenderService._version},
                {},
                {}
            ),
            'DeleteRenderJob': ApiInfo(
                'POST',
                '/',
                {'Action': 'DeleteRenderJob', 'Version': VerenderService._version},
                {},
                {}
            ),
            'FullSpeedRenderJob': ApiInfo(
                'POST',
                '/',
                {'Action': 'FullSpeedRenderJob', 'Version': VerenderService._version},
                {},
                {}
            ),
            'RetryJob': ApiInfo(
                'POST',
                '/',
                {'Action': 'RetryJob', 'Version': VerenderService._version},
                {},
                {}
            ),
            'EditRenderJob': ApiInfo(
                'POST',
                '/',
                {'Action': 'EditRenderJob', 'Version': VerenderService._version},
                {},
                {}
            ),
            'PauseJobs': ApiInfo(
                'POST',
                '/',
                {'Action': 'PauseJobs', 'Version': VerenderService._version},
                {},
                {}
            ),
            'ResumeJobs': ApiInfo(
                'POST',
                '/',
                {'Action': 'ResumeJobs', 'Version': VerenderService._version},
                {},
                {}
            ),
            'StopJobs': ApiInfo(
                'POST',
                '/',
                {'Action': 'StopJobs', 'Version': VerenderService._version},
                {},
                {}
            ),
            'DeleteJobs': ApiInfo(
                'POST',
                '/',
                {'Action': 'DeleteJobs', 'Version': VerenderService._version},
                {},
                {}
            ),
            'FullSpeedRenderJobs': ApiInfo(
                'POST',
                '/',
                {'Action': 'FullSpeedRenderJobs', 'Version': VerenderService._version},
                {},
                {}
            ),
            'ListMyMessages': ApiInfo(
                'GET',
                '/',
                {'Action': 'ListMyMessages', 'Version': VerenderService._version},
                {},
                {}
            ),
            'MarkMessageAsRead': ApiInfo(
                'POST',
                '/',
                {'Action': 'MarkMessageAsRead', 'Version': VerenderService._version},
                {},
                {}
            ),
            'BatchMarkMessagesAsRead': ApiInfo(
                'POST',
                '/',
                {'Action': 'BatchMarkMessagesAsRead', 'Version': VerenderService._version},
                {},
                {}
            ),
            'MarkAllMessagesAsRead': ApiInfo(
                'POST',
                '/',
                {'Action': 'MarkAllMessagesAsRead', 'Version': VerenderService._version},
                {},
                {}
            ),
            'DeleteMessage': ApiInfo(
                'POST',
                '/',
                {'Action': 'DeleteMessage', 'Version': VerenderService._version},
                {},
                {}
            ),
            'BatchDeleteMessages': ApiInfo(
                'POST',
                '/',
                {'Action': 'BatchDeleteMessages', 'Version': VerenderService._version},
                {},
                {}
            ),
            'DeleteAllMessages': ApiInfo(
                'POST',
                '/',
                {'Action': 'DeleteAllMessages', 'Version': VerenderService._version},
                {},
                {}
            ),
            'DeleteAllReadMessages': ApiInfo(
                'POST',
                '/',
                {'Action': 'DeleteAllReadMessages', 'Version': VerenderService._version},
                {},
                {}
            )
        }

        return api_info_map

    @staticmethod
    def get_minio_client(endpoint, ak, sk, token):
        addr = endpoint
        secure = True
        if endpoint[:8] == "https://":
            addr = endpoint[8:]
        elif endpoint[:7] == "http://":
            addr = endpoint[7:]
            secure = False

        return minio.Minio(
            addr,
            access_key=ak,
            secret_key=sk,
            session_token=token,
            secure=secure,
            region=VerenderService._DEFAULT_REGION
        )

    @redo.retriable(retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout),
                    sleeptime=0.1, jitter=0.01, attempts=2)
    def upload_file(self, workspace_id, file_list, file_type="asset"):
        if file_type not in ALLOW_FILE_TYPES:
            raise TypeError("file type must be one of {}".format(ALLOW_FILE_TYPES))

        store_info = self.get_storage_access(workspace_id)

        try:
            endpoint = store_info['Result']['cluster_endpoint']
            ak = store_info['Result']['access_key']
            sk = store_info['Result']['secret_key']
            token = store_info['Result']['bucket_token']
            bucket = store_info['Result']['bucket_name']
        except Exception as ex:
            raise Exception('get storage access for {} error {}'.format(workspace_id, str(ex)))

        objects = []
        cli = VerenderService.get_minio_client(endpoint, ak, sk, token)
        for file_path in file_list:
            object = os.path.basename(file_path)
            cli.fput_object(bucket, object, file_path)
            objects.append(object)

        return objects


    @redo.retriable(retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout),
                    sleeptime=0.1, jitter=0.01, attempts=2)
    def _call_json(self, api_name, param=None, body=None):
        api_info = self.api_info_map.get(api_name)

        if not api_info:
            raise Exception('Api named {} not found.'.format(api_name))

        param = param or {}
        body = json.dumps(body) or ''
        method = {
            'POST': self.json,
            'GET': self.get
        }.get(api_info.method, self.post)

        try:
            res = method(api_name, param, body)
        except Exception as ex:
            raise Exception(str(ex))

        if '' == res:
            raise Exception('Empty response.')

        try:
            res_json = json.loads(res)
        except Exception as ex:
            raise Exception('Invalid json format {}.'.format(str(ex)))

        if 'Error' in res_json.get('ResponseMetadata', {}):
            err = res_json['ResponseMetadata']['Error']
            raise Exception('{} {} {}'.format(
                err.get('CodeN', 0),
                err.get('Code', 'Unknown error'),
                err.get('Message', 'Backend service return an error, but no message were found.')
            ))

        return res_json

    @redo.retriable(retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout),
                    sleeptime=0.1, jitter=0.01, attempts=2)
    def _call_download(self, api_name, save_file, param=None, body=None):
        api_info = self.api_info_map.get(api_name)

        if not api_info:
            raise Exception('Api named {} not found'.format(api_name))

        param = param or {}
        body = body or {}
        method = {
            'GET': self.get,
            'POST': self.post
        }.get(api_info.method, self.post)

        try:
            res = method(api_name, param, body)
        except Exception as ex:
            raise Exception(str(ex))

        with open(save_file, 'w+') as f:
            f.write(res)

    # start_purchase_time 和 end_purchase_time格式应符合RFC3339, 比如 2022-04-01T00:00:00+08:00
    def list_workspaces(self, page_num=1, page_size=10, list_scope=None, workspace_id=None,
                        workspace_name=None, start_purchase_time=None, end_purchase_time=None,
                        order_type=None, orderby=None, fuzzy_workspace_name=None,
                        fuzzy_search_content=None):
        param = {
            'PageNum': page_num,
            'PageSize': page_size
        }

        if list_scope:
            param['ListScope'] = list_scope

        if workspace_id:
            param['WorkspaceId'] = workspace_id

        if workspace_name:
            param['WorkspaceName'] = workspace_name

        if start_purchase_time:
            param['StartPurchaseTime'] = start_purchase_time

        if end_purchase_time:
            param['EndPurchaseTime'] = end_purchase_time

        if order_type:
            param['OrderType'] = order_type

        if orderby:
            param['OrderBy'] = orderby

        if fuzzy_workspace_name:
            param['FuzzyWorkspaceName'] = fuzzy_workspace_name

        if fuzzy_search_content:
            param['FuzzySearchContent'] = fuzzy_search_content

        return self._call_json('ListWorkspaces', param)

    # @param storage_total: 工作区的存储空间上限，默认100G，最大1000G
    # @param resource_pool_id: 可用的ResourcePool通过get_resource_pool接口获取
    # @param cps_id: 可用的CPS集群通过get_resource_pool接口获取
    def purchase_workspace(self, name, description, storage_total, resource_pool_id, cps_id):
        data = {
            'Name': name,
            'Description': description,
            'StorageTotal': storage_total,
            'ResourcePoolId': resource_pool_id,
            'CpsId': cps_id
        }

        return self._call_json('PurchaseWorkspace', {}, body=data)

    def delete_workspace(self, workspace_id):
        param = {
            'WorkspaceId': workspace_id
        }

        return self._call_json('DeleteWorkspace', param)

    def update_workspace(self, workspace_id, name, description, storage_total):
        param = {
            'WorkspaceId': workspace_id
        }

        data = {
            'Name': name,
            'Description': description,
            'StorageTotal': storage_total
        }

        return self._call_json('UpdateWorkspace', param, body=data)

    def get_storage_access(self, workspace_id):
        param = {
            'WorkspaceId': workspace_id
        }

        return self._call_json('GetStorageAccess', param)

    # 返回当前账号可创建的最大工作区数目和单个工作区可申请的最大存储空间
    def get_workspace_limit(self):
        return self._call_json('GetWorkspaceLimit')

    # 返回当前账号可用的{ResourcePool, CPS}列表
    def list_resource_pools(self):
        return self._call_json('ListResourcePools')

    def get_workspace_hardware_specifications(self, workspace_id):
        param = {
            'WorkspaceId': workspace_id
        }

        return self._call_json('GetWorkspaceHardwareSpecifications', param)

    # @ param time_type 目前支持 last_day, last_week, last_month, last_year, all
    # @ param start_time 和 end_time 当前不生效
    def get_account_statistics(self, time_type, start_time=None, end_time=None, workspace_ids=None, user_ids=None):
        param = {
            'TimeType': time_type
        }

        if start_time:
            param['StartTime'] = start_time

        if end_time:
            param['EndTime'] = end_time

        data = {}
        if workspace_ids:
            data['WorkspaceIds'] = workspace_ids

        if user_ids:
            data['UserIds'] = user_ids

        return self._call_json('GetAccountStatistics', param, body=data)

    # @param start_time和end_time的格式需符合RFC3339, 比如 2022-05-01T00:00:00+08:00
    # @param order_type, descend表示降序, ascend表示升序
    # @param order_by, 指明排序的列名, 支持 StartTime 和 TotalCost，默认为 StartTime
    # @param job_types，指明渲染任务类别列表，支持 maya_redshift, maya_arnold, c4d_redshift, blender, octane
    def get_account_statistic_detail(self, start_time, end_time, page_num=1, page_size=10, order_type="descend",
                                    order_by='StartTime', workspace_ids=None, user_ids=None, job_types=None, keyword=None):
        param = {
            'StartTime': start_time,
            'EndTime': end_time,
            'PageNum': page_num,
            'PageSize': page_size,
            'OrderField': order_by
        }

        if order_type in ORDER_TYPE_MAP:
            param['OrderBy'] = ORDER_TYPE_MAP[order_type]

        data = {}
        if workspace_ids:
            data['WorkspaceIds'] = workspace_ids

        if user_ids:
            data['UserIds'] = user_ids

        if job_types:
            data['JobTypes'] = job_types

        if keyword:
            data['Keyword'] = keyword

        return self._call_json('GetAccountStatisticDetails', param, body=data)

    # 将指定条件的统计明细以csv文件的形式返还，save_file指明要保存的文件路径，其他参数参考 get_statistic_details
    def download_statistic_details(self, start_time, end_time, save_file, page_num=1, page_size=10, order_type='descend',
                                    order_by='StartTime', workspace_ids=None, user_ids=None, job_types=None, keyword=None):
        param = {
            'StartTime': start_time,
            'EndTime': end_time,
            'PageNum': page_num,
            'PageSize': page_size,
            'OrderField': order_by
        }

        if order_type in ORDER_TYPE_MAP:
            param['OrderBy'] = ORDER_TYPE_MAP[order_type]

        data = {}
        if workspace_ids:
            data['WorkspaceIds'] = workspace_ids

        if user_ids:
            data['UserIds'] = user_ids

        if job_types:
            data['JobTypes'] = job_types

        if keyword:
            data['Keyword'] = keyword

        return self._call_download('DownloadStatisticDetails', save_file, param, body=data)

    # 获取当前登录用户的详细信息
    def get_current_user(self):
        return self._call_json('GetCurrentUser')

    # 获取当前登录用户提交的渲染任务的概要信息
    def get_job_overall_statistics(self):
        return self._call_json('GetJobOverallStatistics')

    # render_job_cfg = {
    #     'Username': 'username', --username 从接口 get_current_user 获取
    #     'Title': 'Test-Job-1', --Title可以多个任务重复
    #     'Description': '',
    #     'DccTool': 'maya', --支持maya, c4d, blender
    #     'DccVersion': '',
    #     'Renderer': 'redshift', --maya支持redshift/arnold, c4d支持cycles, blender支持redshift
    #     'RendererVersion': '',
    #     'Tryout': true, --true表示先试渲染, false表示正式渲染
    #     'TryoutFrames': ['1', '2', '3'], --试渲染的帧列表, Tryout为true时才有意义, 类型为string
    #     'MayaProjectPath': '', --maya工程里mel文件的路径, 需要先上传到存储，非必选
    #     'SceneFile': 'test_legency_render.ma', --渲染工程的路径，需要先上传到存储后再提交渲染任务
    #     'OutputFormat': 'PNG', --渲染结果格式, 支持PNG和EXR
    #     'Resolutions': [
    #         {
    #             'Width': 100,
    #             'Height': 100
    #         }
    #     ], --各渲染层输出结果的分辨率, 非必选
    #     'PathMapping': {
    #         'C:/': ''
    #     }, --将WINDOWS下的路径映射为LINUX下的路径, 非必选
    #     'FrameSettings': {
    #         'Start': 1,
    #         'End': 10,
    #         'Step': 1
    #     }, --渲染帧信息，非必选, 默认是{0, 1, 1}
    #     'Cameras': ['top', 'side'], --摄像机列表, 非必选
    #     'Layers': ['layer-1'], --渲染层列表, 非必选
    #     'TimeoutReminder': 36000, --超时提醒时间, 单位为分钟, 非必选
    #     'TimeoutStopper': 36000, --超时停止时间, 单位为分钟, 非必选
    #     'OutputImageTemple': {
    #         'padding': 4, --帧号的位数，如0000, 0001
    #         'ImageNameTemple': 'template', --输出结果的模版
    #         'SceneName': 'test', --渲染场景的名称
    #         'Extension': 'ext' --渲染结果的后缀
    #     }, --渲染结果的命名规则，非必选
    #     'WantedCellSpecs': [
    #         {
    #             'ComputerResourceType': 'CPU', --支持CPU/T4, arnold使用CPU, 其他渲染器是用GPU, 建议不配置, 系统自行决定
    #             'ComputerResourceCount': 10
    #         }
    #     ], --用户选择的执行渲染的硬件规格, 非必选
    #     'UseLegacyRenderLayers': true --maya渲染工程是否使用传统层, 非必选
    # }
    def create_render_job(self, workspace_id, render_job_cfg):
        param = {
            'WorkspaceId': workspace_id
        }

        return self._call_json('CreateRenderJob', param, body=render_job_cfg)

    # @param order_by表示结果的排序类型, ascend表示升序, 其他表示降序, 默认为降序, 按照任务的创建时间?
    # @param tryout为0表示正式渲染, 其他为试渲染
    # @param status表示要查询的任务状态, 多个之间使用逗号分隔, 支持Empty, Starting, Queuing, Analyzing, Processing,
    #           Rendered, Cleanup, Paused, Deleted, Stopped, Finished, Error
    # @param job_type表示渲染任务类型, 多个之间使用逗号分隔, 支持maya_redshift, maya_arnold, c4d_redshift, blender_cycle
    def list_render_jobs(self, workspace_id, order_by='descend', page_num=1, page_size=10, tryout=0, status=None, job_type=None):
        param = {
            'WorkspaceId': workspace_id,
            'PageNum': page_num,
            'PageSize': page_size,
            'Tryout': tryout
        }

        if order_by in ORDER_TYPE_MAP:
            param['OrderBy'] = ORDER_TYPE_MAP[order_by]

        if status:
            param['Status'] = status

        # TODO: JobType拆分为 Dcc 和 Render
        if job_type:
            param['JobType'] = job_type

        return self._call_json('ListRenderJobs', param)

    def get_render_job(self, workspace_id, render_job_id):
        param = {
            'WorkspaceId': workspace_id,
            'RenderJobId': render_job_id
        }

        return self._call_json('GetRenderJob', param)

    def get_frames(self, workspace_id, render_job_id, page_num=1, page_size=10):
        param = {
            'WorkspaceId': workspace_id,
            'RenderJobId': render_job_id,
            'PageNum': page_num,
            'PageSize': page_size
        }

        return self._call_json('GetFrames', param)

    # layer_requests = {
    #   'LayerRequests': [
    #       {
    #           'LayerIndex': 0,
    #           'PageNum': 1,
    #           'PageSize': 10,
    #           'Statuses': [0, 1]
    #       }
    #   ]
    # }
    def get_layer_frames(self, workspace_id, render_job_id, layer_requests):
        param = {
            'WorkspaceId': workspace_id,
            'RenderJobId': render_job_id
        }

        return self._call_json('GetLayerFrames', param, body=layer_requests)

    def update_render_job_priority(self, workspace_id, render_job_id, priority):
        param = {
            'WorkspaceId': workspace_id,
            'RenderJobId': render_job_id,
            'Priority': priority
        }

        return self._call_json('UpdateRenderJobPriority', param)

    def start_render_job(self, workspace_id, render_job_id):
        param = {
            'WorkspaceId': workspace_id,
            'RenderJobId': render_job_id
        }

        return self._call_json('StartRenderJob', param)

    def pause_render_job(self, workspace_id, render_job_id):
        param = {
            'WorkspaceId': workspace_id,
            'RenderJobId': render_job_id
        }

        return self._call_json('PauseRenderJob', param)

    def stop_render_job(self, workspace_id, render_job_id):
        param = {
            'WorkspaceId': workspace_id,
            'RenderJobId': render_job_id
        }

        return self._call_json('StopRenderJob', param)

    def delete_render_job(self, workspace_id, render_job_id):
        param = {
            'WorkspaceId': workspace_id,
            'RenderJobId': render_job_id
        }

        return self._call_json('DeleteRenderJob', param)

    def full_speed_render_job(self, workspace_id, render_job_id):
        param = {
            'WorkspaceId': workspace_id,
            'RenderJobId': render_job_id
        }

        return self._call_json('FullSpeedRenderJob', param)

    def retry_render_job(self, workspace_id, render_job_id):
        param = {
            'WorkspaceId': workspace_id,
            'RenderJobId': render_job_id
        }

        return self._call_json('RetryJob', param)

    def edit_render_job(self, workspace_id, render_job_id, title, description):
        param = {
            'WorkspaceId': workspace_id,
            'RenderJobId': render_job_id
        }

        data = {}
        if title:
            data['Title'] = title

        if description:
            data['Description'] = description

        return self._call_json('EditRenderJob', param, body=data)

    def pause_jobs(self, workspace_id, render_job_ids):
        param = {
            'WorkspaceId': workspace_id
        }

        data = {
            'JobIds': render_job_ids
        }

        return self._call_json('PauseJobs', param, body=data)

    def resume_jobs(self, workspace_id, render_job_ids):
        param = {
            'WorkspaceId': workspace_id
        }

        data = {
            'JobIds': render_job_ids
        }

        return self._call_json('ResumeJobs', param, body=data)

    def stop_jobs(self, workspace_id, render_job_ids):
        param = {
            'WorkspaceId': workspace_id
        }

        data = {
            'JobIds': render_job_ids
        }

        return self._call_json('StopJobs', param, body=data)

    def delete_jobs(self, workspace_id, render_job_ids):
        param = {
            'WorkspaceId': workspace_id
        }

        data = {
            'JobIds': render_job_ids
        }

        return self._call_json('DeleteJobs', param, body=data)

    def full_speed_render_jobs(self, workspace_id, render_job_ids):
        param = {
            'WorkspaceId': workspace_id
        }

        data = {
            'JobIds': render_job_ids
        }

        return self._call_json('FullSpeedRenderJobs', param, body=data)

    def list_my_messages(self, page_num=1, page_size=10):
        param = {
            'PageNum': page_num,
            'PageSize': page_size
        }

        return self._call_json('ListMyMessages', param)

    def mark_message_as_read(self, message_id):
        param = {
            'MessageId': message_id
        }

        return self._call_json('MarkMessageAsRead', param)

    def batch_mark_messages_as_read(self, message_ids):
        data = {
            'MessageIds': message_ids
        }

        return self._call_json('BatchMarkMessagesAsRead', {}, body=data)

    def mark_all_messages_as_read(self):
        return self._call_json('MarkAllMessagesAsRead', {})

    def delete_message(self, message_id):
        param = {
            'MessageId': message_id
        }

        return self._call_json('DeleteMessage', param)

    def batch_delete_messages(self, message_ids):
        data = {
            'MessageIds': message_ids
        }

        return self._call_json('BatchDeleteMessages', {}, body=data)

    def delete_all_messages(self):
        return self._call_json('DeleteAllMessages', {})

    def delete_all_read_messages(self):
        return self._call_json('DeleteAllReadMessages', {})