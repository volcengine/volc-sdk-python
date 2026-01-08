# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re
from typing import List, Dict

from volcengine.tls.const import *


def pascal_to_snake(pascal: str) -> str:
    # 先在小写/数字与大写字母之间插入下划线，再在连续大写后接小写的边界插入下划线，
    # 以便正确处理诸如 ID、DSL 等缩略词。
    s1 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", pascal)
    s2 = re.sub(r"([A-Z]+)([A-Z][a-z0-9])", r"\1_\2", s1)
    return s2.lower().strip('_')


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


class TagInfo(TLSData):
    def __init__(self, key: str, value: str = None):
        """
        :param key: 标签Key的值
        :param value: 标签Value的值
        """
        self.key = key
        self.value = value


class ProjectInfo(TLSData):
    def __init__(self, project_name: str = None, project_id: str = None, description: str = None,
                 create_time: str = None, inner_net_domain: str = None, topic_count: int = None,
                 iam_project_name: str = None, tags: List[TagInfo] = None):
        self.project_name = project_name
        self.project_id = project_id
        self.description = description
        self.create_time = create_time
        self.inner_net_domain = inner_net_domain
        self.topic_count = topic_count
        self.iam_project_name = iam_project_name
        self.tags = tags

    @classmethod
    def set_attributes(cls, data: dict):
        project_info = super(ProjectInfo, cls).set_attributes(data)

        if TAGS in data:
            tags = data[TAGS]
            project_info.tags = []
            for i in range(len(tags)):
                project_info.tags.append(  # pylint: disable=no-member
                    TagInfo(tags[i].get(KEY), tags[i].get(VALUE)))

        return project_info

    def get_inner_net_domain(self):
        """
        :return:内网连接域名
        :rtype:str
        """
        return self.inner_net_domain

    def get_create_time(self):
        """
        :return: 创建时间
        :rtype: str
        """
        return self.create_time

    def get_project_id(self):
        """
        :return: 日志项目 ID
        :rtype: str
        """
        return self.project_id

    def get_description(self):
        """
        :return:日志项目描述
        :rtype: str
        """
        return self.description

    def get_project_name(self):
        """
        :return:日志项目名称
        :rtype:str
        """
        return self.project_name

    def get_topic_count(self):
        """
        :return:日志项目下的日志主题数量
        :rtype:int
        """
        return self.topic_count

    def get_iam_project_name(self):
        """
        :return: 日志项目所属的IAM项目
        :rtype: str
        """
        return self.iam_project_name

    def get_tags(self):
        """
        :return: 日志项目标签信息
        :rtype: List[TagInfo]
        """
        return self.tags


class EncryptUserCmkConf(TLSData):
    def __init__(self, user_cmk_id: str, trn: str, region_id: str):
        self.user_cmk_id = user_cmk_id
        self.trn = trn
        self.region_id = region_id

    @classmethod
    def set_attributes(cls, data):
        user_cmk_id = data.get(USER_CMK_ID)
        trn = data.get(TRN)
        region_id = data.get(REGION_ID)

        return cls(user_cmk_id, trn, region_id)

    def json(self):
        return {
            USER_CMK_ID: self.user_cmk_id,
            TRN: self.trn,
            REGION_ID: self.region_id,
        }


class EncryptConf(TLSData):
    def __init__(self, enable: bool = False, encrypt_type: str = "default", user_cmk_info: EncryptUserCmkConf = None):
        self.enable = enable
        self.encrypt_type = encrypt_type
        self.user_cmk_info = user_cmk_info

    @classmethod
    def set_attributes(cls, data):
        enable = data.get(ENABLE_ENCRYPT_CONF)
        encrypt_type = data.get(ENCRYPT_TYPE)
        user_cmk_info = data.get(USER_CMK_INFO)

        return cls(enable, encrypt_type, user_cmk_info)

    def json(self):
        return {
            ENABLE_ENCRYPT_CONF: self.enable,
            ENCRYPT_TYPE: self.encrypt_type,
            USER_CMK_INFO: self.user_cmk_info.json() if self.user_cmk_info is not None else None,
        }


class TopicInfo(TLSData):
    def __init__(self, topic_name: str = None, topic_id: str = None, project_id: str = None, ttl: int = None,
                 create_time: str = None, modify_time: str = None, shard_count: int = None, description: str = None,
                 auto_split: bool = None, max_split_shard: int = None, enable_tracking: bool = None,
                 time_key: str = None, time_format: str = None, tags: List[TagInfo] = None, log_public_ip: bool = None,
                 enable_hot_ttl: bool = None, hot_ttl: int = None, cold_ttl: int = None, archive_ttl: int = None,
                 encrypt_conf: EncryptConf = None):
        self.topic_name = topic_name
        self.topic_id = topic_id
        self.project_id = project_id
        self.ttl = ttl
        self.create_time = create_time
        self.modify_time = modify_time
        self.shard_count = shard_count
        self.description = description
        self.auto_split = auto_split
        self.max_split_shard = max_split_shard
        self.enable_tracking = enable_tracking
        self.time_key = time_key
        self.time_format = time_format
        self.tags = tags
        self.log_public_ip = log_public_ip
        self.enable_hot_ttl = enable_hot_ttl
        self.hot_ttl = hot_ttl
        self.cold_ttl = cold_ttl
        self.archive_ttl = archive_ttl
        self.encrypt_conf = encrypt_conf

    @classmethod
    def set_attributes(cls, data: dict):
        topic_name = data.get(TOPIC_NAME)
        topic_id = data.get(TOPIC_ID)
        project_id = data.get(PROJECT_ID)
        ttl = data.get(TTL)
        create_time = data.get(CREATE_TIME)
        modify_time = data.get(MODIFY_TIME)
        shard_count = data.get(SHARD_COUNT)
        description = data.get(DESCRIPTION)
        auto_split = data.get(AUTO_SPLIT)
        max_split_shard = data.get(MAX_SPLIT_SHARD)
        enable_tracking = data.get(ENABLE_TRACKING)
        time_key = data.get(TIME_KEY)
        time_format = data.get(TIME_FORMAT)
        topic_tags = None
        log_public_ip = data.get(LOG_PUBLIC_IP)
        enable_hot_ttl = data.get(ENABLE_HOT_TTL)
        hot_ttl = data.get(HOT_TTL)
        cold_ttl = data.get(COLD_TTL)
        archive_ttl = data.get(ARCHIVE_TTL)
        encrypt_conf = data.get(ENCRYPT_CONF)

        tags = data.get(TAGS)
        if tags is not None:
            topic_tags = []
            for i in range(len(tags)):
                topic_tags.append(
                    TagInfo(tags[i].get(KEY), tags[i].get(VALUE)))

        return cls(topic_name, topic_id, project_id, ttl, create_time, modify_time, shard_count, description,
                   auto_split, max_split_shard, enable_tracking, time_key, time_format, topic_tags, log_public_ip,
                   enable_hot_ttl, hot_ttl, cold_ttl, archive_ttl, encrypt_conf)

    def get_create_time(self):
        """
        :return: 创建时间
        :rtype: str
        """
        return self.create_time

    def get_project_id(self):
        """
        :return: 日志项目 ID
        :rtype: str
        """
        return self.project_id

    def get_modify_time(self):
        """
        :return:修改时间
        :rtype: str
        """
        return self.modify_time

    def get_shard_count(self):
        """
        :return:日志分区的数量
        :rtype: int
        """
        return self.shard_count

    def get_topic_name(self):
        """
        :return: 日志主题名称
        :rtype: str
        """
        return self.topic_name

    def get_description(self):
        """
        :return:日志主题描述
        :rtype: str
        """
        return self.description

    def get_topic_id(self):
        """

        :return: 日志主题 ID
        :rtype: str
        """
        return self.topic_id

    def get_ttl(self):
        """
        :return: 日志在日志服务中的保存时间, 单位天
        :rtype: int
        """
        return self.ttl

    def is_auto_split(self):
        """
        :return: 是否开启分区的自动分裂功能
        :rtype: bool
        """
        return self.auto_split

    def get_max_split_shard(self):
        """
        :return: 分区的最大分裂数
        :rtype: int
        """
        return self.max_split_shard

    def is_enable_tracking(self):
        """
        :return: 是否开启了WebTracking功能
        :rtype: bool
        """
        return self.enable_tracking

    def get_time_key(self):
        """
        :return: 日志时间字段的字段名称
        :rtype: str
        """
        return self.time_key

    def get_time_format(self):
        """
        :return: 时间字段的解析格式
        :rtype: str
        """
        return self.time_format

    def get_tags(self):
        """
        :return: 日志主题标签信息
        :rtype: List[TagInfo]
        """
        return self.tags

    def get_log_public_ip(self):
        """
        :return: 是否开启了记录外网IP功能
        :rtype: bool
        """
        return self.log_public_ip


class FullTextInfo(TLSData):
    def __init__(self, case_sensitive: bool = None, delimiter: str = None, include_chinese: bool = False):
        """
        :param case_sensitive: 是否大小写敏感
        :type case_sensitive:bool
        :param delimiter:全文索引的分词符
        :type delimiter:string
        :param include_chinese:是否包含中文
        :type include_chinese:bool
        """
        self.case_sensitive = case_sensitive
        self.delimiter = delimiter
        self.include_chinese = include_chinese

    def get_delimiter(self):
        """
        :return: 全文索引的分词符
        :rtype: string
        """
        return self.delimiter

    def get_case_sensitive(self):
        """
        :return: 是否大小写敏感
        :rtype: bool
        """
        return self.case_sensitive

    def get_include_chinese(self):
        """
        :return:是否包含中文
        :rtype: bool
        """
        return self.include_chinese

    @classmethod
    def set_attributes(cls, data: dict):
        case_sensitive = data.get(CASE_SENSITIVE)
        delimiter = data.get(DELIMITER)
        include_chinese = data.get(INCLUDE_CHINESE)

        return cls(case_sensitive, delimiter, include_chinese)


class ValueInfo(TLSData):
    def __init__(self, value_type: str, delimiter: str = None, case_sensitive: bool = False,
                 include_chinese: bool = False, sql_flag: bool = False, index_all: bool = False,
                 json_keys=None, auto_index_flag: bool = False):
        self.value_type = value_type
        self.delimiter = delimiter
        self.case_sensitive = case_sensitive
        self.include_chinese = include_chinese
        self.sql_flag = sql_flag
        self.index_all = index_all
        self.auto_index_flag = auto_index_flag

        if value_type == "json":
            self.json_keys = json_keys
        else:
            self.json_keys = None

    @classmethod
    def set_attributes(cls, data: dict):
        value_type = data.get(VALUE_TYPE)
        delimiter = data.get(DELIMITER)
        case_sensitive = data.get(CASE_SENSITIVE)
        include_chinese = data.get(INCLUDE_CHINESE)
        sql_flag = data.get(SQL_FLAG)
        index_all = data.get(INDEX_ALL)
        json_keys = data.get(JSON_KEYS)
        auto_index_flag = data.get(AUTO_INDEX_FLAG, False)

        return cls(value_type, delimiter, case_sensitive, include_chinese, sql_flag,
                   index_all, json_keys, auto_index_flag)

    def get_auto_index_flag(self):
        """
        :return: 该索引是否是自动索引添加
        :rtype: bool
        """
        return self.auto_index_flag


class KeyValueInfo(TLSData):
    def __init__(self, key: str, value: ValueInfo):
        """
        :param key:需要配置键值索引的字段名称
        :type key:string
        :param value:需要配置键值索引的字段描述信息
        :type value:string
        """
        self.key = key
        self.value = value

    def json(self):
        return {KEY: self.key, VALUE: self.value.json()}

    @classmethod
    def set_attributes(cls, data: dict):
        key = data.get(KEY)
        value = data.get(VALUE)

        # 索引场景下 Value 是 ValueInfo，Trace 场景下 Value 为普通字符串
        if isinstance(value, dict):
            value = ValueInfo.set_attributes(data=value)

        return cls(key=key, value=value)


class AnalysisResult(TLSData):
    def __init__(self, analysis_schema: List[str] = None, analysis_type: dict = None, analysis_data: List[dict] = None):
        self.analysis_schema = analysis_schema
        self.analysis_type = analysis_type
        self.analysis_data = analysis_data

    def get_analysis_schema(self):
        """
        :return:日志分析列的名称
        :rtype:List[str]
        """
        return self.analysis_schema

    def get_analysis_type(self):
        """
        :return:日志分析列对应的属性
        :rtype:dict
        """
        return self.analysis_type

    def get_analysis_data(self):
        """
        :return:分析结果返回的键值对
        :rtype:List[dict]
        """
        return self.analysis_data

    @classmethod
    def set_attributes(cls, data: dict):
        analysis_schema = data.get(SCHEMA)
        analysis_type = data.get(TYPE)
        analysis_data = data.get(DATA)

        return cls(analysis_schema, analysis_type, analysis_data)


class SearchResult(TLSData):
    def __init__(self, result_status: str = None, hit_count: int = None, list_over: bool = None, analysis: bool = None,
                 count: int = None, limit: int = None, context: str = None, logs: List[dict] = None,
                 analysis_result: AnalysisResult = None, highlight: List[dict] = None, elapsed_millisecond: int = None):
        self.result_status = result_status
        self.hit_count = hit_count
        self.list_over = list_over
        self.analysis = analysis
        self.count = count
        self.limit = limit
        self.context = context
        self.logs = logs
        self.analysis_result = analysis_result
        self.highlight = highlight
        self.elapsed_millisecond = elapsed_millisecond

    def get_list_over(self):
        """
        :return: 是否已返回全部结果
        :rtype:bool
        """
        return self.list_over

    def get_analysis_result(self):
        """
        :return: 分析结果
        :rtype: AnalysisResult
        """
        return self.analysis_result

    def get_result_status(self):
        """
        :return: 查询的状态
        :rtype:str
        """
        return self.result_status

    def get_count(self):
        """
        :return: 分析请求命中的条目数
        :rtype: int
        """
        return self.count

    def get_limit(self):
        """
        :return:请求中指定返回的 Limit 条目数
        :rtype: int
        """
        return self.limit

    def get_context(self):
        """
        :return:仅检索日志时，翻页上下文
        :rtype: str
        """
        return self.context

    def get_hit_count(self):
        """
        :return:搜索匹配的总条目数
        :rtype: int
        """
        return self.hit_count

    def get_analysis(self):
        """
        :return:是否分析请求
        :rtype:bool
        """
        return self.analysis

    def get_logs(self):
        """
        :return:检索日志结果
        :rtype: List[dict]
        """
        return self.logs

    def get_highlight(self):
        """
        :return:高亮显示的关键字
        :rtype: List[dict]
        """
        return self.highlight

    def get_elapsed_millisecond(self):
        """
        :return:本次检索所使用的时间，单位为毫秒
        :rtype: int
        """
        return self.elapsed_millisecond

    @classmethod
    def set_attributes(cls, data: dict):
        search_result = super(SearchResult, cls).set_attributes(data)

        if ANALYSIS_RESULT in data:
            search_result.analysis_result = AnalysisResult.set_attributes(
                data=data[ANALYSIS_RESULT])

        # HighLight 字段在后端使用不规则大小写，pascal_to_snake 会将其转换为 "high_light"，
        # 导致默认映射不到 SearchResult.highlight 属性，这里显式修正映射关系。
        if "HighLight" in data:
            search_result.highlight = data["HighLight"]

        # ElapsedMillisecond 字段按常规 PascalCase -> snake_case 映射为 elapsed_millisecond，
        # 但为了避免未来结构调整遗漏，这里也显式同步一次。
        if "ElapsedMillisecond" in data:
            search_result.elapsed_millisecond = data["ElapsedMillisecond"]

        return search_result


class QueryResp(TLSData):
    def __init__(self, topic_id: str = None, shard_id: int = None, inclusive_begin_key: str = None,
                 exclusive_end_key: str = None, status: str = None, modify_time: str = None,
                 stop_write_time: str = None):
        """查询分区信息

        :param topic_id: 日志主题 ID
        :type topic_id: str
        :param shard_id: 分区 ID
        :type shard_id: int
        :param inclusive_begin_key: 分区起始的 key 值（包含）
        :type inclusive_begin_key: str
        :param exclusive_end_key: 分区结束的 key 值（不包含）
        :type exclusive_end_key: str
        :param status: 分区状态，readwrite：读写，readonly：只读
        :type status: str
        :param modify_time: 分区修改时间
        :type modify_time: str
        :param stop_write_time: 分区停止写入的时间
        :type stop_write_time: str
        """
        self.topic_id = topic_id
        self.shard_id = shard_id
        self.inclusive_begin_key = inclusive_begin_key
        self.exclusive_end_key = exclusive_end_key
        self.status = status
        self.modify_time = modify_time
        self.stop_write_time = stop_write_time

    def get_exclusive_end_key(self):
        """返回分区结束的 key 值"""
        return self.exclusive_end_key

    def get_inclusive_begin_key(self):
        """返回分区起始的 key 值"""
        return self.inclusive_begin_key

    def get_shard_id(self):
        """返回日志主题的分区 ID"""
        return self.shard_id

    def get_modify_time(self):
        """返回分区修改时间"""
        return self.modify_time

    def get_topic_id(self):
        """返回日志主题的 ID"""
        return self.topic_id

    def get_status(self):
        """返回分区状态（readwrite：读写，readonly：只读）"""
        return self.status

    def get_stop_write_time(self):
        """返回分区停止写入的时间"""
        return self.stop_write_time


class HistogramInfo(TLSData):
    def __init__(self, time: int = None, count: int = None):
        self.time = time
        self.count = count

    def get_count(self):
        """
        :return:子区间中对应搜索结果的数量
        :rtype:int
        """
        return self.count

    def get_time(self):
        """
        :return:子区间的起始时间点，单位为毫秒
        :rtype:long
        """
        return self.time


class HistogramInfoV1(TLSData):
    def __init__(self, count: int = None, start_time: int = None, end_time: int = None, result_status: str = None):
        self.count = count
        self.start_time = start_time
        self.end_time = end_time
        self.result_status = result_status

    def get_count(self):
        """
        :return:子区间中对应搜索结果的数量，即该时段内符合条件的日志条数
        :rtype:int
        """
        return self.count

    def get_start_time(self):
        """
        :return:查询的开始时间点，单位为毫秒
        :rtype:long
        """
        return self.start_time

    def get_end_time(self):
        """
        :return:查询的开始时间点，单位为毫秒
        :rtype:long
        """
        return self.end_time

    def get_result_status(self):
        """
        :return:查询的状态
        :rtype:str
        """
        return self.result_status


class LogContextInfos(TLSData):
    def __init__(self, source: str = None, context_flow: str = None, package_offset: int = None):
        """下载上下文查询所需的日志信息

        :param source: 日志来源的主机
        :type source: str
        :param context_flow: 指定日志所在的 LogGroup 的 ID
        :type context_flow: str
        :param package_offset: 指定日志在 LogGroup 中的序号
        :type package_offset: int
        """
        self.source = source
        self.context_flow = context_flow
        self.package_offset = package_offset

    @classmethod
    def set_attributes(cls, data: dict):
        if data is None:
            return None

        source = data.get(SOURCE)
        context_flow = data.get(CONTEXT_FLOW)
        package_offset = data.get(PACKAGE_OFFSET)

        return cls(source, context_flow, package_offset)

    def get_source(self):
        """
        :return: 日志来源的主机
        :rtype: str
        """
        return self.source

    def get_context_flow(self):
        """
        :return: 日志所在的 LogGroup 的 ID
        :rtype: str
        """
        return self.context_flow

    def get_package_offset(self):
        """
        :return: 日志在 LogGroup 中的序号
        :rtype: int
        """
        return self.package_offset


class TaskInfo(TLSData):
    def __init__(self, task_id: str = None, task_name: str = None, topic_id: str = None, query: str = None,
                 start_time: str = None, end_time: str = None, data_format: str = None, task_status: str = None,
                 compression: str = None, create_time: str = None, log_size: int = None, log_count: int = None,
                 task_type: int = None, allow_incomplete: bool = None, log_context_infos: LogContextInfos = None):
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
        self.task_type = task_type
        self.allow_incomplete = allow_incomplete
        self.log_context_infos = log_context_infos

    def get_task_name(self):
        """
        :return:下载任务的名称
        :rtype: str
        """
        return self.task_name

    def get_start_time(self):
        """
        :return:起始时间。格式为 yyyy-MM-dd HH:mm:ss
        :rtype: str
        """
        return self.start_time

    def get_data_format(self):
        """
        :return:导出的文件格式，支持 CSV 文件格式或 JSON 格式
        :rtype: str
        """
        return self.data_format

    def get_task_status(self):
        """
        :return:下载任务状态
        :rtype:str
        """
        return self.task_status

    def get_log_count(self):
        """
        :return:下载的日志条数
        :rtype: int
        """
        return self.log_count

    def get_create_time(self):
        """
        :return:下载任务的创建时间
        :rtype: str
        """
        return self.create_time

    def get_query(self):
        """
        :return:日志检索分析语句
        :rtype:str
        """
        return self.query

    def get_end_time(self):
        """
        :return:结束时间。格式为 yyyy-MM-dd HH:mm:ss
        :rtype: str
        """
        return self.end_time

    def get_task_id(self):
        """
        :return:下载任务的 ID
        :rtype:str
        """
        return self.task_id

    def get_log_size(self):
        """
        :return:下载的日志量，单位为字节（Byte）
        :rtype:long
        """
        return self.log_size

    def get_topic_id(self):
        """
        :return:日志主题名称
        :rtype:str
        """
        return self.topic_id

    def get_compression(self):
        """
        :return:导出文件的压缩格式
        :rtype:str
        """
        return self.compression

    def get_task_type(self):
        """
        :return:下载的日志类型
        :rtype: int
        """
        return self.task_type

    def get_allow_incomplete(self):
        """
        :return:是否允许下载查询不精确结果日志
        :rtype: bool
        """
        return self.allow_incomplete

    def get_log_context_infos(self):
        """
        :return:下载上下文查询所需的日志信息
        :rtype: LogContextInfos
        """
        return self.log_context_infos

    @classmethod
    def set_attributes(cls, data: dict):
        if data is None:
            return None

        task_id = data.get(TASK_ID)
        task_name = data.get(TASK_NAME)
        topic_id = data.get(TOPIC_ID)
        query = data.get(QUERY)
        start_time = data.get(START_TIME)
        end_time = data.get(END_TIME)
        data_format = data.get(DATA_FORMAT)
        task_status = data.get(TASK_STATUS)
        compression = data.get(COMPRESSION)
        create_time = data.get(CREATE_TIME)
        log_size = data.get(LOG_SIZE)
        log_count = data.get(LOG_COUNT)
        task_type = data.get(ETL_TASK_TYPE)
        allow_incomplete = data.get(ALLOW_INCOMPLETE)

        log_context_infos_data = data.get(LOG_CONTEXT_INFOS)
        log_context_infos = None
        if log_context_infos_data is not None:
            log_context_infos = LogContextInfos.set_attributes(data=log_context_infos_data)

        return cls(task_id, task_name, topic_id, query, start_time, end_time,
                   data_format, task_status, compression, create_time, log_size,
                   log_count, task_type, allow_incomplete, log_context_infos)


class HostInfo(TLSData):
    def __init__(self, ip: str = None, log_collector_version: str = None, heartbeat_status: int = None):
        self.ip = ip
        self.log_collector_version = log_collector_version
        self.heartbeat_status = heartbeat_status

    def get_ip(self):
        """
        :return:机器的 IP 地址
        :rtype: str
        """
        return self.ip

    def get_log_collector_version(self):
        """
        :return:机器安装的 LogCollector 的版本
        :rtype:str
        """
        return self.log_collector_version

    def get_heartbeat_status(self):
        """
        :return:Agent 的心跳状态。0：心跳正常 1：心跳异常。
        :rtype:int
        """
        return self.heartbeat_status


class HostGroupInfo(TLSData):
    def __init__(self, host_group_id: str = None, host_group_name: str = None, host_group_type: str = None,
                 host_identifier: str = None, host_count: int = None, normal_heartbeat_status_count: int = None,
                 abnormal_heartbeat_status_count: int = None, rule_count: int = None,
                 create_time: str = None, modify_time: str = None, auto_update: bool = False,
                 update_start_time: str = None, update_end_time: str = None, agent_latest_version: str = None,
                 service_logging: bool = None, iam_project_name: str = None):
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
        self.service_logging = service_logging
        self.iam_project_name = iam_project_name

    def get_update_end_time(self):
        """
        :return: 自动升级的结束时间
        :rtype: str
        """
        return self.update_end_time

    def get_update_start_time(self):
        """
        :return: 自动升级的开始时间
        :rtype: str
        """
        return self.update_start_time

    def get_create_time(self):
        """
        :return: 机器组创建时间
        :rtype: str
        """
        return self.create_time

    def get_host_count(self):
        """
        :return: 机器数量
        :rtype: int
        """
        return self.host_count

    def get_modify_time(self):
        """
        :return: 机器组修改时间
        :rtype: str
        """
        return self.modify_time

    def get_host_group_type(self):
        """
        :return: 机器组类型
        :rtype: str
        """
        return self.host_group_type

    def get_host_group_id(self):
        """
        :return: 机器组ID
        :rtype: str
        """
        return self.host_group_id

    def get_host_identifier(self):
        """
        :return: 机器标识符
        :rtype: str
        """
        return self.host_identifier

    def get_abnormal_heartbeat_status_count(self):
        """
        :return: 心跳异常的机器数量
        :rtype: int
        """
        return self.abnormal_heartbeat_status_count

    def get_auto_update(self):
        """
        :return: 是否开启自动升级功能
        :rtype: bool
        """
        return self.auto_update

    def get_host_group_name(self):
        """
        :return: 机器组名称
        :rtype: str
        """
        return self.host_group_name

    def get_agent_latest_version(self):
        """
        :return: 日志服务发布的LogCollector最新版本号
        :rtype: str
        """
        return self.agent_latest_version

    def get_normal_heartbeat_status_count(self):
        """
        :return: 心跳正常的机器数量
        :rtype: int
        """
        return self.normal_heartbeat_status_count

    def get_rule_count(self):
        """
        :return: 绑定的采集配置的数量
        :rtype: int
        """
        return self.rule_count

    def get_service_logging(self):
        """
        :return: 是否开启Logcollector服务日志功能
        :rtype: bool
        """
        return self.service_logging

    def get_iam_project_name(self):
        """
        :return: 机器组所属的IAM项目
        :rtype: str
        """
        return self.iam_project_name


class FilterKeyRegex(TLSData):
    def __init__(self, key: str, regex: str):
        """
        :param key: 过滤字段的名称
        :type key:str
        :param regex:过滤字段的日志内容需要匹配的正则表达式
        :type regex:str
        """
        self.key = key
        self.regex = regex

    @classmethod
    def set_attributes(cls, data: dict):
        key = data.get(KEY)
        regex = data.get(REGEX)

        return cls(key, regex)


class LogTemplate(TLSData):
    def __init__(self, log_type: str, log_format: str):
        """
        :param log_type:日志模板的类型：Nginx
        :type log_type:str
        :param log_format:日志模板内容
        :type log_format:str
        """
        self.log_type = log_type
        self.log_format = log_format

    def json(self):
        return {TYPE: self.log_type, FORMAT: self.log_format}


class ExtractRule(TLSData):
    def __init__(self, delimiter: str = None, begin_regex: str = None, log_regex: str = None, keys: List[str] = None,
                 time_key: str = None, time_format: str = None, time_zone: str = None, filter_key_regex: List[FilterKeyRegex] = None,
                 un_match_up_load_switch: bool = None, un_match_log_key: str = None, log_template: LogTemplate = None,
                 quote: str = None, time_extract_regex: str = None, enable_nanosecond: bool = False, time_sample: str = None):
        """
        :param delimiter: 日志分隔符
        :type delimiter: str
        :param begin_regex: 第一行日志需要匹配的正则表达式
        :type begin_regex: str
        :param log_regex: 整条日志需要匹配的正则表达式
        :type log_regex: str
        :param keys: 日志字段名称
        :type keys: List[str]
        :param time_key: 日志时间字段的字段名称
        :type time_key: str
        :param time_format: 时间字段的解析格式
        :type time_format: str
        :param time_zone: 日志时间字段的时区
        :type time_zone: str
        :param filter_key_regex: 过滤字段的正则表达式
        :type filter_key_regex: List[FilterKeyRegex]
        :param un_match_up_load_switch: 是否上传解析失败的日志
        :type un_match_up_load_switch: bool
        :param un_match_log_key: 当上传解析失败的日志时，解析失败的日志的key名称
        :type un_match_log_key: str
        :param log_template: 根据指定的日志模板自动提取日志字段
        :type log_template: LogTemplate
        :param quote: 引用符
        :type quote: str
        :param time_extract_regex: 时间字段的解析正则表达式
        :type time_extract_regex: str
        :param enable_nanosecond: 是否开启解析纳秒级时间
        :type enable_nanosecond: bool
        :param time_sample: 时间字段的样本日志
        :type time_sample: str
        """
        assert (time_key is None and time_format is None) or (
            time_key is not None and time_format is not None)
        assert (un_match_up_load_switch is None and un_match_log_key is None) or \
               (un_match_up_load_switch is not None and un_match_log_key is not None)

        self.delimiter = delimiter
        self.begin_regex = begin_regex
        self.log_regex = log_regex
        self.keys = keys
        self.time_key = time_key
        self.time_format = time_format
        self.time_zone = time_zone
        self.filter_key_regex = filter_key_regex
        self.un_match_up_load_switch = un_match_up_load_switch
        self.un_match_log_key = un_match_log_key
        self.log_template = log_template
        self.quote = quote
        self.time_extract_regex = time_extract_regex
        self.enable_nanosecond = enable_nanosecond
        self.time_sample = time_sample

    @classmethod
    def set_attributes(cls, data: dict):
        extract_rule = super(ExtractRule, cls).set_attributes(data)

        if FILTER_KEY_REGEX in data:
            extract_rule.filter_key_regex = []
            for one_filter_key_regex in data[FILTER_KEY_REGEX]:
                extract_rule.filter_key_regex.append(  # pylint: disable=no-member
                    FilterKeyRegex.set_attributes(data=one_filter_key_regex))
        if LOG_TEMPLATE in data:
            extract_rule.log_template = LogTemplate(log_type=data[LOG_TEMPLATE].get(TYPE),
                                                    log_format=data[LOG_TEMPLATE].get(FORMAT))  # pylint: disable=no-member

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
        """
        :param path_type:采集路径类型，File或Path
        :type path_type:str
        :param value:采集绝对路径
        :type value:str
        """
        assert path_type == "File" or path_type == "Path"

        self.path_type = path_type
        self.value = value

    def get_path_type(self):
        """
        :return: 采集路径类型，File或Path
        :rtype: str
        """
        return self.path_type

    def get_value(self):
        """
        :return: 采集绝对路径
        :rtype: str
        """
        return self.value

    @classmethod
    def set_attributes(cls, data: dict):
        path_type = data.get(TYPE)
        value = data.get(VALUE)

        return cls(path_type, value)

    def json(self):
        return {TYPE: self.path_type, VALUE: self.value}


class ParsePathRule(TLSData):
    def __init__(self, path_sample: str, regex: str, keys: List[str]):
        """
        :param path_sample:实际场景的采集路径样例
        :type path_sample:str
        :param regex: 用于提取路径字段的正则表达式
        :type regex:str
        :param keys:字段名称列表
        :type keys: List[str]
        """
        self.path_sample = path_sample
        self.regex = regex
        self.keys = keys

    def get_path_sample(self):
        """
        :return: 实际场景的采集路径样例
        :rtype: str
        """
        return self.path_sample

    def get_regex(self):
        """
        :return: 用于提取路径字段的正则表达式
        :rtype: str
        """
        return self.regex

    def get_keys(self):
        """
        :return: 字段名称列表
        :rtype:  List[str]
        """
        return self.keys

    @classmethod
    def set_attributes(cls, data: dict):
        path_sample = data.get(PATH_SAMPLE)
        regex = data.get(REGEX)
        keys = data.get(KEYS)

        return cls(path_sample, regex, keys)


class ShardHashKey(TLSData):
    def __init__(self, hash_key: str):
        """
        :param hash_key:日志组的 HashKey
        :type hash_key: str
        """
        self.hash_key = hash_key

    def get_hash_key(self):
        """
        :return:日志组的 HashKey
        :rtype: str
        """
        return self.hash_key


class Plugin(TLSData):
    def __init__(self, processors: List[Dict]):
        """
        :param processors: LogCollector插件
        :type processors: List[Dict]
        """
        self.processors = processors

    def get_processors(self):
        """
        :return: LogCollector插件
        :rtype: List[Dict]
        """
        return self.processors

    def json(self):
        return {PROCESSORS: self.processors}


class Advanced(TLSData):
    def __init__(self, close_inactive: int = 60, close_timeout: int = 0, no_line_terminator_eof_max_time: int = 5,
                 close_removed: bool = False, close_renamed: bool = False, close_eof: bool = False):
        """
        :param close_inactive: 释放日志文件句柄的等待时间
        :type close_inactive: int
        :param close_timeout: LogCollector监控日志文件的最大时长
        :type close_timeout: int
        :param no_line_terminator_eof_max_time: 日志文件无行终止符时，最大等待时间
        :type no_line_terminator_eof_max_time: int
        :param close_removed: 日志文件被移除之后，是否释放该日志文件的句柄
        :type close_removed: bool
        :param close_renamed: 日志文件被重命名之后，是否释放该日志文件的句柄
        :type close_renamed: bool
        :param close_eof: 读取至日志文件的末尾之后，是否释放该日志文件的句柄
        :type close_eof: bool
        """
        self.no_line_terminator_eof_max_time = no_line_terminator_eof_max_time
        self.close_inactive = close_inactive
        self.close_timeout = close_timeout
        self.close_removed = close_removed
        self.close_renamed = close_renamed
        self.close_eof = close_eof

    def get_close_inactive(self):
        """
        :return: 释放日志文件句柄的等待时间
        :rtype: int
        """
        return self.close_inactive

    def get_close_timeout(self):
        """
        :return: LogCollector监控日志文件的最大时长
        :rtype: int
        """
        return self.close_timeout

    def get_no_line_terminator_eof_max_time(self):
        """
        :return: 日志文件无行终止符时，最大等待时间
        :rtype: int
        """
        return self.no_line_terminator_eof_max_time



    def get_close_removed(self):
        """
        :return: 日志文件被移除之后，是否释放该日志文件的句柄
        :rtype: bool
        """
        return self.close_removed

    def get_close_renamed(self):
        """
        :return: 日志文件被重命名之后，是否释放该日志文件的句柄
        :rtype: bool
        """
        return self.close_renamed

    def get_close_eof(self):
        """
        :return: 读取至日志文件的末尾之后，是否释放该日志文件的句柄
        :rtype: bool
        """
        return self.close_eof

    def json(self):
        return {CLOSE_INACTIVE: self.close_inactive, CLOSE_TIMEOUT: self.close_timeout,
                CLOSE_REMOVED: self.close_removed, CLOSE_RENAMED: self.close_renamed, CLOSE_EOF: self.close_eof,
                NO_LINE_TERMINATOR_EOF_MAX_TIME: self.no_line_terminator_eof_max_time}


class UserDefineRule(TLSData):
    def __init__(self, parse_path_rule: ParsePathRule = None, shard_hash_key: ShardHashKey = None,
                 enable_raw_log: bool = False, fields: dict = None, plugin: Plugin = None, advanced: Advanced = None,
                 tail_files: bool = False, raw_log_key: str = None, enable_hostname: bool = False,
                 hostname_key: str = None, host_group_label_key: str = None, enable_host_group_label: bool = False,
                 tail_size_kb: int = None, ignore_older: int = None, multi_collects_type: str = None):
        """
        :param parse_path_rule: 解析采集路径的规则
        :type parse_path_rule: ParsePathRule
        :param shard_hash_key: 路由日志分区的规则
        :type shard_hash_key: ShardHashKey
        :param enable_raw_log: 是否上传原始日志
        :type enable_raw_log: bool
        :param fields: 为日志添加常量字段
        :type fields: dict
        :param plugin: LogCollector插件配置
        :type plugin: Plugin
        :param advanced: LogCollector扩展配置
        :type advanced: Advanced
        :param tail_files: LogCollector采集策略，即指定LogCollector采集增量日志还是全量日志
        :type tail_files: bool
        :param raw_log_key: 原始日志的键名
        :type raw_log_key: str
        :param enable_hostname: 是否添加主机名字段
        :type enable_hostname: bool
        :param hostname_key: 主机名字段的键名
        :type hostname_key: str
        :param host_group_label_key: 主机分组标签字段的键名
        :type host_group_label_key: str
        :param enable_host_group_label: 是否添加主机分组标签字段
        :type enable_host_group_label: bool
        :param tail_size_kb: 增量采集的回溯阈值。
        :type tail_size_kb: int
        :param ignore_older: 忽略多久没有更新的日志文件, 单位为小时。
        :type ignore_older: int
        :param multi_collects_type: 允许多次采集日志文件。空、RuleID、TopicIDRuleName
        :type multi_collects_type: str
        """
        self.parse_path_rule = parse_path_rule
        self.shard_hash_key = shard_hash_key
        self.enable_raw_log = enable_raw_log
        self.fields = fields
        self.plugin = plugin
        self.advanced = advanced
        self.tail_files = tail_files
        self.raw_log_key = raw_log_key
        self.enable_hostname = enable_hostname
        self.hostname_key = hostname_key
        self.host_group_label_key = host_group_label_key
        self.enable_host_group_label = enable_host_group_label
        self.tail_size_kb = tail_size_kb
        self.ignore_older = ignore_older
        self.multi_collects_type = multi_collects_type

    def get_enable_raw_log(self):
        """
        :return:是否上传原始日志
        :rtype:bool
        """
        return self.enable_raw_log

    def get_shard_hash_key(self):
        """
        :return:路由日志分区的规则
        :rtype: ShardHashKey
        """
        return self.shard_hash_key

    def get_fields(self):
        """
        :return: 为日志添加常量字段
        :rtype: dict
        """
        return self.fields

    def get_parse_path_rule(self):
        """
        :return: 解析采集路径的规则
        :rtype: ParsePathRule
        """
        return self.parse_path_rule

    def get_plugin(self):
        """
        :return: LogCollector插件配置
        :rtype: Plugin
        """
        return self.plugin

    def get_advanced(self):
        """
        :return: LogCollector扩展配置
        :rtype: Advanced
        """
        return self.advanced

    def get_tail_files(self):
        """
        :return: LogCollector采集策略，即指定LogCollector采集增量日志还是全量日志
        :rtype: bool
        """
        return self.tail_files

    def get_raw_log_key(self):
        """
        :return: 原始日志的键名
        :rtype: str
        """
        return self.raw_log_key

    def get_enable_hostname(self):
        """
        :return: 是否添加主机名字段
        :rtype: bool
        """
        return self.enable_hostname

    def get_hostname_key(self):
        """
        :return: 主机名字段的键名
        :rtype: str
        """
        return self.hostname_key

    def get_host_group_label_key(self):
        """
        :return: 主机分组标签字段的键名
        :rtype: str
        """
        return self.host_group_label_key

    def get_enable_host_group_label(self):
        """
        :return: 是否添加主机分组标签字段
        :rtype: bool
        """
        return self.enable_host_group_label
    def get_tail_size_kb(self):
        """
        :return: 增量采集的回溯阈值。
        :rtype: int
        """
        return self.tail_size_kb

    def get_ignore_older(self):
        """
        :return: 忽略多久没有更新的日志文件, 单位为小时。
        :rtype: int
        """
        return self.ignore_older

    def get_multi_collects_type(self):
        """
        :return: 允许多次采集日志文件。空、RuleID、TopicIDRuleName
        :rtype: str
        """
        return self.multi_collects_type



    @classmethod
    def set_attributes(cls, data: dict):
        user_define_rule = super(UserDefineRule, cls).set_attributes(data)

        if SHARD_HASH_KEY in data:
            user_define_rule.shard_hash_key = ShardHashKey(
                hash_key=data[SHARD_HASH_KEY].get(HASH_KEY))
        if PARSE_PATH_RULE in data:
            user_define_rule.parse_path_rule = ParsePathRule.set_attributes(
                data[PARSE_PATH_RULE])
        if PLUGIN in data:
            user_define_rule.plugin = Plugin(
                processors=data[PLUGIN].get(PROCESSORS))
        if ADVANCED in data:
            user_define_rule.advanced = Advanced(close_inactive=data[ADVANCED].get(CLOSE_INACTIVE),
                                                 close_timeout=data[ADVANCED].get(
                                                     CLOSE_TIMEOUT),
                                                 close_removed=data[ADVANCED].get(
                                                     CLOSE_REMOVED),
                                                 close_renamed=data[ADVANCED].get(
                                                     CLOSE_RENAMED),
                                                 no_line_terminator_eof_max_time=data[ADVANCED].get(NO_LINE_TERMINATOR_EOF_MAX_TIME),
                                                 close_eof=data[ADVANCED].get(CLOSE_EOF))

        return user_define_rule

    def json(self):
        json_data = super(UserDefineRule, self).json()

        if self.shard_hash_key is not None:
            json_data[SHARD_HASH_KEY] = self.shard_hash_key.json()
        if self.parse_path_rule is not None:
            json_data[PARSE_PATH_RULE] = self.parse_path_rule.json()
        if self.plugin is not None:
            json_data[PLUGIN] = self.plugin.json()
        if self.advanced is not None:
            json_data[ADVANCED] = self.advanced.json()

        return json_data


class KubernetesRule(TLSData):
    def __init__(self, namespace_name_regex: str = None, workload_type: str = None, workload_name_regex: str = None,
                 include_pod_label_regex: Dict[str, str] = None, exclude_pod_label_regex: Dict[str, str] = None,
                 pod_name_regex: str = None, label_tag: Dict[str, str] = None, annotation_tag: Dict[str, str] = None,
                 enable_all_label_tag: bool = False, exclude_pod_annotation_regex: Dict[str, str] = None,
                 include_pod_annotation_regex: Dict[str, str] = None,):
        """
        :param namespace_name_regex: 待采集的Kubernetes Namespace名称，不指定Namespace名称时表示采集全部容器
        :type namespace_name_regex: str
        :param workload_type: 通过工作负载的类型指定采集的容器，仅支持选择一种类型
        :type workload_type: str
        :param workload_name_regex: 通过工作负载的名称指定待采集的容器
        :type workload_name_regex: str
        :param include_pod_label_regex: Pod Label白名单用于指定待采集的容器
        :type include_pod_label_regex: Dict[str, str]
        :param exclude_pod_label_regex: 通过Pod Label黑名单指定不采集的容器，不启用表示采集全部容器
        :type exclude_pod_label_regex: Dict[str, str]
        :param pod_name_regex: Pod名称用于指定待采集的容器
        :type pod_name_regex: str
        :param label_tag: 是否将Kubernetes Label作为日志标签，添加到原始日志数据中
        :type label_tag: Dict[str, str]
        :param annotation_tag: 是否将Kubernetes Annotation作为日志标签，添加到原始日志数据中
        :type annotation_tag: Dict[str, str]
        :param enable_all_label_tag: 是否将所有 Kubernetes Label 作为日志标签，添加到原始日志数据中
        :type enable_all_label_tag: bool
        :param exclude_pod_annotation_regex: 通过 Pod Annotation 黑名单指定不采集的容器，不启用表示采集全部容器
        :type exclude_pod_annotation_regex: Dict[str, str]
        :param include_pod_annotation_regex: Pod Annotation 白名单用于指定待采集的容器
        :type include_pod_annotation_regex: Dict[str, str]
        """
        self.namespace_name_regex = namespace_name_regex
        self.workload_type = workload_type
        self.workload_name_regex = workload_name_regex
        self.include_pod_label_regex = include_pod_label_regex
        self.exclude_pod_label_regex = exclude_pod_label_regex
        self.pod_name_regex = pod_name_regex
        self.label_tag = label_tag
        self.annotation_tag = annotation_tag
        self.enable_all_label_tag = enable_all_label_tag
        self.exclude_pod_annotation_regex = exclude_pod_annotation_regex
        self.include_pod_annotation_regex = include_pod_annotation_regex

    def get_include_pod_label_regex(self):
        """
        :return: Pod Label 白名单用于指定待采集的容器
        :rtype:Dict[str, str]
        """
        return self.include_pod_label_regex

    def get_workload_name_regex(self):
        """
        :return: 通过工作负载的名称指定待采集的容器
        :rtype:str
        """
        return self.workload_name_regex

    def get_pod_name_regex(self):
        """
        :return: Pod名称用于指定待采集的容器
        :rtype: str
        """
        return self.pod_name_regex

    def get_exclude_pod_label_regex(self):
        """
        :return: 通过 Pod Label 黑名单指定不采集的容器，不启用表示采集全部容器
        :rtype: ict[str, str]
        """
        return self.exclude_pod_label_regex

    def get_label_tag(self):
        """
        :return: 是否将 Kubernetes Label 作为日志标签，添加到原始日志数据中
        :rtype: Dict[str, str]
        """
        return self.label_tag

    def get_namespace_name_regex(self):
        """
        :return: 待采集的 Kubernetes Namespace 名称，不指定 Namespace 名称时表示采集全部容器
        :rtype: str
        """
        return self.namespace_name_regex

    def get_workload_type(self):
        """
        :return:通过工作负载的类型指定采集的容器，仅支持选择一种类型
        :rtype: str
        """
        return self.workload_type

    def get_annotation_tag(self):
        """
        :return: 是否将Kubernetes Annotation作为日志标签，添加到原始日志数据中
        :rtype: Dict[str, str]
        """
        return self.annotation_tag
    def get_enable_all_label_tag(self):
        """
        :return: 是否将所有 Kubernetes Label 作为日志标签，添加到原始日志数据中
        :rtype: bool
        """
        return self.enable_all_label_tag
    def get_exclude_pod_annotation_regex(self):
        """
        :return: 通过 Pod Annotation 黑名单指定不采集的容器，不启用表示采集全部容器
        :rtype: Dict[str, str]
        """
        return self.exclude_pod_annotation_regex
    def get_include_pod_annotation_regex(self):
        """
        :return: Pod Annotation 白名单用于指定待采集的容器
        :rtype: Dict[str, str]
        """
        return self.include_pod_annotation_regex


class ContainerRule(TLSData):
    def __init__(self, stream: str = None, container_name_regex: str = None,
                 include_container_label_regex: Dict[str, str] = None,
                 exclude_container_label_regex: Dict[str, str] = None,
                 include_container_env_regex: Dict[str, str] = None,
                 exclude_container_env_regex: Dict[str, str] = None,
                 env_tag: Dict[str, str] = None, kubernetes_rule: KubernetesRule = None):
        """
        :param stream:采集模式
        :type stream:str
        :param container_name_regex:待采集的容器名称
        :type container_name_regex:str
        :param include_container_label_regex:指定待采集的容器，不启用白名单时指定采集全部容器
        :type include_container_label_regex:Dict[str, str]
        :param exclude_container_label_regex:黑名单用于指定不采集的容器范围，不启用黑名单时表示采集全部容器
        :type exclude_container_label_regex:Dict[str, str]
        :param include_container_env_regex:容器环境变量白名单通过容器环境变量指定待采集的容器，不启用白名单时表示指定采集全部容器
        :type include_container_env_regex:Dict[str, str]
        :param exclude_container_env_regex:容器环境变量黑名单用于指定不采集的容器范围，不启用黑名单时表示采集全部容器
        :type exclude_container_env_regex:Dict[str, str]
        :param env_tag:是否将环境变量作为日志标签，添加到原始日志数据中
        :type env_tag:Dict[str, str]
        :param kubernetes_rule:Kubernetes 容器的采集规则
        :type kubernetes_rule:KubernetesRule
        """
        self.stream = stream
        self.container_name_regex = container_name_regex
        self.include_container_label_regex = include_container_label_regex
        self.exclude_container_label_regex = exclude_container_label_regex
        self.include_container_env_regex = include_container_env_regex
        self.exclude_container_env_regex = exclude_container_env_regex
        self.env_tag = env_tag
        self.kubernetes_rule = kubernetes_rule

    def get_stream(self):
        """
        :return 采集模式
        :rtype str
        """
        return self.stream

    def get_exclude_container_env_regex(self):
        """
        :return: 容器环境变量黑名单用于指定不采集的容器范围，不启用黑名单时表示采集全部容器
        :rtype:Dict[str, str]
        """
        return self.exclude_container_env_regex

    def get_kubernetes_rule(self):
        """
        :return: Kubernetes 容器的采集规则
        :rtype: KubernetesRule
        """
        return self.kubernetes_rule

    def get_include_container_label_regex(self):
        """
        :return: 指定待采集的容器，不启用白名单时指定采集全部容器
        :rtype: Dict[str, str]
        """
        return self.include_container_label_regex

    def get_include_container_env_regex(self):
        """
        :return: 容器环境变量白名单通过容器环境变量指定待采集的容器，不启用白名单时表示指定采集全部容器
        :rtype: Dict[str, str]
        """
        return self.include_container_env_regex

    def get_exclude_container_label_regex(self):
        """
        :return: 黑名单用于指定不采集的容器范围，不启用黑名单时表示采集全部容器
        :rtype: Dict[str, str]
        """
        return self.exclude_container_label_regex

    def get_env_tag(self):
        """
        :return: 是否将环境变量作为日志标签，添加到原始日志数据中
        :rtype: Dict[str, str]
        """
        return self.env_tag

    def get_container_name_regex(self):
        """
        :return:待采集的容器名称
        :rtype: str
        """
        return self.container_name_regex

    @classmethod
    def set_attributes(cls, data: dict):
        container_rule = super(ContainerRule, cls).set_attributes(data)

        if KUBERNETES_RULE in data:
            container_rule.kubernetes_rule = KubernetesRule.set_attributes(
                data=data[KUBERNETES_RULE])

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
                 input_type: int = None, container_rule: ContainerRule = None, pause: int = None):
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
        self.pause = pause

    def get_exclude_paths(self):
        """
        :return:采集黑名单列表
        :rtype:List[ExcludePath]
        """
        return self.exclude_paths

    def get_create_time(self):
        """
        :return:采集配置创建的时间
        :rtype:str
        """
        return self.create_time

    def get_rule_name(self):
        """
        :return:采集配置的名称
        :rtype:str
        """
        return self.rule_name

    def get_container_rule(self):
        """
        :return:容器采集规则。详细说明请查看
        :rtype:ContainerRule
        """
        return self.container_rule

    def get_modify_time(self):
        return self.modify_time

    def get_input_type(self):
        return self.input_type

    def get_user_define_rule(self):
        return self.user_define_rule

    def get_rule_id(self):
        return self.rule_id

    def get_log_type(self):
        return self.log_type

    def get_extract_rule(self):
        return self.extract_rule

    def get_paths(self):
        return self.paths

    def get_topic_name(self):
        return self.topic_name

    def get_topic_id(self):
        return self.topic_id

    def get_pause(self):
        """
        :return: 采集配置的运行状态。0：运行中，1：已暂停
        :rtype: int
        """
        return self.pause

    def get_log_sample(self):
        return self.log_sample

    @classmethod
    def set_attributes(cls, data: dict):
        rule_info = super(RuleInfo, cls).set_attributes(data)

        if EXTRACT_RULE in data:
            rule_info.extract_rule = ExtractRule.set_attributes(
                data=data[EXTRACT_RULE])
        if EXCLUDE_PATHS in data:
            rule_info.exclude_paths = []
            for exclude_path in data[EXCLUDE_PATHS]:
                rule_info.exclude_paths.append(  # pylint: disable=no-member
                    ExcludePath.set_attributes(data=exclude_path))
        if USER_DEFINE_RULE in data:
            rule_info.user_define_rule = UserDefineRule.set_attributes(
                data=data[USER_DEFINE_RULE])
        if CONTAINER_RULE in data:
            rule_info.container_rule = ContainerRule.set_attributes(
                data=data[CONTAINER_RULE])

        return rule_info


class HostGroupHostsRulesInfo(TLSData):
    def __init__(self, host_group_info: HostGroupInfo, host_infos: List[HostInfo], rule_infos: List[RuleInfo]):
        self.host_group_info = host_group_info
        self.host_infos = host_infos
        self.rule_infos = rule_infos

    def get_rule_infos(self):
        """
        :return:所绑定的采集配置信息列表
        :rtype: List[RuleInfo]
        """
        return self.rule_infos

    def get_host_group_info(self):
        """
        :return: 机器组信息
        :rtype:HostGroupInfo
        """
        return self.host_group_info

    def get_host_infos(self):
        """
        :return:
        :rtype:List[HostInfo]
        """
        return self.host_infos





class Receiver(TLSData):
    def __init__(self, receiver_type: str, receiver_names: List[str], receiver_channels: List[str],
                 start_time: str, end_time: str, webhook: str = None, general_webhook_url: str = None,
                 general_webhook_body: str = None, alarm_webhook_at_users: List[str] = None,
                 alarm_webhook_is_at_all: bool = None, alarm_webhook_at_groups: List[str] = None,
                 general_webhook_method: str = None, general_webhook_headers: List['GeneralWebhookHeaderKV'] = None,
                 alarm_content_template_id: str = None, alarm_webhook_integration_id: str = None,
                 alarm_webhook_integration_name: str = None):
        """
        :param receiver_type:接受者类型
        :type receiver_type:str
        :param receiver_names:接收者的名字
        :type receiver_names:List[str]
        :param receiver_channels:通知接收渠道，支持Email、Sms、Phone
        :type receiver_channels:List[str]
        :param start_time:可接收信息的时段中，开始的时间
        :type start_time:str
        :param end_time:可接收信息的时段中
        :type end_time:str
        :param webhook:飞书Webhook请求地址
        :type webhook:str
        :param general_webhook_url:自定义接口回调地址
        :type general_webhook_url:str
        :param general_webhook_body:自定义 WebHook 请求体
        :type general_webhook_body:str
        :param alarm_webhook_at_users:通过 Webhook 集成配置发送通知到飞书、钉钉或企业微信时，需要提醒的用户名
        :type alarm_webhook_at_users:List[str]
        :param alarm_webhook_is_at_all:通过 Webhook 集成配置发送通知到飞书、钉钉或企业微信时，是否提醒所有人
        :type alarm_webhook_is_at_all:bool
        :param alarm_webhook_at_groups:通过 Webhook 集成配置发送通知到飞书、钉钉或企业微信时，需要提醒的用户组名称
        :type alarm_webhook_at_groups:List[str]
        :param general_webhook_method:自定义接口回调方法，仅支持设置为 POST 或 PUT
        :type general_webhook_method:str
        :param general_webhook_headers:自定义接口回调请求头
        :type general_webhook_headers:List[GeneralWebhookHeaderKV]
        :param alarm_content_template_id:告警内容模版 ID
        :type alarm_content_template_id:str
        :param alarm_webhook_integration_id:告警 Webhook 集成配置的 ID
        :type alarm_webhook_integration_id:str
        :param alarm_webhook_integration_name:告警 Webhook 集成配置的名称
        :type alarm_webhook_integration_name:str
        :type alarm_webhook_integration_name:str
        """
        self.receiver_type = receiver_type
        self.receiver_names = receiver_names
        self.receiver_channels = receiver_channels
        self.start_time = start_time
        self.end_time = end_time
        self.webhook = webhook
        self.general_webhook_url = general_webhook_url
        self.general_webhook_body = general_webhook_body
        self.alarm_webhook_at_users = alarm_webhook_at_users
        self.alarm_webhook_is_at_all = alarm_webhook_is_at_all
        self.alarm_webhook_at_groups = alarm_webhook_at_groups
        self.general_webhook_method = general_webhook_method
        self.general_webhook_headers = general_webhook_headers
        self.alarm_content_template_id = alarm_content_template_id
        self.alarm_webhook_integration_id = alarm_webhook_integration_id
        self.alarm_webhook_integration_name = alarm_webhook_integration_name

    def get_start_time(self):
        """
        :return:可接收信息的时段中，开始的时间
        :rtype: str
        """
        return self.start_time

    def get_webhook(self):
        """
        :return: 飞书Webhook请求地址
        :rtype: str
        """
        return self.webhook

    def get_receiver_channels(self):
        """
        :return:通知接收渠道，支持Email、Sms、Phone
        :rtype: List[str]
        """
        return self.receiver_channels

    def get_end_time(self):
        """
        :return: 可接收信息的时段中
        :rtype:str
        """
        return self.end_time

    def get_receiver_names(self):
        """
        :return: 接收者的名字
        :rtype: List[str]
        """
        return self.receiver_names

    def get_receiver_type(self):
        """
        :return:接受者类型
        :rtype: str
        """
        return self.receiver_type

    def get_general_webhook_url(self):
        """
        :return:自定义接口回调地址
        :rtype: str
        """
        return self.general_webhook_url

    def get_general_webhook_body(self):
        """
        :return:自定义 WebHook 请求体
        :rtype: str
        """
        return self.general_webhook_body

    def get_alarm_webhook_at_users(self):
        """
        :return:通过 Webhook 集成配置发送通知到飞书、钉钉或企业微信时，需要提醒的用户名
        :rtype: List[str]
        """
        return self.alarm_webhook_at_users

    def get_alarm_webhook_is_at_all(self):
        """
        :return:通过 Webhook 集成配置发送通知到飞书、钉钉或企业微信时，是否提醒所有人
        :rtype: bool
        """
        return self.alarm_webhook_is_at_all

    def get_alarm_webhook_at_groups(self):
        """
        :return:通过 Webhook 集成配置发送通知到飞书、钉钉或企业微信时，需要提醒的用户组名称
        :rtype: List[str]
        """
        return self.alarm_webhook_at_groups

    def get_general_webhook_method(self):
        """
        :return:自定义接口回调方法，仅支持设置为 POST 或 PUT
        :rtype: str
        """
        return self.general_webhook_method

    def get_general_webhook_headers(self):
        """
        :return:自定义接口回调请求头
        :rtype: List[GeneralWebhookHeaderKV]
        """
        return self.general_webhook_headers

    def get_alarm_content_template_id(self):
        """
        :return:告警内容模版 ID
        :rtype: str
        """
        return self.alarm_content_template_id

    def get_alarm_webhook_integration_id(self):
        """
        :return:告警 Webhook 集成配置的 ID
        :rtype: str
        """
        return self.alarm_webhook_integration_id

    def get_alarm_webhook_integration_name(self):
        """
        :return:告警 Webhook 集成配置的名称
        :rtype: str
        """
        return self.alarm_webhook_integration_name

    @classmethod
    def set_attributes(cls, data: dict):
        receiver_type = data.get(RECEIVER_TYPE)
        receiver_names = data.get(RECEIVER_NAMES)
        receiver_channels = data.get(RECEIVER_CHANNELS)
        start_time = data.get(START_TIME)
        end_time = data.get(END_TIME)
        webhook = data.get(WEBHOOK)
        general_webhook_url = data.get(GENERAL_WEBHOOK_URL)
        general_webhook_body = data.get(GENERAL_WEBHOOK_BODY)
        alarm_webhook_at_users = data.get(ALARM_WEBHOOK_AT_USERS)
        alarm_webhook_is_at_all = data.get(ALARM_WEBHOOK_IS_AT_ALL)
        alarm_webhook_at_groups = data.get(ALARM_WEBHOOK_AT_GROUPS)
        general_webhook_method = data.get(GENERAL_WEBHOOK_METHOD)
        alarm_content_template_id = data.get(ALARM_CONTENT_TEMPLATE_ID)
        alarm_webhook_integration_id = data.get(ALARM_WEBHOOK_INTEGRATION_ID)
        alarm_webhook_integration_name = data.get(ALARM_WEBHOOK_INTEGRATION_NAME)

        general_webhook_headers = None
        if GENERAL_WEBHOOK_HEADERS in data and data[GENERAL_WEBHOOK_HEADERS] is not None:
            general_webhook_headers = []
            for header in data[GENERAL_WEBHOOK_HEADERS]:
                general_webhook_headers.append(  # pylint: disable=no-member
                    GeneralWebhookHeaderKV.set_attributes(data=header))

        receiver = cls(receiver_type, receiver_names, receiver_channels, start_time, end_time, webhook,
                      general_webhook_url, general_webhook_body, alarm_webhook_at_users, alarm_webhook_is_at_all,
                      alarm_webhook_at_groups, general_webhook_method, general_webhook_headers,
                      alarm_content_template_id, alarm_webhook_integration_id, alarm_webhook_integration_name)

        return receiver

    def json(self):
        json_data = super(Receiver, self).json()

        if self.general_webhook_url is not None:
            json_data[GENERAL_WEBHOOK_URL] = self.general_webhook_url
        if self.general_webhook_body is not None:
            json_data[GENERAL_WEBHOOK_BODY] = self.general_webhook_body
        if self.alarm_webhook_at_users is not None:
            json_data[ALARM_WEBHOOK_AT_USERS] = self.alarm_webhook_at_users
        if self.alarm_webhook_is_at_all is not None:
            json_data[ALARM_WEBHOOK_IS_AT_ALL] = self.alarm_webhook_is_at_all
        if self.alarm_webhook_at_groups is not None:
            json_data[ALARM_WEBHOOK_AT_GROUPS] = self.alarm_webhook_at_groups
        if self.general_webhook_method is not None:
            json_data[GENERAL_WEBHOOK_METHOD] = self.general_webhook_method
        if self.general_webhook_headers is not None:
            json_data[GENERAL_WEBHOOK_HEADERS] = []
            for header in self.general_webhook_headers:
                json_data[GENERAL_WEBHOOK_HEADERS].append(header.json())
        if self.alarm_content_template_id is not None:
            json_data[ALARM_CONTENT_TEMPLATE_ID] = self.alarm_content_template_id
        if self.alarm_webhook_integration_id is not None:
            json_data[ALARM_WEBHOOK_INTEGRATION_ID] = self.alarm_webhook_integration_id
        if self.alarm_webhook_integration_name is not None:
            json_data[ALARM_WEBHOOK_INTEGRATION_NAME] = self.alarm_webhook_integration_name

        return json_data



class QueryRequest(TLSData):
    def __init__(self, topic_id: str, query: str, number: int,
                 start_time_offset: int, end_time_offset: int, topic_name: str = None, time_span_type: str = None,
                 truncated_time: str = None, end_time_offset_unit: str = None, start_time_offset_unit: str = None):
        """
        :param topic_id: 日志主题ID
        :type topic_id: str
        :param query: 查询语句，支持的最大长度为1024
        :type query: str
        :param number: 告警对象序号（从1开始递增）
        :type number: int
        :param start_time_offset: 查询范围起始时间相对当前的历史时间，单位为分钟，取值为非正，最大值为0，最小值为-1440
        :type start_time_offset: int
        :param end_time_offset: 查询范围终止时间相对当前的历史时间，单位为分钟，取值为非正，须大于StartTimeOffset，最大值为0，最小值为-1440
        :type end_time_offset: int
        :param topic_name: 告警策略执行的日志主题名称
        :type topic_name: str
        :param time_span_type: 查询是否是整点时间, 新增整点时间,非必填,空白时默认为Relative
        :type time_span_type: str
        :param truncated_time: 对时间取整,对分钟/小时取整
        :type truncated_time: str
        :param end_time_offset_unit: 查询结束时间范围单位, 默认值为分钟，支持秒/分钟/小时（Second，Minute，Hour）
        :type end_time_offset_unit: str
        :param start_time_offset_unit: 查询开始时间范围单位, 默认值为分钟，支持秒/分钟/小时（Second，Minute，Hour）
        :type start_time_offset_unit: str
        """
        self.topic_id = topic_id
        self.query = query
        self.number = number
        self.start_time_offset = start_time_offset
        self.end_time_offset = end_time_offset
        self.topic_name = topic_name
        self.time_span_type = time_span_type
        self.truncated_time = truncated_time
        self.end_time_offset_unit = end_time_offset_unit
        self.start_time_offset_unit = start_time_offset_unit

    def get_number(self):
        """
        :return:告警对象序号；从 1 开始递增
        :rtype: int
        """
        return self.number

    def get_start_time_offset(self):
        """
        :return: 查询范围起始时间相对当前的历史时间，单位为分钟，取值为非正，最大值为 0，最小值为 -1440
        :rtype: int
        """
        return self.start_time_offset

    def get_query(self):
        """
        :return:查询语句，支持的最大长度为 1024
        :rtype: str
        """
        return self.query

    def get_topic_name(self):
        """
        :return: 告警策略执行的日志主题名称
        :rtype: str
        """
        return self.topic_name

    def get_topic_id(self):
        """
        :return: 日志主题 ID
        :rtype: str
        """
        return self.topic_id

    def get_end_time_offset(self):
        """
        :return: 查询范围终止时间相对当前的历史时间，单位为分钟
        :rtype: int
        """
        return self.end_time_offset

    def get_time_span_type(self):
        """
        :return: 查询是否是整点时间, 新增整点时间,非必填,空白时默认为Relative
        :rtype: str
        """
        return self.time_span_type

    def get_truncated_time(self):
        """
        :return: 对时间取整,对分钟/小时取整
        :rtype: str
        """
        return self.truncated_time

    @classmethod
    def set_attributes(cls, data: dict):
        topic_id = data.get(TOPIC_ID)
        topic_name = data.get(TOPIC_NAME)
        query = data.get(QUERY)
        number = data.get(NUMBER)
        start_time_offset = data.get(START_TIME_OFFSET)
        end_time_offset = data.get(END_TIME_OFFSET)
        time_span_type = data.get(TIME_SPAN_TYPE)
        truncated_time = data.get(TRUNCATED_TIME)

        return cls(topic_id, query, number, start_time_offset, end_time_offset, topic_name, time_span_type, truncated_time)


class RequestCycle(TLSData):
    def __init__(self, cycle_type: str, time: int, cron_tab: str = None, cron_time_zone: str = None):
        """
        :param cycle_type: 执行周期类型，Period：周期执行，Fixed：定期执行，Cron：使用Cron表达式
        :type cycle_type:str
        :param time:告警任务执行的周期，或者定期执行的时间点。单位为分钟，取值范围为 1~1440
        :type time:int
        :param cron_tab:Cron表达式，日志服务通过 Cron 表达式指定告警任务定时执行。Cron 表达式的最小粒度为分钟，24 小时制
        :type cron_tab:str
        :param cron_time_zone:设置 Type 为 Cron 时，还需设置时区
        :type cron_time_zone:str
        """
        self.cycle_type = cycle_type
        self.time = time
        self.cron_tab = cron_tab
        self.cron_time_zone = cron_time_zone

    def get_time(self):
        """
        :return:告警任务执行的周期，或者定期执行的时间点。单位为分钟
        :rtype: int
        """
        return self.time

    def get_cycle_type(self):
        """
        :return:执行周期类型，Period：周期执行，Fixed：定期执行
        :rtype: str
        """
        return self.cycle_type

    def get_cron_tab(self):
        """
        :return:Cron表达式，日志服务通过 Cron 表达式指定告警任务定时执行
        :rtype: str
        """
        return self.cron_tab

    def get_cron_time_zone(self):
        """返回设置 Type 为 Cron 时的时区

        :return: 时区信息
        :rtype: str
        """
        return self.cron_time_zone

    @classmethod
    def set_attributes(cls, data: dict):
        cycle_type = data.get(TYPE)
        time = data.get(TIME)
        cron_tab = data.get(CRON_TAB)
        cron_time_zone = data.get(CRON_TIME_ZONE)

        return cls(cycle_type, time, cron_tab, cron_time_zone)

    def json(self):
        result = {TYPE: self.cycle_type, TIME: self.time}
        if self.cron_tab is not None:
            result[CRON_TAB] = self.cron_tab
        if self.cron_time_zone is not None:
            result[CRON_TIME_ZONE] = self.cron_time_zone
        return result


class AlarmNotifyGroupInfo(TLSData):
    def __init__(self, alarm_notify_group_name: str = None, alarm_notify_group_id: str = None,
                 notify_type: List[str] = None, receivers: List[Receiver] = None,
                 create_time: str = None, modify_time: str = None, iam_project_name: str = None,
                 notice_rules: List["NoticeRule"] = None):
        self.alarm_notify_group_name = alarm_notify_group_name
        self.alarm_notify_group_id = alarm_notify_group_id
        self.notify_type = notify_type
        self.receivers = receivers
        self.create_time = create_time
        self.modify_time = modify_time
        self.iam_project_name = iam_project_name
        self.notice_rules = notice_rules

    def get_alarm_notify_group_name(self):
        """
        :return:告警通知组名称
        :rtype: str
        """
        return self.alarm_notify_group_name

    def get_notify_type(self):
        """
        :return:告警通知的类型：Trigger - 告警触发，Recovery - 告警恢复
        :rtype: List[str]
        """
        return self.notify_type

    def get_create_time(self):
        """
        :return:告警通知组创建的时间
        :rtype:str
        """
        return self.create_time

    def get_receivers(self):
        """
        :return:接收告警的 IAM 用户列表
        :rtype:List[Receiver]
        """
        return self.receivers

    def get_modify_time(self):
        """
        :return:告警通知组修改的时间
        :rtype:str
        """
        return self.modify_time

    def get_alarm_notify_group_id(self):
        """
        :return:告警通知组 ID
        :rtype:str
        """
        return self.alarm_notify_group_id

    def get_iam_project_name(self):
        """
        :return: 告警组所属的IAM项目
        :rtype: str
        """
        return self.iam_project_name

    def get_notice_rules(self):
        """
        :return: 通知组规则
        :rtype: List[NoticeRule]
        """
        return self.notice_rules

    @classmethod
    def set_attributes(cls, data: dict):
        alarm_notify_group_info = super(
            AlarmNotifyGroupInfo, cls).set_attributes(data)

        if RECEIVERS in data:
            alarm_notify_group_info.receivers = []
            for receiver in data[RECEIVERS]:
                alarm_notify_group_info.receivers.append(  # pylint: disable=no-member
                    Receiver.set_attributes(data=receiver))

        if NOTICE_RULES in data and data[NOTICE_RULES] is not None:
            alarm_notify_group_info.notice_rules = []
            for notice_rule in data[NOTICE_RULES]:
                alarm_notify_group_info.notice_rules.append(  # pylint: disable=no-member
                    NoticeRule.set_attributes(data=notice_rule))

        return alarm_notify_group_info


class AlarmPeriodSetting(TLSData):
    def __init__(self, sms: int, phone: int, email: int, general_webhook: int):
        self.sms = sms
        self.phone = phone
        self.email = email
        self.general_webhook = general_webhook

    def json(self):
        return {SMS: self.sms, PHONE: self.phone, EMAIL: self.email, GENERAL_WEBHOOK: self.general_webhook}


class JoinConfig(TLSData):
    def __init__(self, set_operation_type: str = None, condition: str = None):
        self.condition = condition
        self.set_operation_type = set_operation_type


class TriggerCondition(TLSData):
    def __init__(self, severity: str = "notice", condition: str = None, count_condition: str = None, no_data: bool = None):
        self.severity = severity
        self.condition = condition
        self.count_condition = count_condition
        self.no_data = no_data


class AlarmInfo(TLSData):
    def __init__(self, alarm_name: str = None, alarm_id: str = None, project_id: str = None, status: bool = None,
                 query_request: List[QueryRequest] = None, request_cycle: RequestCycle = None, condition: str = None,
                 trigger_period: int = None, alarm_period: int = None,
                 alarm_notify_group: List[AlarmNotifyGroupInfo] = None, user_define_msg: str = None,
                 create_time: str = None, modify_time: str = None,
                 severity: str = None, alarm_period_detail: AlarmPeriodSetting = None,
                 join_configurations: List[JoinConfig] = None, trigger_conditions: List[TriggerCondition] = None,
                 send_resolved: bool = None):
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
        self.severity = severity
        self.alarm_period_detail = alarm_period_detail
        self.join_configurations = join_configurations
        self.trigger_conditions = trigger_conditions
        self.send_resolved = send_resolved

    def get_alarm_name(self):
        """
        :return:告警策略名称
        :rtype: str
        """
        return self.alarm_name

    def get_alarm_notify_group(self):
        """
        :return:告警对应的通知列表
        :rtype:List[AlarmNotifyGroupInfo]
        """
        return self.alarm_notify_group

    def get_request_cycle(self):
        """
        :return:告警任务的执行周期
        :rtype:RequestCycle
        """
        return self.request_cycle

    def get_alarm_period(self):
        """
        :return:告警重复的周期
        :rtype: int
        """
        return self.alarm_period

    def get_create_time(self):
        """
        :return:创建告警策略的时间
        :rtype:str
        """
        return self.create_time

    def get_modify_time(self):
        """
        :return:告警策略最近修改的时间
        :rtype:str
        """
        return self.modify_time

    def get_user_define_msg(self):
        """
        :return:告警通知的内容
        :rtype:str
        """
        return self.user_define_msg

    def get_condition(self):
        """
        :return:告警触发条件
        :rtype:str
        """
        return self.condition

    def get_query_request(self):
        """
        :return:检索分析语句，可配置 1~3 条
        :rtype:List[QueryRequest]
        """
        return self.query_request

    def get_project_id(self):
        """
        :return:日志项目 ID
        :rtype: str
        """
        return self.project_id

    def get_trigger_period(self):
        """
        :return:持续周期
        :rtype:int
        """
        return self.trigger_period

    def get_alarm_id(self):
        """
        :return:告警策略的 ID
        :rtype: str
        """
        return self.alarm_id

    def get_status(self):
        """
        :return:是否开启告警策略
        :rtype:bool
        """
        return self.status

    def get_severity(self):
        """
        :return: 告警通知的级别，即告警的严重程度
        :rtype: str
        """
        return self.severity

    def get_alarm_period_detail(self):
        """
        :return: 告警通知发送的周期
        :rtype: AlarmPeriodSetting
        """
        return self.alarm_period_detail

    def get_join_configurations(self):
        """
        :return: 告警策略的 Join 配置
        :rtype: List[JoinConfig]
        """
        return self.join_configurations

    def get_trigger_conditions(self):
        """
        :return: 告警策略的触发条件
        :rtype: List[TriggerCondition]
        """
        return self.trigger_conditions

    def get_send_resolved(self):
        """
        :return: 是否发送恢复通知
        :rtype: bool
        """
        return self.send_resolved

    @classmethod
    def set_attributes(cls, data: dict):
        alarm_info = super(AlarmInfo, cls).set_attributes(data)

        if REQUEST_CYCLE in data:
            alarm_info.request_cycle = RequestCycle.set_attributes(
                data=data[REQUEST_CYCLE])
        if QUERY_REQUEST in data:
            alarm_info.query_request = []
            for one_query_request in data[QUERY_REQUEST]:
                alarm_info.query_request.append(  # pylint: disable=no-member
                    QueryRequest.set_attributes(data=one_query_request))
        if ALARM_NOTIFY_GROUP in data:
            alarm_info.alarm_notify_group = []
            for alarm_notify_group in data[ALARM_NOTIFY_GROUP]:
                alarm_info.alarm_notify_group.append(  # pylint: disable=no-member
                    AlarmNotifyGroupInfo.set_attributes(data=alarm_notify_group))
        if ALARM_PERIOD_DETAIL in data:
            if len(data[ALARM_PERIOD_DETAIL]) == 0:
                alarm_info.alarm_period_detail = None
            else:
                sms = data[ALARM_PERIOD_DETAIL].get(SMS)
                phone = data[ALARM_PERIOD_DETAIL].get(PHONE)
                email = data[ALARM_PERIOD_DETAIL].get(EMAIL)
                general_webhook = data[ALARM_PERIOD_DETAIL].get(
                    GENERAL_WEBHOOK)
                alarm_info.alarm_period_detail = AlarmPeriodSetting(
                    sms, phone, email, general_webhook)
        if JOIN_CONFIGURATIONS in data and data[JOIN_CONFIGURATIONS] is not None:
            alarm_info.join_configurations = []
            for join_configuration in data[JOIN_CONFIGURATIONS]:
                alarm_info.join_configurations.append(  # pylint: disable=no-member
                    JoinConfig.set_attributes(data=join_configuration))
        if TRIGGER_CONDITIONS in data and data[TRIGGER_CONDITIONS] is not None:
            alarm_info.trigger_conditions = []
            for trigger_condition in data[TRIGGER_CONDITIONS]:
                alarm_info.trigger_conditions.append(  # pylint: disable=no-member
                    TriggerCondition.set_attributes(data=trigger_condition))
        if SEND_RESOLVED in data:
            alarm_info.send_resolved = data[SEND_RESOLVED]

        return alarm_info


class ConsumerGroup(TLSData):
    def __init__(self, project_id: str = None, consumer_group_name: str = None,
                 heartbeat_ttl: int = None, ordered_consume: bool = None, topic_id_list: List[str] = None,
                 project_name: str = None):
        self.project_id = project_id
        self.consumer_group_name = consumer_group_name
        self.heartbeat_ttl = heartbeat_ttl
        self.ordered_consume = ordered_consume
        self.topic_id_list = topic_id_list
        self.project_name = project_name

    @classmethod
    def set_attributes(cls, data: dict):
        project_id = data.get(PROJECT_ID_UPPERCASE)
        consumer_group_name = data.get(CONSUMER_GROUP_NAME)
        heartbeat_ttl = data.get(HEARTBEAT_TTL)
        ordered_consume = data.get(ORDERED_CONSUME)
        topic_id_list = data.get(TOPIC_ID_LIST)
        project_name = data.get(PROJECT_NAME)

        return cls(project_id, consumer_group_name, heartbeat_ttl, ordered_consume, topic_id_list, project_name)


class ConsumeShard(TLSData):
    def __init__(self, topic_id: str = None, shard_id: int = None):
        self.topic_id = topic_id
        self.shard_id = shard_id

    @classmethod
    def set_attributes(cls, data: dict):
        topic_id = data.get(TOPIC_ID_UPPERCASE)
        shard_id = data.get(SHARD_ID_UPPERCASE)

        return cls(topic_id, shard_id)

class TosSourceInfo(TLSData):
    def __init__(self, bucket: str = None, region: str = None, compress_type: str = None, prefix: str = None):
        """
        :param bucket: TOS 存储桶名称
        :type bucket: str
        :param region: TOS 存储桶所在区域
        :type region: str
        :param compress_type: 日志压缩类型，可选值为 "none"、"gzip"、"lz4"、"snappy"
        :type compress_type: str
        :param prefix: 日志文件前缀，例如 "log/"
        :type prefix: str, optional
        """
        self.bucket = bucket
        self.region = region
        self.compress_type = compress_type
        self.prefix = prefix

    def json(self):
        return {
            "bucket": self.bucket,
            "region": self.region,
            "compress_type": self.compress_type,
            "prefix": self.prefix,
        }

class KafkaSourceInfo(TLSData):
    def __init__(self, host: str = None, topic: str = None, encode: str = None, protocol: str = None,
                 is_need_auth: bool = None, initial_offset: int = None,
                 time_source_default: int = None, group: str = None, username: str = None, password: str = None,
                 mechanism: str = None, instance_id: str = None):
        """
        :param host: Kafka 集群地址，多个服务地址之间需使用半角逗号（,）分隔。
        :type host: str
        :param topic: Kafka Topic 名称。 多个 Kafka Topic 之间应使用半角逗号（,）分隔。
        :type topic: str
        :param encode: 数据的编码格式。可选值包括 UTF-8、GBK。
        :type encode: str
        :param protocol: Kafka 协议，可选值为 "plaintext"、"ssl"
        :type protocol: str
        :param is_need_auth: 是否开启鉴权。如果您使用的是公网服务地址，建议开启鉴权。
        :type is_need_auth: bool
        :param initial_offset: 数据导入的起始位置。0：最早时间，即从指定的 Kafka Topic 中的第一条数据开始导入；1：最近时间，即从指定的 Kafka Topic 中最新生成的数据开始导入。
        :type initial_offset: int, optional
        :param time_source_default: 指定日志时间。0：使用 Kafka 消息时间戳；1：使用系统当前时间。
        :type time_source_default: int, optional
        :param group: 消费者组 ID，可选值为 None
        :type group: str, optional
        :param username: 用于身份认证的 Kafka SASL 用户名。
        :type username: str, optional
        :param password: 用于身份认证的 Kafka SASL 用户密码。
        :type password: str, optional
        :param mechanism: 密码认证机制，可选值包括 PLAIN、SCRAM-SHA-256 和 SCRAM-SHA-512。
        :type mechanism: str, optional
        :param instance_id: 当您使用的是火山引擎消息队列 Kafka 版时，应设置为 Kafka 实例 ID。
        :type instance_id: str, optional
        """
        self.host = host
        self.topic = topic
        self.encode = encode
        self.protocol = protocol
        self.is_need_auth = is_need_auth
        self.initial_offset = initial_offset
        self.time_source_default = time_source_default
        self.group = group
        self.username = username
        self.password = password
        self.mechanism = mechanism
        self.instance_id = instance_id

    def json(self):
        return {
            "host": self.host,
            "topic": self.topic,
            "encode": self.encode,
            "protocol": self.protocol,
            "is_need_auth": self.is_need_auth,
            "initial_offset": self.initial_offset,
            "time_source_default": self.time_source_default,
            "group": self.group,
            "username": self.username,
            "password": self.password,
            "mechanism": self.mechanism,
            "instance_id": self.instance_id,
        }

class EsSourceInfo(TLSData):
    def __init__(self, endpoint: str = None, import_mode: str = None, index: str = None,
                 log_time_config: dict = None, max_import_time_delay_second: int = None,
                 password: str = None, query_string: str = None, username: str = None):
        """Elasticsearch 导入源配置

        :param endpoint: Elasticsearch 访问地址
        :type endpoint: str, optional
        :param import_mode: 导入模式
        :type import_mode: str, optional
        :param index: Elasticsearch 索引名称
        :type index: str, optional
        :param log_time_config: 日志时间字段配置，对应后端的 LogTimeConfig
        :type log_time_config: dict, optional
        :param max_import_time_delay_second: 最大导入时间延迟（秒）
        :type max_import_time_delay_second: int, optional
        :param password: Elasticsearch 访问密码
        :type password: str, optional
        :param query_string: 查询语句
        :type query_string: str, optional
        :param username: Elasticsearch 访问用户名
        :type username: str, optional
        """
        self.endpoint = endpoint
        self.import_mode = import_mode
        self.index = index
        self.log_time_config = log_time_config
        self.max_import_time_delay_second = max_import_time_delay_second
        self.password = password
        self.query_string = query_string
        self.username = username

    @classmethod
    def set_attributes(cls, data: dict):
        return super(EsSourceInfo, cls).set_attributes(data)

    def json(self):
        return {
            "endpoint": self.endpoint,
            "import_mode": self.import_mode,
            "index": self.index,
            "log_time_config": self.log_time_config,
            "max_import_time_delay_second": self.max_import_time_delay_second,
            "password": self.password,
            "query_string": self.query_string,
            "username": self.username,
        }


class ImportSourceInfo(TLSData):
    def __init__(self, tos_source_info: TosSourceInfo = None, kafka_source_info: KafkaSourceInfo = None,
                 es_source_info: EsSourceInfo = None):
        self.tos_source_info = tos_source_info
        self.kafka_source_info = kafka_source_info
        self.es_source_info = es_source_info

    @classmethod
    def set_attributes(cls, data: dict):
        tos_source_info = None
        kafka_source_info = None
        es_source_info = None
        if TOS_SOURCE_INFO in data:
            tos_source_info = TosSourceInfo.set_attributes(data=data[TOS_SOURCE_INFO])
        if KAFKA_SOURCE_INFO in data:
            kafka_source_info = KafkaSourceInfo.set_attributes(data=data[KAFKA_SOURCE_INFO])
        if "EsSourceInfo" in data:
            es_source_info = EsSourceInfo.set_attributes(data=data["EsSourceInfo"])

        return cls(tos_source_info, kafka_source_info, es_source_info)

    def json(self):
        source_info = {}
        if self.tos_source_info is not None:
            source_info[TOS_SOURCE_INFO] = self.tos_source_info.json()
        if self.kafka_source_info is not None:
            source_info[KAFKA_SOURCE_INFO] = self.kafka_source_info.json()
        if self.es_source_info is not None:
            source_info["EsSourceInfo"] = self.es_source_info.json()
        return source_info



class ImportExtractRule(TLSData):
    def __init__(self, delimiter: str = None, begin_regex: str = None, keys: List[str] = None,
                 time_key: str = None, time_format: str = None, time_zone: str = None, un_match_up_load_switch: bool = None,
                 un_match_log_key: str = None, quote: str = None, time_extract_regex: str = None, skip_line_count: int = None,
                 time_sample: str = None):
        assert (time_key is None and time_format is None) or (time_key is not None and time_format is not None)
        assert (un_match_up_load_switch is None and un_match_log_key is None) or \
               (un_match_up_load_switch is not None and un_match_log_key is not None)

        self.delimiter = delimiter
        self.begin_regex = begin_regex
        self.keys = keys
        self.time_key = time_key
        self.time_format = time_format
        self.time_zone = time_zone
        self.un_match_up_load_switch = un_match_up_load_switch
        self.un_match_log_key = un_match_log_key
        self.quote = quote
        self.time_extract_regex = time_extract_regex
        self.skip_line_count = skip_line_count
        self.time_sample = time_sample

class TargetInfo(TLSData):
    def __init__(self, region: str = None, log_type: str = None, extract_rule: ImportExtractRule = None, log_sample: str = None):
        """
        :param region: 日志主题所在区域
        :type region: str
        :param log_type: 日志类型:delimiter_log、multiline_log、minimalist_log、json_log
        :type log_type: str
        :param extract_rule: 提取规则
        :type extract_rule: ImportExtractRule, optional
        :param log_sample: 日志样例。设置 log_type 为 multiline_log 时，需要配置日志样例
        :type log_sample: str, optional
        """
        self.region = region
        self.log_type = log_type
        self.log_sample = log_sample
        self.extract_rule = extract_rule

    def json(self):
        target_info = super(TargetInfo, self).json()
        if self.extract_rule is not None:
            target_info[EXTRACT_RULE] = self.extract_rule.json()
        return target_info

    @classmethod
    def set_attributes(cls, data: dict):
        target_info = super(TargetInfo, cls).set_attributes(data)
        if EXTRACT_RULE in data:
            target_info.extract_rule = ImportExtractRule.set_attributes(data=data[EXTRACT_RULE])
        return target_info

class TaskStatistics(TLSData):
    def __init__(self, total: int = None, failed: int = None, skipped: int = None, not_exist: int = None,
                 bytes_total: int = None, task_status: str = None, transferred: int = None, bytes_transferred: int = None,):
        self.total = total
        self.failed = failed
        self.skipped = skipped
        self.not_exist = not_exist
        self.bytes_total = bytes_total
        self.task_status = task_status
        self.transferred = transferred
        self.bytes_transferred = bytes_transferred


class ImportTaskInfo(TLSData):
    def __init__(self, task_id: str = None, status: int = None, topic_id: str = None, task_name: str = None, project_id: str = None,
                 topic_name: str = None, project_name: str = None, create_time: str = None, source_type: str = None, description: str = None,
                 import_source_info: ImportSourceInfo = None, target_info: TargetInfo = None, task_statistics: TaskStatistics = None):
        self.task_id = task_id
        self.status = status
        self.topic_id = topic_id
        self.task_name = task_name
        self.project_id = project_id
        self.topic_name = topic_name
        self.project_name = project_name
        self.create_time = create_time
        self.source_type = source_type
        self.description = description
        self.import_source_info = import_source_info
        self.target_info = target_info
        self.task_statistics = task_statistics

    @classmethod
    def set_attributes(cls, data: dict):
        import_task_info = super(ImportTaskInfo, cls).set_attributes(data)
        if TASK_STATISTICS in data:
            import_task_info.task_statistics = TaskStatistics.set_attributes(data=data[TASK_STATISTICS])

        if IMPORT_SOURCE_INFO in data:
            import_task_info.import_source_info = ImportSourceInfo.set_attributes(data=data[IMPORT_SOURCE_INFO])

        if TARGET_INFO in data:
            import_task_info.target_info = TargetInfo.set_attributes(data=data[TARGET_INFO])

        return import_task_info

class JsonInfo(TLSData):
    def __init__(self, enable: bool = None, keys: List[str] = None, escape: bool = None):
        """
        :param enable: 启用标志
        :type enable: bool, optional
        :param keys: 需要投递的字段列表
        :type keys: List[str], optional
        :param escape: 是否转义
        :type escape: bool, optional
        """
        self.enable = enable
        self.keys = keys
        self.escape = escape


class CsvInfo(TLSData):
    def __init__(self, keys: List[str] = None, delimiter: str = None, escape_char: str = None,
                 print_header: bool = None, non_field_content: str = None):
        """
        :param keys: 需要投递的字段列表
        :type keys: List[str], optional
        :param delimiter: 分隔符
        :type delimiter: str, optional
        :param escape_char: 转义符
        :type escape_char: str, optional
        :param print_header: 首行是否打印Key
        :type print_header: bool, optional
        :param non_field_content: 无效字段填充内容
        :type non_field_content: str, optional
        """
        self.keys = keys
        self.delimiter = delimiter
        self.escape_char = escape_char
        self.print_header = print_header
        self.non_field_content = non_field_content

class ContentInfo(TLSData):
    def __init__(self, format: str = None, json_info: JsonInfo = None, csv_info: CsvInfo = None):
        """
        :param format: 日志内容解析格式,投递到 TOS 时，支持配置为 json、csv。投递到 Kafka 时，支持配置为 original、json。
        :type format: str, optional
        :param json_info: JSON格式日志内容配置
        :type json_info: JsonInfo, optional
        :param csv_info: CSV格式日志内容配置
        :type csv_info: CsvInfo, optional
        """
        self.format = format
        self.json_info = json_info
        self.csv_info = csv_info

    def json(self):
        content_info = super(ContentInfo, self).json()
        if self.json_info:
            content_info[JSON_INFO] = self.json_info.json()
        if self.csv_info:
            content_info[CSV_INFO] = self.csv_info.json()
        return content_info

    @classmethod
    def set_attributes(cls, data: dict):
        content_info = super(ContentInfo, cls).set_attributes(data)
        if JSON_INFO in data:
            content_info.json_info = JsonInfo.set_attributes(data=data[JSON_INFO])

        if CSV_INFO in data:
            content_info.csv_info = CsvInfo.set_attributes(data=data[CSV_INFO])

        return content_info



class TosShipperInfo(TLSData):
    def __init__(self, bucket: str = None, prefix: str = None, max_size: int = None, compress: str = None,
                 interval: int = None, partition_format: str = None):
        """
        :param bucket: TOS存储桶名称
        :type bucket: str, optional
        :param prefix: 存储桶的顶级目录名称
        :type prefix: str, optional
        :param max_size: 每个分区最大可投递的原始文件大小，单位为MiB
        :type max_size: int, optional
        :param compress: 压缩格式
        :type compress: str, optional
        :param interval: 投递时间间隔，单位为秒
        :type interval: int, optional
        :param partition_format: 投递日志的分区规则
        :type partition_format: str, optional
        """
        self.bucket = bucket
        self.prefix = prefix
        self.max_size = max_size
        self.compress = compress
        self.interval = interval
        self.partition_format = partition_format


class KafkaShipperInfo(TLSData):
    def __init__(self, instance: str = None, kafka_topic: str = None, compress: str = None,
                 start_time: int = None, end_time: int = None):
        """
        :param instance: Kafka实例
        :type instance: str, optional
        :param kafka_topic: Kafka Topic名称
        :type kafka_topic: str, optional
        :param compress: 压缩格式
        :type compress: str, optional
        :param start_time: 投递开始时间，毫秒时间戳
        :type start_time: int, optional
        :param end_time: 投递结束时间，毫秒时间戳
        :type end_time: int, optional
        """
        self.instance = instance
        self.kafka_topic = kafka_topic
        self.compress = compress
        self.start_time = start_time
        self.end_time = end_time


class ShipperInfo(TLSData):
    def __init__(self, shipper_id: str = None, shipper_name: str = None, project_id: str = None,
                 project_name: str = None, topic_id: str = None, topic_name: str = None,
                 shipper_type: str = None, status: bool = None, create_time: str = None,
                 modify_time: str = None, shipper_start_time: int = None, shipper_end_time: int = None,
                 content_info: ContentInfo = None, tos_shipper_info: TosShipperInfo = None,
                 kafka_shipper_info: KafkaShipperInfo = None, dashboard_id: str = None,
                 role_trn: str = None):
        """
        :param shipper_id: 投递配置ID
        :type shipper_id: str, optional
        :param shipper_name: 投递配置名称
        :type shipper_name: str, optional
        :param project_id: 日志项目ID
        :type project_id: str, optional
        :param project_name: 日志项目名称
        :type project_name: str, optional
        :param topic_id: 日志主题ID
        :type topic_id: str, optional
        :param topic_name: 日志主题名称
        :type topic_name: str, optional
        :param shipper_type: 投递类型
        :type shipper_type: str, optional
        :param status: 是否开启投递配置
        :type status: bool, optional
        :param create_time: 创建时间
        :type create_time: str, optional
        :param modify_time: 修改时间
        :type modify_time: str, optional
        :param shipper_start_time: 投递开始时间
        :type shipper_start_time: int, optional
        :param shipper_end_time: 投递结束时间
        :type shipper_end_time: int, optional
        :param content_info: 日志内容的投递格式配置
        :type content_info: ContentInfo, optional
        :param tos_shipper_info: 投递到TOS的相关信息
        :type tos_shipper_info: TosShipperInfo, optional
        :param kafka_shipper_info: 投递到Kafka的相关信息
        :type kafka_shipper_info: KafkaShipperInfo, optional
        :param dashboard_id: 投递的默认内置仪表盘ID
        :type dashboard_id: str, optional
        :param role_trn: 自定义角色的Trn
        :type role_trn: str, optional
        """
        self.shipper_id = shipper_id
        self.shipper_name = shipper_name
        self.project_id = project_id
        self.project_name = project_name
        self.topic_id = topic_id
        self.topic_name = topic_name
        self.shipper_type = shipper_type
        self.status = status
        self.create_time = create_time
        self.modify_time = modify_time
        self.shipper_start_time = shipper_start_time
        self.shipper_end_time = shipper_end_time
        self.content_info = content_info
        self.tos_shipper_info = tos_shipper_info
        self.kafka_shipper_info = kafka_shipper_info
        self.dashboard_id = dashboard_id
        self.role_trn = role_trn

    @classmethod
    def set_attributes(cls, data: dict):
        shipper_info = super(ShipperInfo, cls).set_attributes(data)
        if CONTENT_INFO in data:
            shipper_info.content_info = ContentInfo.set_attributes(data=data[CONTENT_INFO])
        if TOS_SHIPPER_INFO in data:
            shipper_info.tos_shipper_info = TosShipperInfo.set_attributes(data=data[TOS_SHIPPER_INFO])
        if KAFKA_SHIPPER_INFO in data:
            shipper_info.kafka_shipper_info = KafkaShipperInfo.set_attributes(data=data[KAFKA_SHIPPER_INFO])
        return shipper_info


class TargetResource(TLSData):
    def __init__(self, alias: str, topic_id: str, region: str, role_trn: str = None):
        """
        :param alias: 自定义输出目标的名称，在数据加工规则中需要使用此名称指代输出目标
        :type alias: str
        :param topic_id: 用于存储加工后日志的日志主题
        :type topic_id: str
        :param region: 用于存储加工后日志的日志主题的地域
        :type region: str
        :param role_trn: 跨账号授权角色名
        :type role_trn: str, optional
        """
        self.alias = alias
        self.topic_id = topic_id
        self.region = region
        self.role_trn = role_trn


class TraceInstanceInfo(TLSData):
    def __init__(self, trace_instance_id: str = None, trace_instance_name: str = None, project_id: str = None,
                 project_name: str = None, trace_topic_id: str = None, trace_topic_name: str = None,
                 dependency_topic_id: str = None, dependency_topic_topic_name: str = None,
                 trace_instance_status: str = None, description: str = None,
                 create_time: str = None, modify_time: str = None):
        """
        :param trace_instance_id: Trace实例ID
        :type trace_instance_id: str, optional
        :param trace_instance_name: Trace实例名称
        :type trace_instance_name: str, optional
        :param project_id: 日志项目ID
        :type project_id: str, optional
        :param project_name: 日志项目名称
        :type project_name: str, optional
        :param trace_topic_id: Trace Topic ID
        :type trace_topic_id: str, optional
        :param trace_topic_name: Trace Topic名称
        :type trace_topic_name: str, optional
        :param dependency_topic_id: Dependency Topic ID
        :type dependency_topic_id: str, optional
        :param dependency_topic_topic_name: Dependency Topic名称
        :type dependency_topic_topic_name: str, optional
        :param trace_instance_status: Trace实例状态
        :type trace_instance_status: str, optional
        :param description: Trace实例描述
        :type description: str, optional
        :param create_time: 创建时间
        :type create_time: str, optional
        :param modify_time: 修改时间
        :type modify_time: str, optional
        """
        self.trace_instance_id = trace_instance_id
        self.trace_instance_name = trace_instance_name
        self.project_id = project_id
        self.project_name = project_name
        self.trace_topic_id = trace_topic_id
        self.trace_topic_name = trace_topic_name
        self.dependency_topic_id = dependency_topic_id
        self.dependency_topic_topic_name = dependency_topic_topic_name
        self.trace_instance_status = trace_instance_status
        self.description = description
        self.create_time = create_time
        self.modify_time = modify_time

    def get_trace_instance_id(self):
        """返回 Trace实例ID"""
        return self.trace_instance_id

    def get_trace_instance_name(self):
        """返回 Trace实例名称"""
        return self.trace_instance_name

    def get_trace_instance_status(self):
        """返回 Trace实例状态"""
        return self.trace_instance_status

    def get_project_id(self):
        """返回 日志项目ID"""
        return self.project_id

    def get_project_name(self):
        """返回 日志项目名称"""
        return self.project_name

    def get_description(self):
        """返回 Trace实例描述"""
        return self.description

    def get_create_time(self):
        """返回 创建时间"""
        return self.create_time

    def get_modify_time(self):
        """返回 修改时间"""
        return self.modify_time

    def get_trace_topic_id(self):
        """返回 Trace Topic ID"""
        return self.trace_topic_id

    def get_trace_topic_name(self):
        """返回 Trace Topic名称"""
        return self.trace_topic_name

    def get_dependency_topic_id(self):
        """返回 Dependency Topic ID"""
        return self.dependency_topic_id

    def get_dependency_topic_topic_name(self):
        """返回 Dependency Topic名称"""
        return self.dependency_topic_topic_name


class TargetResourceInfo(TLSData):
    def __init__(self, alias: str = None, topic_id: str = None, project_id: str = None,
                 project_name: str = None, region: str = None, topic_name: str = None, role_trn: str = None):
        """\
        :param alias: 自定义输出目标的名称
        :type alias: str
        :param topic_id: 用于存储加工后日志的日志主题 ID
        :type topic_id: str
        :param project_id: 用于存储加工后日志的日志项目 ID
        :type project_id: str
        :param project_name: 用于存储加工后日志的日志项目名称
        :type project_name: str
        :param region: 用于存储加工后日志的日志项目所属地域
        :type region: str
        :param topic_name: 用于存储加工后日志的日志主题名称
        :type topic_name: str
        :param role_trn: 跨账号授权角色名
        :type role_trn: str
        """
        self.alias = alias
        self.topic_id = topic_id
        self.project_id = project_id
        self.project_name = project_name
        self.region = region
        self.topic_name = topic_name
        self.role_trn = role_trn

    def get_alias(self):
        """\
        :return: 自定义输出目标的名称
        :rtype: str
        """
        return self.alias

    def get_topic_id(self):
        """\
        :return: 用于存储加工后日志的日志主题 ID
        :rtype: str
        """
        return self.topic_id

    def get_project_id(self):
        """\
        :return: 用于存储加工后日志的日志项目 ID
        :rtype: str
        """
        return self.project_id

    def get_project_name(self):
        """\
        :return: 用于存储加工后日志的日志项目名称
        :rtype: str
        """
        return self.project_name

    def get_region(self):
        """\
        :return: 用于存储加工后日志的日志项目所属地域
        :rtype: str
        """
        return self.region

    def get_topic_name(self):
        """\
        :return: 用于存储加工后日志的日志主题名称
        :type topic_name: str
        """
        return self.topic_name

    def get_role_trn(self):
        """\
        :return: 跨账号授权角色名
        :rtype: str
        """
        return self.role_trn


class EtlTaskInfo(TLSData):
    def __init__(
            self,
            task_id: str = None,
            name: str = None,
            source_topic_id: str = None,
            source_topic_name: str = None,
            dsl_type: str = None,
            script: str = None,
            task_type: str = None,
            target_resources: List[TargetResourceInfo] = None,
            enable: bool = None,
            description: str = None,
            etl_status: str = None,
            from_time: int = None,
            to_time: int = None,
            create_time: str = None,
            modify_time: str = None,
            last_enable_time: str = None,
            dashboard_id: str = None,
            project_id: str = None,
            project_name: str = None):
        """ETL 任务信息

        对应服务端 DescribeETLTaskResp 结构，用于承载 DescribeETLTasks 返回的单个任务。
        """
        self.task_id = task_id
        self.name = name
        self.source_topic_id = source_topic_id
        self.source_topic_name = source_topic_name
        self.dsl_type = dsl_type
        self.script = script
        self.task_type = task_type
        self.target_resources = target_resources
        self.enable = enable
        self.description = description
        self.etl_status = etl_status
        self.from_time = from_time
        self.to_time = to_time
        self.create_time = create_time
        self.modify_time = modify_time
        self.last_enable_time = last_enable_time
        self.dashboard_id = dashboard_id
        self.project_id = project_id
        self.project_name = project_name

    @classmethod
    def set_attributes(cls, data: dict):
        etl_task_info = super(EtlTaskInfo, cls).set_attributes(data)

        if ETL_TARGET_RESOURCES in data and data[ETL_TARGET_RESOURCES] is not None:
            etl_task_info.target_resources = []
            for target_resource in data[ETL_TARGET_RESOURCES]:
                etl_task_info.target_resources.append(  # pylint: disable=no-member
                    TargetResourceInfo.set_attributes(data=target_resource)
                )

        return etl_task_info

class RequestCycleInfo(TLSData):
    def __init__(self, time: int = None, task_type: str = None, cron_tab: str = None, cron_time_zone: str = None):
        """
        :param time: 调度的周期或者定期执行的时间点（距离 00:00 的分钟数），取值范围为 1~1440，单位为分钟
        :type time: int, optional
        :param task_type: 调度周期类型。可选值：Period：按照周期进行调度，即每隔一段时间调度一次。
                         Fixed：定期调度，即每天固定时间点调度一次。Cron：使用 Cron 表达式
        :type task_type: str, optional
        :param cron_tab: Cron 表达式，日志服务通过 Cron 表达式指定告警任务定时执行。
                        Cron 表达式的最小粒度为分钟，24 小时制
        :type cron_tab: str, optional
        :param cron_time_zone: 设置 Type 为 Cron 时，还需设置时区
        :type cron_time_zone: str, optional
        """
        self.time = time
        self.type = task_type  # 使用 type 字段以匹配 API 响应格式
        self.cron_tab = cron_tab
        self.cron_time_zone = cron_time_zone


class ScheduleSqlTaskInfo(TLSData):
    def __init__(self, task_id: str = None, task_name: str = None, description: str = None,
                 source_project_id: str = None, source_project_name: str = None,
                 source_topic_id: str = None, source_topic_name: str = None,
                 dest_region: str = None, dest_project_id: str = None,
                 dest_topic_id: str = None, dest_topic_name: str = None,
                 status: int = None, process_start_time: int = None,
                 process_end_time: int = None, process_sql_delay: int = None,
                 process_time_window: str = None, query: str = None,
                 request_cycle: RequestCycleInfo = None, create_time_stamp: int = None,
                 modify_time_stamp: int = None):
        """
        :param task_id: 定时 SQL 分析任务 ID
        :type task_id: str, optional
        :param task_name: 定时 SQL 分析任务名称
        :type task_name: str, optional
        :param description: 定时 SQL 分析任务的简单描述
        :type description: str, optional
        :param source_project_id: 源日志主题所属的日志项目 ID
        :type source_project_id: str, optional
        :param source_project_name: 源日志主题所属的日志项目名称
        :type source_project_name: str, optional
        :param source_topic_id: 进行定时 SQL 分析的原始日志所在的源日志主题 ID
        :type source_topic_id: str, optional
        :param source_topic_name: 进行定时 SQL 分析的原始日志所在的源日志主题名称
        :type source_topic_name: str, optional
        :param dest_region: 目标日志项目所属地域
        :type dest_region: str, optional
        :param dest_project_id: 用于存储定时 SQL 分析结果数据的目标日志主题所属日志项目
        :type dest_project_id: str, optional
        :param dest_topic_id: 用于存储定时 SQL 分析结果数据的目标日志主题 ID
        :type dest_topic_id: str, optional
        :param dest_topic_name: 用于存储定时 SQL 分析结果数据的目标日志主题名称
        :type dest_topic_name: str, optional
        :param status: 完成任务配置后是否立即启动定时 SQL 分析任务。0：关闭任务，后续需手动启动任务。1：立即启动
        :type status: int, optional
        :param process_start_time: 调度定时 SQL 任务的开始时间，即第一个实例的创建时间。格式为秒级时间戳
        :type process_start_time: int, optional
        :param process_end_time: 调度定时 SQL 任务的结束时间。格式为秒级时间戳
        :type process_end_time: int, optional
        :param process_sql_delay: 每次调度的延迟时间。单位为秒
        :type process_sql_delay: int, optional
        :param process_time_window: SQL 时间窗口
        :type process_time_window: str, optional
        :param query: 定时 SQL 分析任务定期执行的检索与分析语句
        :type query: str, optional
        :param request_cycle: 定时 SQL 分析任务的调度周期
        :type request_cycle: RequestCycleInfo, optional
        :param create_time_stamp: 定时 SQL 分析任务的创建时间
        :type create_time_stamp: int, optional
        :param modify_time_stamp: 定时 SQL 分析任务的最近一次修改时间
        :type modify_time_stamp: int, optional
        """
        self.task_id = task_id
        self.task_name = task_name
        self.description = description
        # 规范字段名：source_project_id/source_topic_id/dest_project_id/dest_topic_id
        self.source_project_id = source_project_id
        self.source_project_name = source_project_name
        self.source_topic_id = source_topic_id
        self.source_topic_name = source_topic_name
        self.dest_region = dest_region
        self.dest_project_id = dest_project_id
        self.dest_topic_id = dest_topic_id
        self.dest_topic_name = dest_topic_name
        self.status = status
        self.process_start_time = process_start_time
        self.process_end_time = process_end_time
        self.process_sql_delay = process_sql_delay
        self.process_time_window = process_time_window
        self.query = query
        self.request_cycle = request_cycle
        self.create_time_stamp = create_time_stamp
        self.modify_time_stamp = modify_time_stamp

    @classmethod
    def set_attributes(cls, data: dict):
        schedule_sql_task_info = super(ScheduleSqlTaskInfo, cls).set_attributes(data)

        # 处理嵌套的 RequestCycle 对象
        if REQUEST_CYCLE in data and data[REQUEST_CYCLE] is not None:
            schedule_sql_task_info.request_cycle = RequestCycleInfo.set_attributes(data=data[REQUEST_CYCLE])

        return schedule_sql_task_info


class DingTalkContentTemplateInfo(TLSData):
    def __init__(self, title: str = None, locale: str = None, content: str = None):
        """
        :param title: 告警通知内容的主题
        :param locale: 告警通知中固定内容的语言，可选值为 zh-CN、en-US
        :param content: 告警通知内容，支持普通文本格式，支持插入内容变量、内容函数等
        """
        self.title = title
        self.locale = locale
        self.content = content


class EmailContentTemplateInfo(TLSData):
    def __init__(self, locale: str = None, content: str = None, subject: str = None):
        """
        :param locale: 告警通知中固定内容的语言，可选值为 zh-CN、en-US
        :param content: 告警通知内容，支持普通文本格式，支持插入内容变量、内容函数等
        :param subject: 邮件通知的主题
        """
        self.locale = locale
        self.content = content
        self.subject = subject


class LarkContentTemplateInfo(TLSData):
    def __init__(self, title: str = None, locale: str = None, content: str = None):
        """
        :param title: 告警通知内容的主题
        :param locale: 告警通知中固定内容的语言，可选值为 zh-CN、en-US
        :param content: 告警通知内容，支持普通文本格式，支持插入内容变量、内容函数等
        """
        self.title = title
        self.locale = locale
        self.content = content


class SmsContentTemplateInfo(TLSData):
    def __init__(self, locale: str = None, content: str = None):
        """
        :param locale: 告警通知中固定内容的语言，可选值为 zh-CN、en-US
        :param content: 告警通知内容，支持普通文本格式，支持插入内容变量、内容函数等
        """
        self.locale = locale
        self.content = content


class VmsContentTemplateInfo(TLSData):
    def __init__(self, locale: str = None, content: str = None):
        """
        :param locale: 告警通知中固定内容的语言，可选值为 zh-CN、en-US
        :param content: 告警通知内容，支持普通文本格式，支持插入内容变量、内容函数等
        """
        self.locale = locale
        self.content = content


class WeChatContentTemplateInfo(TLSData):
    def __init__(self, title: str = None, locale: str = None, content: str = None):
        """
        :param title: 告警通知内容的主题
        :param locale: 告警通知中固定内容的语言，可选值为 zh-CN、en-US
        :param content: 告警通知内容，支持普通文本格式，支持插入内容变量、内容函数等
        """
        self.title = title
        self.locale = locale
        self.content = content


class WebhookContentTemplateInfo(TLSData):
    def __init__(self, content: str = None):
        """
        :param content: 告警通知内容，通常为 JSON 格式，支持插入内容变量、内容函数等
        """
        self.content = content


class ContentTemplateInfo(TLSData):
    def __init__(self, sms: SmsContentTemplateInfo = None, vms: VmsContentTemplateInfo = None,
                 lark: LarkContentTemplateInfo = None, email: EmailContentTemplateInfo = None,
                 we_chat: WeChatContentTemplateInfo = None, webhook: WebhookContentTemplateInfo = None,
                 ding_talk: DingTalkContentTemplateInfo = None, is_default: bool = None,
                 create_time: str = None, modify_time: str = None,
                 alarm_content_template_id: str = None,
                 alarm_content_template_name: str = None):
        """告警内容模板信息

        :param sms: 短信通知内容模板相关信息
        :type sms: SmsContentTemplateInfo
        :param vms: 电话通知内容模板相关信息
        :type vms: VmsContentTemplateInfo
        :param lark: 飞书通知内容模板相关信息
        :type lark: LarkContentTemplateInfo
        :param email: 邮件通知内容模板相关信息
        :type email: EmailContentTemplateInfo
        :param we_chat: 企业微信通知内容模板相关信息
        :type we_chat: WeChatContentTemplateInfo
        :param webhook: 自定义 Webhook 通知内容模板相关信息
        :type webhook: WebhookContentTemplateInfo
        :param ding_talk: 钉钉通知内容模板相关信息
        :type ding_talk: DingTalkContentTemplateInfo
        :param is_default: 是否为内置的内容模版
        :type is_default: bool
        :param create_time: 告警通知内容模版的创建时间
        :type create_time: str
        :param modify_time: 告警通知内容模板的修改时间
        :type modify_time: str
        :param alarm_content_template_id: 告警通知内容模板 ID
        :type alarm_content_template_id: str
        :param alarm_content_template_name: 告警通知内容模板名称
        :type alarm_content_template_name: str
        """
        self.sms = sms
        self.vms = vms
        self.lark = lark
        self.email = email
        self.we_chat = we_chat
        self.webhook = webhook
        self.ding_talk = ding_talk
        self.is_default = is_default
        self.create_time = create_time
        self.modify_time = modify_time
        self.alarm_content_template_id = alarm_content_template_id
        self.alarm_content_template_name = alarm_content_template_name

    @classmethod
    def set_attributes(cls, data: dict):
        content_template_info = super(ContentTemplateInfo, cls).set_attributes(data)

        sms_data = data.get("Sms")
        if sms_data is None:
            sms_data = data.get(SMS)
        if sms_data is not None:
            content_template_info.sms = SmsContentTemplateInfo.set_attributes(sms_data)

        if VMS in data and data[VMS] is not None:
            content_template_info.vms = VmsContentTemplateInfo.set_attributes(data[VMS])

        if LARK in data and data[LARK] is not None:
            content_template_info.lark = LarkContentTemplateInfo.set_attributes(data[LARK])

        if EMAIL in data and data[EMAIL] is not None:
            content_template_info.email = EmailContentTemplateInfo.set_attributes(data[EMAIL])

        if WE_CHAT in data and data[WE_CHAT] is not None:
            content_template_info.we_chat = WeChatContentTemplateInfo.set_attributes(data[WE_CHAT])

        if WEBHOOK in data and data[WEBHOOK] is not None:
            content_template_info.webhook = WebhookContentTemplateInfo.set_attributes(data[WEBHOOK])

        if DING_TALK in data and data[DING_TALK] is not None:
            content_template_info.ding_talk = DingTalkContentTemplateInfo.set_attributes(data[DING_TALK])

        return content_template_info


class GeneralWebhookHeaderKV(TLSData):
    def __init__(self, key: str = None, value: str = None):
        """自定义 Webhook 请求头键值对

        :param key: 自定义请求头的 Key
        :type key: str
        :param value: 自定义请求头的 Value
        :type value: str
        """
        self.key = key
        self.value = value

    def get_key(self):
        """返回自定义请求头的 Key

        :return: 自定义请求头的 Key
        :rtype: str
        """
        return self.key

    def get_value(self):
        """返回自定义请求头的 Value

        :return: 自定义请求头的 Value
        :rtype: str
        """
        return self.value

    @classmethod
    def set_attributes(cls, data: dict):
        """从字典构造 GeneralWebhookHeaderKV 对象"""
        key = data.get(KEY)
        value = data.get(VALUE)
        return cls(key, value)

class WebhookIntegrationInfo(TLSData):
    def __init__(self, webhook_id: str = None, create_time: str = None, modify_time: str = None,
                 webhook_url: str = None, webhook_name: str = None, webhook_type: str = None,
                 webhook_method: str = None, webhook_secret: str = None,
                 webhook_headers: List[GeneralWebhookHeaderKV] = None):
        """告警 Webhook 集成配置信息

        :param webhook_id: Webhook 集成配置 ID
        :type webhook_id: str
        :param create_time: Webhook 集成配置创建时间
        :type create_time: str
        :param modify_time: Webhook 集成配置最近一次修改时间
        :type modify_time: str
        :param webhook_url: Webhook 请求地址
        :type webhook_url: str
        :param webhook_name: Webhook 集成配置名称
        :type webhook_name: str
        :param webhook_type: Webhook 类型
        :type webhook_type: str
        :param webhook_method: 自定义 Webhook 请求方法
        :type webhook_method: str
        :param webhook_secret: Webhook 加密密钥
        :type webhook_secret: str
        :param webhook_headers: 自定义 Webhook 的请求头
        :type webhook_headers: List[GeneralWebhookHeaderKV]
        """
        self.webhook_id = webhook_id
        self.create_time = create_time
        self.modify_time = modify_time
        self.webhook_url = webhook_url
        self.webhook_name = webhook_name
        self.webhook_type = webhook_type
        self.webhook_method = webhook_method
        self.webhook_secret = webhook_secret
        self.webhook_headers = webhook_headers

    @classmethod
    def set_attributes(cls, data: dict):
        webhook_integration_info = super(WebhookIntegrationInfo, cls).set_attributes(data)

        if WEBHOOK_HEADERS in data:
            webhook_headers = data[WEBHOOK_HEADERS]
            webhook_integration_info.webhook_headers = []
            for header in webhook_headers:
                webhook_integration_info.webhook_headers.append(  # pylint: disable=no-member
                    GeneralWebhookHeaderKV(header.get(KEY), header.get(VALUE)))

        return webhook_integration_info


class ResourceTagInfo(TLSData):
    def __init__(self, tag_key: str = None, tag_value: str = None, resource_id: str = None, resource_type: str = None):
        """资源标签信息

        :param tag_key: 标签 Key 的值
        :param tag_value: 标签 Value 的值
        :param resource_id: 资源 ID
        :param resource_type: 资源类型
        """
        self.tag_key = tag_key
        self.tag_value = tag_value
        self.resource_id = resource_id
        self.resource_type = resource_type


class StatusInfo(TLSData):
    def __init__(self, code: str = None, message: str = None):
        """
        :param code: 状态码
        :type code: str
        :param message: 错误消息
        :type message: str
        """
        self.code = code
        self.message = message


class ResourceInfo(TLSData):
    def __init__(self, attributes: List[KeyValueInfo] = None):
        """
        :param attributes: 资源属性列表
        :type attributes: List[KeyValueInfo]
        """
        self.attributes = attributes

    @classmethod
    def set_attributes(cls, data: dict):
        resource_info = super(ResourceInfo, cls).set_attributes(data)
        
        if ATTRIBUTES in data and data[ATTRIBUTES] is not None:
            resource_info.attributes = []
            for attr in data[ATTRIBUTES]:
                resource_info.attributes.append(KeyValueInfo.set_attributes(data=attr))  # pylint: disable=no-member
        
        return resource_info


class InstrumentationLibraryInfo(TLSData):
    def __init__(self, name: str = None, version: str = None):
        """
        :param name: 检测库名称
        :type name: str
        :param version: 检测库版本
        :type version: str
        """
        self.name = name
        self.version = version


class SpanLinkInfo(TLSData):
    def __init__(self, trace_id: str = None, span_id: str = None, 
                 trace_state: str = None, attributes: List[KeyValueInfo] = None):
        """
        :param trace_id: Trace ID
        :type trace_id: str
        :param span_id: Span ID
        :type span_id: str
        :param trace_state: Trace状态
        :type trace_state: str
        :param attributes: 属性列表
        :type attributes: List[KeyValueInfo]
        """
        self.trace_id = trace_id
        self.span_id = span_id
        self.trace_state = trace_state
        self.attributes = attributes

    @classmethod
    def set_attributes(cls, data: dict):
        span_link = super(SpanLinkInfo, cls).set_attributes(data)

        if ATTRIBUTES in data and data[ATTRIBUTES] is not None:
            span_link.attributes = []
            for attr in data[ATTRIBUTES]:
                span_link.attributes.append(KeyValueInfo.set_attributes(data=attr))  # pylint: disable=no-member

        return span_link


class SpanEventInfo(TLSData):
    def __init__(self, name: str = None, timestamp: int = None, attributes: List[KeyValueInfo] = None):
        """
        :param name: 事件名称
        :type name: str
        :param timestamp: 时间戳（微秒）
        :type timestamp: int
        :param attributes: 属性列表
        :type attributes: List[KeyValueInfo]
        """
        self.name = name
        self.timestamp = timestamp
        self.attributes = attributes

    @classmethod
    def set_attributes(cls, data: dict):
        span_event = super(SpanEventInfo, cls).set_attributes(data)

        if ATTRIBUTES in data and data[ATTRIBUTES] is not None:
            span_event.attributes = []
            for attr in data[ATTRIBUTES]:
                span_event.attributes.append(KeyValueInfo.set_attributes(data=attr))  # pylint: disable=no-member

        return span_event


class SpanInfo(TLSData):
    def __init__(self, trace_id: str = None, span_id: str = None, kind: str = None, 
                 name: str = None, start_time: int = None, end_time: int = None, 
                 parent_span_id: str = None, trace_state: str = None, 
                 status: StatusInfo = None, resource: ResourceInfo = None,
                 attributes: List[KeyValueInfo] = None, links: List[SpanLinkInfo] = None,
                 events: List[SpanEventInfo] = None, 
                 instrumentation_library: InstrumentationLibraryInfo = None):
        """
        :param trace_id: Trace ID
        :type trace_id: str
        :param span_id: Span ID
        :type span_id: str
        :param kind: Span类型
        :type kind: str
        :param name: Span名称
        :type name: str
        :param start_time: 开始时间（微秒）
        :type start_time: int
        :param end_time: 结束时间（微秒）
        :type end_time: int
        :param parent_span_id: 父Span ID
        :type parent_span_id: str
        :param trace_state: Trace状态
        :type trace_state: str
        :param status: Span状态
        :type status: StatusInfo
        :param resource: 资源信息
        :type resource: ResourceInfo
        :param attributes: 属性列表
        :type attributes: List[KeyValueInfo]
        :param links: 链接列表
        :type links: List[SpanLinkInfo]
        :param events: 事件列表
        :type events: List[SpanEventInfo]
        :param instrumentation_library: 检测库信息
        :type instrumentation_library: InstrumentationLibraryInfo
        """
        self.trace_id = trace_id
        self.span_id = span_id
        self.kind = kind
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.parent_span_id = parent_span_id
        self.trace_state = trace_state
        self.status = status
        self.resource = resource
        self.attributes = attributes
        self.links = links
        self.events = events
        self.instrumentation_library = instrumentation_library

    @classmethod
    def set_attributes(cls, data: dict):
        span_info = super(SpanInfo, cls).set_attributes(data)

        if STATUS in data and data[STATUS] is not None:
            span_info.status = StatusInfo.set_attributes(data=data[STATUS])

        if RESOURCE in data and data[RESOURCE] is not None:
            span_info.resource = ResourceInfo.set_attributes(data=data[RESOURCE])

        if ATTRIBUTES in data and data[ATTRIBUTES] is not None:
            span_info.attributes = []
            for attr in data[ATTRIBUTES]:
                span_info.attributes.append(KeyValueInfo.set_attributes(data=attr))  # pylint: disable=no-member

        if LINKS in data and data[LINKS] is not None:
            span_info.links = []
            for link in data[LINKS]:
                span_info.links.append(SpanLinkInfo.set_attributes(data=link))  # pylint: disable=no-member

        if EVENTS in data and data[EVENTS] is not None:
            span_info.events = []
            for event in data[EVENTS]:
                span_info.events.append(SpanEventInfo.set_attributes(data=event))  # pylint: disable=no-member

        if INSTRUMENTATION_LIBRARY in data and data[INSTRUMENTATION_LIBRARY] is not None:
            span_info.instrumentation_library = InstrumentationLibraryInfo.set_attributes(
                data=data[INSTRUMENTATION_LIBRARY])  # pylint: disable=no-member

        return span_info


class TraceInfo(TLSData):
    def __init__(self, spans: List[SpanInfo] = None,
                 trace_id: str = None, service_name: str = None, operation_name: str = None,
                 start_time: int = None, end_time: int = None, duration: int = None,
                 status_code: str = None, attributes: dict = None):
        """综合 Trace 信息结构

        - DescribeTrace 场景：通过 spans 字段承载完整的 Span 列表；
        - SearchTraces 场景：通过 trace_id / service_name / operation_name / start_time / end_time
          / duration / status_code / attributes 等字段承载 Trace 概要。
        """
        self.spans = spans
        self.trace_id = trace_id
        self.service_name = service_name
        self.operation_name = operation_name
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.status_code = status_code
        self.attributes = attributes

    @classmethod
    def set_attributes(cls, data: dict):
        trace_info = super(TraceInfo, cls).set_attributes(data)

        if SPANS in data and data[SPANS] is not None:
            trace_info.spans = []
            for span in data[SPANS]:
                trace_info.spans.append(SpanInfo.set_attributes(data=span))  # pylint: disable=no-member

        return trace_info

    def get_trace_id(self):
        """返回 Trace ID"""
        return getattr(self, "trace_id", None)

    def get_service_name(self):
        """返回服务名称"""
        return getattr(self, "service_name", None)

    def get_operation_name(self):
        """返回操作名称"""
        return getattr(self, "operation_name", None)

    def get_start_time(self):
        """返回开始时间（微秒）"""
        return getattr(self, "start_time", None)

    def get_end_time(self):
        """返回结束时间（微秒）"""
        return getattr(self, "end_time", None)

    def get_duration(self):
        """返回持续时间（微秒）"""
        return getattr(self, "duration", None)

    def get_status_code(self):
        """返回状态码"""
        return getattr(self, "status_code", None)

    def get_attributes(self):
        """返回自定义属性"""
        return getattr(self, "attributes", None)


class RuleNode(TLSData):
    def __init__(self, type: str = None, value: List[str] = None, children: List['RuleNode'] = None):
        """
        :param type: 当前节点类型。可选值：Operation：操作节点。Condition：条件节点
        :type type: str
        :param value: 节点值
        :type value: List[str]
        :param children: 子节点
        :type children: List[RuleNode]
        """
        self.type = type
        self.value = value
        self.children = children

    def get_type(self):
        """
        :return: 当前节点类型
        :rtype: str
        """
        return self.type

    def get_value(self):
        """
        :return: 节点值
        :rtype: List[str]
        """
        return self.value

    def get_children(self):
        """
        :return: 子节点
        :rtype: List[RuleNode]
        """
        return self.children

    @classmethod
    def set_attributes(cls, data: dict):
        rule_node = super(RuleNode, cls).set_attributes(data)

        if CHILDREN in data and data[CHILDREN] is not None:
            rule_node.children = []
            for child_data in data[CHILDREN]:
                rule_node.children.append(  # pylint: disable=no-member
                    RuleNode.set_attributes(child_data))

        return rule_node

    def json(self):
        json_data = super(RuleNode, self).json()

        if self.children is not None:
            json_data[CHILDREN] = []
            for child in self.children:
                json_data[CHILDREN].append(child.json())

        return json_data


class NoticeRule(TLSData):
    def __init__(self, has_next: bool = None, rule_node: RuleNode = None, 
                 has_end_node: bool = None, receiver_infos: List[Receiver] = None):
        """
        :param has_next: 是否继续进入下一层的条件判断
        :type has_next: bool
        :param rule_node: 规则节点
        :type rule_node: RuleNode
        :param has_end_node: 后面是否存在结束节点
        :type has_end_node: bool
        :param receiver_infos: 通知渠道相关信息
        :type receiver_infos: List[Receiver]
        """
        self.has_next = has_next
        self.rule_node = rule_node
        self.has_end_node = has_end_node
        self.receiver_infos = receiver_infos

    def get_has_next(self):
        """
        :return: 是否继续进入下一层的条件判断
        :rtype: bool
        """
        return self.has_next

    def get_rule_node(self):
        """
        :return: 规则节点
        :rtype: RuleNode
        """
        return self.rule_node

    def get_has_end_node(self):
        """
        :return: 后面是否存在结束节点
        :rtype: bool
        """
        return self.has_end_node

    def get_receiver_infos(self):
        """
        :return: 通知渠道相关信息
        :rtype: List[Receiver]
        """
        return self.receiver_infos

    @classmethod
    def set_attributes(cls, data: dict):
        notice_rule = super(NoticeRule, cls).set_attributes(data)

        if RULE_NODE in data and data[RULE_NODE] is not None:
            notice_rule.rule_node = RuleNode.set_attributes(data[RULE_NODE])

        if RECEIVER_INFOS in data and data[RECEIVER_INFOS] is not None:
            notice_rule.receiver_infos = []
            for receiver_data in data[RECEIVER_INFOS]:
                notice_rule.receiver_infos.append(  # pylint: disable=no-member
                    Receiver.set_attributes(receiver_data))

        return notice_rule

    def json(self):
        json_data = super(NoticeRule, self).json()

        if self.rule_node is not None:
            json_data[RULE_NODE] = self.rule_node.json()

        if self.receiver_infos is not None:
            json_data[RECEIVER_INFOS] = []
            for receiver in self.receiver_infos:
                json_data[RECEIVER_INFOS].append(receiver.json())

        return json_data
