# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

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

    # 创建索引配置
    full_text = FullTextInfo(case_sensitive=False, delimiter=",-;", include_chinese=False)
    value_info_a = ValueInfo(value_type="text", delimiter="", case_sensitive=True,
                             include_chinese=False, sql_flag=False)
    value_info_b = ValueInfo(value_type="long", delimiter="", case_sensitive=False,
                             include_chinese=False, sql_flag=True)
    key_value_info_a = KeyValueInfo(key="test1", value=value_info_a)
    key_value_info_b = KeyValueInfo(key="test2", value=value_info_b)
    key_value = [key_value_info_a, key_value_info_b]
    create_index_request = CreateIndexRequest(topic_id=create_topic_response.topic_id, full_text=full_text,
                                              key_value=key_value)
    create_index_response = tls_service.create_index(create_index_request)

    # 查询索引配置
    describe_index_request = DescribeIndexRequest(topic_id)
    describe_index_response = tls_service.describe_index(describe_index_request)

    # 修改索引配置
    modify_index_request = ModifyIndexRequest(topic_id, full_text=FullTextInfo(case_sensitive=True, delimiter=","))
    modify_index_response = tls_service.modify_index(modify_index_request)

    # 删除索引配置
    delete_index_request = DeleteIndexRequest(topic_id)
    delete_index_response = tls_service.delete_index(delete_index_request)
