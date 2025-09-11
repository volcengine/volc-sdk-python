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
from volcengine.tls.producer.producer import TLSProducer
from volcengine.tls.producer.producer_model import CallBack, ProducerConfig
from volcengine.tls.tls_requests import PutLogsV2LogContent

produce_success_count = 0
produce_failed_count = 0


class MyCallBack(CallBack):
    def __init__(self, logs: list[PutLogsV2LogContent]):
        self.logs = logs

    def on_complete(self, result: 'Result'):
        global produce_success_count
        global produce_failed_count
        if result.success:
            produce_success_count += len(self.logs)
        else:
            produce_failed_count += len(self.logs)


if __name__ == '__main__':
    # 初始化客户端，推荐通过环境变量动态获取火山引擎密钥等身份认证信息，以免AccessKey硬编码引发数据安全风险。详细说明请参考https://www.volcengine.com/docs/6470/1166455
    # 使用STS时，ak和sk均使用临时密钥，且设置VOLCENGINE_TOKEN；不使用STS时，VOLCENGINE_TOKEN部分传空
    # endpoint = "https://tls-cn-beijing.volces.com"
    # region = "cn-beijing"
    # access_key_id = "AKLxxxxxxxx"
    # access_key_secret = "TUxxxxxxxxxx=="
    endpoint = os.environ["VOLCENGINE_ENDPOINT"]
    region = os.environ["VOLCENGINE_REGION"]
    access_key_id = os.environ["VOLCENGINE_ACCESS_KEY_ID"]
    access_key_secret = os.environ["VOLCENGINE_ACCESS_KEY_SECRET"]
    topic_id = "your-topic-id"

    producer_config = ProducerConfig(
        endpoint=endpoint,
        access_key=access_key_id,
        access_secret=access_key_secret,
        region=region,
    )
    tls_producer = TLSProducer(producer_config)
    tls_producer.start()

    for i in range(10):
        logs = [PutLogsV2LogContent(
            log_dict={
                "key": "key-" + str(i),
                "value": "test-message-" + str(i)
            },
            time=int(time.time()) - 300
        ), PutLogsV2LogContent(
            log_dict={
                "key": "key1-" + str(i),
                "value": "test-message1-" + str(i)
            },
            time=int(time.time()) - 300
        )]
        callback = MyCallBack(logs)
        tls_producer.send_logs_v2("", topic_id, "", "", logs, callback)
    # 等待所有消息发送完成
    time.sleep(5)
    tls_producer.close()
    print("*****produce success count: " + str(produce_success_count))
    print("*****produce failed count: " + str(produce_failed_count))
