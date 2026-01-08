# coding=utf-8
import os
import time
import uuid

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import *


if __name__ == "__main__":
    # 初始化客户端，需要设置AccessKey ID/AccessKey Secret，以及服务地域
    endpoint = os.environ["VOLCENGINE_ENDPOINT"]
    region = os.environ["VOLCENGINE_REGION"]
    access_key_id = os.environ["VOLCENGINE_ACCESS_KEY_ID"]
    access_key_secret = os.environ["VOLCENGINE_ACCESS_KEY_SECRET"]

    # 创建TLS客户端
    tls_service = TLSService(endpoint, access_key_id, access_key_secret, region)

    # 创建项目和主题用于测试
    project_name = f"tls-python-sdk-schedule-project-{uuid.uuid4().hex}"
    source_topic_name = f"tls-python-sdk-schedule-source-topic-{uuid.uuid4().hex}"
    dest_topic_name = f"tls-python-sdk-schedule-dest-topic-{uuid.uuid4().hex}"

    # 创建项目
    create_project_request = CreateProjectRequest(
        project_name=project_name,
        region=region,
    )
    create_project_response = tls_service.create_project(create_project_request)
    project_id = create_project_response.get_project_id()
    print(f"Created project: {project_id}")

    # 创建源主题
    create_source_topic_request = CreateTopicRequest(
        project_id=project_id,
        topic_name=source_topic_name,
        shard_count=1,
        ttl=1,
    )
    create_source_topic_response = tls_service.create_topic(create_source_topic_request)
    source_topic_id = create_source_topic_response.get_topic_id()
    print(f"Created source topic: {source_topic_id}")

    # 创建目标主题
    create_dest_topic_request = CreateTopicRequest(
        project_id=project_id,
        topic_name=dest_topic_name,
        shard_count=1,
        ttl=1,
    )
    create_dest_topic_response = tls_service.create_topic(create_dest_topic_request)
    dest_topic_id = create_dest_topic_response.get_topic_id()
    print(f"Created dest topic: {dest_topic_id}")

    # 为源主题创建索引
    create_index_request = CreateIndexRequest(
        topic_id=source_topic_id,
        full_text=FullTextInfo(
            delimiter=",; ",
            case_sensitive=False,
            include_chinese=False,
        ),
    )
    create_index_response = tls_service.create_index(create_index_request)
    print(f"Created index for source topic: {create_index_response.get_request_id()}")

    # 创建定时SQL任务
    current_time = int(time.time())
    task_name = f"tls-python-sdk-schedule-task-{uuid.uuid4().hex}"
    create_schedule_sql_task_request = CreateScheduleSqlTaskRequest(
        task_name=task_name,
        topic_id=source_topic_id,
        dest_topic_id=dest_topic_id,
        process_start_time=current_time + 3600,  # 1小时后开始
        process_time_window="@m-15m,@m",
        query="* | select count(*) as count",
        request_cycle=RequestCycle(
            cycle_type="Period",
            time=60,  # 每60分钟执行一次
        ),
        status=0,  # 关闭任务，后续需手动启动
        description="测试定时SQL任务",
        process_sql_delay=60,
    )

    create_schedule_sql_task_response = tls_service.create_schedule_sql_task(
        create_schedule_sql_task_request)
    task_id = create_schedule_sql_task_response.get_task_id()
    print(f"Created schedule SQL task: {task_id}")

    # 清理资源
    print("Cleaning up resources...")
    # 删除目标主题
    delete_dest_topic_request = DeleteTopicRequest(topic_id=dest_topic_id)
    tls_service.delete_topic(delete_dest_topic_request)
    print(f"Deleted dest topic: {dest_topic_id}")

    # 删除源主题
    delete_source_topic_request = DeleteTopicRequest(topic_id=source_topic_id)
    tls_service.delete_topic(delete_source_topic_request)
    print(f"Deleted source topic: {source_topic_id}")

    # 删除项目
    delete_project_request = DeleteProjectRequest(project_id=project_id)
    tls_service.delete_project(delete_project_request)
    print(f"Deleted project: {project_id}")

    print("Example completed successfully!")