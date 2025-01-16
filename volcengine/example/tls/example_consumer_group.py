# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import time

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import CreateProjectRequest, CreateTopicRequest, DeleteTopicRequest, \
    DeleteProjectRequest, CreateConsumerGroupRequest, DeleteConsumerGroupRequest, DescribeConsumerGroupsRequest

if __name__ == '__main__':
    # 初始化客户端，推荐通过环境变量动态获取火山引擎密钥等身份认证信息，以免AccessKey硬编码引发数据安全风险。详细说明请参考https://www.volcengine.com/docs/6470/1166455
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
    print("Successfully create project, project id is: {} ".format(project_id))

    # 创建日志主题
    # 请根据您的需要，填写project_id、topic_name、ttl、shard_count和description等参数
    # CreateTopic API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112180
    create_topic_request = CreateTopicRequest(topic_name="topic-name-" + now, project_id=project_id,
                                              ttl=3650, description="topic-description", shard_count=2)
    create_topic_response = tls_service.create_topic(create_topic_request)
    topic_id = create_topic_response.get_topic_id()
    print("Successfully create topic, topic id is: {} ".format(topic_id))

    # 创建消费者组
    consumer_group = "test-consumer-group-" + now
    create_consumer_group_request = CreateConsumerGroupRequest(project_id, consumer_group, topic_id_list=[topic_id],
                                                               heartbeat_ttl=10, ordered_consume=True)
    tls_service.create_consumer_group(create_consumer_group_request)
    print("Successfully create consumer group, group is: {} ".format(consumer_group))

    # 查询消费者组
    describe_consumer_groups_request = DescribeConsumerGroupsRequest(project_id)
    describe_consumer_groups_response = tls_service.describe_consumer_groups(describe_consumer_groups_request)
    print("Successfully describe consumer group, count is: {} ".format(len(describe_consumer_groups_response.consumer_groups)))

    # 删除消费者组
    tls_service.delete_consumer_group(DeleteConsumerGroupRequest(project_id, consumer_group))
    print("Successfully delete consumer group, group is: {} ".format(consumer_group))

    # 删除topic
    tls_service.delete_topic(DeleteTopicRequest(topic_id))
    print("Successfully delete topic, topic id is: {} ".format(topic_id))

    # 删除日志项目
    tls_service.delete_project(DeleteProjectRequest(project_id))
    print("Successfully delete project, project id is: {} ".format(project_id))