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
            'CreateCluster':
                ApiInfo('POST', '/', {'Action': 'CreateCluster', 'Version': '2021-03-04'}, {}, {}),
            'ListClusters':
                ApiInfo('POST', '/', {'Action': 'ListClusters', 'Version': '2021-03-04'}, {}, {}),
            'DeleteCluster':
                ApiInfo('POST', '/', {'Action': 'DeleteCluster', 'Version': '2021-03-04'}, {}, {}),
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
        }
        return api_info

    def create_workspace(self, params):
        """ 创建workspace

        https://www.volcengine.com/docs/6971/174344

        Args:
            params (Dict):

                `Name (string)`: 必选, worksapce名称
                    示例值:  test

                `Description (string)`: 必选, Worksapce描述
                    示例值:  test

                `S3Bucket (string)`: 选填, s3的桶地址
                    示例值:  bioos-wcf0cp05eig4883tiu130

                `CopyPublicWorkspaceID (string)`: 选填
                    示例值:  不填即可

                `CoverPath (string)`: 选填, 封面路径（在tos桶中的相对路径）
                    示例值:  template-cover/pic1.png

        Returns:
            Dict:

                `ID (string)`: workspaceID
                    示例值:  wcf0cp05eig4883tiu130

        Examples:
            >>> bioos_service.create_workspace(
            ...    {
            ...        "Name": "test",
            ...        "Description": "test"
            ...    },
            ... )
            {
                    "ID": "wcf0cp05eig4883tiu130"
            }

        """
        return self.__request('CreateWorkspace', params)

    def list_workspaces(self, params):
        """ 查询符合条件的workspace列表

        https://www.volcengine.com/docs/6971/174345

        Args:
            params (Dict):

                `PageNumber (int)`: 选填, 页码
                    示例值:  1

                `PageSize (int)`: 选填, 页长
                    示例值:  10

                `Filter (Dict)`: 选填, 筛选条件

                    `Keyword (string)`: 选填, 根据名称筛选
                        示例值:  test

                    `IDs (List[string])`: 选填, ID列表
                        示例值:  ["test"]

                `SortBy (string)`: 选填, 排序字段（Name CreateTime）
                    示例值:  CreateTime

                `SortOrder (string)`: 选填, 排序顺序（Desc Asc）
                    示例值:  Desc

        Returns:
            Dict:

                List[Dict]: Items, Workspace列表

                    `ID (string)`: WorkspaceID
                        示例值:  wcf0cp05eig4883tiu130

                    `Name (string)`: Workspace 名称
                        示例值:  test

                    `Description (string)`: 描述
                        示例值:  test

                    `CreateTime (int)`: 创建时间戳
                        示例值:  1673525239

                    `UpdateTime (int)`: 更新时间戳
                        示例值:  1673525239

                    `OwnerName (string)`: 创建者名字
                        示例值:  test

                    `CoverDownloadURL (string)`: 封面地址
                        示例值:  template-cover/pic1.png

                    `Role (string)`: 用户角色
                        示例值:  Admin

                    `S3Bucket (string)`: tos桶名称
                        示例值:  bioos-wcf0cp05eig4883tiu130

                `PageNumber (int)`: 页码
                    示例值:  1

                `PageSize (int)`: 页长
                    示例值:  10

                `TotalCount (int)`: 总数量
                    示例值:  10

        """
        return self.__request('ListWorkspaces', params)

    def update_workspace(self, params):
        """ 更新workspace

        https://www.volcengine.com/docs/6971/174346

        Args:
            params (Dict):

                `ID (string)`: 必选, workspaceID
                    示例值:  wcf0cp05eig4883tiu130

                `Name (string)`: 必选, 更新后的workspace名称
                    示例值:  test-1

                `Description (string)`: 必选, 更新后的worksapce描述
                    示例值:  Test description

                `CoverPath (string)`: 选填, 更新后的封面地址
                    示例值:  template-cover/pic1.png

        Returns:
            Dict:

                `Updated (bool)`: 是否完成更新
                    示例值:  true

        """
        return self.__request('UpdateWorkspace', params)

    def delete_workspace(self, params):
        """ 删除workspace

        https://www.volcengine.com/docs/6971/174347

        Args:
            params (Dict):

                `ID (string)`: 必选, workspaceID
                    示例值:  wcf0cp05eig4883tiu130

        Returns:
            Dict: empty dictionary

        """
        return self.__request('DeleteWorkspace', params)

    def bind_cluster_to_workspace(self, params):
        """ 如果workspace内运行工作流，则需要绑定已纳管的集群，已被纳管的集群可通过ListClusters接口查询。

        https://www.volcengine.com/docs/6971/174348

        Args:
            params (Dict):

                `ID (string)`: 必选, workspaceID
                    示例值:  wcf0cp05eig4883tiu130

                `ClusterID (string)`: 必选, 已纳管集群的ID
                    示例值:  ucf0fgideig4de2rjrr9g

                `Type (string)`: 必选, 关联类型（workflow、notebook）
                    示例值:  workspace

        Returns:
            Dict: empty dictionary

        """
        return self.__request('BindClusterToWorkspace', params)

    def unbind_cluster_and_workspace(self, params):
        """ 该接口对已绑定的workspace和cluster进行解绑操作

        https://www.volcengine.com/docs/6971/174349

        Args:
            params (Dict):

                `ID (string)`: 必选, workspaceID
                    示例值:  wcf0cp05eig4883tiu130

                `ClusterID (string)`: 必选, 已纳管集群的ID
                    示例值:  ucf0fgideig4de2rjrr9g

                `Type (string)`: 必选, 关联类型（workflow、notebook）
                    示例值:  workspace

        Returns:
            Dict: empty dictionary

        """
        return self.__request('UnbindClusterAndWorkspace', params)

    def list_clusters_of_workspace(self, params):
        """ 查看workspace所绑定的集群列表

        https://www.volcengine.com/docs/6971/174350

        Args:
            params (Dict):

                ID (string): 必选, workspaceID
                    示例值:  wcf0cp05eig4883tiu130

                Type (string): 必选, 关联类型（workflow、notebook）
                    示例值:  workflow

        Returns:
            Dict:

                `Items (List[Dict])`: cluster列表

                    `ClusterInfo (Dict)`: 集群信息

                        `ID (string)`: 纳管集群ID
                            示例值:  ucf0fgideig4de2rjrr9g

                        `Name (string)`: 纳管集群名称
                            示例值:  test-cluster

                        `Description (string)`: 投递记录描述
                            示例值:  test-description

                        `Status (string)`: 集群纳管状态（Succeeded、Failed、Running）
                            示例值:  ClusterStatus

                        `StartTime (int)`: 起始时间
                            示例值:

                        `StoppedTime (int)`: 截止时间
                            示例值:

                        `Bound (bool)`: 是否存在绑定的 workspace
                            示例值:  false

                        `Public (bool)`: 是否是公共集群
                            示例值:  true

                        `VKEConfig (Dict)`: vke 集群信息

                            `ClusterID (string)`: vke集群的clusterID,通过https://www.volcengine.com/docs/6460/115190查询
                                示例值: cceklvtvqtoft92qm

                            `StorageClass (string)`: vke集群已安装的 StorageClass 的名称
                                示例值:  ebs-ssd

                        `ExternalConfig (ExternalConfig)`: 外部集群配置

                            `WESEndpoint (string)`: Wes地址
                                示例值:  http://unknown:8002/ga4gh/wes/v1

                            `JupyterhubEndpoint (string)`: jupyterhub 地址
                                示例值:  http://jupyterhub-hub:8081/jupyterhub

                            `JupyterhubJWTSecret (string)`: jupyterhub jwt secret, 作为响应时不返回
                                示例值:  xxxxx

                            `ResourceScheduler (string)`: 外部资源调度程序
                                示例值:  SGE

                            `Filesystem (string)`: 工作流计算引擎文件系统（目前支持tos、local）
                                示例值:  tos

                            `ExecutionRootDir (string)`: 响应参数,工作流计算引擎执行根路径, 当且仅当工作流计算引擎依赖的文件系统为 local 时会有
                                示例值:  /data

                        `SharedConfig (SharedConfig)`: 共享集群配置,暂无具体配置信息
                                示例值: {}

                    `Type (string)`: 关联类型（workflow、notebook）
                        示例值:  workflow

                    `BindTime (int)`: 绑定是时间
                        示例值:

                `PageNumber (int)`: 页码
                    示例值:  1

                `PageSize (int)`: 页长
                    示例值:  10

                `TotalCount (int)`: 总数量
                    示例值:  10

        """
        return self.__request('ListClustersOfWorkspace', params)

    def create_cluster(self, params):
        """ 此接口为异步接口，当此接口返回成功时，会返回导入的clusterID信息;
        此时并不表示集群纳管，需要调用接口查看ListClusters集群纳管情况。

        https://www.volcengine.com/docs/6971/174351

        Note:
            VKEConfig、SharedConfig 只能选择一个，若用户需要纳管外部集群，则需联系 Bio-OS 团队

        Args:
            params (Dict):

                `Name (string)`: 必选, 集群名称
                    示例值:  test-cluster

                `Description (string)`: 选填, 集群描述
                    示例值:  test- description

                `VKEConfig (Dict)`: 选填, vke 集群信息

                    `ClusterID (string)`: 必选, vke集群的clusterID,通过https://www.volcengine.com/docs/6460/115190查询
                        示例值: cceklvtvqtoft92qm

                    `StorageClass (string)`: 必选, vke集群已安装的 StorageClass 的名称
                        示例值:  ebs-ssd

                `ExternalConfig (ExternalConfig)`: 选填, 外部集群配置

                    `WESEndpoint (string)`: 必选, Wes地址
                        示例值:  http://unknown:8002/ga4gh/wes/v1

                    `JupyterhubEndpoint (string)`: 必选, jupyterhub 地址
                        示例值:  http://jupyterhub-hub:8081/jupyterhub

                    `JupyterhubJWTSecret (string)`: 必选, jupyterhub jwt secret, 作为响应时不返回
                        示例值:  xxxxx

                    `ResourceScheduler (string)`: 必选, 外部资源调度程序
                        示例值:  SGE

                    `Filesystem (string)`: 必选, 工作流计算引擎文件系统（目前支持tos、local）
                        示例值:  tos

                `SharedConfig (SharedConfig)`: 选填, 共享集群配置,暂无具体配置信息，请求时保证此字段不为空
                        示例值: {}

        Returns:
            Dict:

                `ID (string)`: 集群ID
                    示例值:  ucf0fgideig4de2rjrr9g

        """
        return self.__request('CreateCluster', params)

    def list_clusters(self, params):
        """ 查看所有集群

        https://www.volcengine.com/docs/6971/174352

        Args:
            params (Dict):

                `PageNumber (int)`: 选填, 页码
                    示例值:  1

                `PageSize (int)`: 选填, 页长
                    示例值:  10

                `Filter (Dict)`: 选填, 筛选条件

                    `IDs (List[string])`: 选填, ID列表
                        示例值:  ["test-workflow"]

                    `Status (List[string])`: 选填, 集群状态列表
                        示例值:  ["Running"]

                    `Type (List[string])`: 选填, 集群类型(volc-vke, external, shared)
                        示例值:  ["shared"]

                    `Public (bool)`: 选填, 默认为false，若为true，则集群对所有人可见
                        示例值:  true

                    `Keyword (string)`: 选填, 名称模糊匹配
                        示例值:  "test"

        Returns:
            Dict:

                `Items (List[Dict])`: cluster列表

                    `ID (string)`: 纳管集群ID
                        示例值:  ucf0fgideig4de2rjrr9g

                    `Name (string)`: 纳管集群名称
                        示例值:  test-cluster

                    `Description (string)`: 投递记录描述
                        示例值:  test-description

                    `Status (string)`: 集群纳管状态（Succeeded、Failed、Running）
                        示例值:  ClusterStatus

                    `StartTime (int)`: 起始时间
                        示例值:

                    `StoppedTime (int)`: 截止时间
                        示例值:

                    `Bound (bool)`: 是否存在绑定的 workspace
                        示例值:  false

                    `Public (bool)`: 是否是公共集群
                        示例值:  true

                    `VKEConfig (Dict)`: vke 集群信息

                        `ClusterID (string)`: 必选, vke集群的clusterID,通过https://www.volcengine.com/docs/6460/115190查询
                            示例值: cceklvtvqtoft92qm

                        `StorageClass (string)`: 必选, vke集群已安装的 StorageClass 的名称
                            示例值:  ebs-ssd

                    `ExternalConfig (ExternalConfig)`: 外部集群配置

                        `WESEndpoint (string)`: Wes地址
                            示例值:  http://unknown:8002/ga4gh/wes/v1

                        `JupyterhubEndpoint (string)`: jupyterhub 地址
                            示例值:  http://jupyterhub-hub:8081/jupyterhub

                        `JupyterhubJWTSecret (string)`: jupyterhub jwt secret, 作为响应时不返回
                            示例值:  xxxxx

                        `ResourceScheduler (string)`: 外部资源调度程序
                            示例值:  SGE

                        `Filesystem (string)`: 工作流计算引擎文件系统（目前支持tos、local）
                            示例值:  tos

                        `ExecutionRootDir (string)`: 响应参数,工作流计算引擎执行根路径, 当且仅当工作流计算引擎依赖的文件系统为 local 时会有
                            示例值:  /data

                    `SharedConfig (SharedConfig)`: 共享集群配置,暂无具体配置信息
                            示例值: {}

                `PageNumber (int)`: 页码
                    示例值:  1

                `PageSize (int)`: 页长
                    示例值:  10

                `TotalCount (int)`: 总数量
                    示例值:  10

        """
        return self.__request('ListClusters', params)

    def delete_cluster(self, params):
        """ 删除集群

        https://www.volcengine.com/docs/6971/174353

        Args:
            params (Dict):

                `ID (string)`: 必选, 集群ID
                    示例值:  ucf0fgideig4de2rjrr9g

        Returns:
            Dict: empty dictionary

        """
        return self.__request('DeleteCluster', params)

    def create_data_model(self, params):
        """ 创建实体数据模型

        https://www.volcengine.com/docs/6971/174361

        Args:
            params (Dict):

                `WorkspaceID (string)`: 必选, 导入datamodel的workspaceID
                    示例值:  wcf0cp05eig4883tiu130

                `Name (string)`: 必选, 数据模型文件名
                    示例值:  test-datamodel

                `Headers (List[string])`: 必选, 表头列表
                    示例值:  ["sample_id", "date"]

                `Rows (List[List[string]])`: 必选, 对象列表
                    示例值:  [["sample", "01/01/2022"], ["your-sample-2-id", "02/01/2022"]]

        Returns:
            Dict:

                `ID (string)`: datamodelID
                    示例值:  dccc0ne5eig41ascop420

        """
        return self.__request('CreateDataModel', params)

    def list_data_models(self, params):
        """ 查询实体数据模型列表

        https://www.volcengine.com/docs/6971/174362

        Args:
            params (Dict):

                `WorkspaceID (string)`: 必选, 数据模型所在的workspaceID
                    示例值:  wcf0cp05eig4883tiu130

        Returns:
            Dict:

                `TotalCount (int)`: 数据模型总数
                    示例值:  10

                `Items (List[Dict])`: 列表项

                    `ID (string)`: 数据模型ID
                        示例值:  dccc0ne5eig41ascop420

                    `Name (string)`: 数据模型文件名
                        示例值:  test-datamodel

                    `RowCount (int)`: 数据模型行数
                        示例值:  100

                    `Type (string)`: 数据模型类型（normal、set、workspace）
                        示例值:  normal

        """
        return self.__request('ListDataModels', params)

    def list_data_model_rows(self, params):
        """ 分页查询实体数据模型的详细信息（行和列）

        https://www.volcengine.com/docs/6971/174363

        Args:
            params (Dict):

                `WorkspaceID (string)`: 必选, 数据模型所在的workspaceID
                    示例值:  wcf0cp05eig4883tiu130

                `ID (string)`: 必选, Datamodel ID
                    示例值:  dccc0ne5eig41ascop420

                `PageNumber (int)`: 选填, 页码
                    示例值:  1

                `PageSize (int)`: 选填, 页长
                    示例值:  10

                `Filter (Dict)`: 选填, 筛选条件

                    `Keyword (string)`: 选填, 筛选数据查询
                        示例值:  test

                    `InSetIDs (List[string])`: 选填, 集合表中的实体ID
                        示例值:  ["dcehe12leig4dqi3n7080"]

                `SortBy (string)`: 选填, 排序字段（默认为id）
                    示例值:  CreateTime

                `SortOrder (string)`: 选填, 排序顺序（Desc Asc）
                    示例值:  Desc

        Returns:
            Dict:

                `Headers (List[string]`: 表头列表
                    示例值:  ["sample_id"]

                `Rows (List[List[string]])`: 对象列表
                    示例值:  [["sample"]]

                `PageNumber (int)`: 页码
                    示例值:  1

                `PageSize (int)`: 页长
                    示例值:  10

                `TotalCount (int)`: 总条数
                    示例值:  100

        """
        return self.__request('ListDataModelRows', params)

    def delete_data_model_rows_and_headers(self, params):
        """ 删除实体数据模型的具体行和列

        https://www.volcengine.com/docs/6971/174364

        Args:
            params (Dict):

                `WorkspaceID (string)`: 必选, 数据模型所在的workspaceID
                    示例值:  wcf0cp05eig4883tiu130

                `ID (string)`: 必选, Datamodel ID
                    示例值:  dccc0ne5eig41ascop420

                `RowIDs (List[siring])`: 选填, 需要删除的数据模型行ID
                    示例值:  ["0cafd453-e9fd-4147-bc39-0a16e3d4fedd"]

                `Headers (List[string])`: 选填, 需要删除的数据模型列名
                    示例值:  ["sample_id"]

        Returns:
            Dict: empty dictionary

        """
        return self.__request('DeleteDataModelRowsAndHeaders', params)

    def create_submission(self, params):
        """ 提交工作流投递记录

        https://www.volcengine.com/docs/6971/174365

        Args:
            params (Dict):

                `WorkspaceID (string)`: 必选, 提交submussion的workspaceID
                    示例值:  wcf0cp05eig4883tiu130

                `WorkflowID (string)`: 必选, 提交submission所使用的workflow的ID
                    示例值:  fcbkcdkdeig43pmbqr9dg

                `Name (string)`: 必选, 投递名称
                    示例值:  test-submission

                `Description (string)`: 选填, 投递描述
                    示例值:  test-description

                `DataModelID (string)`: 选填, 数据模型ID
                    示例值:  dccc0ne5eig41ascop420

                `DataModelRowIDs (List[string])`: 选填, 数据模型行ID
                    示例值:  ["0cafd453-e9fd-4147-bc39-0a16e3d4fedd"]

                `Inputs (string)`: 必选, 输入配置，json序列化后的string
                    示例值:  {"test.name1":"this.name1","test.name2":"this.name2","test.request":"this.requestFile"}

                `Outputs (string)`: 必选, 输出配置，json序列化后的string
                    示例值:  {"test.response1":"this.response1","test.response2":"this.response2"}

                `ExposedOptions (Dict)`: 必选, 平台暴露的Workflow Options

                    `ReadFromCache (bool)`: 必选, 是否开启call-cache
                        示例值:  true

                    `ExecutionRootDir (string)`: 必选, 工作流执行根路径，若为vke集群，则为s3:// + workspace所绑定的桶名，若为外部hpc集群，则为共享文件存储路径，如/share/data
                        示例值:  s3://bioos-wcbgb1fleig44vch0ug0g

                `ClusterID (string)`: 必选, 运行集群ID
                    示例值:  ucf0fgideig4de2rjrr9g

        Returns:
            Dict:

                `ID (string)`: Submission ID
                    示例值:  scb6ka15eig43rnbl2bp0

        """
        return self.__request('CreateSubmission', params)

    def list_submissions(self, params):
        """ 查询工作流投递记录列表

        https://www.volcengine.com/docs/6971/174366

        Args:
            params (Dict):

                `WorkspaceID (string)`: 必选, submission所在的workspaceID
                    示例值:  wcf0cp05eig4883tiu130

                `Filter (Dict)`: 选填, 筛选条件

                    `WorkflowID (string)`: 选填, 根据工作流ID筛选
                        示例值:  fcbkcdkdeig43pmbqr9dg

                    `Status (List[string])`: 选填, 根据状态筛选（Succeeded、Failed、Running、Cancelled、Cancelling）
                        示例值:  ["Running","Cancelling"]

                    `ClusterID (string)`: 选填, 根据集群ID筛选
                        示例值:  ucf0fgideig4de2rjrr9g

                    `Keyword (string)`: 选填, 根据名称筛选
                        示例值:  test

                    `IDs (List[string])`: 选填, 根据submission ID筛选
                        示例值:  ["scb6ka15eig43rnbl2bp0"]

                `PageNumber (int)`: 选填, 页码
                    示例值:  1

                `PageSize (int)`: 选填, 页长
                    示例值:  10


        Returns:
            Dict:
                `Items (List[Dict])`: Workflow 列表

                    `ID (string)`: 投递记录ID
                        示例值:  scb6ka15eig43rnbl2bp0

                    `Name (string)`: 投递记录名称
                        示例值:  test-submission

                    `Description (string)`: 投递记录描述
                        示例值:  test-description

                    `Status (string)`: 投递记录状态（Succeeded、Failed、Running）
                        示例值:  Running

                    `RunStatus (Dict)`: 工作流运行状态

                        `Count (int)`: 工作流运行统计
                            示例值:  120

                        `Succeeded (int)`: 运行成功的工作流运行总数
                            示例值:  90

                        `Failed (int)`: 运行失败的工作流运行总数
                            示例值:  5

                        `Running (int)`: 运行中的工作流运行总数
                            示例值:  5

                    `StartTime (int)`: 起始时间
                        示例值:

                    `FinishTime (int)`: 截止时间
                        示例值:

                    `Duration (int)`: 分析耗时（单位为秒）
                        示例值:  1000

                `PageNumber (int)`: 页码
                    示例值:  1

                `PageSize (int)`: 页长
                    示例值:  10

                `TotalCount (int)`: 总数量
                    示例值:  10

        """
        return self.__request('ListSubmissions', params)

    def delete_submission(self, params):
        """ 删除工作流投递记录

        https://www.volcengine.com/docs/6971/174367

        Args:
            params (Dict):

                `WorkspaceID (string)`: 必选, submission所在的workspaceID
                    示例值:  wcf0cp05eig4883tiu130

                `ID (string)`: 必选, Submission ID
                    示例值:  dccc0ne5eig41ascop420

        Returns:
            Dict: empty dictionary

        """
        return self.__request('DeleteSubmission', params)

    def cancel_submission(self, params):
        """ 终止工作流投递记录

        https://www.volcengine.com/docs/6971/215369

        Args:
            params (Dict):

                `WorkspaceID (string)`: 必选, submission所在的workspaceID
                    示例值:  wcf0cp05eig4883tiu130

                `ID (string)`: 必选, Submission ID
                    示例值:  scb6ka15eig43rnbl2bp0

        Returns:
            Dict: empty dictionary

        """
        return self.__request('CancelSubmission', params)

    def list_runs(self, params):
        """ 查询工作流运行列表

        https://www.volcengine.com/docs/6971/174368

        Args:
            params (Dict):

                `WorkspaceID (string)`: 必选, submission所在的workspaceID
                    示例值:  wcf0cp05eig4883tiu130

                `SubmissionID (string)`: 必选, submission的ID
                    示例值:  scb6ka15eig43rnbl2bp0

                `Filter (Dict)`: 选填, 筛选条件

                    `Keyword (string)`: 选填, 运行记录关键字
                        示例值:  test-run

                    `IDs (List[string])`: 选填, 运行记录ID列表
                        示例值:  ["rcb6kdf5eig43rnbl2brg"]

                    `Status (List[string])`: 选填, 根据状态筛选（Pending、Running、Succeeded、Failed、Cancelling、Cancelled）
                        示例值:  ["Pending","Running"]

                `PageNumber (int)`: 选填, 页码
                    示例值:  1

                `PageSize (int)`: 选填, 页长
                    示例值:  10

        Returns:
            Dict:

                `Items (List[Dict])`: Run列表

                    `ID (string)`: 运行记录ID
                        示例值:  rcb6kdf5eig43rnbl2brg

                    `DataEntityRowID (string)`: 数据实体 RowID
                        示例值:  dcehe12leig4dqi3n7080

                    `Status (string)`: 投递记录状态（Succeeded、Failed、Running、Pending、Cancelling、Cancelled）
                        示例值:  Running

                    `StartTime (Int)`: 起始时间
                        示例值:

                    `FinishTime (int)`: 截止时间
                        示例值:

                    `Duration (int)`: 分析耗时(单位为s)
                        示例值:

                    `SubmissionID (string)`: 投递记录ID
                        示例值:  scb6ka15eig43rnbl2bp0

                    `EngineRunID (string)`: 工作流引擎内运行记录 ID
                        示例值:  05693535-dcf4-404f-8d18-2d3cac29916b

                    `Inputs (string)`: 运行记录输入参数，json 序列化后的 string
                        示例值:  {"test.name1":"world","test.name2":"hello","test.request":"s3://vci-dev/jxc-test/aaa.txt"}

                    `Outpus (string)`: 运行记录输出参数，json 序列化后的 string
                        示例值:  {"test.resp":"abc",
                        "test.response1":"s3://bioos-dev-wcb1e3v5eig4635iurevg/analysis/scb8gbtleig4f4jqjbtlg/test/d9ea2df5-b8d8-4603-9f62-496229e922c9/call-step21/execution/resp.txt",
                        "test.response2":"s3://bioos-dev-wcb1e3v5eig4635iurevg/analysis/scb8gbtleig4f4jqjbtlg/test/d9ea2df5-b8d8-4603-9f62-496229e922c9/call-step22/execution/resp.txt"}

                    `TaskStatus (Dict)`: 工作流运行详情状态统计

                        `Count (int)`: 任务运行统计
                            示例值:  120

                        `Succeeded (int)`: 运行成功的工作流运行总数
                            示例值:  90

                        `Failed (int)`: 运行失败的工作流运行总数
                            示例值:  5

                        `Running (int)`: 运行中的工作流运行总数
                            示例值:  5

                        `Queued (int)`: 排队中的工作流运行总数
                            示例值:  5

                        `Initializing (int)`: 启动中的工作流运行总数
                            示例值:  5

                        `Cancelled (int)`: 已终止的工作流运行总数
                            示例值:  10

                    `Log (string)`: 运行记录日志存储路径
                        示例值:  s3://bioos-wcb1e3v5eig4635iurevg/analysis/scbd69kteig472iq3lt5g/workflow.941846fb-158d-4d49-82e0-f2f39372e9e3.log

                    `Message (string)`: 运行记录错误详情
                        示例值:

                `PageNumber (int)`: 页码
                    示例值:  1

                `PageSize (int)`: 页长
                    示例值:  10

                `TotalCount (int)`: 总数量
                    示例值:  10

        """
        return self.__request('ListRuns', params)

    def cancel_run(self, params):
        """ 终止工作流运行记录

        https://www.volcengine.com/docs/6971/215646

        Args:
            params (Dict):

                `WorkspaceID (string)`: 必选, run所在的workspaceID
                    示例值:  wcf0cp05eig4883tiu130
                `ID (string)`: 必选, Run ID
                    示例值:  rcb6kdf5eig43rnbl2brg

        Returns:
            Dict: empty dictionary

        """
        return self.__request('ListRuns', params)

    def list_tasks(self, params):
        """ 查询工作流的task任务列表

        https://www.volcengine.com/docs/6971/174369

        Args:
            params (Dict):

                `WorkspaceID (string)`: 必选, submission所在的workspaceID
                    示例值:  wcf0cp05eig4883tiu130

                `RunID (string)`: 必选, 运行记录ID
                    示例值:  rcb6jdp5eig4f4tigos0g

                `PageNumber (int)`: 选填, 页码
                    示例值:  1

                `PageSize (int)`: 选填, 页长
                    示例值:  10

        Returns:
            Dict:

                `Items (List[Dict])`: Task列表

                    `Name (string)`: 任务名称
                        示例值:  melt.step1.0

                    `RunID (string)`: 运行记录ID
                        示例值:  rcb6kdf5eig43rnbl2brg

                    `Status (string)`: 任务状态（Succeeded、Failed、Running、Queued、Initalizing、Cancelled）
                        示例值:  Running

                    `StartTime (Int)`: 起始时间
                        示例值:

                    `FinishTime (int)`: 截止时间
                        示例值:

                    `Duration (int)`: 分析耗时(单位为s)
                        示例值:

                    `Log (string)`: 运行记录日志存储路径
                        示例值:  s3://bioos-wcb1e3v5eig4635iurevg/analysis/scbd69kteig472iq3lt5g/workflow.941846fb-158d-4d49-82e0-f2f39372e9e3.log

                    `Stdout (string)`: 任务输出存储路径
                        示例值:  s3://bioos-wcb1e3v5eig4635iurevg/analysis/scbqbh2deig40u2tf4ahg/melt/cd28ec5b-75df-4981-a7f5-90f1deba8a94/call-step1/shard-0/execution/stdout

                    `Stderr (string)`: 任务错误存储路径
                        示例值:  s3://bioos-wcb1e3v5eig4635iurevg/analysis/scbqbh2deig40u2tf4ahg/melt/cd28ec5b-75df-4981-a7f5-90f1deba8a94/call-step1/shard-0/execution/stderr

                `PageNumber (int)`: 页码
                    示例值:  1

                `PageSize (int)`: 页长
                    示例值:  10

                `TotalCount (int)`: 总数量
                    示例值:  10

        """
        return self.__request('ListTasks', params)

    def create_workflow(self, params):
        """ 此接口为异步接口，当此接口返回成功时，会返回导入的workflowID信息，此时并不代表workflow导入成功，
        需要调用ListWorkflows接口查看workflow导入情况，其返回的参数WorkflowImportStatus如果为Succeeded则为导入成功。

        https://www.volcengine.com/docs/6971/174357

        Args:
            params (Dict):

                `WorkspaceID (string)`: 必选, 导入workflow的workspaceID
                    示例值:  wcf0cp05eig4883tiu130

                `Name (string)`: 必选, 导入workflow的名字
                    示例值:  test-workflow

                `Description (string)`: 选填, workflow描述信息
                    示例值:  test-workflow- description

                `Language (string)`: 必选, workflow的语言，目前仅支持WDL
                    示例值:  WDL

                `Source (string)`: 必选, wdl存放的git仓库信息
                    示例值:  https://gitee.com/xx/wdl.git

                `Tag (string)`: 必选, wdl的git仓库中的tag
                    示例值:  master

                `Token (string)`: 选填, 若仓库地址为gittee，则需要填写对应token
                    示例值:  fefwdfsdfwefdsdf

                `MainWorkflowPath (string)`: 必选, 主wdl在对应仓库中的地址
                    示例值:  hello.wdl

        Returns:
            Dict:

                `ID (string)`: WorkflowID
                    示例值:  wcf0cp05eig4883tiu130

        """
        return self.__request('CreateWorkflow', params)

    def list_workflows(self, params):
        """ 查询符合条件的workflows列表

        https://www.volcengine.com/docs/6971/174358

        Args:
            params (Dict):

                `WorkspaceID (string)`: 必选, workflow所在的workspaceID
                    示例值:  wcf0cp05eig4883tiu130

                `PageNumber (int)`: 选填, 页码
                    示例值:  1

                `PageSize (int)`: 选填, 页长
                    示例值:  10

                `Filter (Dict)`: 选填, 筛选条件

                    `Keyword (string)`: 选填, 根据名称筛选
                        示例值:  test

                    `IDs (List[string])`: 选填, ID列表
                        示例值:  ["test-workflow"]

                `SortBy (string)`: 选填, 排序字段（Name CreateTime）
                    示例值:  CreateTime

                `SortOrder (string)`: 选填, 排序顺序（Desc Asc）
                    示例值:  Desc

        Returns:
            Dict:

                `Items (List[Dict])`: Workflow 列表

                    `ID (string)`: WorkflowID
                        示例值:  wcf0cp05eig4883tiu130

                    `Name (string)`: Workflow 名称
                        示例值:  test

                    `Description (string)`: 描述
                        示例值:  test

                    `CreateTime (int)`: 创建时间戳
                        示例值:  1673525239

                    `UpdateTime (int)`: 更新时间戳
                        示例值:  1673525239

                    `Language (string)`: workflow语言
                        示例值:  WDL

                    `Source (string)`: wdl仓库地址
                        示例值:  https://gitee.com/xx/wdl.git

                    `Tag (string)`: tag地址
                        示例值:  master

                    `Token (string)`: 用户的git token
                        示例值:  sfsdfwefew

                    `MainWorkflowPath (string)`: 主wdl在仓库中的位置
                        示例值:  hello.wdl

                    `Status (Dict)`: workflow导入状态

                        `Phase (string)`: workflow导入状态（Importing、Succeeded、Failed）
                            示例值:  Succeeded

                        `Message (string)`: 导入失败原因，Phase为Failed时有效
                            示例值:

                    `Inputs (Dict)`: wdl的intput信息

                        `Name (string)`: 参数名称
                            示例值:  test

                        `Type (string)`: 参数类型
                            示例值:  String

                        `Optional (bool)`: 是否是可选参数
                            示例值:  true

                        `Default (string)`: 默认值
                            示例值:  test

                    `Outputs (Dict)`: wdl的output信息

                        `Name (string)`: 参数名称
                            示例值:  test

                        `Type (string)`: 参数类型
                            示例值:  String

                        `Optional (bool)`: 是否是可选参数
                            示例值:  true

                        `Default (string)`: 默认值
                            示例值:  test

                    `OwnerName (string)`: 创建者名字
                        示例值:  test

                `PageNumber (int)`: 页码
                    示例值:  1

                `PageSize (int)`: 页长
                    示例值:  10

                `TotalCount (int)`: 总数量
                    示例值:  10

        """
        return self.__request('ListWorkflows', params)

    def update_workflow(self, params):
        """ 该接口的使用方式与CreateWorkflow类型一样，都需要ListWorkflows接口查看状态

        https://www.volcengine.com/docs/6971/174359

        Args:
            params (Dict):

                `WorkspaceID (string)`: 必选, 导入workflow的workspaceID
                    示例值:  wcf0cp05eig4883tiu130

                `ID (string)`: 必选, workflowID
                    示例值:  fcbkcdkdeig43pmbqr9dg

                `Name (string)`: 必选, 更新后workflow的名字
                    示例值:  test-workflow

                `Description (string)`: 选填, 更新后workflow描述信息
                    示例值:  test-workflow- description

                `Source (string)`: 必选, 更新后wdl存放的git仓库信息
                    示例值:  https://gitee.com/xx/wdl.git

                `Tag (string)`: 必选, 更新后wdl的git仓库中的tag
                    示例值:  master

                `Token (string)`: 选填, 若仓库地址为gittee，则需要填写对应token
                    示例值:  fefwdfsdfwefdsdf

                `MainWorkflowPath (string)`: 必选, 更新后主wdl在对应仓库中的地址
                    示例值:  hello.wdl

        Returns:
            Dict: empty dictionary

        """
        return self.__request('UpdateWorkflow', params)

    def delete_workflow(self, params):
        """ 删除工作流

        https://www.volcengine.com/docs/6971/174360

        Args:
            params (Dict):

                `WorkspaceID (string)`: 必选, workflow所在workspaceID
                    示例值:  wcf0cp05eig4883tiu130

                `ID (string)`: 必选, workflowID
                    示例值:  fcbkcdkdeig43pmbqr9dg

        Returns:
            Dict: empty dictionary

        """
        return self.__request('DeleteWorkflow', params)

    def __request(self, action, params):
        res = self.json(action, dict(), json.dumps(params))
        if res == '':
            raise Exception('empty response')
        res_json = json.loads(res)
        if 'Result' not in res_json.keys():
            return res_json
        return res_json['Result']
