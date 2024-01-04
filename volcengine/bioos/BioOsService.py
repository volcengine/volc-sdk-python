# coding:utf-8
import json
import threading
from urllib.parse import urlparse

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service


class BioOsService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(BioOsService, '_instance'):
            with BioOsService._instance_lock:
                if not hasattr(BioOsService, '_instance'):
                    BioOsService._instance = object.__new__(cls)
        return BioOsService._instance

    def __init__(self, endpoint='https://open.volcengineapi.com', region='cn-beijing'):
        self.service_info = BioOsService.get_service_info(endpoint, region)
        self.api_info = BioOsService.get_api_info()
        super(BioOsService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(endpoint, region):
        parsed = urlparse(endpoint)
        scheme, hostname = parsed.scheme, parsed.hostname
        if not scheme or not hostname:
            raise Exception(f'invalid endpoint format: {endpoint}')
        service_info = ServiceInfo(hostname, {'Accept': 'application/json'},
                                   Credentials('', '', 'bio', region), 5, 5, scheme=scheme)
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            'CreateWorkspace':
                ApiInfo('POST', '/', {'Action': 'CreateWorkspace', 'Version': '2021-03-04'}, {}, {}),
            'ListWorkspaces':
                ApiInfo('POST', '/', {'Action': 'ListWorkspaces', 'Version': '2021-03-04'}, {}, {}),
            'UpdateWorkspace':
                ApiInfo('POST', '/', {'Action': 'UpdateWorkspace', 'Version': '2021-03-04'}, {}, {}),
            'DeleteWorkspace':
                ApiInfo('POST', '/', {'Action': 'DeleteWorkspace', 'Version': '2021-03-04'}, {}, {}),
            'BindClusterToWorkspace':
                ApiInfo('POST', '/', {'Action': 'BindClusterToWorkspace', 'Version': '2021-03-04'}, {}, {}),
            'UnbindClusterAndWorkspace':
                ApiInfo('POST', '/', {'Action': 'UnbindClusterAndWorkspace', 'Version': '2021-03-04'}, {}, {}),
            'ListClustersOfWorkspace':
                ApiInfo('POST', '/', {'Action': 'ListClustersOfWorkspace', 'Version': '2021-03-04'}, {}, {}),
            'ListWorkspaceLabels':
                ApiInfo('POST', '/', {'Action': "ListWorkspaceLabels", 'Version': '2021-03-04'}, {}, {}),
            'ListClusters':
                ApiInfo('POST', '/', {'Action': 'ListClusters', 'Version': '2021-03-04'}, {}, {}),
            'DeleteCluster':
                ApiInfo('POST', '/', {'Action': 'DeleteCluster', 'Version': '2021-03-04'}, {}, {}),
            'UpdateAPIAccessKey':
                ApiInfo('POST', '/', {'Action': 'UpdateAPIAccessKey', 'Version': '2021-03-04'}, {}, {}),
            'GetAPIAccessKey':
                ApiInfo('POST', '/', {'Action': 'GetAPIAccessKey', 'Version': '2021-03-04'}, {}, {}),
            'CreateDataModel':
                ApiInfo('POST', '/', {'Action': 'CreateDataModel', 'Version': '2021-03-04'}, {}, {}),
            'ListDataModels':
                ApiInfo('POST', '/', {'Action': 'ListDataModels', 'Version': '2021-03-04'}, {}, {}),
            'ListDataModelRows':
                ApiInfo('POST', '/', {'Action': 'ListDataModelRows', 'Version': '2021-03-04'}, {}, {}),
            'DeleteDataModelRowsAndHeaders':
                ApiInfo('POST', '/', {'Action': 'DeleteDataModelRowsAndHeaders', 'Version': '2021-03-04'}, {}, {}),
            'CreateSubmission':
                ApiInfo('POST', '/', {'Action': 'CreateSubmission', 'Version': '2021-03-04'}, {}, {}),
            'ListSubmissions':
                ApiInfo('POST', '/', {'Action': 'ListSubmissions', 'Version': '2021-03-04'}, {}, {}),
            'ListOverviewSubmissions':
                ApiInfo('POST', '/', {'Action': 'ListOverviewSubmissions', 'Version': '2021-03-04'}, {}, {}),
            'DeleteSubmission':
                ApiInfo('POST', '/', {'Action': 'DeleteSubmission', 'Version': '2021-03-04'}, {}, {}),
            'CancelSubmission':
                ApiInfo('POST', '/', {'Action': 'CancelSubmission', 'Version': '2021-03-04'}, {}, {}),
            'ListRuns':
                ApiInfo('POST', '/', {'Action': 'ListRuns', 'Version': '2021-03-04'}, {}, {}),
            'CancelRun':
                ApiInfo('POST', '/', {'Action': 'CancelRun', 'Version': '2021-03-04'}, {}, {}),
            'ListTasks':
                ApiInfo('POST', '/', {'Action': 'ListTasks', 'Version': '2021-03-04'}, {}, {}),
            'CreateWorkflow':
                ApiInfo('POST', '/', {'Action': 'CreateWorkflow', 'Version': '2021-03-04'}, {}, {}),
            'ListWorkflows':
                ApiInfo('POST', '/', {'Action': 'ListWorkflows', 'Version': '2021-03-04'}, {}, {}),
            'UpdateWorkflow':
                ApiInfo('POST', '/', {'Action': 'UpdateWorkflow', 'Version': '2021-03-04'}, {}, {}),
            'DeleteWorkflow':
                ApiInfo('POST', '/', {'Action': 'DeleteWorkflow', 'Version': '2021-03-04'}, {}, {}),
            'GetNotebookEditInfo':
                ApiInfo('POST', '/', {'Action': 'GetNotebookEditInfo', 'Version': '2021-03-04'}, {}, {}),
            'GetNotebookServerSettings':
                ApiInfo('POST', '/', {'Action': 'GetNotebookServerSettings', 'Version': '2021-03-04'}, {}, {}),
            'GetNotebookServerStat':
                ApiInfo('POST', '/', {'Action': 'GetNotebookServerStat', 'Version': '2021-03-04'}, {}, {}),
            'ListNotebookServerImages':
                ApiInfo('POST', '/', {'Action': 'ListNotebookServerImages', 'Version': '2021-03-04'}, {}, {}),
            'ListNotebookServerResourceOpts':
                ApiInfo('POST', '/', {'Action': 'ListNotebookServerResourceOpts', 'Version': '2021-03-04'}, {}, {}),
            'StopNotebookServer':
                ApiInfo('POST', '/', {'Action': 'StopNotebookServer', 'Version': '2021-03-04'}, {}, {}),
            'UpdateNotebookServerSettings':
                ApiInfo('POST', '/', {'Action': 'UpdateNotebookServerSettings', 'Version': '2021-03-04'}, {}, {}),
            'CreateNotebookServerImage':
                ApiInfo('POST', '/', {'Action': 'CreateNotebookServerImage', 'Version': '2021-03-04'}, {}, {}),
            'ListNotebookServers':
                ApiInfo('POST', '/', {'Action': 'ListNotebookServers', 'Version': '2021-03-04'}, {}, {}),
            'DeleteNotebookServer':
                ApiInfo('POST', '/', {'Action': 'DeleteNotebookServer', 'Version': '2021-03-04'}, {}, {}),
            'DeleteNotebookServerSettings':
                ApiInfo('POST', '/', {'Action': 'DeleteNotebookServerSettings', 'Version': '2021-03-04'}, {}, {}),
            'GetNotebookServerExtraPackages':
                ApiInfo('POST', '/', {'Action': 'GetNotebookServerExtraPackages', 'Version': '2021-03-04'}, {}, {}),
            'ListDataFiles':
                ApiInfo('POST', '/', {'Action': 'ListDataFiles', 'Version': '2021-03-04'}, {}, {}),
            'ListDataSets':
                ApiInfo('POST', '/', {'Action': 'ListDataSets', 'Version': '2021-03-04'}, {}, {}),
            'CreateDataSet':
                ApiInfo('POST', '/', {'Action': 'CreateDataSet', 'Version': '2021-03-04'}, {}, {}),
            'DeleteDataSet':
                ApiInfo('POST', '/', {'Action': 'DeleteDataSet', 'Version': '2021-03-04'}, {}, {}),
            'GetTRSWorkflowInfo':
                ApiInfo('POST', '/', {'Action': 'GetTRSWorkflowInfo', 'Version': '2021-03-04'}, {}, {}),
        }
        return api_info

    def create_workspace(self, params):
        """ 创建workspace

        Args:
            params (Dict):

                `Name (str)`: 必选, 工作空间名称
                    示例值: name

                `Description (str)`: 必选, 工作空间描述
                    示例值: description

                `S3Bucket (str)`: 选填, 对象存储的存储桶名称, 为空表示自动创建
                    示例值: bioos-wcfxxxxxxxxxxx

                `CopyPublicWorkspaceID (str)`: 选填, 需要复制其内容的公共工作空间ID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

                `CoverPath (str)`: 选填, 封面位于存储桶的路径, 为空表明使用官方第一张图片
                    示例值: template-cover/pic1.png

                `Labels (List[str])`: 选填, 工作空间标签
                    示例值: ["DNA"]

        Returns:
            Dict:

                `ID (str)`: 工作空间 ID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

        """
        return self.__request('CreateWorkspace', params)

    def list_workspaces(self, params):
        """ 查询符合条件的workspace列表

        Args:
            params (Dict):

                `PageNumber (int)`: 选填, 分页页码
                    示例值: 1

                `PageSize (int)`: 选填, 分页页长
                    示例值: 10

                `Filter (Dict)`: 选填, 筛选条件

                    `Keyword (str)`: 选填, 根据名称筛选
                        示例值: test

                    `IDs (List[str])`: 选填, ID列表
                        示例值: ["test"]

                    `IsPublic (bool)`: 选填, 是否公开
                        示例值: False

                    `Labels (List[str])`: 选填, workspace标签
                        示例值: ["DNA"]

                `SortBy (str)`: 选填, 按字段排序 取值有Name CreateTime VisitTime
                    示例值: CreateTime

                `SortOrder (str)`: 选填, 指定排序顺序 取值有Asc Desc
                    示例值: Desc

        Returns:
            Dict:

                `Items (List[Dict])`: Workspace列表

                    `ID (str)`: 工作空间ID
                        示例值: wcxxxxxxxxxxxxxxxxxxx

                    `Name (str)`: 工作空间名称
                        示例值: name

                    `Description (str)`: 工作空间描述
                        示例值: description

                    `CreateTime (int)`: 工作空间创建时间
                        示例值: 1673525239

                    `UpdateTime (int)`: 工作空间更新时间
                        示例值: 1673525239

                    `OwnerName (str)`: 创建者名字
                        示例值: owner

                    `CoverDownloadURL (str)`: 封面地址
                        示例值: template-cover/pic1.png

                    `Role (str)`: 当前用户对于工作空间角色
                        示例值: Admin

                    `S3Bucket (str)`: 当前工作空间存储桶
                        示例值: bioos-wcxxxxxxxxxxxx

                    `PublicMeta (Dict)`: 公共 Workspace 元数据

                        `TosBucketTotalStorage (int)`: 公共工作空间桶存储占用信息(Gb)
                            示例值: 20

                    `Labels (List[str])`: 工作空间标签
                        示例值: ["DNA"]

                `PageNumber (int)`: 页码
                    示例值: 1

                `PageSize (int)`: 页长
                    示例值: 10

                `TotalCount (int)`: 总数量
                    示例值: 10

        """
        return self.__request('ListWorkspaces', params)

    def update_workspace(self, params):
        """ 更新workspace

        Args:
            params (Dict):

                `ID (str)`: 必选, 工作空间 ID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

                `Name (str)`: 必选, 工作空间名称
                    示例值: name

                `Description (str)`: 必选, 工作空间描述
                    示例值: description

                `CoverPath (str)`: 选填, 图片位于存储桶的位置, 为空表明使用官方第一张图片
                    示例值: template-cover/pic1.png

                `Labels (List[str])`: 选填, 标签全量更新
                    示例值: ["DNA"]

        Returns:
            Dict:

                `Updated (bool)`: 是否存在内容更新
                    示例值: False

        """
        return self.__request('UpdateWorkspace', params)

    def delete_workspace(self, params):
        """ 删除workspace

        Args:
            params (Dict):

                `ID (str)`: 必选, workspaceID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

        Returns:
            Dict: empty dictionary

        """
        return self.__request('DeleteWorkspace', params)

    def bind_cluster_to_workspace(self, params):
        """ 如果workspace内运行工作流，则需要绑定已纳管的集群，已被纳管的集群可通过ListClusters接口查询。

        Args:
            params (Dict):

                `ID (str)`: 必选, workspaceID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

                `ClusterID (str)`: 必选, 已纳管集群的ID
                    示例值: ucxxxxxxxxxxxxxxxxxxx

                `Type (str)`: 必选, 关联类型（workflow、notebook）
                    示例值: workspace

        Returns:
            Dict: empty dictionary

        """
        return self.__request('BindClusterToWorkspace', params)

    def unbind_cluster_and_workspace(self, params):
        """ 该接口对已绑定的workspace和cluster进行解绑操作

        Args:
            params (Dict):

                `ID (str)`: 必选, workspaceID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

                `ClusterID (str)`: 必选, 已纳管集群的ID
                    示例值: ucxxxxxxxxxxxxxxxxxxx

                `Type (str)`: 必选, 关联类型（workflow、notebook）
                    示例值: workspace

        Returns:
            Dict: empty dictionary

        """
        return self.__request('UnbindClusterAndWorkspace', params)

    def list_clusters_of_workspace(self, params):
        """ 查看workspace所绑定的集群列表

        Args:
            params (Dict):

                ID (str): 必选, workspaceID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

                Type (str): 必选, 关联类型（workflow、notebook）
                    示例值: workflow

        Returns:
            Dict:

                `Items (List[Dict])`: cluster列表

                    `ClusterInfo (Dict)`: 集群信息

                        `ID (str)`: 纳管集群ID
                            示例值: ucxxxxxxxxxxxxxxxxxxx

                        `Name (str)`: 纳管集群名称
                            示例值: name

                        `Status (str)`: 集群纳管状态（Creating、CreateFailed、Running、Error、Deleting、DeleteFailed、Updating、Stopped）
                            示例值: Creating

                        `StartTime (int)`: 起始时间
                            示例值: 1673525239

                        `Description (str)`: 投递记录描述
                            示例值: description

                        `ErrorMessage (str)`: 集群纳管过程中出现问题时的错误信息
                            示例值: err message

                        `Bound (bool)`: 是否存在绑定的 workspace
                            示例值: False

                        `Public (bool)`: 是否是公共集群
                            示例值: True

                        `VKEConfig (Dict)`: vke 集群信息

                            `ClusterID (str)`: vke集群的clusterID,通过https://www.volcengine.com/docs/6460/115190查询
                                示例值: ccexxxxxxxxxxxxxxxxxx

                            `StorageClass (str)`: vke集群已安装的 StorageClass 的名称
                                示例值: ebs-ssd

                            `VCIEnabled (bool)`: vke集群是否运行VCI
                                示例值: True

                        `ExternalConfig (Dict)`: 外部集群配置

                            `WESEndpoint (str)`: WES 地址
                                示例值: http://192.168.0.1:8002/ga4gh/wes/v1

                            `JupyterhubEndpoint (str)`: jupyterhub 地址
                                示例值: http://jupyterhub-hub:8081/jupyterhub

                            `ResourceScheduler (str)`: 外部资源调度程序
                                示例值: SGE

                            `Filesystem (str)`: 工作流计算引擎依赖的文件系统（tos, local）
                                示例值: tos

                            `ExecutionRootDir (str)`: 工作流计算引擎执行根路径, 当且仅当工作流计算引擎依赖的文件系统为 `local` 时会有
                                示例值: /root

                            `S3ProxyConfig (Dict)`: 文件系统存储的s3proxy代理信息

                                `Endpoint (str)`: 访问地址
                                    示例值: http://192.168.0.3:8000

                                `Region (str)`: 区域
                                    示例值: cn-beijing

                                `AccessKey (str)`: 访问s3proxy的AccessKey
                                    示例值: AKxxxx

                                `SecretKey (str)`: 访问s3proxy的SecretKey
                                    示例值: xxxxxx

                                `ForcePathStyle (bool)`: 是否强制使用path style, 还是使用virtual style
                                    示例值: True

                        `SharedConfig (Dict)`: 共享集群配置,暂无具体配置信息
                                示例值: {}

                        `StoppedTime (int)`: 截止时间
                            示例值: 1673525239

                    `Type (str)`: 关联类型（workflow、notebook）
                        示例值: workflow

                    `BindTime (int)`: 绑定是时间
                        示例值: 1673525239

                `PageNumber (int)`: 页码
                    示例值: 1

                `PageSize (int)`: 页长
                    示例值: 10

                `TotalCount (int)`: 总数量
                    示例值: 10

        """
        return self.__request('ListClustersOfWorkspace', params)

    def list_workspace_labels(self, params):
        """ 获取工作空间的标签列表

        Args:
            params (Dict):

                `Filter (Dict)`: 选填, 筛选条件

                    `Exact (bool)`: 选填, 是否精准匹配
                        示例值: True

                    `MatchPreset (bool)`: 选填, 是否匹配预设标签
                        示例值: True

                    `IsPublic (bool)`: 选填, 是否查询公开workspace
                        示例值: True

                    `Keywords (List[str])`: 选填, 匹配列表
                        示例值: ["DNA"]

        Returns:
            Dict:

                `Items (List[Dict])`: 标签列表

                    `Name (str)`: 标签名称
                        示例值: name

                    `Count (int)`: 标签对应的workspace数目
                        示例值: 10

                `TotalCount (int)`: 标签总数
                    示例值: 10

        """
        return self.__request('ListWorkspaceLabels', params)

    def list_clusters(self, params):
        """ 查看所有集群

        Args:
            params (Dict):

                `PageNumber (int)`: 选填, 页码
                    示例值: 1

                `PageSize (int)`: 选填, 页长
                    示例值: 10

                `Filter (Dict)`: 选填, 筛选条件

                    `IDs (List[str])`: 选填, ID列表
                        示例值: ["ucxxxxxxxxxxxxxxxxxxx"]

                    `Status (List[str])`: 选填, 集群状态列表
                        示例值: ["Running"]

                    `Type (List[str])`: 选填, 集群类型(volc-vke, external, shared)
                        示例值: ["shared"]

                    `Public (bool)`: 选填, 默认为False，若为True，则集群对所有人可见
                        示例值: True

                    `Keyword (str)`: 选填, 名称模糊匹配
                        示例值: "test"

        Returns:
            Dict:

                `Items (List[Dict])`: cluster列表

                    `ID (str)`: 纳管集群ID
                        示例值: ucxxxxxxxxxxxxxxxxxxx

                    `Name (str)`: 纳管集群名称
                        示例值: name

                    `Status (str)`: 集群纳管状态（Creating、CreateFailed、Running、Error、Deleting、DeleteFailed、Updating、Stopped）
                        示例值: Creating

                    `StartTime (int)`: 起始时间
                        示例值: 1673525239

                    `Description (str)`: 投递记录描述
                        示例值: description

                    `ErrorMessage (str)`: 集群纳管过程中出现问题时的错误信息
                        示例值: err message

                    `Bound (bool)`: 是否存在绑定的 workspace
                        示例值: False

                    `Public (bool)`: 是否是公共集群
                        示例值: True

                    `VKEConfig (Dict)`: vke 集群信息

                        `ClusterID (str)`: vke集群的clusterID,通过https://www.volcengine.com/docs/6460/115190查询
                            示例值: ccexxxxxxxxxxxxxxxxxx

                        `StorageClass (str)`: vke集群已安装的 StorageClass 的名称
                            示例值: ebs-ssd

                        `VCIEnabled (bool)`: vke集群是否运行VCI
                            示例值: True

                    `ExternalConfig (Dict)`: 外部集群配置

                        `WESEndpoint (str)`: WES 地址
                            示例值: http://192.168.0.1:8002/ga4gh/wes/v1

                        `JupyterhubEndpoint (str)`: jupyterhub 地址
                            示例值: http://jupyterhub-hub:8081/jupyterhub

                        `ResourceScheduler (str)`: 外部资源调度程序
                            示例值: SGE

                        `Filesystem (str)`: 工作流计算引擎依赖的文件系统（tos, local）
                            示例值: tos

                        `ExecutionRootDir (str)`: 工作流计算引擎执行根路径, 当且仅当工作流计算引擎依赖的文件系统为 `local` 时会有
                            示例值: /root

                        `S3ProxyConfig (Dict)`: 文件系统存储的s3proxy代理信息

                            `Endpoint (str)`: 访问地址
                                示例值: http://192.168.0.3:8000

                            `Region (str)`: 区域
                                示例值: cn-beijing

                            `AccessKey (str)`: 访问s3proxy的AccessKey
                                示例值: AKxxxx

                            `SecretKey (str)`: 访问s3proxy的SecretKey
                                示例值: xxxxxx

                            `ForcePathStyle (bool)`: 是否强制使用path style, 还是使用virtual style
                                示例值: True

                    `SharedConfig (Dict)`: 共享集群配置,暂无具体配置信息
                            示例值: {}

                    `StoppedTime (int)`: 截止时间
                        示例值: 1673525239

                `PageNumber (int)`: 页码
                    示例值: 1

                `PageSize (int)`: 页长
                    示例值: 10

                `TotalCount (int)`: 总数量
                    示例值: 10

        """
        return self.__request('ListClusters', params)

    def delete_cluster(self, params):
        """ 删除集群

        Args:
            params (Dict):

                `ID (str)`: 必选, 集群ID
                    示例值: ucxxxxxxxxxxxxxxxxxxx

        Returns:
            Dict: empty dictionary

        """
        return self.__request('DeleteCluster', params)

    def update_api_accesskey(self, params):
        """ 创建或更新集群的API aksk

        Args:
            params (Dict):

                `ClusterID (str)`: 必选, 集群ID
                    示例值: ucxxxxxxxxxxxxxxxxxxx

                `AccessKeyID (str)`: 必选, 创建或更新的Access Key ID
                    示例值: AKxxxxxxxx

                `SecretAccessKey (str)`: 必选, 创建或更新的Secret Access Key
                    示例值: xxxxxxxxxx

        Returns:
            Dict: empty dictionary

        """
        return self.__request('UpdateAPIAccessKey', params)

    def get_api_accesskey(self, params):
        """ 获取集群配置的API aksk

        Args:
            params (Dict):

                `ClusterID (str)`: 必选, 集群ID
                    示例值: ucxxxxxxxxxxxxxxxxxxx

        Returns:
            Dict:

                `AccessKeyID (str)`: 已经配置的Access Key ID, 未配置则为空

        """
        return self.__request('GetAPIAccessKey', params)

    def create_data_model(self, params):
        """ 创建数据模型

        Args:
            params (Dict):

                `WorkspaceID (str)`: 必选, 工作空间 ID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

                `Name (str)`: 必选, 数据模型文件名
                    示例值: my_entity

                `Headers (List[str])`: 必选, 表头列表
                    示例值: ["my_entity_id","aaa","bbb"]

                `Rows (List[List[str]])`: 必选, 对象列表
                    示例值: [["your-sample-3-id","AAA","BBB"]]

        Returns:
            Dict:

                `ID (str)`: 数据模型 ID
                    示例值: dcxxxxxxxxxxxxxxxxxxx

        """
        return self.__request('CreateDataModel', params)

    def list_data_models(self, params):
        """ 查询实体数据模型列表

        Args:
            params (Dict):

                `WorkspaceID (str)`: 必选, 数据模型所在的workspaceID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

        Returns:
            Dict:

                `TotalCount (int)`: 数据模型总数
                    示例值: 10

                `Items (List[Dict])`: 列表项

                    `ID (str)`: 数据模型ID
                        示例值: dccc0ne5eig41ascop420

                    `Name (str)`: 数据模型文件名
                        示例值: test-datamodel

                    `RowCount (int)`: 数据模型行数
                        示例值: 100

                    `Type (str)`: 数据模型类型（normal、set、workspace）
                        示例值: normal

        """
        return self.__request('ListDataModels', params)

    def list_data_model_rows(self, params):
        """ 分页查询实体数据模型的详细信息（行和列）

        Args:
            params (Dict):

                `WorkspaceID (str)`: 必选, 数据模型所在的workspaceID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

                `ID (str)`: 必选, Datamodel ID
                    示例值: dcxxxxxxxxxxxxxxxxxxx

                `PageNumber (int)`: 选填, 页码
                    示例值: 1

                `PageSize (int)`: 选填, 页长
                    示例值: 10

                `Filter (Dict)`: 选填, 筛选条件

                    `Keyword (str)`: 选填, 筛选数据查询
                        示例值: key

                    `InSetIDs (List[str])`: 选填, 集合表中的实体ID
                        示例值: ["dcxxxxxxxxxxxxxxxxxxx"]

                `SortBy (str)`: 选填, 排序字段（默认为id）
                    示例值: CreateTime

                `SortOrder (str)`: 选填, 排序顺序（Desc Asc）
                    示例值: Desc

        Returns:
            Dict:

                `Headers (List[str])`: 表头列表
                    示例值: ["my_entity_id","aaa","bbb"]

                `Rows (List[List[str]])`: 对象列表
                    示例值: [["your-sample-3-id","AAA","BBB"]]

                `PageNumber (int)`: 分页页码
                    示例值: 1

                `PageSize (int)`: 分页页长
                    示例值: 10

                `TotalCount (int)`: 总条数
                    示例值: 100

        """
        return self.__request('ListDataModelRows', params)

    def delete_data_model_rows_and_headers(self, params):
        """ 删除实体数据模型的具体行和列

        Args:
            params (Dict):

                `WorkspaceID (str)`: 必选, 数据模型所在的workspaceID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

                `ID (str)`: 必选, Datamodel ID
                    示例值: dcxxxxxxxxxxxxxxxxxxx

                `RowIDs (List[siring])`: 选填, 需要删除的数据模型行ID
                    示例值: ["0cafd453-e9fd-4147-bc39-0a16e3d4fedd"]

                `Headers (List[str])`: 选填, 需要删除的数据模型列名
                    示例值: ["sample_id"]

        Returns:
            Dict: empty dictionary

        """
        return self.__request('DeleteDataModelRowsAndHeaders', params)

    def create_submission(self, params):
        """ 投递工作流

        Args:
            params (Dict):

                `WorkspaceID (str)`: 必选, 提交submussion的workspaceID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

                `WorkflowID (str)`: 必选, 提交submission所使用的workflow的ID
                    示例值: fcxxxxxxxxxxxxxxxxxxx

                `Name (str)`: 必选, 投递名称
                    示例值: name

                `Description (str)`: 选填, 投递描述
                    示例值: description

                `DataModelID (str)`: 选填, 数据模型ID
                    示例值: dcxxxxxxxxxxxxxxxxxxx

                `DataModelRowIDs (List[str])`: 选填, 数据模型行ID
                    示例值: ["0cafd453-e9fd-4147-bc39-0a16e3d4fedd"]

                `Inputs (str)`: 必选, 输入配置，json序列化后的string
                    示例值: {"test.name1":"this.name1","test.name2":"this.name2","test.request":"this.requestFile"}

                `Outputs (str)`: 必选, 输出配置，json序列化后的string
                    示例值: {"test.response1":"this.response1","test.response2":"this.response2"}

                `ExposedOptions (Dict)`: 必选, 平台暴露的Workflow Options

                    `ReadFromCache (bool)`: 必选, 是否开启call-cache
                        示例值: True

                    `ExecutionRootDir (str)`: 必选, 工作流执行根路径，若为vke集群，则为s3:// + workspace所绑定的桶名，若为外部hpc集群，则为共享文件存储路径，如/share/data
                        示例值: s3://bioos-wcxxxxxxxxxxxxxxxxxxx

                `ClusterID (str)`: 必选, 运行集群ID
                    示例值: ucxxxxxxxxxxxxxxxxxxx

        Returns:
            Dict:

                `ID (str)`: Submission ID
                    示例值: scxxxxxxxxxxxxxxxxxxx

        """
        return self.__request('CreateSubmission', params)

    def list_submissions(self, params):
        """ 查询工作流投递记录列表

        Args:
            params (Dict):

                `WorkspaceID (str)`: 必选, submission所在的workspaceID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

                `Filter (Dict)`: 选填, 筛选条件

                    `WorkflowID (str)`: 选填, 根据工作流ID筛选
                        示例值: fcxxxxxxxxxxxxxxxxxxx

                    `Status (List[str])`: 选填, 根据状态筛选（Succeeded、Failed、Running、Cancelled、Cancelling）
                        示例值: ["Running","Cancelling"]

                    `ClusterID (str)`: 选填, 根据集群ID筛选
                        示例值: ucxxxxxxxxxxxxxxxxxxx

                    `Keyword (str)`: 选填, 根据名称筛选
                        示例值: key

                    `IDs (List[str])`: 选填, 根据submission ID筛选
                        示例值: ["scxxxxxxxxxxxxxxxxxxx"]

                `PageNumber (int)`: 选填, 页码
                    示例值: 1

                `PageSize (int)`: 选填, 页长
                    示例值: 10


        Returns:
            Dict:
                `Items (List[Dict])`: Workflow 列表

                    `ID (str)`: 投递记录ID
                        示例值: scxxxxxxxxxxxxxxxxxxx

                    `Name (str)`: 投递记录名称
                        示例值: name

                    `Description (str)`: 投递记录描述
                        示例值: description

                    `Status (str)`: 投递记录状态（Succeeded、Failed、Running、Cancelled、Cancelling）
                        示例值: Running

                    `RunStatus (Dict)`: 工作流运行状态

                        `Count (int)`: 工作流运行统计
                            示例值: 120

                        `Succeeded (int)`: 运行成功的工作流运行总数
                            示例值: 90

                        `Failed (int)`: 运行失败的工作流运行总数
                            示例值: 5

                        `Running (int)`: 运行中的工作流运行总数
                            示例值: 5

                        `Pending (int)`: 启动中的工作流运行总数
                            示例值: 5

                        `Cancelling (int)`: 终止中的工作流运行总数
                            示例值: 5

                        `Cancelled (int)`: 已终止的工作流运行总数
                            示例值: 10

                    `StartTime(int)`: 起始时间
                        示例值: 1673525239

                    `FinishTime(int)`: 截止时间
                        示例值: 1673525239

                    `Duration(int)`: 分析耗时(单位为s)
                        示例值: 10

                    `WorkflowID (str)`: 工作流ID
                        示例值: fcxxxxxxxxxxxxxxxxxxx

                    `ClusterID (str)`: 集群ID
                        示例值: ucxxxxxxxxxxxxxxxxxxx

                    `ClusterType (str)`: 集群类型（volc-vke、external、shared）若集群不存在则为空
                        示例值: shared

                    `DataModelID (str)`: 数据实体ID
                        示例值: dcxxxxxxxxxxxxxxxxxxx

                    `Inputs (str)`: 输入配置, json序列化后的字符串
                        示例值: {"test.name1":"this.name1", "test.name2":"this.name2", "test.request":"this.requestFile"}

                    `Outputs (str)`: 输出配置, json序列化后的字符串
                        示例值: {"test.response1":"this.response1", "test.response2":"this.response2"}

                    `ExposeOptions (Dict)`: 平台暴露的Workflow Options

                        `ReadFromCache (bool)`: 是否开启读call-cache功能
                            示例值: False

                        `ExecutionRootDir (str)`: 工作流执行根路径
                            示例值: /root

                    `OwnerName (str)`: 创建者名称
                        示例值: name

                    `DataEntity (Dict)`: 数据实体统计

                        `ID (str)`: 数据实体ID
                            示例值: dcxxxxxxxxxxxxxxxxxxx

                        `Name (str)`: 数据实体名称
                            示例值: name

                        `RowIDs (List[str])`: 数据实体行IDs
                            示例值: ["1"]

                `PageNumber (int)`: 页码
                    示例值: 1

                `PageSize (int)`: 页长
                    示例值: 10

                `TotalCount (int)`: 总数量
                    示例值: 10

        """
        return self.__request('ListSubmissions', params)

    def list_overview_submissions(self, params):
        """ 获取全局投递列表

        Args:
            params (Dict):

                `PageNumber (int)`: 选填, 分页页码
                    示例值: 1

                `PageSize (int)`: 选填, 分页页长
                    示例值: 10

                `SortBy (str)`: 选填, 按字段排序（OwnerName StartTime）
                    示例值: OwnerName

                `SortOrder (str)`: 选填, 排序顺序
                    示例值: Desc

        Returns:
            Dict:

                `Items (List[Dict])`: 投递记录列表

                    `ID (str)`: 投递记录 ID
                        示例值: scxxxxxxxxxxxxxxxxxxx

                    `Name (str)`: 投递记录名称
                        示例值: name

                    `WorkspaceID (str)`: 工作空间 ID
                        示例值: wcxxxxxxxxxxxxxxxxxxx

                    `WorkspaceName (str)`: 工作空间名称
                        示例值: name

                    `OwnerUserID (int)`: 创建者用户ID 仅子账号有值
                        示例值: 123456

                    `OwnerName (str)`: 创建者名称
                        示例值: name

                    `Description (str)`: 投递记录描述
                        示例值: description

                    `Status (str)`: 投递记录状态 Succeeded,Failed,Running,Cancelled,Cancelling
                        示例值: Succeeded

                    `StartTime (int)`: 起始时间
                        示例值: 1673525239

                    `Duration (int)`: 分析耗时(单位为s)
                        示例值: 10

                    `WorkflowID (str)`: 工作流 ID
                        示例值: fcxxxxxxxxxxxxxxxxxxx

                `PageNumber (int)`: 分页页码
                    示例值: 1

                `PageSize (int)`: 分页页长
                    示例值: 10

                `TotalCount (int)`: 总条数
                    示例值: 100

        """
        return self.__request('ListOverviewSubmissions', params)

    def delete_submission(self, params):
        """ 删除工作流投递记录

        Args:
            params (Dict):

                `ID (str)`: 必选, 投递记录 ID
                    示例值: scxxxxxxxxxxxxxxxxxxx

                `WorkspaceID (str)`: 必选, 工作空间 ID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

        Returns:
            Dict: empty dictionary

        """
        return self.__request('DeleteSubmission', params)

    def cancel_submission(self, params):
        """ 终止工作流投递记录

        Args:
            params (Dict):

                `ID (str)`: 必选, 投递记录 ID
                    示例值: scxxxxxxxxxxxxxxxxxxx

                `WorkspaceID (str)`: 必选, 工作空间 ID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

        Returns:
            Dict: empty dictionary

        """
        return self.__request('CancelSubmission', params)

    def list_runs(self, params):
        """ 查询工作流运行列表

        Args:
            params (Dict):

                `WorkspaceID (str)`: 必选, submission所在的workspaceID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

                `SubmissionID (str)`: 必选, submission的ID
                    示例值: scxxxxxxxxxxxxxxxxxxx

                `Filter (Dict)`: 选填, 筛选条件

                    `Keyword (str)`: 选填, 运行记录关键字
                        示例值: key

                    `IDs (List[str])`: 选填, 运行记录ID列表
                        示例值: ["rcxxxxxxxxxxxxxxxxxxx"]

                    `Status (List[str])`: 选填, 根据状态筛选（Pending、Running、Succeeded、Failed、Cancelling、Cancelled）
                        示例值: ["Pending","Running"]

                `PageNumber (int)`: 选填, 页码
                    示例值: 1

                `PageSize (int)`: 选填, 页长
                    示例值: 10

        Returns:
            Dict:

                `Items (List[Dict])`: Run列表

                    `ID (str)`: 运行记录ID
                        示例值: rcxxxxxxxxxxxxxxxxxxx

                    `DataEntityRowID (str)`: 数据实体 RowID
                        示例值: 1

                    `Status (str)`: 投递记录状态（Succeeded、Failed、Running、Pending、Cancelling、Cancelled）
                        示例值: Running

                    `StartTime (int)`: 起始时间
                        示例值: 1673525239

                    `FinishTime (int)`: 截止时间
                        示例值: 1673525239

                    `Duration (int)`: 分析耗时(单位为s)
                        示例值: 10

                    `SubmissionID (str)`: 投递记录ID
                        示例值: scxxxxxxxxxxxxxxxxxxx

                    `EngineRunID (str)`: 工作流引擎内运行记录 ID
                        示例值: 05693535-dcf4-404f-8d18-2d3cac29916b

                    `Inputs (str)`: 运行记录输入参数，json 序列化后的 string
                        示例值: {"test.name1":"world","test.name2":"hello","test.request":"s3://vci-dev/jxc-test/aaa.txt"}

                    `Outpus (str)`: 运行记录输出参数，json 序列化后的 string
                        示例值: {"test.resp":"abc",
                        "test.response1":"s3://bioos-dev-wcb1e3v5eig4635iurevg/analysis/scb8gbtleig4f4jqjbtlg/test/d9ea2df5-b8d8-4603-9f62-496229e922c9/call-step21/execution/resp.txt",
                        "test.response2":"s3://bioos-dev-wcb1e3v5eig4635iurevg/analysis/scb8gbtleig4f4jqjbtlg/test/d9ea2df5-b8d8-4603-9f62-496229e922c9/call-step22/execution/resp.txt"}

                    `TaskStatus (Dict)`: 工作流运行详情状态统计

                        `Count (int)`: 任务运行统计
                            示例值: 120

                        `Succeeded (int)`: 运行成功的工作流运行总数
                            示例值: 90

                        `Failed (int)`: 运行失败的工作流运行总数
                            示例值: 5

                        `Running (int)`: 运行中的工作流运行总数
                            示例值: 5

                        `Queued (int)`: 排队中的工作流运行总数
                            示例值: 5

                        `Initializing (int)`: 启动中的工作流运行总数
                            示例值: 5

                        `Cancelled (int)`: 已终止的工作流运行总数
                            示例值: 10

                    `Log (str)`: 运行记录日志存储路径
                        示例值: s3://bioos-wcxxxxxxxxxxxxxxxxxxx/analysis/scxxxxxxxxxxxxxxxxxxx/workflow.941846fb-158d-4d49-82e0-f2f39372e9e3.log

                    `Message (str)`: 运行记录错误详情
                        示例值: error message

                `PageNumber (int)`: 页码
                    示例值: 1

                `PageSize (int)`: 页长
                    示例值: 10

                `TotalCount (int)`: 总数量
                    示例值: 10

        """
        return self.__request('ListRuns', params)

    def cancel_run(self, params):
        """ 取消工作流运行

        Args:
            params (Dict):

                `ID (str)`: 必选, 运行记录 ID
                    示例值:

                `WorkspaceID (str)`: 必选, 工作空间ID
                    示例值:

        Returns:
            Dict: empty dictionary

        """
        return self.__request('CancelRun', params)

    def list_tasks(self, params):
        """ 查询工作流的task任务列表

        Args:
            params (Dict):

                `WorkspaceID (str)`: 必选, submission所在的workspaceID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

                `RunID (str)`: 必选, 运行记录ID
                    示例值: rcxxxxxxxxxxxxxxxxxxx

                `PageNumber (int)`: 选填, 页码
                    示例值: 1

                `PageSize (int)`: 选填, 页长
                    示例值: 10

        Returns:
            Dict:

                `Items (List[Dict])`: Task列表

                    `Name (str)`: 任务名称
                        示例值: name

                    `RunID (str)`: 运行记录 ID
                        示例值: rcxxxxxxxxxxxxxxxxxxx

                    `Status (str)`: 任务状态，Succeeded -> 分析成功, Failed -> 分析失败, Running -> 分析中, Queued -> 排队中, Initializing -> 启动中, Cancelled -> 已终止
                        示例值: Succeeded

                    `StartTime (int)`: 起始时间
                        示例值: 1687143483

                    `FinishTime (int)`: 截止时间
                        示例值: 1687143668

                    `Duration (int)`: 分析耗时(单位为s)
                        示例值: 185

                    `Log (str)`: 任务日志存储路径
                        示例值: s3://bioos-wcxxxxxxxxxxxxxxxxxxx/analysis/scxxxxxxxxxxxxxxxxxxx/workflow.941846fb-158d-4d49-82e0-f2f39372e9e3.log

                    `Stdout (str)`: 任务输出存储路径
                        示例值: s3://bioos-wcxxxxxxxxxxxxxxxxxxx/analysis/scxxxxxxxxxxxxxxxxxxx/melt/cd28ec5b-75df-4981-a7f5-90f1deba8a94/call-step1/shard-0/execution/stdout

                    `Stderr (str)`: 任务错误存储路径
                        示例值: s3://bioos-wcxxxxxxxxxxxxxxxxxxx/analysis/scxxxxxxxxxxxxxxxxxxx/melt/cd28ec5b-75df-4981-a7f5-90f1deba8a94/call-step1/shard-0/execution/stderr

                    `ExecuteDuration (int)`: 实际运行分析耗时(单位为s)
                        示例值: 0

                    `JobName (str)`: job名称
                        示例值: task-xxxxxxxx-ex-00

                    `resourceClaimed (Dict)`: 资源申领

                        `CPUCore (int)`: CPU 核数
                            示例值: 1

                        `MemoryGiB (int)`: 内存大小，单位GiB
                            示例值: 2

                        `StorageGiB (int)`: 存储大小，单位GiB
                            示例值: 2

                        `GPUGiB (int)`: GPU显存大小，单位GiB
                            示例值: 2

                    `resourceUsed (Dict)`: 资源消耗

                        `CPUCore (int)`: CPU 核数
                            示例值: 1

                        `MemoryGiB (int)`: 内存大小，单位GiB
                            示例值: 2

                        `StorageGiB (int)`: 存储大小，单位GiB
                            示例值: 2

                        `GPUGiB (int)`: GPU显存大小，单位GiB
                            示例值: 2

                `PageNumber (int)`: 页码
                    示例值: 1

                `PageSize (int)`: 页长
                    示例值: 10

                `TotalCount (int)`: 总数量
                    示例值: 10

        """
        return self.__request('ListTasks', params)

    def create_workflow(self, params):
        """ 此接口为异步接口，当此接口返回成功时，会返回导入的workflowID信息，此时并不代表workflow导入成功，
        需要调用ListWorkflows接口查看workflow导入情况，其返回的参数WorkflowImportStatus如果为Succeeded则为导入成功。

        Args:
            params (Dict):

                `WorkspaceID (str)`: 必选, 工作空间 ID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

                `Name (str)`: 必选, 工作流名称
                    示例值: name

                `Description (str)`: 选填, 工作流描述
                    示例值: description

                `Language (str)`: 必选, 语言类型, 包括 WDL/CWL/Nextflow
                    示例值: WDL

                `Source (str)`: 选填, 来源, http(s) 开头的地址, 为 file 来源类型时不填
                    示例值: https://aaa.bbb.git

                `Tag (str)`: 选填, tag, 为 dockstore 来源类型时对应 version, 为 file 来源类型时不填
                    示例值: v1.0.0

                `Token (str)`: 选填, git token, 为 dockstore/file 来源类型时不填
                    示例值:

                `MainWorkflowPath (str)`: 选填, 主工作流文件路径, 为 dockstore 来源时不填
                    示例值: main.wdl

                `SourceType (str)`: 必选, 来源类型, 包括 git dockstore file
                    示例值: git

                `Content (bytes)`: 选填, 文件导入的二进制 zip 包 base64 编码
                    示例值:

        Returns:
            Dict:

                `ID (str)`: WorkflowID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

        """
        return self.__request('CreateWorkflow', params)

    def list_workflows(self, params):
        """ 查询符合条件的workflows列表

        Args:
            params (Dict):

                `WorkspaceID (str)`: 必选, workflow所在的workspaceID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

                `PageNumber (int)`: 选填, 页码
                    示例值: 1

                `PageSize (int)`: 选填, 页长
                    示例值: 10

                `Filter (Dict)`: 选填, 筛选条件

                    `Keyword (str)`: 选填, 根据名称筛选
                        示例值: key

                    `IDs (List[str])`: 选填, ID列表
                        示例值: ["wcxxxxxxxxxxxxxxxxxxx"]

                `SortBy (str)`: 选填, 排序字段（Name CreateTime）
                    示例值: CreateTime

                `SortOrder (str)`: 选填, 排序顺序（Desc Asc）
                    示例值: Desc

        Returns:
            Dict:

                `Items (List[Dict])`: Workflow 列表

                    `ID (str)`: 工作流 ID
                        示例值: fcxxxxxxxxxxxxxxxxxxx

                    `Name (str)`: 工作流名称
                        示例值: name

                    `Description (str)`: 工作流描述
                        示例值: description

                    `CreateTime (int)`: 创建时间
                        示例值: 1673525239

                    `UpdateTime (int)`: 更新时间
                        示例值: 1673525239

                    `Language (str)`: 语言类型
                        示例值: WDL

                    `Source (str)`: 来源, http(s) 开头的地址
                        示例值: https://aaa.bbb.git

                    `Tag (str)`: tag
                        示例值: master

                    `Token (str)`: token
                        示例值:

                    `MainWorkflowPath (str)`: 主工作流文件路径
                        示例值: main.wdl

                    `Status (Dict)`: workflow导入状态

                        `Phase (str)`: workflow导入状态（Importing、Succeeded、Failed）
                            示例值: Succeeded

                        `Message (str)`: 导入失败原因，Phase为Failed时有效
                            示例值:

                    `Inputs (Dict)`: wdl的intput信息

                        `Name (str)`: 参数名称
                            示例值: test

                        `Type (str)`: 参数类型
                            示例值: String

                        `Optional (bool)`: 是否是可选参数
                            示例值: True

                        `Default (str)`: 默认值
                            示例值: test

                    `Outputs (Dict)`: wdl的output信息

                        `Name (str)`: 参数名称
                            示例值: test

                        `Type (str)`: 参数类型
                            示例值: String

                        `Optional (bool)`: 是否是可选参数
                            示例值: True

                        `Default (str)`: 默认值
                            示例值: test

                    `OwnerName (str)`: 创建者名称
                        示例值: name

                    `Graph (str)`: wdl graph
                        示例值:

                    `SourceType (str)`: 来源类型, 包括git dockstore
                        示例值: git

                `PageNumber (int)`: 页码
                    示例值: 1

                `PageSize (int)`: 页长
                    示例值: 10

                `TotalCount (int)`: 总数量
                    示例值: 10

        """
        return self.__request('ListWorkflows', params)

    def update_workflow(self, params):
        """ 该接口的使用方式与CreateWorkflow类型一样，都需要ListWorkflows接口查看状态

        Args:
            params (Dict):

                `WorkspaceID (str)`: 必选, 工作空间 ID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

                `ID (str)`: 必选, 工作流 ID
                    示例值: fcxxxxxxxxxxxxxxxxxxx

                `Name (str)`: 必选, 工作流名称
                    示例值: name

                `Description (str)`: 选填, 工作流描述
                    示例值: description

                `Source (str)`: 选填, 来源, http(s) 开头的地址, 为 file 来源类型时不填
                    示例值: https://aaa.bbb.git

                `Tag (str)`: 选填, tag, 为 dockstore 来源类型时对应 version, 为 file 来源类型时不填
                    示例值: master

                `Token (str)`: 选填, token, 为 dockstore/file 来源类型时不填
                    示例值:

                `MainWorkflowPath (str)`: 选填, 主工作流文件路径, 为 dockstore 来源时不填
                    示例值: main.wdl

                `Content (bytes)`: 选填, 文件导入的二进制 zip 包
                    示例值:

        Returns:
            Dict: empty dictionary

        """
        return self.__request('UpdateWorkflow', params)

    def delete_workflow(self, params):
        """ 删除工作流

        Args:
            params (Dict):

                `WorkspaceID (str)`: 必选, 工作空间 ID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

                `ID (str)`: 必选, 工作流 ID
                    示例值: fcxxxxxxxxxxxxxxxxxxx

        Returns:
            Dict: empty dictionary

        """
        return self.__request('DeleteWorkflow', params)

    def get_notebook_edit_info(self, params):
        """ 启动Notebook Server并获取访问链接

        Args:
            params (Dict):

                `WorkspaceID (str)`: 必选, 工作空间 ID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

                `Name (str)`: 选填, Notebook文件名 对于Dashboard则为__dashboard__
                    示例值: __dashboard__

        Returns:
            Dict:

                `URL (str)`: jupyter访问链接
                    示例值: https://bioos-xxx.xxx.volcanicengine.com/notebook-01/user/ucxxxxxxxxxxxxxxxxxxx/wcxxxxxxxxxxxxxxxxxxx

        """
        return self.__request('GetNotebookEditInfo', params)

    def get_notebook_server_settings(self, params):
        """ 获取当前Notebook Server配置信息

        Args:
            params (Dict):

                `WorkspaceID (str)`: 必选, 工作空间 ID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

        Returns:
            Dict:

                `ResourceSize (str)`: 资源规格，如果从未配置过返回"" small,middle,large等
                    示例值: small

                `ImageID (str)`: 镜像 ID，如果从未配置过返回""
                    示例值: 1

                `TempImageName (str)`: 临时镜像名，如果从未配置过返回""
                    示例值: jupyter/minimal-notebook

                `MountTOSEnabled (bool)`: 是否挂载TOS桶
                    示例值: True

                `StorageCapacity (int)`: 存储容量（byte）
                    示例值: 107374182400

        """
        return self.__request('GetNotebookServerSettings', params)

    def get_notebook_server_stat(self, params):
        """ 获取当前Notebook Server状态

        Args:
            params (Dict):

                `WorkspaceID (str)`: 必选, 工作空间 ID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

        Returns:
            Dict:

                `Status (str)`: Server当前状态, spawn,ready,stop,absent
                    示例值: spawn

                `TOSAccessible (str)`: TOS挂载生效状态 取值有 OK ClusterNotSupport AccessKeyNotSet AccessKeyInvalid CSINotInstall CSINotReady BucketNotExist
                    示例值: OK

        """
        return self.__request('GetNotebookServerStat', params)

    def list_notebook_server_images(self, params):
        """ 列举Notebook Server镜像信息

        Args:
            params (Dict):

                `ImageIDs (List[str])`: 选填, 镜像ID，不传则返回所有
                    示例值: ["1","2"]

                `Source (str)`: 选填, 镜像来源 official,customized
                    示例值: official

                `Status (str)`: 选填, 镜像审核状态 pending,approve,reject
                    示例值: pending

                `DisplayName (str)`: 选填, 镜像名
                    示例值:

                `ImageName (str)`: 选填, 镜像地址
                    示例值: python:latest

                `OwnByMe (bool)`: 选填, 是否仅查看当前登录者所建镜像
                    示例值: True

                `PageNumber (int)`: 分页页码
                    示例值: 1

                `PageSize (int)`: 分页页长
                    示例值: 10

                `SortBy (str)`: 按字段排序, 取值有CreateTime ID
                    示例值: CreateTime

                `SortOrder (str)`: 排序顺序, Desc Asc
                    示例值: Desc

        Returns:
            Dict:

                `Images (List[Dict])`: 镜像信息列表

                    `ImageID (str)`: 镜像 ID
                        示例值: 1

                   `DisplayName (str)`: 镜像名称(展示用)
                       示例值: minimal-notebook

                   `ImageName (str)`: 镜像名称
                       示例值: jupyter/minimal-notebook

                   `Description (str)`: 描述
                       示例值: description

                   `AccountID (int)`: 创建者主账户ID
                       示例值: 0

                   `UserID (int)`: 创建者租户ID
                       示例值: 0

                   `Status (str)`: 镜像状态 pending,approve,building,failure
                       示例值: pending

                   `Source (str)`: 镜像来源 official,building
                       示例值: official

                   `Packages (Dict)`: 工具包

                        `Pip (Dict[str, str])`: pip工具包
                            示例值: {"numpy":"1.22.2"}

                        `Conda (Dict[str, str])`: conda工具包
                            示例值: {"numpy":"1.22.2"}

                        `R (Dict[str, str])`: R工具包
                            示例值: {"ggplot2":"3.4.4"}

                        `APT (Dict[str, str])`: apt工具包
                            示例值: {"python3-dev":"1.22.2"}

                   `BasicEnv (List[str])`: 基础环境参数，如python3.8等
                       示例值: ["Python3.9.10", "R 4.1.2", "Julia 1.7.2"]

                   `ImageVersion (str)`: 镜像版本
                       示例值: 1.0.0

                   `CreateTime (int)`: 创建时间
                       示例值: 1680554098

                   `UpdateTime (int)`: 更新时间
                       示例值: 1680554098

        """
        return self.__request('ListNotebookServerImages', params)

    def list_notebook_server_resource_opts(self, params):
        """ 列举Notebook Server可用资源配置

        Args:
            params (Dict): empty dictionary

        Returns:
            Dict:

                `ResourceSize (List[Dict])`: 资源规格

                    `ResourceSize (str)`: 资源规格枚举 small,middle,large等
                        示例值: small

                    `Cpu (int)`: 资源规格内容 cpu内核数（个）
                        示例值: 2

                    `Memory (int)`: 资源规格内容 memory大小（byte）
                        示例值: 8589934592

        """
        return self.__request('ListNotebookServerResourceOpts', params)

    def stop_notebook_server(self, params):
        """ 即时暂停当前Notebook Server

        Args:
            params (Dict):

                `WorkspaceID (str)`: 必选, 工作空间 ID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

        Returns:
            Dict: empty dictionary

        """
        return self.__request('StopNotebookServer', params)

    def update_notebook_server_settings(self, params):
        """ 更新Notebook Server配置并异步暂停当前Notebook Server

        Args:
            params (Dict):

                `WorkspaceID (str)`: 必选, 工作空间 ID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

                `ResourceSize (str)`: 选填, 资源规格，没变化则不传 small,middle,large
                    示例值: small

                `ImageID (str)`: 选填, 镜像 ID，没变化则不传，与临时镜像名字端互斥
                    示例值: 1

                `MountTOSEnabled (bool)`: 选填, 是否挂载TOS桶，没变化则不传
                    示例值: False

                `TempImageName (str)`: 选填, 临时镜像名，没变化则不传，与镜像ID字段互斥
                    示例值: jupyter/minimal-notebook

        Returns:
            Dict: empty dictionary

        """
        return self.__request('UpdateNotebookServerSettings', params)

    def create_notebook_server_image(self, params):
        """ 创建Notebook Server镜像

        Args:
            params (Dict):

                `BaseImage (str)`: 必选, 基础镜像。仅building镜像需要
                    示例值: python:latest

                `ImageName (str)`: 必选, 镜像名称
                    示例值: custom:v1.0.0

                `DisplayName (str)`: 必选, 镜像名称（展示用）
                    示例值: custom

                `Description (str)`: 选填, 镜像描述
                    示例值: description

                `BuildScript (str)`: 选填, 构建镜像中需要执行的shell脚本内容
                    示例值:

                `Source (str)`: 必选, 镜像来源, 取值为building
                    示例值: building

                `Packages (Dict)`: 必选, 工具包

                    `Pip (Dict[str, str])`: 选填, pip工具包
                        示例值: {"numpy":"1.22.2"}

                    `Conda (Dict[str, str])`: 选填, conda工具包
                        示例值: {"numpy":"1.22.2"}

                    `R (Dict[str, str])`: 选填, R工具包
                        示例值: {"ggplot2":"3.4.4"}

                    `APT (Dict[str, str])`: 选填, apt工具包
                        示例值: {"python3-dev":"1.22.2"}

                `BasicEnv (List[str])`: 选填, 基础环境参数，如python3.8等
                    示例值: ["Python3.9.10", "R 4.1.2", "Julia 1.7.2"]

                `ImageVersion (str)`: 必选, 镜像版本
                    示例值: 1.0.0

        """
        return self.__request('CreateNotebookServerImage', params)

    def list_notebook_servers(self, params):
        """ 获取全局Notebook Server列表

        Args:
            params (Dict):

                `PageNumber (int)`: 选填, 分页页码
                    示例值: 1

                `PageSize (int)`: 选填, 分页页长
                    示例值: 10

                `Filter (Dict)`: 选填, 筛选条件

                    `Status	(List[str])`: 选填, 筛选状态（spawn,ready,stop,absent）
                        示例值: spawn

                    `WorkspaceID (str)`: 选填, 工作空间 ID
                        示例值: wcxxxxxxxxxxxxxxxxxxx

                    `UserID	 (int)`: 选填, 创建者用户ID 查主账号时则填0
                        示例值: 123456

                `SortBy (str)`: 选填, 按字段排序（OwnerName StartTime StorageCapacity LastActivityTime）
                    示例值: OwnerName

                `SortOrder (str)`: 选填, 排序顺序
                    示例值: Desc

        Returns:
            Dict:

                List[Dict]: Items, 列表

                    `Name (str)`: 名称
                        示例值: name

                    `WorkspaceID (str)`: 工作空间 ID
                        示例值: wcxxxxxxxxxxxxxxxxxxx

                    `WorkspaceName (str)`: 工作空间名称
                        示例值: name

                    `UserID (int)`: 创建者用户ID 主账号则为空
                        示例值: 123456

                    `OwnerName (str)`: 创建者名称
                        示例值: ownerName

                    `StorageCapacity (int)`: 存储容量（byte）
                        示例值: 107374182400

                    `Status (str)`: Server当前状态（spawn,ready,stop,absent）
                        示例值: spawn

                    `LastActivityTime (int)`: 最近活跃时间
                        示例值: 1691493675

                    `StartTime (int)`: 创建时间
                        示例值: 1691493674

                    `Duration (int)`: 使用时长(单位为s)
                        示例值: 1

                `TotalCount (int)`: 总条数
                    示例值: 10

        """
        return self.__request('ListNotebookServers', params)

    def delete_notebook_server(self, params):
        """ 删除当成Notebook Server

        Args:
            params (Dict):

                `WorkspaceID (str)`: 必选, 工作空间ID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

                `UserID (int)`: 选填, 子用户ID，不传代表操作主账号
                    示例值: 123456

        Returns:
            Dict: empty dictionary

        """
        return self.__request('DeleteNotebookServer', params)

    def delete_notebook_server_settings(self, params):
        """ 删除当成Notebook Server配置信息

        Args:
            params (Dict):

                `WorkspaceID (str)`: 必选, 工作空间ID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

        Returns:
            Dict: empty dictionary

        """
        return self.__request('DeleteNotebookServerSettings', params)

    def get_notebook_server_extra_packages(self, params):
        """ 获取当前Notebook Server安装的额外包信息

        Args:
            params (Dict):

                `WorkspaceID (str)`: 必选, 工作空间ID
                    示例值: wcxxxxxxxxxxxxxxxxxxx

        Returns:
            Dict:

                `ExtraPackages (Dict)`: 额外工具包

                    `Pip (Dict[str, str])`: 选填, pip工具包
                        示例值: {"numpy":"1.22.2"}

                    `Conda (Dict[str, str])`: 选填, conda工具包
                        示例值: {"numpy":"1.22.2"}

                    `R (Dict[str, str])`: 选填, R工具包
                        示例值: {"ggplot2":"3.4.4"}

                    `APT (Dict[str, str])`: 选填, apt工具包
                        示例值: {"python3-dev":"1.22.2"}

        """
        return self.__request('GetNotebookServerExtraPackages', params)

    def list_data_files(self, params):
        """ 获取数据集文件列表

        Args:
            params (Dict):

                `DataSetID (str)`: 必选, 数据集ID
                    示例值: tcxxxxxxxxxxxxxxxxxxx

                `PageNumber (int)`: 选填, 分页页码
                    示例值: 1

                `PageSize (int)`: 选填, 分页页长
                    示例值: 10

                `Filter (Dict)`: 选填, 筛选条件

                    `IDs (List[str])`: 选填, 数据集ID
                        示例值: ["tcxxxxxxxxxxxxxxxxxxx"]

                    `FileType (List[str])`: 选填, 文件类型列表
                        示例值: ["csv"]

                    `Keyword (str)`: 选填, 模糊匹配名称/描述
                        示例值: key

                `SortBy (str)`: 选填, 按字段排序（Name CreateTime UpdateTime FileSize）
                    示例值: Name

                `SortOrder (str)`: 选填, 排序顺序
                    示例值: Desc

        Returns:
            Dict:

                `Items (List[Dict])`: 数据文件列表

                    `ID (str)`: 数据文件ID
                        示例值: ecxxxxxxxxxxxxxxxxxxx

                    `Name (str)`: 名称
                        示例值: name

                    `Description (str)`: 描述
                        示例值: description

                    `CreateTime (int)`: 创建时间
                        示例值: 1691493674

                    `UpdateTime (int)`: 更新时间
                        示例值: 1691493674

                    `FileType (str)`: 文件类型
                        示例值: csv

                    `FileSize (int)`: 文件大小(byte)
                        示例值: 123

                    `Source (str)`: 数据来源
                        示例值: https://cromwell.tos-xxx.volces.com/xxx.csv

                    `DRSURL (str)`: DRS 路径
                        示例值: drs://drs.xxx.xxx.com/ecxxxxxxxxxxxxxxxxxxx

                    `SampleRow (List[str])`: 数据文件样本信息
                        示例值: ["test", "测试", "2011-01-02", "2011-01-02", "txt", "", "s3://xxx/test.txt"]

                `PageNumber (int)`: 分页页码
                    示例值: 1

                `PageSize (int)`: 分页页长
                    示例值: 10

                `TotalCount (int)`: 总条数
                    示例值: 100

        """
        return self.__request('ListDataFiles', params)

    def list_data_sets(self, params):
        """ 获取数据集列表

        Args:
            params (Dict):

                `PageNumber (int)`: 选填, 分页页码
                    示例值: 1

                `PageSize (int)`: 选填, 分页页长
                    示例值: 10

                `Filter (Dict)`: 选填, 过滤条件

                    `IDs (List[str])`: 选填, 数据集ID
                        示例值: ["tcxxxxxxxxxxxxxxxxxxx"]

                    `ProjectDataTypes (List[str])`: 选填, 项目数据类型列表 ID
                        示例值:

                    `Categories	(List[str])`: 选填, 项目数据类型 ID 列表
                        示例值: ["示例数据"]

                    `Keyword (str)`: 选填, 模糊匹配名称/描述/所有者
                        示例值: key

                    `Owner (str)`: 选填, 模糊匹配数据所有者
                        示例值: ownerName

                    `Catalogues (List[str])`: 选填, 数据集编目列表 ID
                        示例值: 【“OMICSDATA”】

                `SortBy (str)`: 选填, 按字段排序（Name CreateTime）
                    示例值: Name

                `SortOrder (str)`: 选填, 排序顺序
                    示例值: Desc

        Returns:
            Dict:

                `Items (List[Dict])`: 数据集列表

                    `ID (str)`: 数据集ID
                        示例值: tcxxxxxxxxxxxxxxxxxxx

                    `Name (str)`: 名称
                        示例值: name

                    `Description (str)`: 描述
                        示例值: desc

                    `CreateTime (int)`: 创建时间
                        示例值: 1691493674

                    `UpdateTime	(int)`: 更新时间
                        示例值: 1691493674

                    `Owners (List[str])`: 数据集所有者
                        示例值: ["owner1", "owner2"]

                    `Admin (str)`: 数据集管理员
                        示例值: admin

                    `Category (str)`: 领域 ID 列表
                        示例值: 示例数据

                    `Labels	(List[str])`: 标签 ID 列表
                        示例值: ["demo"]

                    `DocURL (str)`: 帮助文档链接
                        示例值: https://console.volcengine.com/bioos/region:bioos+cn-beijing/public-workspace/wcxxxxxxxxxxxxxxxxxxx/dashboard

                    `Email (str)`: email
                        示例值: bioos@xxx.xxx

                    `Licence (str)`: 许可/使用条款
                        示例值: MIT

                    `ProjectDataTypes (List[str])`: 项目数据类型列表 ID
                        示例值:

                    `SampleScope (str)`: 样本范围
                        示例值: 111

                    `ExternalLink (str)`: 外部链接
                        示例值: https://bytedance.feishu.cn/docx/Mcxxxxxxxxxxxxxxxxxxxx

                    `ExternalLinkDescription (str)`: 外部链接描述
                        示例值: description

                    `ExampleTutorial (str)`: 示例教程
                        示例值: 111

                    `Tools (str)`: 工具/应用
                        示例值: https://bytedance.feishu.cn/docx/Mcxxxxxxxxxxxxxxxxxxxx

                    `Publications (List[Dict])`: 出版物

                        `ID (str)`: 出版物 ID
                            示例值: pcxxxxxxxxxxxxxxxxxxx

                        `Name (str)`: 名称
                            示例值: name

                        `AccessURL (str)`: 在线地址
                            示例值: http://222.com

                        `Authors (List[str])`: 作者
                            示例值: ["author1", "author2"]

                        `Quotation (str)`: 引文
                            示例值:

                    `SampleHeaders (List[str])`: 数据文件样本信息表头
                        示例值: ["文件名", "文件描述", "建立时间", "更新时间", "文件类型", "数据来源", "数据路径"]

                    `CustomHeaderOrders (Dict[str, str])`: 数据文件自定义表头顺序
                        示例值:

                    `CollectedBy (str)`: 被收藏的数据项目 ID
                        示例值: ocxxxxxxxxxxxxxxxxxxx

                    `Catalogue (str)`: 数据集编目 ID
                        示例值: OMICSDATA

                `PageNumber (int)`: 分页页码
                    示例值: 1

                `PageSize (int)`: 分页页长
                    示例值: 10

                `TotalCount (int)`: 总条数
                    示例值: 100

        """
        return self.__request('ListDataSets', params)

    def create_data_set(self, params):
        """ 创建数据集

        Args:
            params (Dict):

                `Name (str)`: 必选, 名称
                    示例值: name

                `Description (str)`: 必选, 描述
                    示例值: description

                `CreateTime (int)`: 必选, 创建时间
                    示例值: 1691493674

                `UpdateTime (int)`: 必选, 更新时间
                    示例值: 1691493674

                `Owners (List[str])`: 必选, 用户
                    示例值: ["user1", "user2"]

                `Category (str)`: 必选, 领域 ID 列表
                    示例值: 示例数据

                `Labels (List[str])`: 选填, 标签 ID 列表
                    示例值: ["demo"]

                `DocURL (str)`: 必选, 帮助文档链接
                    示例值: https://console.volcengine.com/bioos/region:bioos+cn-beijing/public-workspace/wcxxxxxxxxxxxxxxxxxxx/dashboard

                `Email (str)`: 必选, email
                    示例值: bioos

                `Licence (str)`: 选填, 许可/使用条款
                    示例值: MIT

                `ProjectDataTypes (List[str])`: 选填, 项目数据类型列表
                    示例值:

                `SampleScope (str)`: 选填, 样本范围
                    示例值: 111

                `ExternalLink (str)`: 选填, 外部链接
                    示例值: https://bytedance.feishu.cn/docx/Mcxxxxxxxxxxxxxxxxxxxx

                `ExternalLinkDescription (str)`: 选填, 外部链接描述
                    示例值: description

                `ExampleTutorial (str)`: 选填, 示例教程
                    示例值:

                `Tools (str)`: 选填, 工具/应用
                    示例值:

                `Catalogue (str)`: 必选, 数据集编目 ID
                    示例值: OMICSDATA

                `Publications (List[Dict])`: 选填, 出版物

                    `Name (str)`: 必选, 名称
                                示例值: name

                    `AccessURL (str)`: 选填, 在线地址
                                示例值: http://222.com

                    `Authors (List[str})`: 选填, 作者
                                示例值: ["author1", "author2"]

                    `Quotation (str)`: 选填, 引文
                                示例值:

                `DataFilesAccessURL (str)`: 选填, 数据文件 csv 下载路径
                    示例值:

                `DataFileSamplesAccessURL (str)`: 选填, 数据文件样本信息 csv 下载路径
                    示例值:

                `DataFileAccessMethodURL (str)`: 选填, 数据文件访问方法文件下载路径
                    示例值:

        Returns:
            Dict:

                `ID (str)`: 数据集ID
                    示例值: tcxxxxxxxxxxxxxxxxxxx

        """
        return self.__request('CreateDataSet', params)

    def delete_data_set(self, params):
        """ 删除数据集

        Args:
            params (Dict):

                `ID (str)`: 必选, 数据集 ID
                    示例值: tcxxxxxxxxxxxxxxxxxxx

        Returns:
            Dict: empty dictionary

        """
        return self.__request('DeleteDataSet', params)

    def get_trs_workflow_info(self, params):
        """ 查询trs工作流信息

        Args:
            params (Dict):

                `TRSServer (str)`: 必选, trs Server地址
                    示例值: https://dockstore.org

                `ID (str)`: 必选, trs ID
                    示例值: #workflow/github.com/aaa/bbb/ccc

        Returns:
            Dict:

                `Name (str)`: trs工作流名称
                    示例值: name

                `Description (str)`: trs工作流描述
                    示例值: description

                `VersionsInfo (List[Dict])`: trs工作流具体版本信息

                    `Name (str)`: 版本名称
                        示例值: master

                    `Language (str)`: 语言类型, 包括 WDL/CWL/Nextflow
                        示例值: WDL

        """
        return self.__request('GetTRSWorkflowInfo', params)

    def __request(self, action, params):
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception('empty response')
        res_json = json.loads(res)
        if 'Result' not in res_json.keys():
            return res_json
        return res_json['Result']
