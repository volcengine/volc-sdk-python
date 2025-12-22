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

        self.full_text = FullTextInfo()
        if self.response[FULL_TEXT] is not None:
            self.full_text = FullTextInfo.set_attributes(data=self.response[FULL_TEXT])
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

    def get_max_text_len(self):
        """
        :return: 统计字段值的最大长度
        :rtype: int
        """
        return self.max_text_len


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


class ConsumeLogsResponse(TLSResponse):
    def __init__(self, response: Response, compression: str):
        super(ConsumeLogsResponse, self).__init__(response)

        self.x_tls_cursor = self.headers[X_TLS_CURSOR]
        self.x_tls_count = int(self.headers[X_TLS_COUNT])
        self.pb_message = None

        if DATA in self.response:
            pb_message = self.response[DATA]
            if compression == LZ4:
                pb_message = lz4.decompress(struct.pack('<I', int(self.headers[X_TLS_BODYRAWSIZE])) + pb_message)
            if compression == ZLIB:
                pb_message = zlib.decompress(pb_message)

            self.pb_message = LogGroupList()
            try:
                self.pb_message.ParseFromString(pb_message)
            except Exception as e:
                log_content_patch.ParseLogGroupListFromString(self.pb_message, pb_message)

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
        consumer_groups = self.response[CONSUMER_GROUPS]

        if consumer_groups is None:
            return

        for i in range(len(consumer_groups)):
            self.consumer_groups.append(ConsumerGroup.set_attributes(data=consumer_groups[i]))


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
        self.enable = self.response.get(ENABLE)
        self.from_time = self.response.get(FROM_TIME)
        self.last_enable_time = self.response.get(LAST_ENABLE_TIME)
        self.modify_time = self.response.get(MODIFY_TIME)
        self.name = self.response.get(NAME)
        self.project_id = self.response.get(PROJECT_ID)
        self.project_name = self.response.get(PROJECT_NAME)
        self.script = self.response.get(SCRIPT)
        self.source_topic_id = self.response.get(SOURCE_TOPIC_ID)
        self.source_topic_name = self.response.get(SOURCE_TOPIC_NAME)
        self.task_id = self.response.get(TASK_ID)
        self.task_type = self.response.get(TASK_TYPE)
        self.to_time = self.response.get(TO_TIME)

        # 目标资源列表
        self.target_resources = []
        target_resources_data = self.response.get(TARGET_RESOURCES, [])
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
