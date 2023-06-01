# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import time

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import *

if __name__ == "__main__":
    # 请查询控制台，填写以下参数值
    endpoint = os.environ["endpoint"]
    access_key_id = os.environ["access_key_id"]
    access_key_secret = os.environ["access_key_secret"]
    region = os.environ["region"]

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

    # 查询指定日志主题信息
    describe_topic_request = DescribeTopicRequest(topic_id)
    describe_topic_response = tls_service.describe_topic(describe_topic_request)
    print("topic id:{}".format(describe_topic_response.get_topic().get_topic_id()))

    # 查询所有日志主题信息
    describe_topics_request = DescribeTopicsRequest(project_id)
    describe_topics_response = tls_service.describe_topics(describe_topics_request)
    print("topics total:{} first topic name:{}".format(describe_topics_response.get_total(),
                                                       describe_topics_response.get_topics()[0].get_topic_name()))

    # 修改日志主题
    modify_topic_request = ModifyTopicRequest(topic_id, topic_name="change-topic-name",
                                              description="change-topic-description")
    modify_topic_response = tls_service.modify_topic(modify_topic_request)

    # 删除日志主题
    delete_topic_request = DeleteTopicRequest(topic_id)
    delete_topic_response = tls_service.delete_topic(delete_topic_request)

    # 删除日志项目
    tls_service.delete_project(DeleteProjectRequest(project_id))
