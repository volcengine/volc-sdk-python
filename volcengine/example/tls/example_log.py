# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import *


if __name__ == "__main__":
    # 请查询控制台，填写以下参数值
    endpoint = ""
    access_key_id = ""
    access_key_secret = ""
    region = ""

    # 实例化TLS客户端
    tls_service = TLSService(endpoint, access_key_id, access_key_secret, region)

    # 创建日志项目
    create_project_request = CreateProjectRequest(project_name="project-name", region=region,
                                                  description="project-description")
    create_project_response = tls_service.create_project(create_project_request)
    project_id = create_project_response.project_id

    # 创建日志主题
    create_topic_request = CreateTopicRequest(topic_name="topic-name", project_id=project_id,
                                              ttl=3650, description="topic-description", shard_count=2)
    create_topic_response = tls_service.create_topic(create_topic_request)
    topic_id = create_topic_response.topic_id

    # 创建索引
    full_text = FullTextInfo(case_sensitive=False, delimiter=",-;", include_chinese=False)
    value_info_a = ValueInfo(value_type="text", delimiter="", case_sensitive=True,
                             include_chinese=False, sql_flag=False)
    value_info_b = ValueInfo(value_type="long", delimiter="", case_sensitive=False,
                             include_chinese=False, sql_flag=True)
    key_value_info_a = KeyValueInfo(key="key1", value=value_info_a)
    key_value_info_b = KeyValueInfo(key="key2", value=value_info_b)
    key_value = [key_value_info_a, key_value_info_b]
    create_index_request = CreateIndexRequest(topic_id, full_text, key_value)
    create_index_response = tls_service.create_index(create_index_request)

    # 写入日志数据
    log_group_list = LogGroupList()

    log_group = log_group_list.log_groups.add()
    log_group.source = "127.0.0.1"
    log_group.filename = "sys.log"

    log = log_group.logs.add()
    log.time = 1346457600000

    log_content = log.contents.add()
    log_content.key = "key1"
    log_content.value = "error"

    put_logs_request = PutLogsRequest(topic_id, log_group_list, compression="lz4")
    tls_service.put_logs(put_logs_request)
    time.sleep(30)

    # 查询消费游标
    describe_cursor_request = DescribeCursorRequest(topic_id, shard_id=0, from_time="begin")
    describe_cursor_response = tls_service.describe_cursor(describe_cursor_request)

    # 消费日志数据
    consume_logs_request = ConsumeLogsRequest(topic_id, shard_id=0, cursor=describe_cursor_response.cursor)
    consume_logs_response = tls_service.consume_logs(consume_logs_request)

    # 查询日志数据（全文检索）
    search_logs_request = SearchLogsRequest(topic_id, query="error", limit=10,
                                            start_time=1346457600000, end_time=1630454400000)
    search_logs_response = tls_service.search_logs(search_logs_request)

    # 查询日志数据（键值检索）
    search_logs_request = SearchLogsRequest(topic_id, query="key1:error", limit=10,
                                            start_time=1346457600000, end_time=1630454400000)
    search_logs_response = tls_service.search_logs(search_logs_request)

    # 查询日志数据（SQL分析）
    search_logs_request = SearchLogsRequest(topic_id, query="* | select key1, key2", limit=10,
                                            start_time=1346457600000, end_time=1630454400000)
    search_logs_response = tls_service.search_logs(search_logs_request)
