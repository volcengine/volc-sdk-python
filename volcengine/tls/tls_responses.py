# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import struct

from volcengine.tls import log_content_patch
from volcengine.tls.util import TLSUtil

try:
    import lz4.block as lz4
except ImportError:
    try:
        import lz4
    except ImportError:
        lz4 = None

try:
    import zlib
except ImportError:
    zlib = None

from requests import Response

from volcengine.tls.log_pb2 import LogGroupList
from volcengine.tls.data import *


class TLSResponse:
    def __init__(self, response: Response):
        self.headers = response.headers
        self.request_id = response.headers[X_TLS_REQUEST_ID]

        if "json" in self.headers[CONTENT_TYPE]:
            if response.text != "":
                self.response = json.loads(response.text)
            else:
                self.response = {}
        else:
            self.response = {DATA: response.content}

    def get_headers(self):
        """
        :return: 请求headers
        :rtype: dict
        """
        return self.headers

    def get_request_id(self):
        """
        :return: tls请求id
        :rtype: str
        """
        return self.request_id

    @staticmethod
    def _get_host_group_hosts_rules_info(host_group_hosts_rules_info) -> HostGroupHostsRulesInfo:
        host_group_hosts_rules_info[HOST_GROUP_INFO] = \
            HostGroupInfo.set_attributes(data=host_group_hosts_rules_info[HOST_GROUP_INFO])
        host_group_info = host_group_hosts_rules_info[HOST_GROUP_INFO]

        host_infos = []
        for i in range(len(host_group_hosts_rules_info[HOST_INFOS])):
            host_infos.append((HostInfo.set_attributes(data=host_group_hosts_rules_info[HOST_INFOS][i])))

        rule_infos = []
        for i in range(len(host_group_hosts_rules_info[RULE_INFOS])):
            rule_infos.append(RuleInfo.set_attributes(data=host_group_hosts_rules_info[RULE_INFOS][i]))

        return HostGroupHostsRulesInfo(host_group_info, host_infos, rule_infos)


class CreateProjectResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateProjectResponse, self).__init__(response)

        self.project_id = self.response[PROJECT_ID]

    def get_project_id(self):
        """
        :return:日志项目id
        :rtype: str
        """
        return self.project_id


class DeleteProjectResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DeleteProjectResponse, self).__init__(response)


class ModifyProjectResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ModifyProjectResponse, self).__init__(response)


class DescribeProjectResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeProjectResponse, self).__init__(response)

        self.project = ProjectInfo.set_attributes(data=self.response)

    def get_project(self):
        """
        :return: 日志项目
        :rtype: ProjectInfo
        """
        return self.project


class DescribeProjectsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeProjectsResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        self.projects = []
        projects = self.response[PROJECTS]

        for i in range(len(projects)):
            self.projects.append(ProjectInfo.set_attributes(data=projects[i]))

    def get_total(self):
        """
        :return: project总数
        :rtype: int
        """
        return self.total

    def get_projects(self):
        """
        :return: 日志项目列表
        :rtype: List[ProjectInfo]
        """
        return self.projects


class CreateTopicResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateTopicResponse, self).__init__(response)

        self.topic_id = self.response[TOPIC_ID]

    def get_topic_id(self):
        """
        :return: 日志主题 ID
        :rtype: str
        """
        return self.topic_id


class DeleteTopicResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DeleteTopicResponse, self).__init__(response)


class ModifyTopicResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ModifyTopicResponse, self).__init__(response)


class DescribeTopicResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeTopicResponse, self).__init__(response)

        self.topic = TopicInfo.set_attributes(data=self.response)

    def get_topic(self):
        """
        :return: 日志主题
        :rtype: TopicInfo
        """
        return self.topic


class DescribeTopicsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeTopicsResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        topics = self.response[TOPICS]
        self.topics = []
        self.cursor = self.response.get(CURSOR)
        self.regions = self.response.get(REGIONS)

        for i in range(len(topics)):
            self.topics.append(TopicInfo.set_attributes(data=topics[i]))

    def get_total(self):
        """
        :return: topic总数
        :rtype: int
        """
        return self.total

    def get_topics(self):
        """
        :return: topic列表
        :rtype: List[TopicInfo]
        """
        return self.topics

    def get_cursor(self):
        return self.cursor

    def get_regions(self):
        return self.regions


class CreateIndexResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateIndexResponse, self).__init__(response)

        self.topic_id = self.response[TOPIC_ID]


class DeleteIndexResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DeleteIndexResponse, self).__init__(response)


class ModifyIndexResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ModifyIndexResponse, self).__init__(response)


class DescribeIndexResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeIndexResponse, self).__init__(response)

        # L5-D1：暴露 topic_id 字段，与 Go/Java/C++ V2 SDK 对齐。
        # wire 缺失时返回 None，避免 KeyError；调用方按需判空。
        self.topic_id = self.response.get(TOPIC_ID)

        full_text_wire = self.response.get(FULL_TEXT)
        self._has_full_text = full_text_wire is not None
        if full_text_wire is None:
            self.full_text = FullTextInfo()
        else:
            self.full_text = FullTextInfo.set_attributes(data=full_text_wire)
            self.full_text.delimiter = TLSUtil.replace_white_space_character(self.full_text.delimiter)

        self.key_value = []
        key_value = self.response[KEY_VALUE]
        for i in range(len(key_value)):
            self.key_value.append(KeyValueInfo(key=key_value[i][KEY],
                                               value=ValueInfo.set_attributes(data=key_value[i][VALUE])))
            self.key_value[i].value.delimiter = TLSUtil.replace_white_space_character(self.key_value[i].value.delimiter)

        self.user_inner_key_value = []
        user_inner_key_value = self.response[USER_INNER_KEY_VALUE]
        for i in range(len(user_inner_key_value)):
            self.user_inner_key_value.append(KeyValueInfo(key=user_inner_key_value[i][KEY],
                                                          value=ValueInfo.set_attributes(data=user_inner_key_value[i][VALUE])))
            self.user_inner_key_value[i].value.delimiter = TLSUtil.replace_white_space_character(self.user_inner_key_value[i].value.delimiter)

        self.create_time = self.response[CREATE_TIME]
        self.modify_time = self.response[MODIFY_TIME]
        self.enable_auto_index = self.response.get(ENABLE_AUTO_INDEX, False)
        self.enable_phrase_index = self.response.get(ENABLE_PHRASE_INDEX, False)
        self.max_text_len = self.response.get(MAX_TEXT_LEN, 2048)

    def get_create_time(self):
        """
        :return: 创建时间
        :rtype: str
        """
        return self.create_time

    def get_full_text(self):
        """
        :return: 全文索引配置
        :rtype: FullTextInfo
        """
        return self.full_text

    def has_full_text(self):
        return self._has_full_text

    def get_modify_time(self):
        """
         :return: 修改时间
         :rtype: str
         """
        return self.modify_time

    def get_key_value(self):
        """
        :return: 键值索引配置
        :rtype: List[KeyValueInfo]
        """
        return self.key_value

    def get_user_inner_key_value(self):
        """
        :return: 预留字段索引配置
        :rtype: List[KeyValueInfo]
        """
        return self.user_inner_key_value

    def get_enable_auto_index(self):
        """
        :return: 是否开启索引自动更新
        :rtype: bool
        """
        return self.enable_auto_index

    def get_enable_phrase_index(self):
        """
        :return: 是否开启索引版短语查询
        :rtype: bool
        """
        return self.enable_phrase_index

    def get_max_text_len(self):
        """
        :return: 统计字段值的最大长度
        :rtype: int
        """
        return self.max_text_len


class CreateProcessorResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateProcessorResponse, self).__init__(response)
        self.processor_id = self.response[PROCESSOR_ID_HUMP]

    def get_processor_id(self):
        return self.processor_id


class DeleteProcessorResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DeleteProcessorResponse, self).__init__(response)


class ModifyProcessorResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ModifyProcessorResponse, self).__init__(response)


class DescribeProcessorResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeProcessorResponse, self).__init__(response)
        self.processor = ProcessorInfo.set_attributes(self.response)

    def get_processor(self):
        return self.processor


class DescribeProcessorsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeProcessorsResponse, self).__init__(response)
        self.total = self.response[TOTAL]
        self.items = [
            ProcessorInfo.set_attributes(item)
            for item in self.response.get(ITEMS, [])
        ]

    def get_total(self):
        return self.total

    def get_items(self):
        return self.items


class ExecProcessorResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ExecProcessorResponse, self).__init__(response)
        self.exec_status = self.response.get(EXEC_STATUS)
        self.processed_log = self.response.get(PROCESSED_LOG)
        self.error = self.response.get(ERROR)

    def get_exec_status(self):
        return self.exec_status

    def get_processed_log(self):
        return self.processed_log

    def get_error(self):
        return self.error


class OperateProcessorResponse(TLSResponse):
    def __init__(self, response: Response):
        super(OperateProcessorResponse, self).__init__(response)


class DescribeTopicsByProcessorResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeTopicsByProcessorResponse, self).__init__(response)
        self.total = self.response[TOTAL]
        self.items = [
            ProcessorTopicInfo.set_attributes(item)
            for item in self.response.get(ITEMS, [])
        ]

    def get_total(self):
        return self.total

    def get_items(self):
        return self.items


class BindTopicProcessorResponse(TLSResponse):
    def __init__(self, response: Response):
        super(BindTopicProcessorResponse, self).__init__(response)


class BatchBindTopicsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(BatchBindTopicsResponse, self).__init__(response)


class UnbindTopicProcessorResponse(TLSResponse):
    def __init__(self, response: Response):
        super(UnbindTopicProcessorResponse, self).__init__(response)


class DescribeProcessorBindingsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeProcessorBindingsResponse, self).__init__(response)
        self.total = self.response[TOTAL]
        self.items = [
            ProcessorBinding.set_attributes(item)
            for item in self.response.get(ITEMS, [])
        ]

    def get_total(self):
        return self.total

    def get_items(self):
        return self.items


class DescribeProcessorFunctionsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeProcessorFunctionsResponse, self).__init__(response)
        self.functions = {}
        for group, functions in self.response.get(FUNCTIONS, {}).items():
            self.functions[group] = [
                ProcessorFunctionInfo.set_attributes(function)
                for function in functions
            ]

    def get_functions(self):
        return self.functions


class PutLogsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(PutLogsResponse, self).__init__(response)


class DescribeCursorResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeCursorResponse, self).__init__(response)

        self.cursor = self.response[CURSOR]

    def get_cursor(self):
        """
        :return: 游标
        :rtype: str
        """
        return self.cursor


class DescribeCursorTimeResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeCursorTimeResponse, self).__init__(response)

        self.cursor_time = self.response[CURSOR_TIME]


class ConsumeLogsResponse(TLSResponse):
    def __init__(self, response: Response, compression: str, original: bool = False):
        super(ConsumeLogsResponse, self).__init__(response)

        self.x_tls_cursor = self.headers[X_TLS_CURSOR]
        self.x_tls_count = int(self.headers[X_TLS_COUNT])
        self.cursor = self.x_tls_cursor
        self.count = self.x_tls_count
        self.pb_message = None
        self.logs = None

        if DATA in self.response:
            pb_message = self.response[DATA]

            self.pb_message = LogGroupList()
            if original and str(self.headers.get(X_TLS_ORIGINAL, "")).lower() == "true":
                log_content_patch.ParseRawLogGroupListListFromString(
                    self.pb_message, pb_message, self._decompress_log_group_list)
            else:
                pb_message = self._decompress_log_group_list(
                    compression, int(self.headers.get(X_TLS_BODYRAWSIZE, 0) or 0), pb_message)
                try:
                    self.pb_message.ParseFromString(pb_message)
                except Exception as e:
                    log_content_patch.ParseLogGroupListFromString(self.pb_message, pb_message)
            self.logs = self.pb_message

    @staticmethod
    def _decompress_log_group_list(compression: str, raw_size: int, pb_message: bytes) -> bytes:
        if compression == LZ4:
            return lz4.decompress(struct.pack('<I', raw_size) + pb_message)
        if compression == ZLIB:
            return zlib.decompress(pb_message)
        return pb_message

    def get_x_tls_count(self):
        """

        :return: 本次读取的 logGroup 数量
        :rtype: int
        """
        return self.x_tls_count

    def get_pb_message(self):
        """

        :return:日志数据
        :rtype:LogGroupList
        """
        return self.pb_message

    def get_x_tls_cursor(self):
        """
        :return: 当前读取数据下一条 Cursor
        :rtype: str
        """
        return self.x_tls_cursor

    def get_count(self):
        return self.count

    def get_cursor(self):
        return self.cursor

    def get_logs(self):
        return self.logs


class SearchLogsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(SearchLogsResponse, self).__init__(response)

        self.search_result = SearchResult.set_attributes(data=self.response)

    def get_search_result(self):
        """
        :return: 搜索结果
        :rtype: SearchResult
        """
        return self.search_result


class DescribeLogContextResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeLogContextResponse, self).__init__(response)

        self.log_context_infos = self.response[LOG_CONTEXT_INFOS]
        self.prev_over = self.response[PREV_OVER]
        self.next_over = self.response[NEXT_OVER]

    def get_prev_over(self):
        """
        :return:除 LogContextInfos 中的日志以外，是否还存在其他上文
        :rtype:bool
        """
        return self.prev_over

    def get_log_context_infos(self):
        """
        :return:日志的上下文日志信息
        :rtype:List[dict]
        """
        return self.log_context_infos

    def get_next_over(self):
        """
        :return:除 LogContextInfos 中的日志以外，是否还存在其他下文
        :rtype:bool
        """
        return self.next_over


class WebTracksResponse(TLSResponse):
    def __init__(self, response: Response):
        super(WebTracksResponse, self).__init__(response)


class DescribeHistogramResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeHistogramResponse, self).__init__(response)

        self.result_status = self.response[RESULT_STATUS]
        self.interval = self.response[INTERVAL]
        self.total_count = self.response[TOTAL_COUNT]
        self.histogram = []
        histogram = self.response[HISTOGRAM]

        for i in range(len(histogram)):
            self.histogram.append(HistogramInfo.set_attributes(data=histogram[i]))

    def get_histogram(self):
        """
        :return:所有子区间的结果集
        :rtype:List[HistogramInfo]
        """
        return self.histogram

    def get_result_status(self):
        """
        :return:查询的状态
        :rtype:str
        """
        return self.result_status

    def get_total_count(self):
        """
        :return:请求所有直方图数据总和
        :rtype:int
        """
        return self.total_count

    def get_interval(self):
        """
        :return:直方图的子区间长度
        :rtype:int
        """
        return self.interval

class DescribeHistogramV1Response(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeHistogramV1Response, self).__init__(response)

        self.histogram = []
        self.result_status = self.response[RESULT_STATUS]
        self.total_count = self.response[TOTAL_COUNT]

        histogram = self.response[HISTOGRAM]

        for i in range(len(histogram)):
            self.histogram.append(HistogramInfoV1.set_attributes(data=histogram[i]))

    def get_histogram(self):
        """
        :return:所有子区间的结果集
        :rtype:List[HistogramInfo]
        """
        return self.histogram

    def get_result_status(self):
        """
        :return:查询的状态
        :rtype:str
        """
        return self.result_status

    def get_total_count(self):
        """
        :return:请求所有直方图数据总和
        :rtype:int
        """
        return self.total_count

class CreateDownloadTaskResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateDownloadTaskResponse, self).__init__(response)

        self.task_id = self.response[TASK_ID]

    def get_task_id(self):
        """
        :return: 下载任务id
        :rtype: str
        """
        return self.task_id


class DescribeDownloadTasksResponse(TLSResponse):
    def __init__(self, response):
        super(DescribeDownloadTasksResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        self.tasks = []
        tasks = self.response[TASKS]

        for i in range(len(tasks)):
            self.tasks.append(TaskInfo.set_attributes(data=tasks[i]))

    def get_total(self):
        """
        :return: 下载任务总数
        :rtype:int
        """
        return self.total

    def get_tasks(self):
        """
        :return:下载任务列表
        :rtype: List[TaskInfo]
        """
        return self.tasks


class DescribeDownloadUrlResponse(TLSResponse):
    def __init__(self, response):
        super(DescribeDownloadUrlResponse, self).__init__(response)

        self.download_url = self.response[DOWNLOAD_URL]

    def get_download_url(self):
        """
        :return:下载文件链接
        :rtype: str
        """
        return self.download_url


class CreateLogBackFlowTaskResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateLogBackFlowTaskResponse, self).__init__(response)

        self.task_id = self.response[TASK_ID]


class DeleteLogBackFlowTaskResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DeleteLogBackFlowTaskResponse, self).__init__(response)


class DescribeLogBackFlowTasksResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeLogBackFlowTasksResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        self.log_back_flow_tasks = []
        for task in self.response[LOG_BACK_FLOW_TASKS]:
            self.log_back_flow_tasks.append(LogBackFlowTaskInfo.set_attributes(data=task))


class ModifyLogBackFlowTaskResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ModifyLogBackFlowTaskResponse, self).__init__(response)


class DescribeShardsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeShardsResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        self.shards = []
        shards = self.response[SHARDS]

        for i in range(len(shards)):
            self.shards.append(QueryResp.set_attributes(data=shards[i]))

    def get_shards(self):
        """
        :return:shard列表
        :rtype: List[QueryResp]
        """
        return self.shards

    def get_total(self):
        """
        :return:shard总数
        :rtype: int
        """
        return self.total


class ManualShardSplitResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ManualShardSplitResponse, self).__init__(response)

        self.shards = []
        shards = self.response[SHARDS]

        for shard in shards:
            self.shards.append(QueryResp.set_attributes(data=shard))

    def get_shards(self):
        """
        :return: 日志分区的范围等详细信息
        :rtype: List[QueryResp]
        """
        return self.shards


class CreateHostGroupResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateHostGroupResponse, self).__init__(response)

        self.host_group_id = self.response[HOST_GROUP_ID]

    def get_host_group_id(self):
        """
        :return:机器组id
        :rtype: str
        """
        return self.host_group_id


class DeleteHostGroupResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DeleteHostGroupResponse, self).__init__(response)


class ModifyHostGroupResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ModifyHostGroupResponse, self).__init__(response)


class DescribeHostGroupResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeHostGroupResponse, self).__init__(response)

        self.host_group_hosts_rules_info = \
            DescribeHostGroupResponse._get_host_group_hosts_rules_info(self.response[HOST_GROUP_HOSTS_RULES_INFO])
        self.response[HOST_GROUP_HOSTS_RULES_INFO] = self.host_group_hosts_rules_info

    def get_host_group_hosts_rules_info(self):
        """
        :return:机器组详细信息
        :rtype:HostGroupHostsRulesInfo
        """
        return self.host_group_hosts_rules_info


class DescribeHostGroupResponseV2(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeHostGroupResponseV2, self).__init__(response)

        self.host_group_hosts_rules_info = \
            HostGroupHostsRulesInfoV2.set_attributes(data=self.response[HOST_GROUP_HOSTS_RULES_INFO])
        self.response[HOST_GROUP_HOSTS_RULES_INFO] = self.host_group_hosts_rules_info


class DescribeHostGroupsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeHostGroupsResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        self.host_group_hosts_rules_infos = []
        host_group_hosts_rules_infos = self.response[HOST_GROUP_HOSTS_RULES_INFOS]

        for i in range(len(host_group_hosts_rules_infos)):
            self.host_group_hosts_rules_infos.append(
                DescribeHostGroupsResponse._get_host_group_hosts_rules_info(host_group_hosts_rules_infos[i]))

    def get_total(self):
        """
        :return:机器组总数
        :rtype: int
        """
        return self.total

    def get_host_group_hosts_rules_infos(self):
        """
        :return:机器组列表
        :rtype: List[HostGroupHostsRulesInfo]
        """
        return self.host_group_hosts_rules_infos


class DescribeHostGroupsResponseV2(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeHostGroupsResponseV2, self).__init__(response)

        self.total = self.response[TOTAL]
        self.host_group_hosts_rules_infos = []
        host_group_hosts_rules_infos = self.response[HOST_GROUP_HOSTS_RULES_INFOS]

        for i in range(len(host_group_hosts_rules_infos)):
            self.host_group_hosts_rules_infos.append(
                HostGroupHostsRulesInfoV2.set_attributes(data=host_group_hosts_rules_infos[i]))


class ModifyHostGroupsAutoUpdateResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ModifyHostGroupsAutoUpdateResponse, self).__init__(response)


class DescribeHostsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeHostsResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        self.host_infos = []

        for i in range(len(self.response[HOST_INFOS])):
            self.host_infos.append(HostInfo.set_attributes(data=self.response[HOST_INFOS][i]))

    def get_total(self):
        """
        :return:host总数
        :rtype: int
        """
        return self.total

    def get_host_infos(self):
        """
        :return:host列表
        :rtype: List[HostInfo]
        """
        return self.host_infos


class DeleteHostResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DeleteHostResponse, self).__init__(response)


class DescribeHostGroupRulesResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeHostGroupRulesResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        self.rule_infos = []
        for i in range(len(self.response[RULE_INFOS])):
            rule_info = RuleInfo.set_attributes(data=self.response[RULE_INFOS][i])
            self.rule_infos.append(rule_info)

    def get_total(self):
        """
        :return:机器组采集配置总数
        :rtype: int
        """
        return self.total

    def get_rule_infos(self):
        """
        :return:采集配置列表
        :rtype: List[RuleInfo]
        """
        return self.rule_infos


class DeleteAbnormalHostsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DeleteAbnormalHostsResponse, self).__init__(response)


class CreateRuleResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateRuleResponse, self).__init__(response)

        self.rule_id = self.response[RULE_ID]

    def get_rule_id(self):
        """
        :return:采集配置的 ID
        :rtype:str
        """
        return self.rule_id


class DeleteRuleResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DeleteRuleResponse, self).__init__(response)


class ModifyRuleResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ModifyRuleResponse, self).__init__(response)


class DescribeRuleResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeRuleResponse, self).__init__(response)

        self.project_id = self.response[PROJECT_ID]
        self.project_name = self.response[PROJECT_NAME]
        self.topic_id = self.response[TOPIC_ID]
        self.topic_name = self.response[TOPIC_NAME]
        self.rule_info = RuleInfo.set_attributes(data=self.response[RULE_INFO])
        self.response[RULE_INFO] = self.rule_info
        self.host_group_infos = []

        for i in range(len(self.response[HOST_GROUP_INFOS])):
            self.host_group_infos.append(
                HostGroupInfo.set_attributes(data=self.response[HOST_GROUP_INFOS][i]))

    def get_project_id(self):
        """
        :return: 日志项目 ID
        :rtype: str
        """
        return self.project_id

    def get_rule_info(self):
        """
        :return: 采集配置
        :rtype: RuleInfo
        """
        return self.rule_info

    def get_project_name(self):
        """
        :return:日志项目的名称
        :rtype: str
        """
        return self.project_name

    def get_host_group_infos(self):
        """
        :return: 机器组列表
        :rtype: List[HostGroupInfo]
        """
        return self.host_group_infos


class DescribeRuleResponseV2(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeRuleResponseV2, self).__init__(response)

        self.project_id = self.response[PROJECT_ID]
        self.project_name = self.response[PROJECT_NAME]
        self.topic_id = self.response[TOPIC_ID]
        self.topic_name = self.response[TOPIC_NAME]
        self.rule_info = RuleInfo.set_attributes(data=self.response[RULE_INFO])
        self.response[RULE_INFO] = self.rule_info
        self.cs_account_channel = self.response.get(CS_ACCOUNT_CHANNEL)
        self.allow_edit = self.response.get(ALLOW_EDIT)
        self.allow_delete = self.response.get(ALLOW_DELETE)


class DescribeBoundHostGroupsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeBoundHostGroupsResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        self.host_group_infos = []
        for host_group_info in self.response[HOST_GROUP_INFOS]:
            self.host_group_infos.append(HostGroupInfo.set_attributes(data=host_group_info))


class DescribeRulesResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeRulesResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        self.rule_infos = []

        for i in range(len(self.response[RULE_INFOS])):
            self.rule_infos.append(RuleInfo.set_attributes(data=self.response[RULE_INFOS][i]))

    def get_total(self):
        """
        :return:采集配置总数
        :rtype: int
        """
        return self.total

    def get_rule_infos(self):
        """
        :return:采集配置列表
        :rtype: List[RuleInfo]
        """
        return self.rule_infos


class ApplyRuleToHostGroupsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ApplyRuleToHostGroupsResponse, self).__init__(response)


class DeleteRuleFromHostGroupsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DeleteRuleFromHostGroupsResponse, self).__init__(response)


class CreateAlarmNotifyGroupResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateAlarmNotifyGroupResponse, self).__init__(response)

        self.alarm_notify_group_id = self.response[ALARM_NOTIFY_GROUP_ID]

    def get_alarm_notify_group_id(self):
        """
        :return:告警通知组id
        :rtype: str
        """
        return self.alarm_notify_group_id


class DeleteAlarmNotifyGroupResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DeleteAlarmNotifyGroupResponse, self).__init__(response)


class ModifyAlarmNotifyGroupResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ModifyAlarmNotifyGroupResponse, self).__init__(response)


class DescribeAlarmNotifyGroupsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeAlarmNotifyGroupsResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        self.alarm_notify_groups = []

        if self.response[ALARM_NOTIFY_GROUPS] is None:
            self.response[ALARM_NOTIFY_GROUPS] = []

        for i in range(len(self.response[ALARM_NOTIFY_GROUPS])):
            self.alarm_notify_groups.append(AlarmNotifyGroupInfo.set_attributes(
                data=self.response[ALARM_NOTIFY_GROUPS][i]))

    def get_total(self):
        """
        :return:告警通知组总数
        :rtype: int
        """
        return self.total

    def get_alarm_notify_groups(self):
        """
        :return:告警通知组列表
        :rtype: List[AlarmNotifyGroupInfo]
        """
        return self.alarm_notify_groups


class CreateAlarmResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateAlarmResponse, self).__init__(response)

        self.alarm_id = self.response[ALARM_ID]

    def get_alarm_id(self):
        """
        :return:告警id
        :rtype: str
        """
        return self.alarm_id


class DeleteAlarmResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DeleteAlarmResponse, self).__init__(response)


class ModifyAlarmResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ModifyAlarmResponse, self).__init__(response)


class DescribeAlarmsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeAlarmsResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        self.alarms = []

        for i in range(len(self.response[ALARMS])):
            self.alarms.append(AlarmInfo.set_attributes(data=self.response[ALARMS][i]))

    def get_total(self):
        """
        :return:告警总数
        :rtype: int
        """
        return self.total

    def get_alarms(self):
        """
        :return:告警列表
        :rtype: List[AlarmInfo]
        """
        return self.alarms


class OpenKafkaConsumerResponse(TLSResponse):
    def __init__(self, response: Response):
        super(OpenKafkaConsumerResponse, self).__init__(response)


class CloseKafkaConsumerResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CloseKafkaConsumerResponse, self).__init__(response)


class DescribeKafkaConsumerResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeKafkaConsumerResponse, self).__init__(response)

        self.allow_consume = self.response[ALLOW_CONSUME]
        self.consume_topic = self.response[CONSUME_TOPIC]

    def get_allow_consume(self):
        """
        :return: 日志主题是否已开启了 Kafka 协议消费功能
        :rtype:bool
        """
        return self.allow_consume

    def get_consume_topic(self):
        """
        :return:Kafka 协议消费主题 ID，格式为 out+日志主题 ID
        :rtype: str
        """
        return self.consume_topic


class CreateConsumerGroupResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateConsumerGroupResponse, self).__init__(response)


class DeleteConsumerGroupResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DeleteConsumerGroupResponse, self).__init__(response)


class ModifyConsumerGroupResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ModifyConsumerGroupResponse, self).__init__(response)


class DescribeConsumerGroupsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeConsumerGroupsResponse, self).__init__(response)

        self.consumer_groups = []
        self.total = self.response.get(TOTAL)
        self.dashboard_id = self.response.get(DASHBOARD_ID)
        consumer_groups = self.response[CONSUMER_GROUPS]

        if consumer_groups is None:
            return

        for i in range(len(consumer_groups)):
            self.consumer_groups.append(ConsumerGroup.set_attributes(data=consumer_groups[i]))

    def get_total(self):
        return self.total

    def get_dashboard_id(self):
        return self.dashboard_id


class ConsumerHeartbeatResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ConsumerHeartbeatResponse, self).__init__(response)

        self.shards = []
        shards = self.response.get(SHARDS)

        if shards is not None:
            for i in range(len(shards)):
                self.shards.append(ConsumeShard.set_attributes(data=shards[i]))


class ModifyCheckpointResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ModifyCheckpointResponse, self).__init__(response)


class ResetCheckpointResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ResetCheckpointResponse, self).__init__(response)


class DescribeCheckpointResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeCheckpointResponse, self).__init__(response)

        self.shard_id = self.response.get(SHARD_ID_UPPERCASE)
        self.checkpoint = self.response.get(CHECKPOINT)
        self.update_time = self.response.get(UPDATE_TIME)
        self.consumer = self.response.get(CONSUMER)


class AddTagsToResourceResponse(TLSResponse):
    def __init__(self, response: Response):
        super(AddTagsToResourceResponse, self).__init__(response)


class RemoveTagsFromResourceResponse(TLSResponse):
    def __init__(self, response: Response):
        super(RemoveTagsFromResourceResponse, self).__init__(response)


class TagResourcesResponse(TLSResponse):
    def __init__(self, response: Response):
        super(TagResourcesResponse, self).__init__(response)


class UntagResourcesResponse(TLSResponse):
    def __init__(self, response: Response):
        super(UntagResourcesResponse, self).__init__(response)

class CreateImportTaskResponse(TLSResponse):
    def __init__(self, response):
        super(CreateImportTaskResponse, self).__init__(response)
        self.task_id = self.response[TASK_ID]

    def get_task_id(self):
        """
        :return:导入任务id
        :rtype: str
        """
        return self.task_id

class DeleteImportTaskResponse(TLSResponse):
    def __init__(self, response):
        super(DeleteImportTaskResponse, self).__init__(response)

class ModifyImportTaskResponse(TLSResponse):
    def __init__(self, response):
        super(ModifyImportTaskResponse, self).__init__(response)

class DescribeImportTaskResponse(TLSResponse):
    def __init__(self, response):
        super(DescribeImportTaskResponse, self).__init__(response)
        self.task_info = None
        if TASK_INFO in self.response and self.response[TASK_INFO]:
            self.task_info = ImportTaskInfo.set_attributes(data=self.response[TASK_INFO])

    def get_task_info(self):
        """
        :return:导入任务详情
        :rtype: ImportTaskInfo
        """
        return self.task_info



class DescribeImportTasksResponse(TLSResponse):
    def __init__(self, response):
        super(DescribeImportTasksResponse, self).__init__(response)
        self.total = self.response[TOTAL]
        task_info = self.response[TASK_INFO]
        self.task_info = []

        if task_info is None:
            return

        for i in range(len(task_info)):
            self.task_info.append(ImportTaskInfo.set_attributes(data=task_info[i]))

    def get_task_info(self):
        """
        :return:导入任务详情列表
        :rtype: list[ImportTaskInfo]
        """
        return self.task_info

    def get_task_infos(self):
        """返回导入任务详情列表的别名接口，兼容历史命名"""
        return self.task_info

    def get_total(self):
        """
        :return:导入任务总数
        :rtype: int
        """
        return self.total


class CreateShipperResponse(TLSResponse):
    def __init__(self, response):
        super(CreateShipperResponse, self).__init__(response)
        self.shipper_id = self.response[SHIPPER_ID]

    def get_shipper_id(self):
        """
        :return:投递配置id
        :rtype: str
        """
        return self.shipper_id


class DeleteShipperResponse(TLSResponse):
    def __init__(self, response):
        super(DeleteShipperResponse, self).__init__(response)


class ModifyShipperResponse(TLSResponse):
    def __init__(self, response):
        super(ModifyShipperResponse, self).__init__(response)


class DescribeShipperResponse(TLSResponse):
    def __init__(self, response):
        super(DescribeShipperResponse, self).__init__(response)
        self.shipper_id = self.response[SHIPPER_ID]
        self.shipper_name = self.response[SHIPPER_NAME]
        self.project_id = self.response[PROJECT_ID]
        self.project_name = self.response[PROJECT_NAME]
        self.topic_id = self.response[TOPIC_ID]
        self.topic_name = self.response[TOPIC_NAME]
        self.shipper_type = self.response[SHIPPER_TYPE]
        self.status = self.response[STATUS]
        self.create_time = self.response[CREATE_TIME]
        self.modify_time = self.response[MODIFY_TIME]
        self.shipper_start_time = self.response[SHIPPER_START_TIME]
        self.shipper_end_time = self.response[SHIPPER_END_TIME]
        self.content_info = ContentInfo.set_attributes(data=self.response[CONTENT_INFO])
        self.tos_shipper_info = None
        if TOS_SHIPPER_INFO in self.response and self.response[TOS_SHIPPER_INFO]:
            self.tos_shipper_info = TosShipperInfo.set_attributes(data=self.response[TOS_SHIPPER_INFO])
        self.kafka_shipper_info = None
        if KAFKA_SHIPPER_INFO in self.response and self.response[KAFKA_SHIPPER_INFO]:
            self.kafka_shipper_info = KafkaShipperInfo.set_attributes(data=self.response[KAFKA_SHIPPER_INFO])
        self.dashboard_id = self.response[DASHBOARD_ID]
        self.role_trn = self.response[ROLE_TRN]

    def get_shipper_id(self):
        """
        :return:投递配置id
        :rtype: str
        """
        return self.shipper_id
    def get_shipper_name(self):
        """
        :return:投递配置名称
        :rtype: str
        """
        return self.shipper_name
    def get_project_id(self):
        """
        :return:项目id
        :rtype: str
        """
        return self.project_id
    def get_topic_id(self):
        """
        :return:日志主题id
        :rtype: str
        """
        return self.topic_id
    def get_topic_name(self):
        """
        :return:日志主题名称
        :rtype: str
        """
        return self.topic_name
    def get_shipper_type(self):
        """
        :return:投递配置类型
        :rtype: str
        """
        return self.shipper_type
    def get_status(self):
        """
        :return:投递配置状态
        :rtype: str
        """
        return self.status
    def get_create_time(self):
        """
        :return:创建时间
        :rtype: str
        """
        return self.create_time
    def get_modify_time(self):
        """
        :return:修改时间
        :rtype: str
        """
        return self.modify_time
    def get_shipper_start_time(self):
        """
        :return:投递配置开始时间
        :rtype: int
        """
        return self.shipper_start_time
    def get_shipper_end_time(self):
        """
        :return:投递配置结束时间
        :rtype: int
        """
        return self.shipper_end_time
    def get_content_info(self):
        """
        :return:投递配置内容信息
        :rtype: ContentInfo
        """
        return self.content_info
    def get_tos_shipper_info(self):
        """
        :return:投递配置TOS信息
        :rtype: TosShipperInfo
        """
        return self.tos_shipper_info
    def get_kafka_shipper_info(self):
        """
        :return:投递配置Kafka信息
        :rtype: KafkaShipperInfo
        """
        return self.kafka_shipper_info
    def get_dashboard_id(self):
        """
        :return:监控看板id
        :rtype: str
        """
        return self.dashboard_id
    def get_role_trn(self):
        """
        :return:角色trn
        :rtype: str
        """
        return self.role_trn


class ActiveTlsAccountResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ActiveTlsAccountResponse, self).__init__(response)


class DeleteScheduleSqlTaskResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DeleteScheduleSqlTaskResponse, self).__init__(response)


class ModifyScheduleSqlTaskResponse(TLSResponse):
    def __init__(self, response):
        super(ModifyScheduleSqlTaskResponse, self).__init__(response)


class DescribeShippersResponse(TLSResponse):
    def __init__(self, response):
        super(DescribeShippersResponse, self).__init__(response)
        self.total = self.response[TOTAL]
        self.shippers = []

        shippers_data = self.response.get(SHIPPERS, [])
        for shipper_data in shippers_data:
            self.shippers.append(ShipperInfo.set_attributes(data=shipper_data))

    def get_total(self):
        """
        :return:投递配置总数
        :rtype: int
        """
        return self.total

    def get_shippers(self):
        """
        :return:投递配置列表
        :rtype: List[ShipperInfo]
        """
        return self.shippers


class ModifyETLTaskResponse(TLSResponse):
    def __init__(self, response):
        super(ModifyETLTaskResponse, self).__init__(response)


class CreateTraceInstanceResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateTraceInstanceResponse, self).__init__(response)

        self.trace_instance_id = self.response[TRACE_INSTANCE_ID]

    def get_trace_instance_id(self):
        """
        :return: Trace实例id
        :rtype: str
        """
        return self.trace_instance_id


class DeleteTraceInstanceResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DeleteTraceInstanceResponse, self).__init__(response)


class DescribeTraceInstanceResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeTraceInstanceResponse, self).__init__(response)

        self.trace_instance = TraceInstanceInfo.set_attributes(data=self.response)

    def get_trace_instance(self):
        """
        :return: Trace实例信息
        :rtype: TraceInstanceInfo
        """
        return self.trace_instance


class DescribeTraceInstancesResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeTraceInstancesResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        self.trace_instances = []

        trace_instances_data = self.response.get(TRACE_INSTANCES, [])
        for trace_instance_data in trace_instances_data:
            self.trace_instances.append(TraceInstanceInfo.set_attributes(data=trace_instance_data))

    def get_total(self):
        """
        :return: Trace实例总数
        :rtype: int
        """
        return self.total

    def get_trace_instances(self):
        """
        :return: Trace实例列表
        :rtype: List[TraceInstanceInfo]
        """
        return self.trace_instances


class ModifyTraceInstanceResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ModifyTraceInstanceResponse, self).__init__(response)


class DescribeETLTaskResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeETLTaskResponse, self).__init__(response)

        # 基础字段
        self.create_time = self.response.get(CREATE_TIME)
        self.dsl_type = self.response.get(DSL_TYPE)
        self.description = self.response.get(DESCRIPTION)
        self.etl_status = self.response.get(ETL_STATUS)
        self.enable = self.response.get(ETL_ENABLE)
        self.from_time = self.response.get(ETL_FROM_TIME)
        self.last_enable_time = self.response.get(ETL_LAST_ENABLE_TIME)
        self.modify_time = self.response.get(MODIFY_TIME)
        self.name = self.response.get(NAME)
        self.project_id = self.response.get(PROJECT_ID)
        self.project_name = self.response.get(PROJECT_NAME)
        self.script = self.response.get(ETL_SCRIPT)
        self.source_topic_id = self.response.get(ETL_SOURCE_TOPIC_ID)
        self.source_topic_name = self.response.get(SOURCE_TOPIC_NAME)
        self.task_id = self.response.get(TASK_ID)
        self.task_type = self.response.get(ETL_TASK_TYPE)
        self.to_time = self.response.get(ETL_TO_TIME)

        # 目标资源列表
        self.target_resources = []
        target_resources_data = self.response.get(ETL_TARGET_RESOURCES, [])
        if target_resources_data:
            for target_resource_data in target_resources_data:
                self.target_resources.append(TargetResourceInfo.set_attributes(data=target_resource_data))

    def get_create_time(self):
        """\
        :return: 加工任务的创建时间
        :rtype: str
        """
        return self.create_time

    def get_dsl_type(self):
        """\
        :return: DSL 类型
        :rtype: str
        """
        return self.dsl_type

    def get_description(self):
        """\
        :return: 数据加工任务的描述信息
        :rtype: str
        """
        return self.description

    def get_etl_status(self):
        """\
        :return: 任务调度状态
        :rtype: str
        """
        return self.etl_status

    def get_enable(self):
        """\
        :return: 是否启用数据任务
        :rtype: bool
        """
        return self.enable

    def get_from_time(self):
        """\
        :return: 待加工数据的开始时间
        :rtype: int
        """
        return self.from_time

    def get_last_enable_time(self):
        """\
        :return: 最近启动时间
        :rtype: str
        """
        return self.last_enable_time

    def get_modify_time(self):
        """\
        :return: 加工任务的修改时间
        :rtype: str
        """
        return self.modify_time

    def get_name(self):
        """\
        :return: 加工任务名称
        :rtype: str
        """
        return self.name

    def get_project_id(self):
        """\
        :return: 待加工数据所在的日志项目 ID
        :rtype: str
        """
        return self.project_id

    def get_project_name(self):
        """\
        :return: 待加工数据所在的日志项目名称
        :rtype: str
        """
        return self.project_name

    def get_script(self):
        """\
        :return: 加工规则
        :rtype: str
        """
        return self.script

    def get_source_topic_id(self):
        """\
        :return: 待加工数据所在的日志主题 ID
        :rtype: str
        """
        return self.source_topic_id

    def get_source_topic_name(self):
        """\
        :return: 待加工数据所在的日志主题名称
        :rtype: str
        """
        return self.source_topic_name

    def get_task_id(self):
        """\
        :return: 加工任务 ID
        :rtype: str
        """
        return self.task_id

    def get_task_type(self):
        """\
        :return: 任务类型
        :rtype: str
        """
        return self.task_type

    def get_to_time(self):
        """\
        :return: 日志加工数据范围的结束时间
        :rtype: int
        """
        return self.to_time

    def get_target_resources(self):
        """\
        :return: 输出目标的相关信息
        :rtype: List[TargetResourceInfo]
        """
        return self.target_resources


class DescribeETLTasksResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeETLTasksResponse, self).__init__(response)

        self.total = self.response.get(TOTAL, 0)
        self.tasks = []

        tasks_data = self.response.get(TASKS, [])
        for task_data in tasks_data:
            self.tasks.append(EtlTaskInfo.set_attributes(data=task_data))

    def get_total(self):
        """返回 ETL 任务总数

        :return: ETL 任务总数
        :rtype: int
        """
        return self.total

    def get_tasks(self):
        """返回 ETL 任务列表

        :return: ETL 任务列表
        :rtype: List[EtlTaskInfo]
        """
        return self.tasks


class CancelDownloadTaskResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CancelDownloadTaskResponse, self).__init__(response)


class GetAccountStatusResponse(TLSResponse):
    def __init__(self, response: Response):
        super(GetAccountStatusResponse, self).__init__(response)
        self.arch_version = self.response.get(ARCH_VERSION)
        self.status = self.response.get(STATUS)

    def get_arch_version(self):
        """
        :return: 日志服务版本：2.0：新架构；1.0：老架构
        :rtype: str
        """
        return self.arch_version

    def get_status(self):
        """
        :return: 是否已开通日志服务：Activated：已开通日志服务；NonActivated：未开通日志服务
        :rtype: str
        """
        return self.status


class DescribeTraceResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeTraceResponse, self).__init__(response)
        
        self.trace = TraceInfo.set_attributes(data=self.response.get(TRACE, {}))
    
    def get_trace(self):
        """
        :return: Trace详情
        :rtype: TraceInfo
        """
        return self.trace


class CreateAlarmWebhookIntegrationResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateAlarmWebhookIntegrationResponse, self).__init__(response)
        self.alarm_webhook_integration_id = self.response[ALARM_WEBHOOK_INTEGRATION_ID]

    def get_alarm_webhook_integration_id(self):
        """
        :return: Webhook 集成配置 ID
        :rtype: str
        """
        return self.alarm_webhook_integration_id


class CreateETLTaskResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateETLTaskResponse, self).__init__(response)

        self.task_id = self.response[ETL_TASK_ID]

    def get_task_id(self):
        """
        :return: ETL任务ID
        :rtype: str
        """
        return self.task_id


class ModifyETLTaskStatusResponse(TLSResponse):
    def __init__(self, response):
        super(ModifyETLTaskStatusResponse, self).__init__(response)


class DeleteETLTaskResponse(TLSResponse):
    def __init__(self, response):
        super(DeleteETLTaskResponse, self).__init__(response)


class CreateScheduleSqlTaskResponse(TLSResponse):
    def __init__(self, response):
        super(CreateScheduleSqlTaskResponse, self).__init__(response)
        self.task_id = self.response[TASK_ID]

    def get_task_id(self):
        """
        :return: 定时SQL分析任务ID
        :rtype: str
        """
        return self.task_id


class DescribeScheduleSqlTaskResponse(TLSResponse):
    def __init__(self, response):
        super(DescribeScheduleSqlTaskResponse, self).__init__(response)
        self.schedule_sql_task_info = ScheduleSqlTaskInfo.set_attributes(data=self.response)

    def get_schedule_sql_task_info(self):
        """
        :return: 定时 SQL 分析任务信息
        :rtype: ScheduleSqlTaskInfo
        """
        return self.schedule_sql_task_info


class DescribeScheduleSqlTasksResponse(TLSResponse):
    def __init__(self, response):
        super(DescribeScheduleSqlTasksResponse, self).__init__(response)
        self.total = self.response[TOTAL]
        self.tasks = []
        tasks = self.response[TASKS]

        for i in range(len(tasks)):
            self.tasks.append(ScheduleSqlTaskInfo.set_attributes(data=tasks[i]))

    def get_total(self):
        """
        :return: 定时SQL任务总数
        :rtype: int
        """
        return self.total

    def get_tasks(self):
        """
        :return: 定时SQL任务列表
        :rtype: List[ScheduleSqlTaskInfo]
        """
        return self.tasks


class CreateAlarmContentTemplateResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateAlarmContentTemplateResponse, self).__init__(response)
        self.alarm_content_template_id = self.response.get(ALARM_CONTENT_TEMPLATE_ID)

    def get_alarm_content_template_id(self):
        """
        :return: 告警通知模版 ID
        :rtype: str
        """
        return self.alarm_content_template_id


class ModifyAlarmContentTemplateResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ModifyAlarmContentTemplateResponse, self).__init__(response)


class DeleteAlarmContentTemplateResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DeleteAlarmContentTemplateResponse, self).__init__(response)


class DeleteAlarmWebhookIntegrationResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DeleteAlarmWebhookIntegrationResponse, self).__init__(response)


class DescribeAlarmWebhookIntegrationsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeAlarmWebhookIntegrationsResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        self.webhook_integrations = []

        for integration in self.response.get(WEBHOOK_INTEGRATIONS, []):
            self.webhook_integrations.append(
                WebhookIntegrationInfo.set_attributes(data=integration))

    def get_total(self):
        """返回 Webhook 集成配置数量

        :return: Webhook 集成配置数量
        :rtype: int
        """
        return self.total

    def get_webhook_integrations(self):
        """返回 Webhook 集成配置列表

        :return: Webhook 集成配置列表
        :rtype: List[WebhookIntegrationInfo]
        """
        return self.webhook_integrations

class DescribeAlarmContentTemplatesResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeAlarmContentTemplatesResponse, self).__init__(response)
        self.alarm_content_templates = []
        self.total = self.response.get(TOTAL, 0)

        if ALARM_CONTENT_TEMPLATES in self.response:
            for template_data in self.response[ALARM_CONTENT_TEMPLATES]:
                self.alarm_content_templates.append(
                    ContentTemplateInfo.set_attributes(template_data))

    def get_alarm_content_templates(self):
        """返回告警内容模板列表

        :return: 告警内容模板列表
        :rtype: List[ContentTemplateInfo]
        """
        return self.alarm_content_templates

    def get_total(self):
        """返回告警内容模板数量

        :return: 告警内容模板数量
        :rtype: int
        """
        return self.total
class ModifyAlarmWebhookIntegrationResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ModifyAlarmWebhookIntegrationResponse, self).__init__(response)


class ListTagsForResourcesResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ListTagsForResourcesResponse, self).__init__(response)
        self.resource_tags = []
        self.next_token = self.response.get("NextToken", "")

        resource_tags_data = self.response.get("ResourceTags", [])
        for tag_data in resource_tags_data:
            self.resource_tags.append(ResourceTagInfo.set_attributes(data=tag_data))

    def get_resource_tags(self):
        """返回资源所绑定的标签列表"""
        return self.resource_tags

    def get_next_token(self):
        """返回分页查询凭证"""
        return self.next_token


class SearchTracesResponse(TLSResponse):
    def __init__(self, response: Response):
        super(SearchTracesResponse, self).__init__(response)
        self.total = self.response.get(TOTAL, 0)
        self.trace_infos = []

        trace_infos_data = self.response.get(TRACE_INFOS, [])
        for trace_info_data in trace_infos_data:
            self.trace_infos.append(TraceInfo.set_attributes(data=trace_info_data))

    def get_total(self):
        """返回符合条件的 Trace 总数"""
        return self.total

    def get_trace_infos(self):
        """返回 Trace 列表"""
        return self.trace_infos


# ===== Text Analysis - App Instance / Scene Meta / Session Answer =====
# 复杂嵌套结构（InstanceInfo / DescribeClusterStoreMeta / DescribeClusterMeta /
# DescribeSessionMeta / DescribeSessionMessage / DescribeKnowledgeBinding 等）
# 当前以 dict 形式直接透传，未来如有 DTO 需求再补类。

class CreateAppInstanceResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateAppInstanceResponse, self).__init__(response)
        # 服务端字段为 InstanceID（大写 ID），同时兼容 InstanceId
        self.instance_id = self.response.get(INSTANCE_ID_RSP, "") or self.response.get(INSTANCE_ID, "")

    def get_instance_id(self):
        return self.instance_id


class ModifyAppInstanceResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ModifyAppInstanceResponse, self).__init__(response)


class DeleteAppInstanceResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DeleteAppInstanceResponse, self).__init__(response)


class DescribeAppInstancesResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeAppInstancesResponse, self).__init__(response)
        self.total = self.response.get(TOTAL, 0)
        self.instances = self.response.get(INSTANCE_INFO, [])

    def get_total(self):
        return self.total

    def get_instances(self):
        """返回实例信息列表（dict 列表，结构详见服务端 InstanceInfo）"""
        return self.instances


class CreateAppSceneMetaResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateAppSceneMetaResponse, self).__init__(response)
        self.id = self.response.get(ID_FIELD, "")

    def get_id(self):
        return self.id


class ModifyAppSceneMetaResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ModifyAppSceneMetaResponse, self).__init__(response)


class DeleteAppSceneMetaResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DeleteAppSceneMetaResponse, self).__init__(response)


class DescribeAppSceneMetasResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeAppSceneMetasResponse, self).__init__(response)
        self.page_context = self.response.get(PAGE_CONTEXT, "")
        self.total = self.response.get(TOTAL, 0)
        self.items = self.response.get(ITEMS, [])

    def get_page_context(self):
        return self.page_context

    def get_total(self):
        return self.total

    def get_items(self):
        """返回 DescribeAppSceneMetasRes 列表（dict 列表，含 6 个嵌套子字段）"""
        return self.items


class DescribeAppSceneMetaResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeAppSceneMetaResponse, self).__init__(response)
        # DescribeAppSceneMetasRes 的 6 个嵌套字段直接以 dict 暴露
        self.describe_cluster_store_meta = self.response.get("DescribeClusterStoreMeta")
        self.describe_cluster_meta = self.response.get("DescribeClusterMeta")
        self.describe_session_meta = self.response.get("DescribeSessionMeta")
        self.describe_session_message = self.response.get("DescribeSessionMessage")
        self.describe_session_suggestion = self.response.get("DescribeSessionSuggestion", "")
        self.describe_knowledge_binding = self.response.get("DescribeKnowledgeBinding")

    def get_describe_cluster_store_meta(self):
        return self.describe_cluster_store_meta

    def get_describe_cluster_meta(self):
        return self.describe_cluster_meta

    def get_describe_session_meta(self):
        return self.describe_session_meta

    def get_describe_session_message(self):
        return self.describe_session_message

    def get_describe_session_suggestion(self):
        return self.describe_session_suggestion

    def get_describe_knowledge_binding(self):
        return self.describe_knowledge_binding


class DescribeSessionAnswerResponse(TLSResponse):
    """SSE 风格响应；MVP 阶段以 dict 透传整体 response，并提供少量便捷方法。"""

    def __init__(self, response: Response):
        content_type = response.headers.get(CONTENT_TYPE, "")
        if "text/event-stream" in content_type:
            self.raw_response = response
            self.headers = response.headers
            self.request_id = response.headers[X_TLS_REQUEST_ID]
            self.response = {}
            self.message_id = ""
            self.session_id = ""
            self.question_id = ""
            return
        self.raw_response = response
        super(DescribeSessionAnswerResponse, self).__init__(response)
        self.message_id = self.response.get(MESSAGE_ID, "")
        self.session_id = self.response.get(SESSION_ID, "")
        self.question_id = self.response.get(QUESTION_ID, "")

    def get_message_id(self):
        return self.message_id

    def get_session_id(self):
        return self.session_id

    def get_question_id(self):
        return self.question_id

    def get_response(self):
        """返回完整响应字典（详见服务端 DescribeSessionAnswerResp）"""
        return self.response

    def iter_lines(self, *args, **kwargs):
        return self.raw_response.iter_lines(*args, **kwargs)
