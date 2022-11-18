# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import struct

try:
    import lz4
except ImportError:
    lz4 = None
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

    @staticmethod
    def _get_host_group_hosts_rules_info(host_group_hosts_rules_info) -> HostGroupHostsRulesInfo:
        host_group_hosts_rules_info[HOST_GROUP_INFO] = \
            HostGroupInfo.set_attributes(data=host_group_hosts_rules_info[HOST_GROUP_INFO])
        host_group_info = host_group_hosts_rules_info[HOST_GROUP_INFO]

        host_infos = host_group_hosts_rules_info[HOST_INFOS]
        for i in range(len(host_infos)):
            host_infos[i] = HostInfo.set_attributes(data=host_infos[i])

        rule_infos = host_group_hosts_rules_info[RULE_INFOS]
        for i in range(len(rule_infos)):
            rule_infos[i] = RuleInfo.set_attributes(data=rule_infos[i])

        return HostGroupHostsRulesInfo(host_group_info, host_infos, rule_infos)


class CreateProjectResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateProjectResponse, self).__init__(response)

        self.project_id = self.response[PROJECT_ID]


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


class DescribeProjectsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeProjectsResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        self.projects = self.response[PROJECTS]

        for i in range(len(self.projects)):
            self.projects[i] = ProjectInfo.set_attributes(data=self.projects[i])


class CreateTopicResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateTopicResponse, self).__init__(response)

        self.topic_id = self.response[TOPIC_ID]


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


class DescribeTopicsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeTopicsResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        self.topics = self.response[TOPICS]

        for i in range(len(self.topics)):
            self.topics[i] = TopicInfo.set_attributes(data=self.topics[i])


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

        if self.response[FULL_TEXT] is not None:
            self.full_text = FullTextInfo.set_attributes(data=self.response[FULL_TEXT])
        else:
            self.full_text = None
        self.key_value = self.response[KEY_VALUE]
        self.create_time = self.response[CREATE_TIME]
        self.modify_time = self.response[MODIFY_TIME]

        for i in range(len(self.key_value)):
            self.key_value[i] = KeyValueInfo(key=self.key_value[i][KEY],
                                             value=ValueInfo.set_attributes(data=self.key_value[i][VALUE]))


class PutLogsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(PutLogsResponse, self).__init__(response)


class DescribeCursorResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeCursorResponse, self).__init__(response)

        self.cursor = self.response[CURSOR]


class ConsumeLogsResponse(TLSResponse):
    def __init__(self, response: Response, compression: str):
        super(ConsumeLogsResponse, self).__init__(response)

        self.x_tls_cursor = self.headers[X_TLS_CURSOR]
        self.x_tls_count = int(self.headers[X_TLS_COUNT])
        self.pb_message = None

        if DATA in self.response:
            pb_message = self.response[DATA]
            if compression == LZ4:
                pb_message = lz4.uncompress(struct.pack('<I', int(self.headers[X_TLS_BODYRAWSIZE])) + pb_message)

            self.pb_message = LogGroupList()
            self.pb_message.ParseFromString(pb_message)


class SearchLogsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(SearchLogsResponse, self).__init__(response)

        self.search_result = SearchResult.set_attributes(data=self.response)


class DescribeLogContextResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeLogContextResponse, self).__init__(response)

        self.log_context_infos = self.response[LOG_CONTEXT_INFOS]
        self.prev_over = self.response[PREV_OVER]
        self.next_over = self.response[NEXT_OVER]


class WebTracksResponse(TLSResponse):
    def __init__(self, response: Response):
        super(WebTracksResponse, self).__init__(response)


class DescribeHistogramResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeHistogramResponse, self).__init__(response)

        self.result_status = self.response[RESULT_STATUS]
        self.interval = self.response[INTERVAL]
        self.total_count = self.response[TOTAL_COUNT]
        self.histogram = self.response[HISTOGRAM]

        for i in range(len(self.histogram)):
            self.histogram[i] = HistogramInfo.set_attributes(data=self.histogram[i])


class CreateDownloadTaskResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateDownloadTaskResponse, self).__init__(response)

        self.task_id = self.response[TASK_ID]


class DescribeDownloadTasksResponse(TLSResponse):
    def __init__(self, response):
        super(DescribeDownloadTasksResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        self.tasks = self.response[TASKS]

        for i in range(len(self.tasks)):
            self.tasks[i] = TaskInfo.set_attributes(data=self.tasks[i])


class DescribeDownloadUrlResponse(TLSResponse):
    def __init__(self, response):
        super(DescribeDownloadUrlResponse, self).__init__(response)

        self.download_url = self.response[DOWNLOAD_URL]


class DescribeShardsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeShardsResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        self.shards = self.response[SHARDS]

        for i in range(len(self.shards)):
            self.shards[i] = QueryResp.set_attributes(data=self.shards[i])


class CreateHostGroupResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateHostGroupResponse, self).__init__(response)

        self.host_group_id = self.response[HOST_GROUP_ID]


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


class DescribeHostGroupsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeHostGroupsResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        self.host_group_hosts_rules_infos = self.response[HOST_GROUP_HOSTS_RULES_INFOS]

        for i in range(len(self.host_group_hosts_rules_infos)):
            self.host_group_hosts_rules_infos[i] = \
                DescribeHostGroupsResponse._get_host_group_hosts_rules_info(self.host_group_hosts_rules_infos[i])


class ModifyHostGroupsAutoUpdateResponse(TLSResponse):
    def __init__(self, response: Response):
        super(ModifyHostGroupsAutoUpdateResponse, self).__init__(response)


class DescribeHostsResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeHostsResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        self.host_infos = self.response[HOST_INFOS]

        for i in range(len(self.host_infos)):
            self.host_infos[i] = HostInfo.set_attributes(data=self.host_infos[i])


class DeleteHostResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DeleteHostResponse, self).__init__(response)


class DescribeHostGroupRulesResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeHostGroupRulesResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        self.rule_infos = self.response[RULE_INFOS]

        for i in range(len(self.rule_infos)):
            self.rule_infos[i] = RuleInfo.set_attributes(data=self.rule_infos[i])


class CreateRuleResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateRuleResponse, self).__init__(response)

        self.rule_id = self.response[RULE_ID]


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
        self.host_group_infos = self.response[HOST_GROUP_INFOS]

        for i in range(len(self.host_group_infos)):
            self.host_group_infos[i] = HostGroupInfo.set_attributes(data=self.host_group_infos[i])


class DescribeRulesResponse(TLSResponse):
    def __init__(self, response: Response):
        super(DescribeRulesResponse, self).__init__(response)

        self.total = self.response[TOTAL]
        self.rule_infos = self.response[RULE_INFOS]

        for i in range(len(self.rule_infos)):
            self.rule_infos[i] = RuleInfo.set_attributes(data=self.rule_infos[i])


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
        self.alarm_notify_groups = self.response[ALARM_NOTIFY_GROUPS]

        for i in range(len(self.alarm_notify_groups)):
            self.alarm_notify_groups[i] = AlarmNotifyGroupInfo.set_attributes(data=self.alarm_notify_groups[i])


class CreateAlarmResponse(TLSResponse):
    def __init__(self, response: Response):
        super(CreateAlarmResponse, self).__init__(response)

        self.alarm_id = self.response[ALARM_ID]


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
        self.alarms = self.response[ALARMS]

        for i in range(len(self.alarms)):
            self.alarms[i] = AlarmInfo.set_attributes(data=self.alarms[i])


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
