# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re
from typing import List, Dict

from volcengine.tls.const import *


def pascal_to_snake(pascal: str) -> str:
    return re.sub(r"(?P<key>[A-Z])", r"_\g<key>", pascal).lower().strip('_')


def snake_to_pascal(snake: str) -> str:
    return ''.join(word.title() for word in snake.split('_'))


class TLSData:
    @classmethod
    def set_attributes(cls, data: dict):
        if data is None or len(data) == 0:
            return None

        tls_data_dict = {}

        for key in data.keys():
            tls_data_dict[pascal_to_snake(key)] = data[key]

        tls_data = cls()

        for key in tls_data.__dict__.keys():
            tls_data.__dict__[key] = None

        tls_data.__dict__.update(tls_data_dict)

        return tls_data

    def json(self):
        json_data = {}

        for key in self.__dict__.keys():
            if self.__dict__[key] is not None:
                json_data[snake_to_pascal(key)] = self.__dict__[key]

        return json_data


class ProjectInfo(TLSData):
    def __init__(self, project_name: str = None, project_id: str = None, description: str = None,
                 create_time: str = None, inner_net_domain: str = None, topic_count: int = None):
        self.project_name = project_name
        self.project_id = project_id
        self.description = description
        self.create_time = create_time
        self.inner_net_domain = inner_net_domain
        self.topic_count = topic_count


class TopicInfo(TLSData):
    def __init__(self, topic_name: str = None, topic_id: str = None, project_id: str = None, ttl: int = None,
                 create_time: str = None, modify_time: str = None, shard_count: int = None, description: str = None):
        self.topic_name = topic_name
        self.topic_id = topic_id
        self.project_id = project_id
        self.ttl = ttl
        self.create_time = create_time
        self.modify_time = modify_time
        self.shard_count = shard_count
        self.description = description


class FullTextInfo(TLSData):
    def __init__(self, case_sensitive: bool, delimiter: str, include_chinese: bool = False):
        self.case_sensitive = case_sensitive
        self.delimiter = delimiter
        self.include_chinese = include_chinese

    @classmethod
    def set_attributes(cls, data: dict):
        case_sensitive = data.get(CASE_SENSITIVE)
        delimiter = data.get(DELIMITER)
        include_chinese = data.get(INCLUDE_CHINESE)

        return cls(case_sensitive, delimiter, include_chinese)


class ValueInfo(TLSData):
    def __init__(self, value_type: str, delimiter: str = None, case_sensitive: bool = False,
                 include_chinese: bool = False, sql_flag: bool = False):
        self.value_type = value_type
        self.delimiter = delimiter
        self.case_sensitive = case_sensitive
        self.include_chinese = include_chinese
        self.sql_flag = sql_flag

    @classmethod
    def set_attributes(cls, data: dict):
        value_type = data.get(VALUE_TYPE)
        delimiter = data.get(DELIMITER)
        case_sensitive = data.get(CASE_SENSITIVE)
        include_chinese = data.get(INCLUDE_CHINESE)
        sql_flag = data.get(SQL_FLAG)

        return cls(value_type, delimiter, case_sensitive, include_chinese, sql_flag)


class KeyValueInfo(TLSData):
    def __init__(self, key: str, value: ValueInfo):
        self.key = key
        self.value = value

    def json(self):
        return {KEY: self.key, VALUE: self.value.json()}


class AnalysisResult(TLSData):
    def __init__(self, analysis_schema: List[str] = None, analysis_type: dict = None, analysis_data: List[dict] = None):
        self.analysis_schema = analysis_schema
        self.analysis_type = analysis_type
        self.analysis_data = analysis_data

    @classmethod
    def set_attributes(cls, data: dict):
        analysis_schema = data.get(SCHEMA)
        analysis_type = data.get(TYPE)
        analysis_data = data.get(DATA)

        return cls(analysis_schema, analysis_type, analysis_data)


class SearchResult(TLSData):
    def __init__(self, result_status: str = None, hit_count: int = None, list_over: bool = None, analysis: bool = None,
                 count: int = None, limit: int = None, context: str = None, logs: List[dict] = None,
                 analysis_result: AnalysisResult = None):
        self.result_status = result_status
        self.hit_count = hit_count
        self.list_over = list_over
        self.analysis = analysis
        self.count = count
        self.limit = limit
        self.context = context
        self.logs = logs
        self.analysis_result = analysis_result

    @classmethod
    def set_attributes(cls, data: dict):
        search_result = super(SearchResult, cls).set_attributes(data)

        if ANALYSIS_RESULT in data:
            search_result.analysis_result = AnalysisResult.set_attributes(data=data[ANALYSIS_RESULT])

        return search_result


class QueryResp(TLSData):
    def __init__(self, topic_id: str = None, shard_id: int = None, inclusive_begin_key: str = None,
                 exclusive_end_key: str = None, status: str = None, modify_time: str = None):
        self.topic_id = topic_id
        self.shard_id = shard_id
        self.inclusive_begin_key = inclusive_begin_key
        self.exclusive_end_key = exclusive_end_key
        self.status = status
        self.modify_time = modify_time


class HistogramInfo(TLSData):
    def __init__(self, time: int = None, count: int = None):
        self.time = time
        self.count = count


class TaskInfo(TLSData):
    def __init__(self, task_id: str = None, task_name: str = None, topic_id: str = None, query: str = None,
                 start_time: str = None, end_time: str = None, data_format: str = None, task_status: str = None,
                 compression: str = None, create_time: str = None, log_size: int = None, log_count: int = None):
        self.task_id = task_id
        self.task_name = task_name
        self.topic_id = topic_id
        self.query = query
        self.start_time = start_time
        self.end_time = end_time
        self.data_format = data_format
        self.task_status = task_status
        self.compression = compression
        self.create_time = create_time
        self.log_size = log_size
        self.log_count = log_count


class HostInfo(TLSData):
    def __init__(self, ip: str = None, log_collector_version: str = None, heartbeat_status: int = None):
        self.ip = ip
        self.log_collector_version = log_collector_version
        self.heartbeat_status = heartbeat_status


class HostGroupInfo(TLSData):
    def __init__(self, host_group_id: str = None, host_group_name: str = None, host_group_type: str = None,
                 host_identifier: str = None, host_count: int = None, normal_heartbeat_status_count: int = None,
                 abnormal_heartbeat_status_count: int = None, rule_count: int = None,
                 create_time: str = None, modify_time: str = None, auto_update: bool = False,
                 update_start_time: str = None, update_end_time: str = None, agent_latest_version: str = None):
        self.host_group_id = host_group_id
        self.host_group_name = host_group_name
        self.host_group_type = host_group_type
        self.host_identifier = host_identifier
        self.host_count = host_count
        self.normal_heartbeat_status_count = normal_heartbeat_status_count
        self.abnormal_heartbeat_status_count = abnormal_heartbeat_status_count
        self.rule_count = rule_count
        self.create_time = create_time
        self.modify_time = modify_time
        self.auto_update = auto_update
        self.update_start_time = update_start_time
        self.update_end_time = update_end_time
        self.agent_latest_version = agent_latest_version


class FilterKeyRegex(TLSData):
    def __init__(self, key: str, regex: str):
        self.key = key
        self.regex = regex

    @classmethod
    def set_attributes(cls, data: dict):
        key = data.get(KEY)
        regex = data.get(REGEX)

        return cls(key, regex)


class LogTemplate(TLSData):
    def __init__(self, log_type: str, log_format: str):
        self.log_type = log_type
        self.log_format = log_format

    def json(self):
        return {TYPE: self.log_type, FORMAT: self.log_format}


class ExtractRule(TLSData):
    def __init__(self, delimiter: str = None, begin_regex: str = None, log_regex: str = None, keys: List[str] = None,
                 time_key: str = None, time_format: str = None, filter_key_regex: List[FilterKeyRegex] = None,
                 un_match_up_load_switch: bool = None, un_match_log_key: str = None, log_template: LogTemplate = None):
        assert (time_key is None and time_format is None) or (time_key is not None and time_format is not None)
        assert (un_match_up_load_switch is None and un_match_log_key is None) or \
               (un_match_up_load_switch is not None and un_match_log_key is not None)

        self.delimiter = delimiter
        self.begin_regex = begin_regex
        self.log_regex = log_regex
        self.keys = keys
        self.time_key = time_key
        self.time_format = time_format
        self.filter_key_regex = filter_key_regex
        self.un_match_up_load_switch = un_match_up_load_switch
        self.un_match_log_key = un_match_log_key
        self.log_template = log_template

    @classmethod
    def set_attributes(cls, data: dict):
        extract_rule = super(ExtractRule, cls).set_attributes(data)

        if FILTER_KEY_REGEX in data:
            extract_rule.filter_key_regex = []
            for one_filter_key_regex in data[FILTER_KEY_REGEX]:
                extract_rule.filter_key_regex.append(FilterKeyRegex.set_attributes(data=one_filter_key_regex))
        if LOG_TEMPLATE in data:
            extract_rule.log_template = LogTemplate(log_type=data[LOG_TEMPLATE].get(TYPE),
                                                    log_format=data[LOG_TEMPLATE].get(FORMAT))

        return extract_rule

    def json(self):
        json_data = super(ExtractRule, self).json()

        if self.filter_key_regex is not None:
            json_data[FILTER_KEY_REGEX] = []
            for regex in self.filter_key_regex:
                json_data[FILTER_KEY_REGEX].append(regex.json())
        if self.log_template is not None:
            json_data[LOG_TEMPLATE] = self.log_template.json()

        return json_data


class ExcludePath(TLSData):
    def __init__(self, path_type: str, value: str):
        assert path_type == "File" or path_type == "Path"

        self.path_type = path_type
        self.value = value

    @classmethod
    def set_attributes(cls, data: dict):
        path_type = data.get(TYPE)
        value = data.get(VALUE)

        return cls(path_type, value)

    def json(self):
        return {TYPE: self.path_type, VALUE: self.value}


class ParsePathRule(TLSData):
    def __init__(self, path_sample: str, regex: str, keys: List[str]):
        self.path_sample = path_sample
        self.regex = regex
        self.keys = keys

    @classmethod
    def set_attributes(cls, data: dict):
        path_sample = data.get(PATH_SAMPLE)
        regex = data.get(REGEX)
        keys = data.get(KEYS)

        return cls(path_sample, regex, keys)


class ShardHashKey(TLSData):
    def __init__(self, hash_key: str):
        self.hash_key = hash_key


class UserDefineRule(TLSData):
    def __init__(self, parse_path_rule: ParsePathRule = None, shard_hash_key: ShardHashKey = None,
                 enable_raw_log: bool = False, fields: dict = None):
        self.parse_path_rule = parse_path_rule
        self.shard_hash_key = shard_hash_key
        self.enable_raw_log = enable_raw_log
        self.fields = fields

    @classmethod
    def set_attributes(cls, data: dict):
        user_define_rule = super(UserDefineRule, cls).set_attributes(data)

        if SHARD_HASH_KEY in data:
            user_define_rule.shard_hash_key = ShardHashKey(hash_key=data[SHARD_HASH_KEY].get(HASH_KEY))
        if PARSE_PATH_RULE in data:
            user_define_rule.parse_path_rule = ParsePathRule.set_attributes(data[PARSE_PATH_RULE])

        return user_define_rule

    def json(self):
        json_data = super(UserDefineRule, self).json()

        if self.shard_hash_key is not None:
            json_data[SHARD_HASH_KEY] = self.shard_hash_key.json()
        if self.parse_path_rule is not None:
            json_data[PARSE_PATH_RULE] = self.parse_path_rule.json()

        return json_data


class KubernetesRule(TLSData):
    def __init__(self, namespace_name_regex: str = None, workload_type: str = None, workload_name_regex: str = None,
                 include_pod_label_regex: Dict[str, str] = None, exclude_pod_label_regex: Dict[str, str] = None,
                 pod_name_regex: str = None, label_tag: Dict[str, str] = None):
        self.namespace_name_regex = namespace_name_regex
        self.workload_type = workload_type
        self.workload_name_regex = workload_name_regex
        self.include_pod_label_regex = include_pod_label_regex
        self.exclude_pod_label_regex = exclude_pod_label_regex
        self.pod_name_regex = pod_name_regex
        self.label_tag = label_tag


class ContainerRule(TLSData):
    def __init__(self, stream: str = None, container_name_regex: str = None,
                 include_container_label_regex: Dict[str, str] = None,
                 exclude_container_label_regex: Dict[str, str] = None,
                 include_container_env_regex: Dict[str, str] = None,
                 exclude_container_env_regex: Dict[str, str] = None,
                 env_tag: Dict[str, str] = None, kubernetes_rule: KubernetesRule = None):
        self.stream = stream
        self.container_name_regex = container_name_regex
        self.include_container_label_regex = include_container_label_regex
        self.exclude_container_label_regex = exclude_container_label_regex
        self.include_container_env_regex = include_container_env_regex
        self.exclude_container_env_regex = exclude_container_env_regex
        self.env_tag = env_tag
        self.kubernetes_rule = kubernetes_rule

    @classmethod
    def set_attributes(cls, data: dict):
        container_rule = super(ContainerRule, cls).set_attributes(data)

        if KUBERNETES_RULE in data:
            container_rule.kubernetes_rule = KubernetesRule.set_attributes(data=data[KUBERNETES_RULE])

        return container_rule

    def json(self):
        json_data = super(ContainerRule, self).json()

        if self.kubernetes_rule is not None:
            json_data[KUBERNETES_RULE] = self.kubernetes_rule.json()

        return json_data


class RuleInfo(TLSData):
    def __init__(self, topic_id: str = None, topic_name: str = None, rule_id: str = None, rule_name: str = None,
                 paths: List[str] = None, log_type: str = None, extract_rule: ExtractRule = None,
                 exclude_paths: List[ExcludePath] = None, log_sample: str = None,
                 user_define_rule: UserDefineRule = None, create_time: str = None, modify_time: str = None,
                 input_type: int = None, container_rule: ContainerRule = None):
        self.topic_id = topic_id
        self.topic_name = topic_name
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.paths = paths
        self.log_type = log_type
        self.extract_rule = extract_rule
        self.exclude_paths = exclude_paths
        self.log_sample = log_sample
        self.user_define_rule = user_define_rule
        self.create_time = create_time
        self.modify_time = modify_time
        self.input_type = input_type
        self.container_rule = container_rule

    @classmethod
    def set_attributes(cls, data: dict):
        rule_info = super(RuleInfo, cls).set_attributes(data)

        if EXTRACT_RULE in data:
            rule_info.extract_rule = ExtractRule.set_attributes(data=data[EXTRACT_RULE])
        if EXCLUDE_PATHS in data:
            rule_info.exclude_paths = []
            for exclude_path in data[EXCLUDE_PATHS]:
                rule_info.exclude_paths.append(ExcludePath.set_attributes(data=exclude_path))
        if USER_DEFINE_RULE in data:
            rule_info.user_define_rule = UserDefineRule.set_attributes(data=data[USER_DEFINE_RULE])
        if CONTAINER_RULE in data:
            rule_info.container_rule = ContainerRule.set_attributes(data=data[CONTAINER_RULE])

        return rule_info


class HostGroupHostsRulesInfo(TLSData):
    def __init__(self, host_group_info: HostGroupInfo, host_infos: List[HostInfo], rule_infos: List[RuleInfo]):
        self.host_group_info = host_group_info
        self.host_infos = host_infos
        self.rule_infos = rule_infos


class Receiver(TLSData):
    def __init__(self, receiver_type: str, receiver_names: List[str], receiver_channels: List[str],
                 start_time: str, end_time: str, webhook: str = None):
        self.receiver_type = receiver_type
        self.receiver_names = receiver_names
        self.receiver_channels = receiver_channels
        self.start_time = start_time
        self.end_time = end_time
        self.webhook = webhook

    @classmethod
    def set_attributes(cls, data: dict):
        receiver_type = data.get(RECEIVER_TYPE)
        receiver_names = data.get(RECEIVER_NAMES)
        receiver_channels = data.get(RECEIVER_CHANNELS)
        start_time = data.get(START_TIME)
        end_time = data.get(END_TIME)
        webhook = data.get(WEBHOOK)

        return cls(receiver_type, receiver_names, receiver_channels, start_time, end_time, webhook)


class QueryRequest(TLSData):
    def __init__(self, topic_id: str, query: str, number: int,
                 start_time_offset: int, end_time_offset: int, topic_name: str = None):
        self.topic_id = topic_id
        self.query = query
        self.number = number
        self.start_time_offset = start_time_offset
        self.end_time_offset = end_time_offset
        self.topic_name = topic_name

    @classmethod
    def set_attributes(cls, data: dict):
        topic_id = data.get(TOPIC_ID)
        topic_name = data.get(TOPIC_NAME)
        query = data.get(QUERY)
        number = data.get(NUMBER)
        start_time_offset = data.get(START_TIME_OFFSET)
        end_time_offset = data.get(END_TIME_OFFSET)

        return cls(topic_id, topic_name, query, number, start_time_offset, end_time_offset)


class RequestCycle(TLSData):
    def __init__(self, cycle_type: str, time: int):
        self.cycle_type = cycle_type
        self.time = time

    @classmethod
    def set_attributes(cls, data: dict):
        cycle_type = data.get(TYPE)
        time = data.get(TIME)

        return cls(cycle_type, time)

    def json(self):
        return {TYPE: self.cycle_type, TIME: self.time}


class AlarmNotifyGroupInfo(TLSData):
    def __init__(self, alarm_notify_group_name: str = None, alarm_notify_group_id: str = None,
                 notify_type: List[str] = None, receivers: List[Receiver] = None,
                 create_time: str = None, modify_time: str = None):
        self.alarm_notify_group_name = alarm_notify_group_name
        self.alarm_notify_group_id = alarm_notify_group_id
        self.notify_type = notify_type
        self.receivers = receivers
        self.create_time = create_time
        self.modify_time = modify_time

    @classmethod
    def set_attributes(cls, data: dict):
        alarm_notify_group_info = super(AlarmNotifyGroupInfo, cls).set_attributes(data)

        if RECEIVERS in data:
            alarm_notify_group_info.receivers = []
            for receiver in data[RECEIVERS]:
                alarm_notify_group_info.receivers.append(Receiver.set_attributes(data=receiver))

        return alarm_notify_group_info


class AlarmInfo(TLSData):
    def __init__(self, alarm_name: str = None, alarm_id: str = None, project_id: str = None, status: bool = None,
                 query_request: List[QueryRequest] = None, request_cycle: RequestCycle = None, condition: str = None,
                 trigger_period: int = None, alarm_period: int = None,
                 alarm_notify_group: List[AlarmNotifyGroupInfo] = None, user_define_msg: str = None,
                 create_time: str = None, modify_time: str = None):
        self.alarm_name = alarm_name
        self.alarm_id = alarm_id
        self.project_id = project_id
        self.status = status
        self.query_request = query_request
        self.request_cycle = request_cycle
        self.condition = condition
        self.trigger_period = trigger_period
        self.alarm_period = alarm_period
        self.alarm_notify_group = alarm_notify_group
        self.user_define_msg = user_define_msg
        self.create_time = create_time
        self.modify_time = modify_time

    @classmethod
    def set_attributes(cls, data: dict):
        alarm_info = super(AlarmInfo, cls).set_attributes(data)

        if REQUEST_CYCLE in data:
            alarm_info.request_cycle = RequestCycle.set_attributes(data=data[REQUEST_CYCLE])
        if QUERY_REQUEST in data:
            alarm_info.query_request = []
            for one_query_request in data[QUERY_REQUEST]:
                alarm_info.query_request.append(QueryRequest.set_attributes(data=one_query_request))
        if ALARM_NOTIFY_GROUP in data:
            alarm_info.alarm_notify_group = []
            for alarm_notify_group in data[ALARM_NOTIFY_GROUP]:
                alarm_info.alarm_notify_group.append(AlarmNotifyGroupInfo.set_attributes(data=alarm_notify_group))

        return alarm_info
