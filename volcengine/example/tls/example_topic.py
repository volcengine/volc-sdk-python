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
    # 请根据您的需要，填写project_id、topic_name、ttl、shard_count和description等参数
    # CreateTopic API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112180
    create_topic_request = CreateTopicRequest(
        topic_name="topic-name-" + now,
        project_id=project_id,
        ttl=3650,
        description="topic-description",
        shard_count=2,
        enable_hot_ttl=True,
        hot_ttl=30,
        cold_ttl=70,
        archive_ttl=3550,
    )
    create_topic_response = tls_service.create_topic(create_topic_request)
    topic_id = create_topic_response.get_topic_id()

    # 查询指定日志主题信息
    # 请根据您的需要，填写待查询的topic_id
    # DescribeTopic API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112184
    describe_topic_request = DescribeTopicRequest(topic_id)
    describe_topic_response = tls_service.describe_topic(describe_topic_request)
    print("topic id: {}".format(describe_topic_response.get_topic().get_topic_id()))

    # 修改日志主题
    # 请根据您的需要，填写topic_id以及待修改的各项参数
    # ModifyTopic API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112183
    modify_topic_request = ModifyTopicRequest(
        topic_id,
        topic_name="change-topic-name",
        description="change-topic-description",
        ttl=3650,
        enable_hot_ttl=True,
        hot_ttl=100,
        cold_ttl=100,
        archive_ttl=3450,
    )
    modify_topic_response = tls_service.modify_topic(modify_topic_request)

    # 查询所有日志主题信息
    # 请根据您的需要，填写待查询的project_id
    # DescribeTopics API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112185
    describe_topics_request = DescribeTopicsRequest(
        project_id,
        project_name="project-name",
    )
    describe_topics_response = tls_service.describe_topics(describe_topics_request)
    if describe_topics_response.get_total() > 0:
        print("topics total: {}\nfirst topic name: {}".format(describe_topics_response.get_total(),
                                                              describe_topics_response.get_topics()[0].get_topic_name()))
    else:
        print("no topics")

    # 删除日志主题
    # 请根据您的需要，填写待删除的topic_id
    # DeleteTopic API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112182
    delete_topic_request = DeleteTopicRequest(topic_id)
    delete_topic_response = tls_service.delete_topic(delete_topic_request)

    # 删除日志项目
    tls_service.delete_project(DeleteProjectRequest(project_id))
