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

如需使用 API Key 匿名鉴权写入日志，请使用显式 API Key 初始化入口。当前匿名鉴权仅支持最终请求为 `/PutLogs` 的接口，例如 `put_logs`、`put_logs_v2` 和 Producer 写入；其他接口仍需要完整 AK/SK。

```python
tls_service = TLSService.with_api_key(
    endpoint=os.environ["VOLCENGINE_ENDPOINT"],
    region=os.environ["VOLCENGINE_REGION"],
    api_key=os.environ["VOLCENGINE_TLS_API_KEY"],
)
```

如果同时配置 API Key 与 AK/SK，`put_logs`/`put_logs_v2` 会优先使用 API Key 匿名鉴权，其他接口继续使用 AK/SK 签名：

```python
tls_service = TLSService.with_api_key(
    endpoint,
    region,
    os.environ["VOLCENGINE_TLS_API_KEY"],
    access_key_id=access_key_id,
    access_key_secret=access_key_secret,
)
```

Producer 可通过 `ProducerConfig` 透传 API Key：

```python
producer_config = ProducerConfig(endpoint, region, "", "", api_key=os.environ["VOLCENGINE_TLS_API_KEY"])
```

API Key 可在运行时更新：

```python
tls_service.reset_api_key(os.environ["VOLCENGINE_TLS_API_KEY_NEW"])
producer.reset_api_key(os.environ["VOLCENGINE_TLS_API_KEY_NEW"])
```

请勿在日志或错误信息中打印 API Key 原文。

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

## Producer 内存韧性配置

Python Producer默认保持兼容模式：`retry_mode="legacy_double_retry"`，breaker关闭，`total_size_in_bytes`继续作为batch/payload兼容预算。新增`max_producer_memory_bytes`用于限制Producer生命周期内SDK持有的日志reservation，覆盖payload、retry队列和发送阶段临时buffer；默认值为`2 * total_size_in_bytes`。

注意：`max_producer_memory_bytes`不是Python进程RSS硬上限，也不是解释器总内存上限。它只限制Producer内部对日志生命周期的reservation，压缩库、解释器对象、线程栈和第三方依赖仍会产生额外内存。

推荐生产profile：设置`retry_mode="producer_managed"`，开启`CircuitBreakerConfig(enabled=True)`，`failure_policy`使用`"fail_fast"`或`"drop_with_callback"`，并把`max_block_ms`设为`0`，让限流、熔断和丢弃通过回调快速反馈。


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

## 本地健康观测（get_stats）

Producer 和 Consumer 默认关闭观测。快照只读取本实例的预聚合状态，不执行网络请求、
文件读写或用户回调，也不遍历业务队列。读取不会启动采样线程。

### 配置和读取

```python
from volcengine.tls.producer.producer import TLSProducer
from volcengine.tls.producer.producer_model import ProducerConfig
from volcengine.tls.stats import StatsOptions, DeltaAdapter, evaluate_health

producer = TLSProducer(ProducerConfig(
    endpoint, region, access_key_id, access_key_secret,
    metrics_level="core",
))
options = StatsOptions("operational")
snapshot = producer.get_stats(options)
print(snapshot.lifecycle_state, snapshot.consistency)
print(snapshot.to_dict())
```

ConsumerConfig 同样支持末尾的可选参数 `metrics_level="off"`。
`get_stats(StatsOptions(view))` 必须显式选择视图，返回统一的 `StatsSnapshot`。
采集内容由 `metrics_level` 控制，耗时桶边界由 SDK 固定选择。
Python 的级别和视图使用字符串；Go 使用数值枚举。区块、计数、能力位与事实口径对齐，
不要把两种语言的枚举编码当成完全相同的 JSON。

| 采集级别 | 采集内容 |
|:---|:---|
| `off`（默认） | 元信息和生命周期；业务区块缺失 |
| `core` | 累计计数、当前队列/持有量、worker 汇总、成功/失败年龄、可归因内存 |
| `detailed` | Core 加固定 worker/retry 明细、四项固定边界延迟直方图、支持的内存分解 |

| 读取视图 | 请求内容 |
|:---|:---|
| `health` | 健康信号及 Producer 支持的 managed_memory |
| `operational` | Health 加累计计数和业务 gauge |
| `debug` | Operational 加 Detailed 明细 |

视图不会提升采集级别。请求但未采集的区块会省略，并通过 `partial` 和
`missing_sections` 声明；不支持的能力以 `capabilities` 位集合区分，不伪造为 0。
快照及嵌套对象不可变；`to_dict()` 返回独立副本。序列化结果不包含凭证、endpoint、
topic、异常正文或其他高基数标识。

### 运行中切换与关闭

组件处于 Running 时可调用 `producer.set_metrics_level("detailed")`，
Consumer 接口相同。配置对象仅决定初始级别；New、Closing、Closed、Failed 状态拒绝切换。

Core 与 Detailed 互切保留累计计数。跨越 Off 会增加 `collection_generation`，
保留既有累计计数并重建当前采集代的 gauge/年龄基线；关闭采集期间的业务不会补记。
旧采集代开始、之后才结束的工作也不会混入新采集代。Detailed 时延独立校验采样代，
只记录边界完整的样本。因此累计 accepted/terminal 与当前代 owned 不应跨 Off 断点直接做守恒比较。

关闭等待超时后仍存在发送或回调时，快照保持 Closing/weak；真正结束并释放资源后才发布
稳定的 final 快照。Consumer 完整停止后支持再次 start；实例标识保持不变、采集代增加，
旧 final 快照仍是不可变的历史值。

Consumer 常驻角色异常退出会进入 Failed，并停止其他角色。关闭达到超时后不再无限重试
checkpoint；已发出的网络请求仍须实际返回后才能结束。未成功保存的 checkpoint 可能导致
下次启动重复消费，业务处理应保持幂等。不会通过提前发布 final 掩盖仍在执行的任务。

### Delta 和健康判断

```python
adapter = DeltaAdapter()
previous = producer.get_stats(options)

# 由业务自己的定时器调用，例如每 15 秒读取一次。
current = producer.get_stats(options)
sample = current.counter_sample()  # Off 或 Health 视图时为 None
if sample is None:
    adapter.reset()
else:
    interval = adapter.observe(sample)
    if interval.valid:
        print(interval.rates_per_second["accepted_logs_total"])
    else:
        print(interval.reset_reason)
print(evaluate_health(previous, current).to_dict())
```

DeltaAdapter 仅保留一个计数基线；首次采样、实例/采集代变化、序列不递增、
uptime 回退、墙上 capture 时间不递增、计数回退或集合变化均不输出速率。
每次无效区间都会更新基线。健康适配器为纯函数，默认队列/内存压力阈值 0.8；
缺基线、未采集或生命周期不适合判断时返回 unknown，不能将未知当作健康。
可用 `HealthPolicy` 指定阈值。

手工构造 `CounterSample` 时，计数器必须是非负 uint64 整数。含 `None`、非整数或超界值的
区间返回 `metrics_unavailable`，不会把缺失值当作 0。`HealthPolicy` 的 `None` 或非有限数值
在评估时使用默认阈值 0.8。

Producer 的 `rejected_memory_full_total` 与 `rejected_managed_admission_total`
描述同一类内存准入拒绝，是跨 SDK 字段映射，不能相加。

### 延迟与内存口径

Detailed 固定采集以下四项；每项携带 start/end/unit/object/includes_retry 元数据，
桶边界与 Go SDK 对应，`bucket_profile` 为 `fast` 或 `slow`。
耗时使用单调时钟，快照 capture 使用墙上时间。

| 组件 | 四项直方图 |
|:---|:---|
| Producer | batch_queue_delay（batch ready 到发送尝试）、send_call_duration（transport 调用）、batch_delivery_duration（首次发送尝试到终态）、callback_duration |
| Consumer | fetch_call_duration、dispatch_delay、process_duration、checkpoint_call_duration |

Producer `managed_memory` 是现有 SDK 限制器的 payload 与有界临时 buffer 记账，
不代表 Python 进程 RSS、解释器、分配器或第三方 HTTP client 的全部内存。
`used_bytes = payload_owned_bytes + bounded_runtime_buffer_bytes`；
Detailed 分解中的 ingress/aggregate/send/retry 所有权之和等于 payload。
Off 切换期间存在无法可靠归入新采集代的旧分配时，相关区块标为缺失，待旧分配释放后恢复。

Python 没有 Go 独立的 batch_inflight gate，不声明该能力。有效内存压力取已有
payload admission 和总 lifecycle 限额利用率的较大值，来源分别为
`managed_payload_admission` / `managed_lifecycle`；不能只用总利用率掩盖 payload 拒绝。
Consumer 不声明 managed_memory 或 memory_breakdown。

同一连续采集代内，Producer 接受后只结算一次终态，重试不会再次 accepted。
Consumer 待处理 batch 在回调开始时释放 held/ready 记账，回调期间只计入 process_in_flight；
回调失败并等待重试时重新计入 held/ready，每次接管都只释放一次。
checkpoint pending 反映真实待提交项，未可靠采集的最老年龄不输出。

### 离线示例

`python -m volcengine.tls.example.get_stats_example` 可离线运行，不访问 TLS 服务。
支持 Python 3.7 及以上。

### 离线测试

安装项目依赖后，在仓库根目录执行：

```bash
python -m volcengine.tls.test.run_observability_tests
```

该入口运行观测、生命周期、并发、内存、重试和计量回归测试，并检查意外网络请求与
测试结束后的线程泄漏。测试按职责组织，不依赖真实 TLS 环境。
