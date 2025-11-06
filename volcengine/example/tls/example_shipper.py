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
    create_project_request = CreateProjectRequest(project_name="shipper-project-" + now, region=region,
                                                  description="project for shipper test")
    create_project_response = tls_service.create_project(create_project_request)
    project_id = create_project_response.get_project_id()
    print("创建日志项目成功，project_id: {}".format(project_id))

    # 创建日志主题
    create_topic_request = CreateTopicRequest(
        topic_name="shipper-topic-" + now,
        project_id=project_id,
        ttl=5,
        description="topic for shipper test",
        shard_count=2,
    )
    create_topic_response = tls_service.create_topic(create_topic_request)
    topic_id = create_topic_response.get_topic_id()
    print("创建日志主题成功，topic_id: {}".format(topic_id))

    # 示例1：创建TOS投递配置
    print("\n=== 创建TOS投递配置 ===")
    
    # JSON格式内容配置
    json_info = JsonInfo(
        enable=True,
        keys=["__content__", "__time__", "__source__", "level", "message"],  # 指定要投递的字段
        escape=True
    )
    
    # 内容信息配置
    content_info = ContentInfo(
        format="json",  # JSON格式
        json_info=json_info
    )
    
    # TOS投递信息配置
    tos_shipper_info = TosShipperInfo(
        bucket="bucket-for-import-sdk-test",  # 请替换为您的TOS存储桶名称
        prefix="logs/shipper/",  # 投递路径前缀
        max_size=256,  # 每个分片最大投递文件大小（MiB）
        compress="snappy",  # 压缩格式
        interval=300,  # 投递时间间隔（秒）
        partition_format="%Y/%m/%d/%H"  # 分区格式
    )
    
    # 创建TOS投递配置请求
    create_tos_shipper_request = CreateShipperRequest(
        topic_id=topic_id,
        shipper_name="tos-shipper-" + now,
        shipper_type="tos",  # TOS投递类型
        content_info=content_info,
        tos_shipper_info=tos_shipper_info,
        shipper_start_time=int(time.time() * 1000),  # 当前时间作为开始时间
        shipper_end_time=int((time.time() + 3600) * 1000)  # 1小时后结束
    )
    
    try:
        create_tos_response = tls_service.create_shipper(create_tos_shipper_request)
        tos_shipper_id = create_tos_response.get_shipper_id()
        print("TOS投递配置创建成功，shipper_id: {}".format(tos_shipper_id))
        
        # 验证查询TOS投递配置
        print("\n=== 验证查询TOS投递配置 ===")
        try:
            describe_tos_request = DescribeShipperRequest(shipper_id=tos_shipper_id)
            tos_info = tls_service.describe_shipper(describe_tos_request)
            print("查询TOS投递配置成功")
            print("投递配置名称: {}".format(tos_info.get_shipper_name()))
            print("投递类型: {}".format(tos_info.get_shipper_type()))
            print("状态: {}".format(tos_info.get_status()))
            print("TOS存储桶: {}".format(tos_info.get_tos_shipper_info().bucket))
            print("投递路径: {}".format(tos_info.get_tos_shipper_info().prefix))
        except Exception as e:
            print("查询TOS投递配置失败: {}".format(str(e)))
        
        # 验证修改TOS投递配置
        print("\n=== 验证修改TOS投递配置 ===")
        try:
            # 修改投递间隔和压缩格式
            modified_tos_info = TosShipperInfo(
                bucket="bucket-for-import-sdk-test",
                prefix="logs/modified/",
                max_size=128,  # 修改为128MiB
                compress="gzip",  # 修改为gzip压缩
                interval=600,  # 修改为10分钟
                partition_format="%Y/%m/%d"  # 修改分区格式
            )
            
            modify_tos_request = ModifyShipperRequest(
                shipper_id=tos_shipper_id,
                shipper_name="modified-tos-shipper-" + now,
                tos_shipper_info=modified_tos_info,
                status=False  # 暂停投递
            )
            
            modify_tos_response = tls_service.modify_shipper(modify_tos_request)
            print("修改TOS投递配置成功")
        except Exception as e:
            print("修改TOS投递配置失败: {}".format(str(e)))
            
    except Exception as e:
        print("TOS投递配置创建失败: {}".format(str(e)))
        tos_shipper_id = None

    # 示例2：创建Kafka投递配置
    print("\n=== 创建Kafka投递配置 ===")
    
    # original格式内容配置
    json_info = JsonInfo(
        keys=["timestamp", "level", "service", "message", "request_id"],  # JSON字段
        escape=True
    )
    
    # 内容信息配置
    content_info_csv = ContentInfo(
        format="original",  # CSV格式
        json_info=json_info
    )
    
    # Kafka投递信息配置
    kafka_shipper_info = KafkaShipperInfo(
        instance="kafka-cnoe27xibel3vjxd",  # Kafka实例ID
        kafka_topic="test1",  # Kafka Topic名称
        compress="snappy",  # 压缩格式
        start_time=int(time.time() * 1000),  # 开始时间
        end_time=int((time.time() + 3600) * 1000)  # 1小时后结束
    )
    
    # 创建Kafka投递配置请求
    create_kafka_shipper_request = CreateShipperRequest(
        topic_id=topic_id,
        shipper_name="kafka-shipper-" + now,
        shipper_type="kafka",  # Kafka投递类型
        content_info=content_info_csv,
        kafka_shipper_info=kafka_shipper_info
    )
    
    try:
        create_kafka_response = tls_service.create_shipper(create_kafka_shipper_request)
        kafka_shipper_id = create_kafka_response.get_shipper_id()
        print("Kafka投递配置创建成功，shipper_id: {}".format(kafka_shipper_id))
        
        # 验证查询Kafka投递配置
        print("\n=== 验证查询Kafka投递配置 ===")
        try:
            describe_kafka_request = DescribeShipperRequest(shipper_id=kafka_shipper_id)
            describe_kafka_response = tls_service.describe_shipper(describe_kafka_request)
            print("查询Kafka投递配置成功")
            print("投递配置名称: {}".format(describe_kafka_response.get_shipper_name()))
            print("投递类型: {}".format(describe_kafka_response.get_shipper_type()))
            print("Kafka实例: {}".format(describe_kafka_response.get_kafka_shipper_info().instance))
            print("Kafka Topic: {}".format(describe_kafka_response.get_kafka_shipper_info().kafka_topic))
        except Exception as e:
            print("查询Kafka投递配置失败: {}".format(str(e)))
        
        # 验证修改Kafka投递配置
        print("\n=== 验证修改Kafka投递配置 ===")
        try:
            # 修改Kafka配置
            modified_kafka_info = KafkaShipperInfo(
                instance="kafka-cnoe27xibel3vjxd",
                kafka_topic="test1",  # 修改Topic名称
                compress="gzip"  # 修改为gzip压缩
            )
            
            modify_kafka_request = ModifyShipperRequest(
                shipper_id=kafka_shipper_id,
                shipper_name="modified-kafka-shipper-" + now,
                kafka_shipper_info=modified_kafka_info,
                status=True  # 启用投递
            )
            
            modify_kafka_response = tls_service.modify_shipper(modify_kafka_request)
            print("修改Kafka投递配置成功")
        except Exception as e:
            print("修改Kafka投递配置失败: {}".format(str(e)))
            
    except Exception as e:
        print("Kafka投递配置创建失败: {}".format(str(e)))
        kafka_shipper_id = None

    # 示例3：查询投递配置列表
    print("\n=== 查询投递配置列表 ===")
    try:
        # 查询所有投递配置
        describe_shippers_request = DescribeShippersRequest(
            project_id=project_id,
            topic_id=topic_id,
            page_number=1,
            page_size=20
        )
        
        shippers_response = tls_service.describe_shippers(describe_shippers_request)
        print("查询投递配置列表成功")
        print("总配置数: {}".format(shippers_response.get_total()))
        
        shipper_list = shippers_response.get_shippers()
        print("获取到 {} 个投递配置".format(len(shipper_list)))
        
        for i, shipper in enumerate(shipper_list):
            print("配置 {}: ID={}, 名称={}, 类型={}, 状态={}".format(
                i + 1,
                shipper.shipper_id,
                shipper.shipper_name,
                shipper.shipper_type,
                shipper.status
            ))
            
    except Exception as e:
        print("查询投递配置列表失败: {}".format(str(e)))

    # 示例4：按类型筛选查询
    print("\n=== 按类型筛选投递配置 ===")
    try:
        # 查询TOS类型的投递配置
        tos_shippers_request = DescribeShippersRequest(
            page_number=1,
            page_size=10
        )
        
        tos_shippers_response = tls_service.describe_shippers(tos_shippers_request)
        print("TOS类型投递配置数: {}".format(tos_shippers_response.get_total()))
        if tos_shippers_response.get_shippers():
            print("第一个投递配置: {}".format(
                tos_shippers_response.get_shippers()[0].json()
            ))
        
        # 查询Kafka类型的投递配置
        kafka_shippers_request = DescribeShippersRequest(
            shipper_type="kafka",  # 筛选Kafka类型
            page_number=1,
            page_size=10
        )
        
        kafka_shippers_response = tls_service.describe_shippers(kafka_shippers_request)
        print("Kafka类型投递配置数: {}".format(kafka_shippers_response.get_total()))
        if kafka_shippers_response.get_shippers():
            print("第一个Kafka配置: {}".format(
                kafka_shippers_response.get_shippers()[0].json()
            ))

    except Exception as e:
        print("按类型筛选查询失败: {}".format(str(e)))

    # 清理资源
    print("\n=== 清理投递配置 ===")
    if tos_shipper_id:
        try:
            delete_tos_request = DeleteShipperRequest(shipper_id=tos_shipper_id)
            tls_service.delete_shipper(delete_tos_request)
            print("TOS投递配置删除成功")
        except Exception as e:
            print("TOS投递配置删除失败: {}".format(str(e)))
    
    if kafka_shipper_id:
        try:
            delete_kafka_request = DeleteShipperRequest(shipper_id=kafka_shipper_id)
            tls_service.delete_shipper(delete_kafka_request)
            print("Kafka投递配置删除成功")
        except Exception as e:
            print("Kafka投递配置删除失败: {}".format(str(e)))

    # 删除日志主题和项目
    print("\n=== 清理日志资源 ===")
    delete_topic_request = DeleteTopicRequest(topic_id)
    tls_service.delete_topic(delete_topic_request)
    print("日志主题删除成功")

    tls_service.delete_project(DeleteProjectRequest(project_id))
    print("日志项目删除成功")
    
    print("\n=== Shipper示例程序执行完成 ===")