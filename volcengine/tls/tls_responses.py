# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import struct

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
from volcengine.tls.tls_exception import TLSException


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
            self.pb_message.ParseFromString(pb_message)

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
