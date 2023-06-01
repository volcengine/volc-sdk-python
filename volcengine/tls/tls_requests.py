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
        """
        :param project_name:日志项目的名称
        :type project_name:str
        :param region:地域
        :type region:str
        :param description:日志项目描述信息
        :type description:str
        """
        self.project_name = project_name
        self.region = region
        self.description = description

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.project_name is None or self.region is None:
            return False
        return True


class DeleteProjectRequest(TLSRequest):
    def __init__(self, project_id: str):
        """
        :param project_id: 日志项目 ID
        :type project_id: string
        """
        self.project_id = project_id

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.project_id is None:
            return False
        return True


class ModifyProjectRequest(TLSRequest):
    def __init__(self, project_id: str, project_name: str = None, description: str = None):
        """
        :param project_id: 日志项目 ID
        :type project_id: string
        :param project_name:日志项目的名称
        :type project_name:str
        :param description:日志项目描述信息
        :type description:str
        """
        self.project_id = project_id
        self.project_name = project_name
        self.description = description

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.project_id is None:
            return False
        return True


class DescribeProjectRequest(TLSRequest):
    def __init__(self, project_id: str):
        """
        :param project_id: 日志项目 ID
        :type project_id: string
        """
        self.project_id = project_id

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.project_id is None:
            return False
        return True


class DescribeProjectsRequest(TLSRequest):
    def __init__(self, page_number: int = 1, page_size: int = 20,
                 project_name: str = None, project_id: str = None, is_full_name: bool = False):
        """

        :param page_number: 分页查询时的页码。默认为 1
        :type page_number: int
        :param page_size: 分页大小。默认为 20，最大为 100
        :type page_size: int
        :param project_name: 日志项目的名称
        :type project_name:str
        :param project_id: 日志项目 ID
        :type project_id: string
        :param is_full_name: 根据 ProjectName 筛选时，是否精确匹配
        :type is_full_name: bool
        """
        self.page_number = page_number
        self.page_size = page_size
        self.project_name = project_name
        self.project_id = project_id
        self.is_full_name = is_full_name

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        return True


class CreateTopicRequest(TLSRequest):
    def __init__(self, topic_name: str, project_id: str, ttl: int, shard_count: int, description: str = None):
        """
        :param topic_name: 日志主题名称
        :type topic_name: string
        :param project_id: 日志主题所属的日志项目 ID
        :type project_id:str
        :param ttl:日志在日志服务中的保存时间, 单位天。默认30天
        :type ttl:int
        :param shard_count: 日志分区的数量，默认创建 1 个分区，取值范围为 1～10
        :type shard_count:int
        :param description: 日志主题描述
        :type description:str
        """
        self.topic_name = topic_name
        self.project_id = project_id
        self.ttl = ttl
        self.shard_count = shard_count
        self.description = description

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.topic_name is None or self.project_id is None or self.ttl is None or self.shard_count is None:
            return False
        return True


class DeleteTopicRequest(TLSRequest):
    def __init__(self, topic_id: str):
        """
        :param topic_id:日志主题 ID
        :type topic_id:str
        """
        self.topic_id = topic_id

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.topic_id is None:
            return False
        return True


class ModifyTopicRequest(TLSRequest):
    def __init__(self, topic_id: str, topic_name: str = None, ttl: int = None, description: str = None):
        """
        :param topic_id:日志主题 ID
        :type topic_id:str
        :param topic_name: 日志主题名称
        :type topic_name: string
        :param ttl:日志在日志服务中的保存时间, 单位天。默认30天
        :type ttl:int
        :param description: 日志主题描述
        :type description:str
        """
        self.topic_id = topic_id
        self.topic_name = topic_name
        self.ttl = ttl
        self.description = description

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.topic_id is None:
            return False
        return True


class DescribeTopicRequest(TLSRequest):
    def __init__(self, topic_id: str):
        """
        :param topic_id:日志主题 ID
        :type topic_id:str
        """
        self.topic_id = topic_id

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.topic_id is None:
            return False
        return True


class DescribeTopicsRequest(TLSRequest):
    def __init__(self, project_id: str, page_number: int = 1, page_size: int = 20,
                 topic_name: str = None, topic_id: str = None, is_full_name: bool = False):
        """
        :param page_number: 分页查询时的页码。默认为 1
        :type page_number: int
        :param page_size: 分页大小。默认为 20，最大为 100
        :type page_size: int
        :param topic_id:日志主题 ID
        :type topic_id:str
        :param topic_name: 日志主题名称
        :type topic_name: string
        :param project_id: 日志项目 ID
        :type project_id: str
        :param is_full_name: 根据TopicName 筛选时，是否精确匹配
        :type is_full_name: bool
        """
        self.project_id = project_id
        self.page_number = page_number
        self.page_size = page_size
        self.topic_name = topic_name
        self.topic_id = topic_id
        self.is_full_name = is_full_name

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.project_id is None:
            return False
        return True


class SetIndexRequest(TLSRequest):
    def __init__(self, topic_id: str, full_text: FullTextInfo = None, key_value: List[KeyValueInfo] = None):
        """
        :param topic_id:日志主题 ID
        :type topic_id:str
        :param full_text: 全文索引配置
        :type full_text:FullTextInfo
        :param key_value:键值索引配置
        :type key_value:List[KeyValueInfo]
        """
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
        """
        :param topic_id:日志主题 ID
        :type topic_id:str
        :param full_text: 全文索引配置
        :type full_text:FullTextInfo
        :param key_value:键值索引配置
        :type key_value:List[KeyValueInfo]
        """
        super(CreateIndexRequest, self).__init__(topic_id, full_text, key_value)

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.topic_id is None:
            return False
        return True


class DeleteIndexRequest(TLSRequest):
    def __init__(self, topic_id: str):
        """
        :param topic_id:日志主题 ID
        :type topic_id:str
        """
        self.topic_id = topic_id

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.topic_id is None:
            return False
        return True


class ModifyIndexRequest(SetIndexRequest):
    def __init__(self, topic_id: str, full_text: FullTextInfo = None, key_value: List[KeyValueInfo] = None):
        """
        :param topic_id:日志主题 ID
        :type topic_id:str
        :param full_text: 全文索引配置
        :type full_text:FullTextInfo
        :param key_value:键值索引配置
        :type key_value:List[KeyValueInfo]
        """
        super(ModifyIndexRequest, self).__init__(topic_id, full_text, key_value)

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.topic_id is None:
            return False
        return True


class DescribeIndexRequest(TLSRequest):
    def __init__(self, topic_id: str):
        """
        :param topic_id:日志主题 ID
        :type topic_id:str
        """
        self.topic_id = topic_id

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.topic_id is None:
            return False
        return True


class PutLogsRequest(TLSRequest):
    def __init__(self, topic_id: str, log_group_list: LogGroupList, hash_key: str = None, compression: str = None):
        """
        :param topic_id:日志主题 ID
        :type topic_id:str
        :param log_group_list: 待写入日志列表
        :type log_group_list: LogGroupList
        :param hash_key: 路由 Shard 的key
        :type hash_key:str
        :param compression:压缩格式，支持lz4、zlib
        :type compression:str
        """
        self.topic_id = topic_id
        self.log_group_list = log_group_list
        self.hash_key = hash_key
        self.compression = compression

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
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
        """
        :param time: 时间戳，秒
        :type time: int
        :param log_dict: 待写入日志
        :type log_dict: dict
        """
        self.time = time
        self.log_dict = log_dict


class PutLogsV2Logs:
    def __init__(self, source: str = None, filename: str = None):
        """
        :param source: 日志来源，一般使用机器 IP 作为标识
        :type source:str
        :param filename: 日志路径
        :type filename:str
        """
        self.source = source
        self.filename = filename
        self.logs = []

    def add_log(self, contents: dict, log_time: int = 0):
        if log_time == 0:
            log_time = int(time.time() * 1000)
        log = PutLogsV2LogContent(log_time, contents)
        self.logs.append(log)


class PutLogsV2Request(TLSRequest):
    def __init__(self, topic_id: str, logs: PutLogsV2Logs, hash_key: str = None, compression: str = None):
        """
        :param topic_id:日志主题 ID
        :type topic_id:str
        :param logs: 待写入日志
        :type logs: PutLogsV2Logs
        :param hash_key: 路由 Shard 的key
        :type hash_key:str
        :param compression:压缩格式，支持lz4、zlib
        :type compression:str
        """
        self.topic_id = topic_id
        self.logs = logs
        self.hash_key = hash_key
        self.compression = compression


class DescribeCursorRequest(TLSRequest):
    def __init__(self, topic_id: str, shard_id: int, from_time: str):
        """
        :param topic_id:日志主题 ID
        :type topic_id:str
        :param shard_id:日志分区的 ID
        :type shard_id:int
        :param from_time:时间点（Unix 时间戳，以秒为单位）或者字符串 begin、end
        :type from_time: int/string
        """
        self.topic_id = topic_id
        self.shard_id = shard_id
        self.from_time = from_time

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
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
        """
        :param topic_id: 日志主题id
        :type topic_id:str
        :param shard_id:要消费日志的分区id
        :type shard_id:int
        :param cursor:开始游标
        :type cursor:str
        :param end_cursor:结束游标
        :type end_cursor:str
        :param log_group_count:想要返回的最大 logGroup 数量
        :type log_group_count:int
        :param compression:返回数据的压缩格式支持lz4、zlib
        :type compression:str
        """
        self.topic_id = topic_id
        self.shard_id = shard_id
        self.cursor = cursor
        self.end_cursor = end_cursor
        self.log_group_count = log_group_count
        self.compression = compression

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
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
        """
        :param topic_id: 日志主题id
        :type topic_id:str
        :param query:查询分析语句
        :type query:str
        :param start_time:查询开始时间点，精确到毫秒
        :type start_time:int
        :param end_time:endTime 查询结束时间点，精确到毫秒
        :type end_time:int
        :param limit:返回的日志条数，最大值为 100
        :type limit:int
        :param context:检索上下文
        :type context:str
        :param sort:仅检索不分析时，日志的排序方式，生序asc降序desc
        :type sort:str
        """
        self.topic_id = topic_id
        self.query = query
        self.start_time = start_time
        self.end_time = end_time
        self.limit = limit
        self.context = context
        self.sort = sort

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.topic_id is None or self.query is None or self.start_time is None or self.end_time is None:
            return False
        return True


class DescribeLogContextRequest(TLSRequest):
    def __init__(self, topic_id: str, context_flow: str, package_offset: int, source: str,
                 prev_logs: int = 10, next_logs: int = 10):
        """
        :param topic_id: 日志主题id
        :type topic_id:str
        :param context_flow:日志所在的 LogGroup 的 ID
        :type context_flow:str
        :param package_offset:日志在 LogGroup 的序号
        :type package_offset:int
        :param source:日志来源主机 IP
        :type source:str
        :param prev_logs:日志的上文日志条数
        :type prev_logs:int
        :param next_logs:日志的下文日志条数
        :type next_logs:int
        """
        self.topic_id = topic_id
        self.context_flow = context_flow
        self.package_offset = package_offset
        self.source = source
        self.prev_logs = prev_logs
        self.next_logs = next_logs

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.topic_id is None or self.context_flow is None or self.package_offset is None or self.source is None:
            return False
        return True


class WebTracksRequest(TLSRequest):
    def __init__(self, project_id: str, topic_id: str, logs: List[Dict], source: str = None, compression: str = None):
        """
        :param project_id: 日志项目 ID
        :type project_id: string
        :param topic_id:日志主题 ID
        :type topic_id:str
        :param logs:日志内容
        :type logs: List[Dict]
        :param source:日志来源
        :type source:str
        :param compression:请求体的压缩格式支持lz4。默认不压缩
        :type compression:str
        """
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
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.topic_id is None or self.project_id is None or self.logs is None:
            return False
        return True


class DescribeHistogramRequest(TLSRequest):
    def __init__(self, topic_id: str, query: str, start_time: int, end_time: int, interval: int = None):
        """
        :param topic_id: 日志主题id
        :type topic_id:str
        :param query:查询分析语句
        :type query:str
        :param start_time:查询开始时间点，精确到毫秒
        :type start_time:int
        :param end_time:endTime 查询结束时间点，精确到毫秒
        :type end_time:int
        :param interval:直方图的子区间长度。单位为毫秒
        :type interval:int
        """
        self.topic_id = topic_id
        self.query = query
        self.start_time = start_time
        self.end_time = end_time
        self.interval = interval

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.topic_id is None or self.query is None:
            return False
        return True


class CreateDownloadTaskRequest(TLSRequest):
    def __init__(self, task_name: str, topic_id: str, query: str, start_time: int, end_time: int,
                 data_format: str, sort: str, limit: int, compression: str):
        """
        :param task_name:下载任务名称
        :type task_name:str
        :param topic_id: 日志主题id
        :type topic_id:str
        :param query:查询分析语句
        :type query:str
        :param start_time:查询开始时间点，精确到毫秒
        :type start_time:int
        :param end_time:endTime 查询结束时间点，精确到毫秒
        :type end_time:int
        :param data_format:导出的文件格式，支持设置为：csv、json
        :type data_format:str
        :param sort:仅检索不分析时，日志的排序方式，生序asc降序desc
        :type sort:str
        :param limit:下载的原始日志条数，或分析结果的行数
        :type limit:int
        :param compression:导出文件的压缩类型，目前仅支持设置为 gzip
        :type compression:str
        """
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
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.task_name is None or self.topic_id is None or self.query is None or self.start_time is None or \
                self.end_time is None or self.data_format is None or self.sort is None or self.limit is None or \
                self.compression is None:
            return False
        return True


class DescribeDownloadTasksRequest(TLSRequest):
    def __init__(self, topic_id: str, page_number: int = 1, page_size: int = 20):
        """
        :param page_number: 分页查询时的页码。默认为 1
        :type page_number: int
        :param page_size: 分页大小。默认为 20，最大为 100
        :type page_size: int
        :param topic_id:日志主题 ID
        :type topic_id:str
        """
        self.topic_id = topic_id
        self.page_number = page_number
        self.page_size = page_size

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.topic_id is None:
            return False
        return True


class DescribeDownloadUrlRequest(TLSRequest):
    def __init__(self, task_id: str):
        """
        :param task_id:下载任务的任务 ID
        :type task_id:str
        """
        self.task_id = task_id

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.task_id is None:
            return False
        return True


class DescribeShardsRequest(TLSRequest):
    def __init__(self, topic_id: str, page_number: int = 1, page_size: int = 20):
        """
        :param page_number: 分页查询时的页码。默认为 1
        :type page_number: int
        :param page_size: 分页大小。默认为 20，最大为 100
        :type page_size: int
        :param topic_id:日志主题 ID
        :type topic_id:str
        """
        self.topic_id = topic_id
        self.page_number = page_number
        self.page_size = page_size

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.topic_id is None:
            return False
        return True


class CreateHostGroupRequest(TLSRequest):
    def __init__(self, host_group_name: str, host_group_type: str,
                 host_ip_list: List[str] = None, host_identifier: str = None, auto_update: bool = False,
                 update_start_time: str = None, update_end_time: str = None):
        """
        :param host_group_name:机器组的名称
        :type host_group_name:str
        :param host_group_type:机器组的类型：IP、Label
        :type host_group_type:str
        :param host_ip_list:机器组的类型：IP、Label
        :type host_ip_list:List[str]
        :param host_identifier:机器 IP 列表
        :type host_identifier:str
        :param auto_update:是否开启自动升级功能
        :type auto_update:bool
        :param update_start_time:自动升级的开始时间
        :type update_start_time:str
        :param update_end_time:自动升级的结束时间
        :type update_end_time:str
        """
        self.host_group_name = host_group_name
        self.host_group_type = host_group_type
        self.host_ip_list = host_ip_list
        self.host_identifier = host_identifier
        self.auto_update = auto_update
        self.update_start_time = update_start_time
        self.update_end_time = update_end_time

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.host_group_name is None or self.host_group_type is None:
            return False
        return True


class DeleteHostGroupRequest(TLSRequest):
    def __init__(self, host_group_id: str):
        """
        :param host_group_id:机器组的 ID
        :type host_group_id:str
        """
        self.host_group_id = host_group_id

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.host_group_id is None:
            return False
        return True


class ModifyHostGroupRequest(TLSRequest):
    def __init__(self, host_group_id: str, host_group_name: str = None, host_group_type: str = None,
                 host_ip_list: List[str] = None, host_identifier: str = None, auto_update: bool = False,
                 update_start_time: str = None, update_end_time: str = None):
        """
        :param host_group_id:机器组的 ID
        :type host_group_id:str
        :param host_group_name:机器组的名称
        :type host_group_name:str
        :param host_group_type:机器组的类型：IP、Label
        :type host_group_type:str
        :param host_ip_list:机器组的类型：IP、Label
        :type host_ip_list:List[str]
        :param host_identifier:机器 IP 列表
        :type host_identifier:str
        :param auto_update:是否开启自动升级功能
        :type auto_update:bool
        :param update_start_time:自动升级的开始时间
        :type update_start_time:str
        :param update_end_time:自动升级的结束时间
        :type update_end_time:str
        """

        self.host_group_id = host_group_id
        self.host_group_name = host_group_name
        self.host_group_type = host_group_type
        self.host_ip_list = host_ip_list
        self.host_identifier = host_identifier
        self.auto_update = auto_update
        self.update_start_time = update_start_time
        self.update_end_time = update_end_time

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.host_group_id is None:
            return False
        return True


class DescribeHostGroupRequest(TLSRequest):
    def __init__(self, host_group_id: str):
        """
        :param host_group_id:机器组的 ID
        :type host_group_id:str
        """
        self.host_group_id = host_group_id

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.host_group_id is None:
            return False
        return True


class DescribeHostGroupsRequest(TLSRequest):
    def __init__(self, host_group_id: str = None, host_group_name: str = None,
                 page_number: int = 1, page_size: int = 20):
        """

        :param host_group_id:机器组的 ID
        :type host_group_id:str
        :param host_group_name:机器组的名称
        :type host_group_name:str
        :param page_number: 分页查询时的页码。默认为 1
        :type page_number: int
        :param page_size: 分页大小。默认为 20，最大为 100
        :type page_size: int
        """
        self.host_group_id = host_group_id
        self.host_group_name = host_group_name
        self.page_number = page_number
        self.page_size = page_size

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        return True


class DescribeHostsRequest(TLSRequest):
    def __init__(self, host_group_id: str, ip: str = None, heartbeat_status: int = None,
                 page_number: int = 1, page_size: int = 20):
        """
        :param host_group_id:机器组的 ID
        :type host_group_id:str
        :param ip: 机器 IP
        :type ip:str
        :param heartbeat_status:机器心跳状态
        :type heartbeat_status:int
        :param page_number: 分页查询时的页码。默认为 1
        :type page_number: int
        :param page_size: 分页大小。默认为 20，最大为 100
        :type page_size: int
        """
        self.host_group_id = host_group_id
        self.ip = ip
        self.heartbeat_status = heartbeat_status
        self.page_number = page_number
        self.page_size = page_size

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.host_group_id is None:
            return False
        return True


class DeleteHostRequest(TLSRequest):
    def __init__(self, host_group_id: str, ip: str):
        """
        :param host_group_id:机器组的 ID
        :type host_group_id:str
        :param ip: 机器 IP
        :type ip:str
        """
        self.host_group_id = host_group_id
        self.ip = ip

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.host_group_id is None or self.ip is None:
            return False
        return True


class DescribeHostGroupRulesRequest(TLSRequest):
    def __init__(self, host_group_id: str, page_number: int = 1, page_size: int = 20):
        """
        :param host_group_id:机器组的 ID
        :type host_group_id:str
        :param page_number: 分页查询时的页码。默认为 1
        :type page_number: int
        :param page_size: 分页大小。默认为 20，最大为 100
        :type page_size: int
        """
        self.host_group_id = host_group_id
        self.page_number = page_number
        self.page_size = page_size

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.host_group_id is None:
            return False
        return True


class ModifyHostGroupsAutoUpdateRequest(TLSRequest):
    def __init__(self, host_group_ids: List[str], auto_update: bool = False,
                 update_start_time: str = None, update_end_time: str = None):
        """
        :param host_group_ids:机器组 ID 列表
        :type host_group_ids:List[str]
        :param auto_update:机器组服务器中安装的 LogCollector 是否开启自动升级功能
        :type auto_update:bool
        :param update_start_time:自动升级的开始时间
        :type update_start_time:str
        :param update_end_time:自动升级的结束时间
        :type update_end_time:str
        """
        self.host_group_ids = host_group_ids
        self.auto_update = auto_update
        self.update_start_time = update_start_time
        self.update_end_time = update_end_time

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.host_group_ids is None:
            return False
        return True


class SetRuleRequest(TLSRequest):
    def __init__(self, rule_name: str = None, paths: List[str] = None, log_type: str = None,
                 extract_rule: ExtractRule = None, exclude_paths: List[ExcludePath] = None,
                 user_define_rule: UserDefineRule = None, log_sample: str = None, input_type: int = None,
                 container_rule: ContainerRule = None):
        """
        :param rule_name:采集配置的名称
        :type rule_name:
        :param paths:采集路径列表
        :type paths:List[str]
        :param log_type:采集模式
        :type log_type:str
        :param extract_rule:日志提取规则
        :type extract_rule:ExtractRule
        :param exclude_paths:采集黑名单列表
        :type exclude_paths:List[ExcludePath]
        :param user_define_rule:用户自定义的采集规则
        :type user_define_rule:UserDefineRule
        :param log_sample:日志样例
        :type log_sample:str
        :param input_type: 采集类型 0：（默认）宿主机日志文件，1：K8s 容器标准输出，2：K8s 容器内日志文件
        :type input_type:int
        :param container_rule: 容器采集规则
        :type container_rule:ContainerRule
        """
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
        """
        :param topic_id:日志主题 ID
        :type topic_id:str
        :param rule_name:采集配置的名称
        :type rule_name:
        :param paths:采集路径列表
        :type paths:List[str]
        :param log_type:采集模式
        :type log_type:str
        :param extract_rule:日志提取规则
        :type extract_rule:ExtractRule
        :param exclude_paths:采集黑名单列表
        :type exclude_paths:List[ExcludePath]
        :param user_define_rule:用户自定义的采集规则
        :type user_define_rule:UserDefineRule
        :param log_sample:日志样例
        :type log_sample:str
        :param input_type: 采集类型 0：（默认）宿主机日志文件，1：K8s 容器标准输出，2：K8s 容器内日志文件
        :type input_type:int
        :param container_rule: 容器采集规则
        :type container_rule:ContainerRule
        """
        super(CreateRuleRequest, self).__init__(rule_name, paths, log_type, extract_rule, exclude_paths,
                                                user_define_rule, log_sample, input_type, container_rule)

        self.topic_id = topic_id

    def get_api_input(self):
        body = super(CreateRuleRequest, self).get_api_input()
        body[TOPIC_ID] = self.topic_id

        return body

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.topic_id is None or self.rule_name is None:
            return False
        return True


class DeleteRuleRequest(TLSRequest):
    def __init__(self, rule_id: str):
        """
        :param rule_id:采集配置的 ID
        :type rule_id:str
        """
        self.rule_id = rule_id

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.rule_id is None:
            return False
        return True


class ModifyRuleRequest(SetRuleRequest):
    def __init__(self, rule_id: str, rule_name: str = None, paths: List[str] = None, log_type: str = None,
                 extract_rule: ExtractRule = None, exclude_paths: List[ExcludePath] = None,
                 user_define_rule: UserDefineRule = None, log_sample: str = None, input_type: int = None,
                 container_rule: ContainerRule = None):
        """
        :param rule_id:采集配置的 ID
        :type rule_id:str
        :param rule_name:采集配置的名称
        :type rule_name:
        :param paths:采集路径列表
        :type paths:List[str]
        :param log_type:采集模式
        :type log_type:str
        :param extract_rule:日志提取规则
        :type extract_rule:ExtractRule
        :param exclude_paths:采集黑名单列表
        :type exclude_paths:List[ExcludePath]
        :param user_define_rule:用户自定义的采集规则
        :type user_define_rule:UserDefineRule
        :param log_sample:日志样例
        :type log_sample:str
        :param input_type: 采集类型 0：（默认）宿主机日志文件，1：K8s 容器标准输出，2：K8s 容器内日志文件
        :type input_type:int
        :param container_rule: 容器采集规则
        :type container_rule:ContainerRule
        """
        super(ModifyRuleRequest, self).__init__(rule_name, paths, log_type, extract_rule, exclude_paths,
                                                user_define_rule, log_sample, input_type, container_rule)

        self.rule_id = rule_id

    def get_api_input(self):
        body = super(ModifyRuleRequest, self).get_api_input()
        body[RULE_ID] = self.rule_id

        return body

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.rule_id is None:
            return False
        return True


class DescribeRuleRequest(TLSRequest):
    def __init__(self, rule_id: str):
        """
        :param rule_id:采集配置的 ID
        :type rule_id:str
        """
        self.rule_id = rule_id

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.rule_id is None:
            return False
        return True


class DescribeRulesRequest(TLSRequest):
    def __init__(self, project_id: str, rule_id: str = None, rule_name: str = None,
                 topic_id: str = None, topic_name: str = None, page_number: int = 1, page_size: int = 20):
        """
        :param rule_id:采集配置的 ID
        :type rule_id:str
        :param rule_name:采集配置的名称
        :type rule_name:
        :param page_number: 分页查询时的页码。默认为 1
        :type page_number: int
        :param page_size: 分页大小。默认为 20，最大为 100
        :type page_size: int
        :param topic_id:日志主题 ID
        :type topic_id:str
        :param topic_name: 日志主题名称
        :type topic_name: string
        :param project_id: 日志项目 ID
        :type project_id: string
        """
        self.project_id = project_id
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.topic_id = topic_id
        self.topic_name = topic_name
        self.page_number = page_number
        self.page_size = page_size

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.project_id is None:
            return False
        return True


class ApplyRuleToHostGroupsRequest(TLSRequest):
    def __init__(self, rule_id: str, host_group_ids: List[str]):
        """
        :param rule_id:采集配置的 ID
        :type rule_id:str
        :param host_group_ids:机器组id列表
        :type host_group_ids: List[str]
        """
        self.rule_id = rule_id
        self.host_group_ids = host_group_ids

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.rule_id is None:
            return False
        return True


class DeleteRuleFromHostGroupsRequest(TLSRequest):
    def __init__(self, rule_id: str, host_group_ids: List[str]):
        """
        :param rule_id:采集配置的 ID
        :type rule_id:str
        :param host_group_ids:机器组id列表
        :type host_group_ids: List[str]
        """
        self.rule_id = rule_id
        self.host_group_ids = host_group_ids

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.rule_id is None or self.host_group_ids is None:
            return False
        return True


class CreateAlarmNotifyGroupRequest(TLSRequest):
    def __init__(self, alarm_notify_group_name: str, notify_type: List[str], receivers: List[Receiver]):
        """
        :param alarm_notify_group_name:告警通知组名称
        :type alarm_notify_group_name:str
        :param notify_type: 告警通知的类型 Trigger告警触发、Recovery告警恢复
        :type notify_type: List[str]
        :param receivers:接收告警的 IAM 用户列表
        :type receivers:List[Receiver]
        """
        self.alarm_notify_group_name = alarm_notify_group_name
        self.notify_type = notify_type
        self.receivers = receivers

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
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
        """
        :param alarm_notify_group_id:告警通知组 ID
        :type alarm_notify_group_id:str
        """
        self.alarm_notify_group_id = alarm_notify_group_id

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.alarm_notify_group_id is None:
            return False
        return True


class ModifyAlarmNotifyGroupRequest(TLSRequest):
    def __init__(self, alarm_notify_group_id: str, alarm_notify_group_name: str = None,
                 notify_type: List[str] = None, receivers: List[Receiver] = None):
        """
        :param alarm_notify_group_id: 告警通知组 ID
        :type alarm_notify_group_id:str
        :param alarm_notify_group_name:告警通知组名称
        :type alarm_notify_group_name:str
        :param notify_type: 告警通知的类型 Trigger告警触发、Recovery告警恢复
        :type notify_type: List[str]
        :param receivers:接收告警的 IAM 用户列表
        :type receivers:List[Receiver]
        """
        self.alarm_notify_group_id = alarm_notify_group_id
        self.alarm_notify_group_name = alarm_notify_group_name
        self.notify_type = notify_type
        self.receivers = receivers

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
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
        """
        :param alarm_notify_group_id: 告警通知组 ID
        :type alarm_notify_group_id:str
        :param alarm_notify_group_name:告警通知组名称
        :type alarm_notify_group_name:str
        :param receiver_name:接收告警的 IAM 用户
        :type receiver_name:str
        :param page_number: 分页查询时的页码。默认为 1
        :type page_number: int
        :param page_size: 分页大小。默认为 20，最大为 100
        :type page_size: int
        """
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
        """
        :param alarm_name:告警策略名称
        :type alarm_name:str
        :param query_request:检索分析语句，可配置 1~3 条
        :type query_request: List[QueryRequest]
        :param request_cycle:告警任务的执行周期
        :type request_cycle:RequestCycle
        :param condition: 告警触发条件
        :type condition:str
        :param alarm_period:告警重复的周期
        :type alarm_period:int
        :param alarm_notify_group:告警对应的通知列表
        :type alarm_notify_group:List[str]
        :param status:是否开启告警策略。默认值为 true
        :type status:bool
        :param trigger_period:triggerPeriod 触发告警持续周期。最小值为 1，最大值为10。
        :type trigger_period:int
        :param user_define_msg:告警通知的内容
        :type user_define_msg:str
        """
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
        """
        :param project_id: 日志项目 ID
        :type project_id: string
        :param alarm_name:告警策略名称
        :type alarm_name:str
        :param query_request:检索分析语句，可配置 1~3 条
        :type query_request: List[QueryRequest]
        :param request_cycle:告警任务的执行周期
        :type request_cycle:RequestCycle
        :param condition: 告警触发条件
        :type condition:str
        :param alarm_period:告警重复的周期
        :type alarm_period:int
        :param alarm_notify_group:告警对应的通知列表
        :type alarm_notify_group:List[str]
        :param status:是否开启告警策略。默认值为 true
        :type status:bool
        :param trigger_period:triggerPeriod 触发告警持续周期。最小值为 1，最大值为10。
        :type trigger_period:int
        :param user_define_msg:告警通知的内容
        :type user_define_msg:str
        """
        super(CreateAlarmRequest, self).__init__(alarm_name, query_request, request_cycle, condition, alarm_period,
                                                 alarm_notify_group, status, trigger_period, user_define_msg)
        self.project_id = project_id

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.alarm_name is None or self.project_id is None or self.request_cycle is None or self.condition is None \
                or self.alarm_period is None or self.alarm_notify_group is None:
            return False
        return True


class DeleteAlarmRequest(TLSRequest):
    def __init__(self, alarm_id: str):
        """
        :param alarm_id:告警策略 ID
        :type alarm_id:str
        """
        self.alarm_id = alarm_id

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.alarm_id is None:
            return False
        return True


class ModifyAlarmRequest(SetAlarmRequest):
    def __init__(self, alarm_id: str, alarm_name: str = None, query_request: List[QueryRequest] = None,
                 request_cycle: RequestCycle = None, condition: str = None, alarm_period: int = None,
                 alarm_notify_group: List[str] = None, status: bool = None, trigger_period: int = None,
                 user_define_msg: str = None):
        """
        :param alarm_id:告警策略 ID
        :type alarm_id:str
        :param alarm_name:告警策略名称
        :type alarm_name:str
        :param query_request:检索分析语句，可配置 1~3 条
        :type query_request: List[QueryRequest]
        :param request_cycle:告警任务的执行周期
        :type request_cycle:RequestCycle
        :param condition: 告警触发条件
        :type condition:str
        :param alarm_period:告警重复的周期
        :type alarm_period:int
        :param alarm_notify_group:告警对应的通知列表
        :type alarm_notify_group:List[str]
        :param status:是否开启告警策略。默认值为 true
        :type status:bool
        :param trigger_period:triggerPeriod 触发告警持续周期。最小值为 1，最大值为10。
        :type trigger_period:int
        :param user_define_msg:告警通知的内容
        :type user_define_msg:str
        """
        super(ModifyAlarmRequest, self).__init__(alarm_name, query_request, request_cycle, condition, alarm_period,
                                                 alarm_notify_group, status, trigger_period, user_define_msg)
        self.alarm_id = alarm_id

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.alarm_id is None:
            return False
        return True


class DescribeAlarmsRequest(TLSRequest):
    def __init__(self, project_id: str, alarm_name: str = None, alarm_id: str = None, topic_name: str = None,
                 topic_id: str = None, status: bool = None, page_number: int = 1, page_size: int = 20):
        """
        :param project_id: 日志项目 ID
        :type project_id: string
        :param alarm_name:告警策略名称
        :type alarm_name:str
        :param alarm_id:告警策略 ID
        :type alarm_id:str
        :param status:是否开启告警策略。默认值为 true
        :type status:bool
        :param page_number: 分页查询时的页码。默认为 1
        :type page_number: int
        :param page_size: 分页大小。默认为 20，最大为 100
        :type page_size: int
        :param topic_id:日志主题 ID
        :type topic_id:str
        :param topic_name: 日志主题名称
        :type topic_name: string
        """

        self.project_id = project_id
        self.alarm_name = alarm_name
        self.alarm_id = alarm_id
        self.topic_name = topic_name
        self.topic_id = topic_id
        self.status = status
        self.page_number = page_number
        self.page_size = page_size

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.project_id is None:
            return False
        return True


class OpenKafkaConsumerRequest(TLSRequest):
    def __init__(self, topic_id: str):
        """
        :param topic_id:日志主题 ID
        :type topic_id:str
        """
        self.topic_id = topic_id

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.topic_id is None:
            return False
        return True


class CloseKafkaConsumerRequest(TLSRequest):
    def __init__(self, topic_id: str):
        """
        :param topic_id:日志主题 ID
        :type topic_id:str
        """
        self.topic_id = topic_id

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.topic_id is None:
            return False
        return True


class DescribeKafkaConsumerRequest(TLSRequest):
    def __init__(self, topic_id: str):
        """
        :param topic_id:日志主题 ID
        :type topic_id:str
        """
        self.topic_id = topic_id

    def check_validation(self):
        """
        :return: 参数是否合法
        :rtype: bool
        """
        if self.topic_id is None:
            return False
        return True
