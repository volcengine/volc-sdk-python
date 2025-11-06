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
    create_project_request = CreateProjectRequest(project_name="import-project-" + now, region=region,
                                                  description="project for import task test")
    create_project_response = tls_service.create_project(create_project_request)
    project_id = create_project_response.get_project_id()
    print("创建日志项目成功，project_id: {}".format(project_id))

    # 创建日志主题
    create_topic_request = CreateTopicRequest(
        topic_name="import-topic-" + now,
        project_id=project_id,
        ttl=5,
        description="topic for import task test",
        shard_count=2,
    )
    create_topic_response = tls_service.create_topic(create_topic_request)
    topic_id = create_topic_response.get_topic_id()
    print("创建日志主题成功，topic_id: {}".format(topic_id))

    # 示例1：创建TOS导入任务
    print("\n=== 创建TOS导入任务 ===")
    
    # TOS源信息配置
    tos_source_info = TosSourceInfo(
        bucket="bucket-for-import-sdk-test",  # 请替换为您的TOS存储桶名称
        region="cn-guilin-boe",  # 请替换为您的TOS存储桶所在区域
        compress_type="none",  # 日志压缩类型：none、gzip、lz4、snappy
        prefix="logs/"  # 日志文件前缀
    )
    
    # 导入源信息
    import_source_info = ImportSourceInfo(tos_source_info=tos_source_info)
    
    # 提取规则配置
    import_extract_rule = ImportExtractRule(
        delimiter="|",  # 分隔符
        keys=["time", "level", "message"],  # 字段名
        time_key="time",  # 时间字段名
        time_format="%Y-%m-%d %H:%M:%S",  # 时间格式
        time_zone="Asia/Shanghai",  # 时区
        un_match_up_load_switch=True,  # 上传解析失败的日志
        un_match_log_key="LogParseFailed"  # 解析失败日志的字段名
    )
    
    # 目标信息配置
    target_info = TargetInfo(
        region=region,  # 日志主题所在区域
        log_type="delimiter_log",  # 日志类型
        extract_rule=import_extract_rule,  # 提取规则
        log_sample="2023-12-01 10:00:00|INFO|This is a sample log"  # 日志样例
    )
    
    # 创建TOS导入任务请求
    create_import_task_request = CreateImportTaskRequest(
        topic_id=topic_id,
        task_name="tos-import-task-" + now,
        source_type="tos",  # 源类型：tos
        import_source_info=import_source_info,
        target_info=target_info,
        project_id=project_id,
        description="TOS导入任务测试"
    )
    
    try:
        create_response = tls_service.create_import_task(create_import_task_request)
        task_id = create_response.get_task_id()
        print("TOS导入任务创建成功，task_id: {}".format(task_id))
        
        # 查询导入任务
        print("\n=== 验证查询导入任务功能 ===")
        try:
            describe_request = DescribeImportTaskRequest(task_id=task_id)
            describe_response = tls_service.describe_import_task(describe_request)
            print("查询导入任务成功，任务名称: {}".format(describe_response.get_task_info().task_name))
        except Exception as e:
            print("查询导入任务失败: {}".format(str(e)))
        
        # 验证新增方法 - 修改导入任务
        print("\n=== 验证修改导入任务功能 ===")
        try:
            # 修改任务状态为已停止（状态码4）
            modify_request = ModifyImportTaskRequest(
                task_id=task_id,
                status=4,  # 已停止
                topic_id=topic_id,
                task_name="modified-tos-import-task-" + now,
                source_type="tos",
                import_source_info=import_source_info,
                target_info=target_info,
                project_id=project_id,
                description="修改后的TOS导入任务测试"
            )
            modify_response = tls_service.modify_import_task(modify_request)
            print("修改导入任务成功")
        except Exception as e:
            print("修改导入任务失败: {}".format(str(e)))
        
        # 验证新增方法 - 查询导入任务列表
        print("\n=== 验证查询导入任务列表功能 ===")
        try:
            describe_tasks_request = DescribeImportTasksRequest(
                project_id=project_id,
                topic_id=topic_id,
                source_type="tos",
                page_number=1,
                page_size=10
            )
            tasks_response = tls_service.describe_import_tasks(describe_tasks_request)
            print("查询导入任务列表成功，总数: {}".format(tasks_response.get_total()))
            if tasks_response.get_task_info():
                print("第一个任务名称: {}".format(tasks_response.get_task_info()[0].task_name))
        except Exception as e:
            print("查询导入任务列表失败: {}".format(str(e)))
            
    except Exception as e:
        print("TOS导入任务创建失败: {}".format(str(e)))
        task_id = None

    # 示例2：创建Kafka导入任务
    print("\n=== 创建Kafka导入任务 ===")
    
    # Kafka源信息配置
    kafka_source_info = KafkaSourceInfo(
        host="kafka1.example.com:9092,kafka2.example.com:9092",  # Kafka集群地址
        topic="app-logs",  # Kafka Topic名称
        encode="UTF-8",  # 数据编码格式
        protocol="plaintext",  # Kafka协议
        is_need_auth=False,  # 是否开启鉴权
        initial_offset=0,  # 从最早时间开始导入
        time_source_default=0,  # 使用Kafka消息时间戳
    )
    
    # 导入源信息
    import_source_info_kafka = ImportSourceInfo(kafka_source_info=kafka_source_info)
    
    # 提取规则配置（JSON日志类型）
    import_extract_rule_json = ImportExtractRule(
        time_key="timestamp",  # 时间字段名
        time_format="%Y-%m-%dT%H:%M:%S.%fZ",  # ISO时间格式
        time_zone="UTC",  # UTC时区
        un_match_up_load_switch=True,
        un_match_log_key="LogParseFailed"
    )
    
    # 目标信息配置
    target_info_kafka = TargetInfo(
        region=region,
        log_type="json_log",  # JSON日志类型
        extract_rule=import_extract_rule_json,
        log_sample='{"@timestamp":"2023-12-01T10:00:00.000Z","level":"INFO","message":"Sample log message"}'
    )
    
    # 创建Kafka导入任务请求
    create_kafka_import_request = CreateImportTaskRequest(
        topic_id=topic_id,
        task_name="kafka-import-task-" + now,
        source_type="kafka",  # 源类型：kafka
        import_source_info=import_source_info_kafka,
        target_info=target_info_kafka,
        project_id=project_id,
        description="Kafka导入任务测试"
    )
    
    try:
        create_kafka_response = tls_service.create_import_task(create_kafka_import_request)
        kafka_task_id = create_kafka_response.get_task_id()
        print("Kafka导入任务创建成功，task_id: {}".format(kafka_task_id))
        
        # 验证新增方法 - 查询Kafka导入任务
        print("\n=== 验证查询Kafka导入任务功能 ===")
        try:
            describe_kafka_request = DescribeImportTaskRequest(task_id=kafka_task_id)
            describe_kafka_response = tls_service.describe_import_task(describe_kafka_request)
            print("查询Kafka导入任务成功，任务名称: {}".format(describe_kafka_response.get_task_info().task_name))
        except Exception as e:
            print("查询Kafka导入任务失败: {}".format(str(e)))
        
        # 验证新增方法 - 修改Kafka导入任务
        print("\n=== 验证修改Kafka导入任务功能 ===")
        try:

            modify_kafka_request = ModifyImportTaskRequest(
                task_id=kafka_task_id,
                status=5,  # 导入中
                topic_id=topic_id,
                task_name="modified-kafka-import-task-" + now,
                source_type="kafka",
                import_source_info=import_source_info_kafka,
                target_info=target_info_kafka,
                project_id=project_id,
                description="修改后的Kafka导入任务测试"
            )
            modify_kafka_response = tls_service.modify_import_task(modify_kafka_request)
            print("修改Kafka导入任务成功")
        except Exception as e:
            print("修改Kafka导入任务失败: {}".format(str(e)))
        
        # 验证新增方法 - 查询Kafka导入任务列表（按状态筛选）
        print("\n=== 验证按状态查询导入任务列表功能 ===")
        try:
            describe_kafka_tasks_request = DescribeImportTasksRequest(
                project_id=project_id,
                topic_id=topic_id,
                source_type="kafka",
                page_number=1,
                page_size=10
            )
            kafka_tasks_response = tls_service.describe_import_tasks(describe_kafka_tasks_request)
            print("按状态查询导入任务列表成功，总数: {}".format(kafka_tasks_response.get_total()))
            if kafka_tasks_response.get_task_info():
                print("第一个Kafka任务名称: {}".format(kafka_tasks_response.get_task_info()[0].task_name))
        except Exception as e:
            print("按状态查询导入任务列表失败: {}".format(str(e)))
            
    except Exception as e:
        print("Kafka导入任务创建失败: {}".format(str(e)))
        kafka_task_id = None

    # 验证新增方法 - 综合查询所有导入任务
    print("\n=== 验证综合查询导入任务列表功能 ===")
    try:
        all_tasks_request = DescribeImportTasksRequest(
            page_number=1,
            page_size=20
        )
        all_tasks_response = tls_service.describe_import_tasks(all_tasks_request)
        print("查询所有导入任务列表成功，总数: {}".format(all_tasks_response.get_total()))
        if all_tasks_response.get_task_info():
            print("任务列表中包含 {} 个任务".format(len(all_tasks_response.get_task_info())))
            for i, task in enumerate(all_tasks_response.get_task_info()):
                print("任务 {}: ID={}, 名称={}, 类型={}, 状态={}".format(
                    i+1, 
                    task.task_id,
                    task.task_name,
                    task.source_type,
                    task.status
                ))
    except Exception as e:
        print("综合查询导入任务列表失败: {}".format(str(e)))

    # 删除导入任务（清理资源）
    print("\n=== 清理导入任务 ===")
    if task_id:
        try:
            delete_request = DeleteImportTaskRequest(task_id=task_id)
            tls_service.delete_import_task(delete_request)
            print("TOS导入任务删除成功")
        except Exception as e:
            print("TOS导入任务删除失败: {}".format(str(e)))
    
    if kafka_task_id:
        try:
            delete_kafka_request = DeleteImportTaskRequest(task_id=kafka_task_id)
            tls_service.delete_import_task(delete_kafka_request)
            print("Kafka导入任务删除成功")
        except Exception as e:
            print("Kafka导入任务删除失败: {}".format(str(e)))

    # 删除日志主题
    print("\n=== 清理资源 ===")
    delete_topic_request = DeleteTopicRequest(topic_id)
    tls_service.delete_topic(delete_topic_request)
    print("日志主题删除成功")

    # 删除日志项目
    tls_service.delete_project(DeleteProjectRequest(project_id))
    print("日志项目删除成功")
    
    print("\n=== 导入任务示例程序执行完成 ===")