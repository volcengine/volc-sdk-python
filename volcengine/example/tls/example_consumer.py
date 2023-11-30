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
    consumer_config = ConsumerConfig(project_id="your-project-id",
                                     consumer_group_name="python-consumer-group",
                                     consumer_name="python-consumer",
                                     topic_id_list=["your-topic-id"])
    tls_consumer = TLSConsumer(consumer_config, tls_service, MyLogProcessor())

    # 调用start方法开始持续消费
    tls_consumer.start()

    # 可通过调用tls_consumer.stop()来结束消费组消费
    time.sleep(10)
    tls_consumer.stop()
