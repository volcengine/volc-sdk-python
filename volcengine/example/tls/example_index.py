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
    project_id = create_project_response.get_project_id()

    # 创建日志主题
    create_topic_request = CreateTopicRequest(topic_name="topic-name-" + now, project_id=project_id,
                                              ttl=3650, description="topic-description", shard_count=2)
    create_topic_response = tls_service.create_topic(create_topic_request)
    topic_id = create_topic_response.get_topic_id()

    # 创建索引配置
    # 请根据您的需要，配置full_text全文索引或key_value键值索引
    # CreateIndex API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112187
    full_text = FullTextInfo(case_sensitive=False, delimiter=",-;", include_chinese=False)
    value_info_a = ValueInfo(value_type="text", delimiter="", case_sensitive=True,
                             include_chinese=False, sql_flag=False)
    value_info_b = ValueInfo(value_type="long", delimiter="", case_sensitive=False,
                             include_chinese=False, sql_flag=True)

    value_c1_json_keys = ValueInfo(value_type="text", delimiter="", case_sensitive=False,
                                  include_chinese=False, sql_flag=True)
    value_c2_json_keys = ValueInfo(value_type="long", delimiter="", case_sensitive=False,
                                  include_chinese=False, sql_flag=True)
    value_info_c = ValueInfo(value_type="json", delimiter="", case_sensitive=False,
                             include_chinese=False, sql_flag=True, index_all=True,
                             json_keys=[
                                 KeyValueInfo("test", value_c1_json_keys).json(),
                                 KeyValueInfo("key-l", value_c2_json_keys).json(),
                             ])

    key_value_info_a = KeyValueInfo(key="test1", value=value_info_a)
    key_value_info_b = KeyValueInfo(key="test2", value=value_info_b)
    key_value_info_c = KeyValueInfo(key="test3", value=value_info_c)
    key_value = [key_value_info_a, key_value_info_b, key_value_info_c]
    create_index_request = CreateIndexRequest(topic_id=create_topic_response.topic_id, full_text=full_text,
                                              key_value=key_value)
    create_index_response = tls_service.create_index(create_index_request)

    # 查询索引配置
    # 请根据您的需要，填写待查询的topic_id
    # DescribeIndex API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112190
    describe_index_request = DescribeIndexRequest(topic_id)
    describe_index_response = tls_service.describe_index(describe_index_request)
    print("index delimiter: {}".format(describe_index_response.get_full_text().get_delimiter()))

    # 修改索引配置
    # 请根据您的需要，填写topic_id和待修改的full_text或key_value配置
    # ModifyIndex API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112189
    modify_index_request = ModifyIndexRequest(topic_id, full_text=FullTextInfo(case_sensitive=True, delimiter=","))
    modify_index_response = tls_service.modify_index(modify_index_request)

    # 删除索引配置
    # 请根据您的需要，填写待删除索引的topic_id
    # DeleteIndex API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112188
    delete_index_request = DeleteIndexRequest(topic_id)
    delete_index_response = tls_service.delete_index(delete_index_request)

    # 删除topic
    tls_service.delete_topic(DeleteTopicRequest(topic_id))

    # 删除日志项目
    tls_service.delete_project(DeleteProjectRequest(project_id))
