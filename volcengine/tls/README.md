# 日志服务Python SDK

火山引擎日志服务 Python SDK 封装了日志服务的常用接口，您可以通过日志服务 Python SDK 调用服务端 API，实现日志采集、日志检索等功能。

## 快速开始

### 初始化客户端

初始化 Client 实例之后，才可以向 TLS 服务发送请求。初始化时推荐通过环境变量动态获取火山引擎密钥等身份认证信息，以免 AccessKey 硬编码引发数据安全风险。

初始化代码如下：

```python
import os
from volcengine.tls.TLSService import TLSService

# 注意，环境变量中的endpoint不包含协议头（https://或http://），例如 tls-cn-beijing.ivolces.com。
endpoint = os.environ["VOLCENGINE_ENDPOINT"]
region = os.environ["VOLCENGINE_REGION"]
access_key_id = os.environ["VOLCENGINE_ACCESS_KEY_ID"]
access_key_secret = os.environ["VOLCENGINE_ACCESS_KEY_SECRET"]

tls_service = TLSService(endpoint, access_key_id, access_key_secret, region)
```

### 示例代码

本示例中，创建一个 example_tls.py 文件，并调用接口分别完成创建项目、创建主题、创建索引、写入日志数据、消费日志和查询日志数据。

代码示例如下：

```python
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
    logs = PutLogsV2Logs(source="192.168.1.1", filename="sys.log")
    for i in range(100):
        logs.add_log(contents={"key1": "value1-" + str(i + 1), "key2": "value2-" + str(i + 1)},
                     log_time=int(round(time.time())))
    tls_service.put_logs_v2(PutLogsV2Request(topic_id, logs))
    time.sleep(30)

    # 查询消费游标
    describe_cursor_request = DescribeCursorRequest(topic_id, shard_id=0, from_time="begin")
    describe_cursor_response = tls_service.describe_cursor(describe_cursor_request)

    # 消费日志数据
    consume_logs_request = ConsumeLogsRequest(topic_id, shard_id=0, cursor=describe_cursor_response.cursor)
    consume_logs_response = tls_service.consume_logs(consume_logs_request)

    # 当您需要检索和分析日志时，推荐您使用Python SDK提供的search_logs_v2方法，下面的代码提供了具体的调用示例
    # 查询日志数据（全文检索）
    search_logs_request = SearchLogsRequest(topic_id, query="error", limit=10,
                                            start_time=1346457600000, end_time=1630454400000)
    search_logs_response = tls_service.search_logs_v2(search_logs_request)

    # 查询日志数据（键值检索）
    search_logs_request = SearchLogsRequest(topic_id, query="key1:error", limit=10,
                                            start_time=1346457600000, end_time=1630454400000)
    search_logs_response = tls_service.search_logs_v2(search_logs_request)

    # 查询日志数据（SQL分析）
    search_logs_request = SearchLogsRequest(topic_id, query="* | select key1, key2", limit=10,
                                            start_time=1346457600000, end_time=1630454400000)
    search_logs_response = tls_service.search_logs_v2(search_logs_request)

    # 查询日志数据（SQL分析）
    search_logs_request = SearchLogsRequest(topic_id, query="* | select key1, key2", limit=10,
                                            start_time=1346457600000, end_time=1630454400000)
    search_logs_response = tls_service.search_logs(search_logs_request)
```


## 通过消费组消费数据

日志服务提供消费日志的OpenAPI接口ConsumeLogs，支持实时消费采集到服务端的日志数据。
在使用ConsumeLogs接口时，需要按照日志分区维度消费日志数据，消费时自行指定日志主题ID、Shard ID和起始结束游标（Cursor），所以消费日志的进度受限于单个Shard的读写能力，还需要自行维护消费进度，在Shard自动分裂的场景下消费逻辑与流程繁琐。

日志服务通过SDK提供了消费组（ConsumerGroup）功能，支持通过消费组消费日志数据，通过消费组消费时，日志服务会自动均衡各个消费者的消费能力与进度，自动分配Shard，您无需关注消费组的内部调度细节及消费者之间的负载均衡、故障转移等，只需要专注于业务逻辑。

日志服务提供了Consumer异步日志消费库，支持消费同一个日志项目下多个日志主题，具有异步消费、高性能、失败重试、优雅关闭等特性。

关于通过消费组消费数据的基本概念和限制说明等更多信息，请您参阅[通过消费组消费数据](https://www.volcengine.com/docs/6470/1152208)。

### 示例代码

以下代码以Python SDK为例，演示通过SDK创建消费组和消费者，并消费日志的整体流程。

```python
# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import time

from volcengine.tls.TLSService import TLSService
from volcengine.tls.consumer.consumer import TLSConsumer, LogProcessor
from volcengine.tls.consumer.consumer_model import ConsumerConfig
from volcengine.tls.log_pb2 import LogGroupList


# 用户需要实现一个继承LogProcessor的类，并按照业务需要自行实现process函数，用于处理消费到的每个LogGroupList
class MyLogProcessor(LogProcessor):
    def process(self, topic_id: str, shard_id: int, log_group_list: LogGroupList):
        print(topic_id + " --- " + str(shard_id))

        count = 0

        for log_group in log_group_list.log_groups:
            for log in log_group.logs:
                count += 1
                print("*** Count = {} ***".format(count))

                for content in log.contents:
                    print("{}: {}".format(content.key, content.value))
                print()


if __name__ == '__main__':
    # 初始化客户端，推荐通过环境变量动态获取火山引擎密钥等身份认证信息，以免AccessKey硬编码引发数据安全风险。详细说明请参考https://www.volcengine.com/docs/6470/1166455
    # 使用STS时，ak和sk均使用临时密钥，且设置VOLCENGINE_TOKEN；不使用STS时，VOLCENGINE_TOKEN部分传空
    endpoint = os.environ["VOLCENGINE_ENDPOINT"]
    region = os.environ["VOLCENGINE_REGION"]
    access_key_id = os.environ["VOLCENGINE_ACCESS_KEY_ID"]
    access_key_secret = os.environ["VOLCENGINE_ACCESS_KEY_SECRET"]

    # 实例化TLS客户端
    tls_service = TLSService(endpoint, access_key_id, access_key_secret, region)

    # 配置消费组的必填参数，ConsumerConfig构造函数设定了一些默认参数，您也可根据需要自定义配置
    consumer_config = ConsumerConfig(project_id="ProjectID",
                                     consumer_group_name="python-consumer-group",
                                     consumer_name="python-consumer",
                                     topic_id_list=["TopicID"])
    tls_consumer = TLSConsumer(consumer_config, tls_service, MyLogProcessor())

    # 调用start方法开始持续消费
    tls_consumer.start()

    # 可通过调用tls_consumer.stop()来结束消费组消费
    time.sleep(10)
    tls_consumer.stop()
```

### 配置说明

在上述示例代码中，ConsumerConfig类的构造函数返回了Python SDK消费组配置，并向您展示了如何配置您的endpoint、region、accessKeyID、accessKeySecret等基本信息、日志项目ID和日志主题ID列表、消费组名称和消费者名称。

除此之外，您还可通过ConsumerConfig的其他字段进行额外的自定义配置。ConsumerConfig的可配置字段如下所示。

| 参数                                  | 类型   | 示例值   | 描述                                                                                                                                                                      |
|:------------------------------------|:-----|:------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| max_fetch_log_group_count           | int  | 100   | 消费者单次消费日志时，最大获取LogGroup数量，默认为100，最大为1000。                                                                                                                               |
| heartbeat_interval_in_second        | int  | 20    | Consumer心跳上报时间间隔，单位为秒。                                                                                                                                                  |
| data_fetch_interval_in_millisecond  | int  | 200   | Consumer消费日志时间间隔，单位为毫秒。                                                                                                                                                 |
| flush_checkpoint_interval_in_second | int  | 5     | Consumer上传消费进度的时间间隔，单位为秒。                                                                                                                                               |
| consume_from                        | str  | begin | 开始消费时的默认消费位点，与DescribeCursor的From参数一致，仅在该消费者从未上传过消费位点时有效。                                                                                                               |
| ordered_consume                     | bool | false | 是否开启顺序消费。开启顺序消费后，消费者会根据Shard分裂的父子关系进行消费。例如Shard0分裂为Shard1与Shard2，而Shard1又分裂为Shard3与Shard4。在开启顺序消费之后，会根据(Shard0) -> (Shard1, Shard2) -> (Shard2, Shard3, Shard4)的顺序进行消费。 |