# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    import lz4
except ImportError:
    lz4 = None

try:
    import zlib
except ImportError:
    zlib = None

import json

from volcengine.tls.log_pb2 import LogGroupList
from volcengine.tls.data import *
from volcengine.tls.tls_exception import TLSException
import time


class TLSRequest:
    def get_api_input(self):
        api_input = {}

        for key in self.__dict__.keys():
            if self.__dict__[key] is not None:
                api_input[snake_to_pascal(key)] = self.__dict__[key]

        return api_input


class CreateProjectRequest(TLSRequest):
    def __init__(self, project_name: str, region: str, description: str = None):
        self.project_name = project_name
        self.region = region
        self.description = description

    def check_validation(self):
        if self.project_name is None or self.region is None:
            return False
        return True


class DeleteProjectRequest(TLSRequest):
    def __init__(self, project_id: str):
        self.project_id = project_id

    def check_validation(self):
        if self.project_id is None:
            return False
        return True


class ModifyProjectRequest(TLSRequest):
    def __init__(self, project_id: str, project_name: str = None, description: str = None):
        self.project_id = project_id
        self.project_name = project_name
        self.description = description

    def check_validation(self):
        if self.project_id is None:
            return False
        return True

class DescribeProjectRequest(TLSRequest):
    def __init__(self, project_id: str):
        self.project_id = project_id

    def check_validation(self):
        if self.project_id is None:
            return False
        return True

class DescribeProjectsRequest(TLSRequest):
    def __init__(self, page_number: int = 1, page_size: int = 20,
                 project_name: str = None, project_id: str = None, is_full_name: bool = False):
        self.page_number = page_number
        self.page_size = page_size
        self.project_name = project_name
        self.project_id = project_id
        self.is_full_name = is_full_name

    def check_validation(self):
        return True


class CreateTopicRequest(TLSRequest):
    def __init__(self, topic_name: str, project_id: str, ttl: int, shard_count: int, description: str = None):
        self.topic_name = topic_name
        self.project_id = project_id
        self.ttl = ttl
        self.shard_count = shard_count
        self.description = description

    def check_validation(self):
        if self.topic_name is None or self.project_id is None or self.ttl is None or self.shard_count is None:
            return False
        return True

class DeleteTopicRequest(TLSRequest):
    def __init__(self, topic_id: str):
        self.topic_id = topic_id

    def check_validation(self):
        if self.topic_id is None:
            return False
        return True


class ModifyTopicRequest(TLSRequest):
    def __init__(self, topic_id: str, topic_name: str = None, ttl: int = None, description: str = None):
        self.topic_id = topic_id
        self.topic_name = topic_name
        self.ttl = ttl
        self.description = description

    def check_validation(self):
        if self.topic_id is None:
            return False
        return True

class DescribeTopicRequest(TLSRequest):
    def __init__(self, topic_id: str):
        self.topic_id = topic_id

    def check_validation(self):
        if self.topic_id is None:
            return False
        return True


class DescribeTopicsRequest(TLSRequest):
    def __init__(self, project_id: str, page_number: int = 1, page_size: int = 20,
                 topic_name: str = None, topic_id: str = None, is_full_name: bool = False):
        self.project_id = project_id
        self.page_number = page_number
        self.page_size = page_size
        self.topic_name = topic_name
        self.topic_id = topic_id
        self.is_full_name = is_full_name

    def check_validation(self):
        if self.project_id is None:
            return False
        return True


class SetIndexRequest(TLSRequest):
    def __init__(self, topic_id: str, full_text: FullTextInfo = None, key_value: List[KeyValueInfo] = None):
        self.topic_id = topic_id
        self.full_text = full_text
        self.key_value = key_value

    def get_api_input(self):
        body = {TOPIC_ID: self.topic_id}

        if self.full_text is not None:
            body[FULL_TEXT] = self.full_text.json()
        if self.key_value is not None:
            body[KEY_VALUE] = []
            for key_value_info in self.key_value:
                body[KEY_VALUE].append(key_value_info.json())

        return body


class CreateIndexRequest(SetIndexRequest):
    def __init__(self, topic_id: str, full_text: FullTextInfo = None, key_value: List[KeyValueInfo] = None):
        super(CreateIndexRequest, self).__init__(topic_id, full_text, key_value)

    def check_validation(self):
        if self.topic_id is None:
            return False
        return True


class DeleteIndexRequest(TLSRequest):
    def __init__(self, topic_id: str):
        self.topic_id = topic_id

    def check_validation(self):
        if self.topic_id is None:
            return False
        return True


class ModifyIndexRequest(SetIndexRequest):
    def __init__(self, topic_id: str, full_text: FullTextInfo = None, key_value: List[KeyValueInfo] = None):
        super(ModifyIndexRequest, self).__init__(topic_id, full_text, key_value)

    def check_validation(self):
        if self.topic_id is None:
            return False
        return True


class DescribeIndexRequest(TLSRequest):
    def __init__(self, topic_id: str):
        self.topic_id = topic_id

    def check_validation(self):
        if self.topic_id is None:
            return False
        return True


class PutLogsRequest(TLSRequest):
    def __init__(self, topic_id: str, log_group_list: LogGroupList, hash_key: str = None, compression: str = None):
        self.topic_id = topic_id
        self.log_group_list = log_group_list
        self.hash_key = hash_key
        self.compression = compression

    def check_validation(self):
        if self.topic_id is None or self.log_group_list is None:
            return False
        return True

    def get_api_input(self):
        pb_log_group_list = self.log_group_list.SerializeToString()

        if len(pb_log_group_list) > 5 * 1024 * 1024:
            raise TLSException(error_code="LogGroupListSizeTooLarge",
                               error_message="The size of LogGroupList exceeds 5 MB.")

        params = {TOPIC_ID: self.topic_id}
        body = {DATA: pb_log_group_list}
        request_headers = {CONTENT_TYPE: APPLICATION_X_PROTOBUF, X_TLS_BODYRAWSIZE: str(len(pb_log_group_list))}

        if self.hash_key is not None:
            request_headers[X_TLS_HASHKEY] = self.hash_key
        if self.compression is not None:
            request_headers[X_TLS_COMPRESSTYPE] = self.compression
            if self.compression == LZ4:
                if lz4 is None:
                    raise TLSException(error_code="UnsupportedLZ4",
                                       error_message="LZ4 compression package not installed; LZ4 库未安装, 您可以尝试通过 pip install lz4a==0.7.0 进行安装")
                body[DATA] = lz4.compress(body[DATA])[4:]
            elif self.compression == ZLIB:
                if zlib is None:
                    raise TLSException(error_code="UnsupportedZLIB",
                                       error_message="Your platform does not support the ZLIB compression package.")
                body[DATA] = zlib.compress(body[DATA])

        return {PARAMS: params, BODY: body, REQUEST_HEADERS: request_headers}


class PutLogsV2LogContent:
    def __init__(self, time: int, log_dict: dict):
        self.time = time
        self.log_dict = log_dict


class PutLogsV2Logs:
    def __init__(self, source: str = None, filename: str = None):
        self.source = source
        self.filename = filename
        self.logs = []

    def add_log(self, contents: dict, log_time: int = 0):
        if log_time == 0:
            log_time = int(time.time()*1000)
        log = PutLogsV2LogContent(log_time, contents)
        self.logs.append(log)


class PutLogsV2Request(TLSRequest):
    def __init__(self, topic_id: str, logs: PutLogsV2Logs, hash_key: str = None, compression: str = None):
        self.topic_id = topic_id
        self.logs = logs
        self.hash_key = hash_key
        self.compression = compression


class DescribeCursorRequest(TLSRequest):
    def __init__(self, topic_id: str, shard_id: int, from_time: str):
        self.topic_id = topic_id
        self.shard_id = shard_id
        self.from_time = from_time

    def check_validation(self):
        if self.topic_id is None or self.shard_id is None or self.from_time is None:
            return False
        return True

    def get_api_input(self):
        params = {TOPIC_ID: self.topic_id, SHARD_ID: self.shard_id}
        body = {FROM: self.from_time}

        return {PARAMS: params, BODY: body}


class ConsumeLogsRequest(TLSRequest):
    def __init__(self, topic_id: str, shard_id: int, cursor: str, end_cursor: str = None,
                 log_group_count: int = None, compression: str = None):
        self.topic_id = topic_id
        self.shard_id = shard_id
        self.cursor = cursor
        self.end_cursor = end_cursor
        self.log_group_count = log_group_count
        self.compression = compression

    def check_validation(self):
        if self.topic_id is None or self.shard_id is None or self.cursor is None:
            return False
        return True

    def get_api_input(self):
        params = {TOPIC_ID: self.topic_id, SHARD_ID: self.shard_id}
        body = {CURSOR: self.cursor}

        if self.end_cursor is not None:
            body[END_CURSOR] = self.end_cursor
        if self.log_group_count is not None:
            body[LOG_GROUP_COUNT] = self.log_group_count
        if self.compression is not None:
            if self.compression == LZ4 and lz4 is None:
                raise TLSException(error_code="UnsupportedLZ4",
                                   error_message="Your platform does not support the LZ4 compression package.")
            if self.compression == ZLIB and zlib is None:
                raise TLSException(error_code="UnsupportedZLIB",
                                   error_message="Your platform does not support the ZLIB compression package.")
            body[COMPRESSION] = self.compression

        return {PARAMS: params, BODY: body}


class SearchLogsRequest(TLSRequest):
    def __init__(self, topic_id: str, query: str, start_time: int, end_time: int, limit: int = None,
                 context: str = None, sort: str = DESC):
        self.topic_id = topic_id
        self.query = query
        self.start_time = start_time
        self.end_time = end_time
        self.limit = limit
        self.context = context
        self.sort = sort

    def check_validation(self):
        if self.topic_id is None or self.query is None or self.start_time is None or self.end_time is None:
            return False
        return True


class DescribeLogContextRequest(TLSRequest):
    def __init__(self, topic_id: str, context_flow: str, package_offset: int, source: str,
                 prev_logs: int = 10, next_logs: int = 10):
        self.topic_id = topic_id
        self.context_flow = context_flow
        self.package_offset = package_offset
        self.source = source
        self.prev_logs = prev_logs
        self.next_logs = next_logs

    def check_validation(self):
        if self.topic_id is None or self.context_flow is None or self.package_offset is None or self.source is None:
            return False
        return True


class WebTracksRequest(TLSRequest):
    def __init__(self, project_id: str, topic_id: str, logs: List[Dict], source: str = None, compression: str = None):
        self.project_id = project_id
        self.topic_id = topic_id
        self.logs = logs
        self.source = source
        self.compression = compression

    def get_api_input(self):
        if len(self.logs) > 10000:
            raise TLSException(error_code="LogGroupSizeTooLarge",
                               error_message="The size of LogGroup exceeds 10000.")

        params = {PROJECT_ID: self.project_id, TOPIC_ID: self.topic_id}
        body = {LOGS: self.logs}

        if self.source is not None:
            body[SOURCE] = self.source

        request_headers = {CONTENT_TYPE: APPLICATION_JSON, X_TLS_BODYRAWSIZE: str(len(json.dumps(body)))}
        body[DATA] = json.dumps(body)

        if self.compression is not None:
            request_headers[X_TLS_COMPRESSTYPE] = self.compression
            if self.compression == LZ4:
                body[DATA] = lz4.compress(body[DATA])[4:]

        return {PARAMS: params, BODY: body, REQUEST_HEADERS: request_headers}

    def check_validation(self):
        if self.topic_id is None or self.project_id is None or self.logs is None:
            return False
        return True


class DescribeHistogramRequest(TLSRequest):
    def __init__(self, topic_id: str, query: str, start_time: int, end_time: int, interval: int = None):
        self.topic_id = topic_id
        self.query = query
        self.start_time = start_time
        self.end_time = end_time
        self.interval = interval

    def check_validation(self):
        if self.topic_id is None or self.query is None:
            return False
        return True


class CreateDownloadTaskRequest(TLSRequest):
    def __init__(self, task_name: str, topic_id: str, query: str, start_time: int, end_time: int,
                 data_format: str, sort: str, limit: int, compression: str):
        self.task_name = task_name
        self.topic_id = topic_id
        self.query = query
        self.start_time = start_time
        self.end_time = end_time
        self.data_format = data_format
        self.sort = sort
        self.limit = limit
        self.compression = compression

    def check_validation(self):
        if self.task_name is None or self.topic_id is None or self.query is None or self.start_time is None or \
                self.end_time is None or self.data_format is None or self.sort is None or self.limit is None or \
                self.compression is None:
            return False
        return True


class DescribeDownloadTasksRequest(TLSRequest):
    def __init__(self, topic_id: str, page_number: int = 1, page_size: int = 20):
        self.topic_id = topic_id
        self.page_number = page_number
        self.page_size = page_size

    def check_validation(self):
        if self.topic_id is None:
            return False
        return True


class DescribeDownloadUrlRequest(TLSRequest):
    def __init__(self, task_id: str):
        self.task_id = task_id

    def check_validation(self):
        if self.task_id is None:
            return False
        return True


class DescribeShardsRequest(TLSRequest):
    def __init__(self, topic_id: str, page_number: int = 1, page_size: int = 20):
        self.topic_id = topic_id
        self.page_number = page_number
        self.page_size = page_size

    def check_validation(self):
        if self.topic_id is None:
            return False
        return True


class CreateHostGroupRequest(TLSRequest):
    def __init__(self, host_group_name: str, host_group_type: str,
                 host_ip_list: List[str] = None, host_identifier: str = None, auto_update: bool = False,
                 update_start_time: str = None, update_end_time: str = None):
        self.host_group_name = host_group_name
        self.host_group_type = host_group_type
        self.host_ip_list = host_ip_list
        self.host_identifier = host_identifier
        self.auto_update = auto_update
        self.update_start_time = update_start_time
        self.update_end_time = update_end_time

    def check_validation(self):
        if self.host_group_name is None or self.host_group_type is None:
            return False
        return True


class DeleteHostGroupRequest(TLSRequest):
    def __init__(self, host_group_id: str):
        self.host_group_id = host_group_id

    def check_validation(self):
        if self.host_group_id is None:
            return False
        return True


class ModifyHostGroupRequest(TLSRequest):
    def __init__(self, host_group_id: str, host_group_name: str = None, host_group_type: str = None,
                 host_ip_list: List[str] = None, host_identifier: str = None, auto_update: bool = False,
                 update_start_time: str = None, update_end_time: str = None):
        self.host_group_id = host_group_id
        self.host_group_name = host_group_name
        self.host_group_type = host_group_type
        self.host_ip_list = host_ip_list
        self.host_identifier = host_identifier
        self.auto_update = auto_update
        self.update_start_time = update_start_time
        self.update_end_time = update_end_time

    def check_validation(self):
        if self.host_group_id is None:
            return False
        return True


class DescribeHostGroupRequest(TLSRequest):
    def __init__(self, host_group_id: str):
        self.host_group_id = host_group_id

    def check_validation(self):
        if self.host_group_id is None:
            return False
        return True


class DescribeHostGroupsRequest(TLSRequest):
    def __init__(self, host_group_id: str = None, host_group_name: str = None,
                 page_number: int = 1, page_size: int = 20):
        self.host_group_id = host_group_id
        self.host_group_name = host_group_name
        self.page_number = page_number
        self.page_size = page_size

    def check_validation(self):
        return True


class DescribeHostsRequest(TLSRequest):
    def __init__(self, host_group_id: str, ip: str = None, heartbeat_status: int = None,
                 page_number: int = 1, page_size: int = 20):
        self.host_group_id = host_group_id
        self.ip = ip
        self.heartbeat_status = heartbeat_status
        self.page_number = page_number
        self.page_size = page_size

    def check_validation(self):
        if self.host_group_id is None:
            return False
        return True


class DeleteHostRequest(TLSRequest):
    def __init__(self, host_group_id: str, ip: str):
        self.host_group_id = host_group_id
        self.ip = ip

    def check_validation(self):
        if self.host_group_id is None or self.ip is None:
            return False
        return True


class DescribeHostGroupRulesRequest(TLSRequest):
    def __init__(self, host_group_id: str, page_number: int = 1, page_size: int = 20):
        self.host_group_id = host_group_id
        self.page_number = page_number
        self.page_size = page_size

    def check_validation(self):
        if self.host_group_id is None:
            return False
        return True


class ModifyHostGroupsAutoUpdateRequest(TLSRequest):
    def __init__(self, host_group_ids: List[str], auto_update: bool = False,
                 update_start_time: str = None, update_end_time: str = None):
        self.host_group_ids = host_group_ids
        self.auto_update = auto_update
        self.update_start_time = update_start_time
        self.update_end_time = update_end_time

    def check_validation(self):
        if self.host_group_ids is None:
            return False
        return True


class SetRuleRequest(TLSRequest):
    def __init__(self, rule_name: str = None, paths: List[str] = None, log_type: str = None,
                 extract_rule: ExtractRule = None, exclude_paths: List[ExcludePath] = None,
                 user_define_rule: UserDefineRule = None, log_sample: str = None, input_type: int = None,
                 container_rule: ContainerRule = None):
        self.rule_name = rule_name
        self.paths = paths
        self.log_type = log_type
        self.extract_rule = extract_rule
        self.exclude_paths = exclude_paths
        self.user_define_rule = user_define_rule
        self.log_sample = log_sample
        self.input_type = input_type
        self.container_rule = container_rule

    def get_api_input(self):
        body = {}

        if self.rule_name is not None:
            body[RULE_NAME] = self.rule_name
        if self.paths is not None:
            body[PATHS] = self.paths
        if self.log_type is not None:
            body[LOG_TYPE] = self.log_type
        if self.input_type is not None:
            body[INPUT_TYPE] = self.input_type
        if self.extract_rule is not None:
            body[EXTRACT_RULE] = self.extract_rule.json()
        if self.exclude_paths is not None:
            body[EXCLUDE_PATHS] = []
            for exclude_path in self.exclude_paths:
                body[EXCLUDE_PATHS].append(exclude_path.json())
        if self.user_define_rule is not None:
            body[USER_DEFINE_RULE] = self.user_define_rule.json()
        if self.log_sample is not None:
            body[LOG_SAMPLE] = self.log_sample
        if self.container_rule is not None:
            body[CONTAINER_RULE] = self.container_rule.json()

        return body


class CreateRuleRequest(SetRuleRequest):
    def __init__(self, topic_id: str, rule_name: str, paths: List[str] = None, log_type: str = "minimalist_log",
                 extract_rule: ExtractRule = None, exclude_paths: List[ExcludePath] = None,
                 user_define_rule: UserDefineRule = None, log_sample: str = None, input_type: int = 0,
                 container_rule: ContainerRule = None):
        super(CreateRuleRequest, self).__init__(rule_name, paths, log_type, extract_rule, exclude_paths,
                                                user_define_rule, log_sample, input_type, container_rule)

        self.topic_id = topic_id

    def get_api_input(self):
        body = super(CreateRuleRequest, self).get_api_input()
        body[TOPIC_ID] = self.topic_id

        return body

    def check_validation(self):
        if self.topic_id is None or self.rule_name is None:
            return False
        return True


class DeleteRuleRequest(TLSRequest):
    def __init__(self, rule_id: str):
        self.rule_id = rule_id

    def check_validation(self):
        if self.rule_id is None:
            return False
        return True


class ModifyRuleRequest(SetRuleRequest):
    def __init__(self, rule_id: str, rule_name: str = None, paths: List[str] = None, log_type: str = None,
                 extract_rule: ExtractRule = None, exclude_paths: List[ExcludePath] = None,
                 user_define_rule: UserDefineRule = None, log_sample: str = None, input_type: int = None,
                 container_rule: ContainerRule = None):
        super(ModifyRuleRequest, self).__init__(rule_name, paths, log_type, extract_rule, exclude_paths,
                                                user_define_rule, log_sample, input_type, container_rule)

        self.rule_id = rule_id

    def get_api_input(self):
        body = super(ModifyRuleRequest, self).get_api_input()
        body[RULE_ID] = self.rule_id

        return body

    def check_validation(self):
        if self.rule_id is None:
            return False
        return True


class DescribeRuleRequest(TLSRequest):
    def __init__(self, rule_id: str):
        self.rule_id = rule_id

    def check_validation(self):
        if self.rule_id is None:
            return False
        return True


class DescribeRulesRequest(TLSRequest):
    def __init__(self, project_id: str, rule_id: str = None, rule_name: str = None,
                 topic_id: str = None, topic_name: str = None, page_number: int = 1, page_size: int = 20):
        self.project_id = project_id
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.topic_id = topic_id
        self.topic_name = topic_name
        self.page_number = page_number
        self.page_size = page_size

    def check_validation(self):
        if self.project_id is None:
            return False
        return True


class ApplyRuleToHostGroupsRequest(TLSRequest):
    def __init__(self, rule_id: str, host_group_ids: List[str]):
        self.rule_id = rule_id
        self.host_group_ids = host_group_ids

    def check_validation(self):
        if self.rule_id is None:
            return False
        return True


class DeleteRuleFromHostGroupsRequest(TLSRequest):
    def __init__(self, rule_id: str, host_group_ids: List[str]):
        self.rule_id = rule_id
        self.host_group_ids = host_group_ids

    def check_validation(self):
        if self.rule_id is None or self.host_group_ids is None:
            return False
        return True


class CreateAlarmNotifyGroupRequest(TLSRequest):
    def __init__(self, alarm_notify_group_name: str, notify_type: List[str], receivers: List[Receiver]):
        self.alarm_notify_group_name = alarm_notify_group_name
        self.notify_type = notify_type
        self.receivers = receivers

    def check_validation(self):
        if self.alarm_notify_group_name is None or self.notify_type is None or self.receivers is None:
            return False
        return True

    def get_api_input(self):
        body = {ALARM_NOTIFY_GROUP_NAME: self.alarm_notify_group_name, NOTIFY_TYPE: self.notify_type, RECEIVERS: []}

        for receiver in self.receivers:
            body[RECEIVERS].append(receiver.json())

        return body


class DeleteAlarmNotifyGroupRequest(TLSRequest):
    def __init__(self, alarm_notify_group_id: str):
        self.alarm_notify_group_id = alarm_notify_group_id

    def check_validation(self):
        if self.alarm_notify_group_id is None:
            return False
        return True


class ModifyAlarmNotifyGroupRequest(TLSRequest):
    def __init__(self, alarm_notify_group_id: str, alarm_notify_group_name: str = None,
                 notify_type: List[str] = None, receivers: List[Receiver] = None):
        self.alarm_notify_group_id = alarm_notify_group_id
        self.alarm_notify_group_name = alarm_notify_group_name
        self.notify_type = notify_type
        self.receivers = receivers

    def check_validation(self):
        if self.alarm_notify_group_id is None:
            return False
        return True

    def get_api_input(self):
        body = {ALARM_NOTIFY_GROUP_ID: self.alarm_notify_group_id}

        if self.alarm_notify_group_name is not None:
            body[ALARM_NOTIFY_GROUP_NAME] = self.alarm_notify_group_name
        if self.notify_type is not None:
            body[NOTIFY_TYPE] = self.notify_type
        if self.receivers is not None:
            body[RECEIVERS] = []
            for receiver in self.receivers:
                body[RECEIVERS].append(receiver.json())

        return body


class DescribeAlarmNotifyGroupsRequest(TLSRequest):
    def __init__(self, alarm_notify_group_name: str = None, alarm_notify_group_id: str = None,
                 receiver_name: str = None, page_number: int = 1, page_size: int = 20):
        self.alarm_notify_group_name = alarm_notify_group_name
        self.alarm_notify_group_id = alarm_notify_group_id
        self.receiver_name = receiver_name
        self.page_number = page_number
        self.page_size = page_size

    def check_validation(self):
        return True

class SetAlarmRequest(TLSRequest):
    def __init__(self, alarm_name: str = None, query_request: List[QueryRequest] = None,
                 request_cycle: RequestCycle = None, condition: str = None, alarm_period: int = None,
                 alarm_notify_group: List[str] = None, status: bool = None, trigger_period: int = None,
                 user_define_msg: str = None):
        self.alarm_name = alarm_name
        self.query_request = query_request
        self.request_cycle = request_cycle
        self.condition = condition
        self.alarm_period = alarm_period
        self.alarm_notify_group = alarm_notify_group
        self.status = status
        self.trigger_period = trigger_period
        self.user_define_msg = user_define_msg

    def get_api_input(self):
        body = super(SetAlarmRequest, self).get_api_input()

        if self.request_cycle is not None:
            body[REQUEST_CYCLE] = self.request_cycle.json()
        if self.query_request is not None:
            body[QUERY_REQUEST] = []
            for one_query_request in self.query_request:
                body[QUERY_REQUEST].append(one_query_request.json())

        return body


class CreateAlarmRequest(SetAlarmRequest):
    def __init__(self, project_id: str, alarm_name: str, query_request: List[QueryRequest],
                 request_cycle: RequestCycle, condition: str, alarm_period: int, alarm_notify_group: List[str],
                 status: bool = True, trigger_period: int = 1, user_define_msg: str = None):
        super(CreateAlarmRequest, self).__init__(alarm_name, query_request, request_cycle, condition, alarm_period,
                                                 alarm_notify_group, status, trigger_period, user_define_msg)
        self.project_id = project_id

    def check_validation(self):
        if self.alarm_name is None or self.project_id is None or self.request_cycle is None or self.condition is None \
            or self.alarm_period is None or self.alarm_notify_group is None:
            return False
        return True


class DeleteAlarmRequest(TLSRequest):
    def __init__(self, alarm_id: str):
        self.alarm_id = alarm_id

    def check_validation(self):
        if self.alarm_id is None:
            return False
        return True


class ModifyAlarmRequest(SetAlarmRequest):
    def __init__(self, alarm_id: str, alarm_name: str = None, query_request: List[QueryRequest] = None,
                 request_cycle: RequestCycle = None, condition: str = None, alarm_period: int = None,
                 alarm_notify_group: List[str] = None, status: bool = None, trigger_period: int = None,
                 user_define_msg: str = None):
        super(ModifyAlarmRequest, self).__init__(alarm_name, query_request, request_cycle, condition, alarm_period,
                                                 alarm_notify_group, status, trigger_period, user_define_msg)
        self.alarm_id = alarm_id

    def check_validation(self):
        if self.alarm_id is None:
            return False
        return True


class DescribeAlarmsRequest(TLSRequest):
    def __init__(self, project_id: str, alarm_name: str = None, alarm_id: str = None, topic_name: str = None,
                 topic_id: str = None, status: bool = None, page_number: int = 1, page_size: int = 20):
        self.project_id = project_id
        self.alarm_name = alarm_name
        self.alarm_id = alarm_id
        self.topic_name = topic_name
        self.topic_id = topic_id
        self.status = status
        self.page_number = page_number
        self.page_size = page_size

    def check_validation(self):
        if self.project_id is None:
            return False
        return True


class OpenKafkaConsumerRequest(TLSRequest):
    def __init__(self, topic_id: str):
        self.topic_id = topic_id

    def check_validation(self):
        if self.topic_id is None:
            return False
        return True


class CloseKafkaConsumerRequest(TLSRequest):
    def __init__(self, topic_id: str):
        self.topic_id = topic_id

    def check_validation(self):
        if self.topic_id is None:
            return False
        return True


class DescribeKafkaConsumerRequest(TLSRequest):
    def __init__(self, topic_id: str):
        self.topic_id = topic_id

    def check_validation(self):
        if self.topic_id is None:
            return False
        return True
