# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import *


if __name__ == "__main__":
    # 初始化客户端，推荐通过环境变量动态获取火山引擎密钥等身份认证信息，以免AccessKey硬编码引发数据安全风险。详细说明请参考 https://www.volcengine.com/docs/6470/1166455
    # 使用STS时，ak和sk均使用临时密钥，且设置VOLCENGINE_TOKEN；不使用STS时，VOLCENGINE_TOKEN部分传空
    endpoint = os.environ["VOLCENGINE_ENDPOINT"]
    region = os.environ["VOLCENGINE_REGION"]
    access_key_id = os.environ["VOLCENGINE_ACCESS_KEY_ID"]
    access_key_secret = os.environ["VOLCENGINE_ACCESS_KEY_SECRET"]

    # 实例化TLS客户端
    tls_service = TLSService(endpoint, access_key_id, access_key_secret, region)
    now = str(int(time.time()))

    # 创建日志项目
    create_project_request = CreateProjectRequest(project_name="project-name-" + now, region=region,
                                                  description="project-description")
    create_project_response = tls_service.create_project(create_project_request)
    project_id = create_project_response.project_id

    # 创建日志主题
    create_topic_request = CreateTopicRequest(topic_name="topic-name-" + now, project_id=project_id,
                                              ttl=3650, description="topic-description", shard_count=2)
    create_topic_response = tls_service.create_topic(create_topic_request)
    topic_id = create_topic_response.get_topic_id()

    # 创建索引
    full_text = FullTextInfo(case_sensitive=False, delimiter=",-;", include_chinese=False)
    value_info_a = ValueInfo(value_type="text", delimiter="", case_sensitive=True,
                             include_chinese=False, sql_flag=True)
    value_info_b = ValueInfo(value_type="long", delimiter="", case_sensitive=False,
                             include_chinese=False, sql_flag=True)
    key_value_info_a = KeyValueInfo(key="key1", value=value_info_a)
    key_value_info_b = KeyValueInfo(key="key2", value=value_info_b)
    key_value = [key_value_info_a, key_value_info_b]
    create_index_request = CreateIndexRequest(topic_id, full_text, key_value)
    create_index_response = tls_service.create_index(create_index_request)

    # 写入日志数据
    # 建议您一次性聚合多条日志后调用一次put_logs_v2接口，以提高日志上传吞吐率
    # 请根据您的需要，填写topic_id、source、filename和logs列表，建议您使用lz4压缩
    # PutLogs API的请求参数规范和限制请参阅 https://www.volcengine.com/docs/6470/112191
    logs = PutLogsV2Logs(source="192.168.1.1", filename="sys.log")
    for i in range(100):
        logs.add_log(contents={"key1": "value1-" + str(i + 1), "key2": "value2-" + str(i + 1)},
                     log_time=int(round(time.time())))
    tls_service.put_logs_v2(PutLogsV2Request(topic_id, logs))
    time.sleep(30)

    # 查询日志直方图情况
    # 请根据您的需要，填写topic_id、query、start_time、end_time、interval
    # DescribeHistogramV1 API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/1347899
    start_time = int(round(time.time())) - 60
    end_time = start_time + 60 * 2
    # Deprecated, use DescribeHistogramV1 instead.
    describe_histogram_request = DescribeHistogramRequest(topic_id, "", start_time, end_time, interval=None)
    describe_histogram_response = tls_service.describe_histogram(describe_histogram_request)
    describe_histogram_v1_request = DescribeHistogramV1Request(topic_id, "", start_time, end_time, interval=None)
    describe_histogram_v1_response = tls_service.describe_histogram_v1(describe_histogram_v1_request)

    # 查询消费游标
    # 请根据您的需要，填写topic_id、shard_id和from_time
    # DescribeCursor API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112193
    describe_cursor_request = DescribeCursorRequest(topic_id, shard_id=0, from_time="begin")
    describe_cursor_response = tls_service.describe_cursor(describe_cursor_request)

    # 消费日志数据
    # 请根据您的需要，填写topic_id、shard_id、cursor等参数
    # ConsumeLogs API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112194
    consume_logs_request = ConsumeLogsRequest(topic_id, shard_id=0, cursor=describe_cursor_response.cursor)
    consume_logs_response = tls_service.consume_logs(consume_logs_request)

    # 查询分析日志数据
    # 请根据您的需要，填写topic_id、query、start_time、end_time、limit等参数值
    # SearchLogs API的请求参数规范和限制请参阅 https://www.volcengine.com/docs/6470/112195

    # 当您需要检索和分析日志时，推荐您使用Python SDK提供的search_logs_v2方法，下面的代码提供了具体的调用示例
    # 查询日志数据（全文检索）
    search_logs_request = SearchLogsRequest(topic_id, query="error", limit=10,
                                            start_time=1672502400000, end_time=1688140800000)
    search_logs_response = tls_service.search_logs_v2(search_logs_request)

    # 查询日志数据（键值检索）
    search_logs_request = SearchLogsRequest(topic_id, query="key1:error", limit=10,
                                            start_time=1672502400000, end_time=1688140800000)
    search_logs_response = tls_service.search_logs_v2(search_logs_request)

    # 查询日志数据（SQL分析）
    search_logs_request = SearchLogsRequest(topic_id, query="* | select key1, key2", limit=10,
                                            start_time=1672502400000, end_time=1688140800000)
    search_logs_response = tls_service.search_logs_v2(search_logs_request)

    # 查询日志数据（SQL分析）
    search_logs_request = SearchLogsRequest(topic_id, query="* | select key1, key2", limit=10,
                                            start_time=1672502400000, end_time=1688140800000)
    search_logs_response = tls_service.search_logs(search_logs_request)
