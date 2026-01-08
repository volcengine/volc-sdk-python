# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import time

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import *


if __name__ == "__main__":
    # 初始化客户端，推荐通过环境变量动态获取火山引擎密钥等身份认证信息，
    # 以免AccessKey硬编码引发数据安全风险。详细说明请参考
    # https://www.volcengine.com/docs/6470/1166455
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

    # 创建源日志主题
    create_source_topic_request = CreateTopicRequest(
        topic_name="source-topic-name-" + now,
        project_id=project_id,
        ttl=3650,
        description="source-topic-description",
        shard_count=2,
    )
    create_source_topic_response = tls_service.create_topic(create_source_topic_request)
    source_topic_id = create_source_topic_response.get_topic_id()

    # 创建目标日志主题
    create_target_topic_request = CreateTopicRequest(
        topic_name="target-topic-name-" + now,
        project_id=project_id,
        ttl=3650,
        description="target-topic-description",
        shard_count=2,
    )
    create_target_topic_response = tls_service.create_topic(create_target_topic_request)
    target_topic_id = create_target_topic_response.get_topic_id()

    # 创建ETL任务
    # 请根据您的需要，填写相关参数
    # CreateETLTask API的请求参数规范请参阅相关文档
    create_etl_task_request = CreateETLTaskRequest(
        dsl_type="NORMAL",
        name="etl-task-name-" + now,
        description="etl-task-description",
        enable=True,
        source_topic_id=source_topic_id,
        script='f_set("key", "value")',
        task_type="Resident",
        target_resources=[
            {
                "alias": "test",
                "topic_id": target_topic_id,
                "region": region
            }
        ]
    )
    create_etl_task_response = tls_service.create_etl_task(create_etl_task_request)
    etl_task_id = create_etl_task_response.get_task_id()

    print(f"ETL Task created successfully, task_id: {etl_task_id}")

    # 删除日志主题
    delete_source_topic_request = DeleteTopicRequest(source_topic_id)
    tls_service.delete_topic(delete_source_topic_request)

    delete_target_topic_request = DeleteTopicRequest(target_topic_id)
    tls_service.delete_topic(delete_target_topic_request)

    # 删除日志项目
    delete_project_request = DeleteProjectRequest(project_id=project_id)
    tls_service.delete_project(delete_project_request)
