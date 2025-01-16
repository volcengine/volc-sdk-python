# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import threading
import time
from typing import List

from volcengine.tls.TLSService import TLSService
from volcengine.tls.const import ERROR_CONSUMER_GROUP_ALREADY_EXISTS
from volcengine.tls.consumer.checkpoint_manager import CheckpointManager
from volcengine.tls.consumer.consumer_model import ConsumerConfig, ConsumerStatus
from volcengine.tls.consumer.heartbeat_runner import HeartbeatRunner
from volcengine.tls.consumer.log_consumer import LogConsumer
from volcengine.tls.data import ConsumeShard
from volcengine.tls.log_pb2 import LogGroupList
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import CreateConsumerGroupRequest, DescribeConsumerGroupsRequest
from volcengine.tls.util import get_logger


class LogProcessor:
    @abc.abstractmethod
    def process(self, topic_id: str, shard_id: int, log_group_list: LogGroupList):
        raise NotImplementedError("Please implement the process method.")


class TLSConsumer:
    def __init__(self, consumer_config: ConsumerConfig, tls_service: TLSService, log_processor: LogProcessor):
        consumer_config.validate()
        self.logger = get_logger("tls-python-sdk-consumer-logger")

        self.consumer_config = consumer_config
        self.tls_service = tls_service
        self.log_processor = log_processor

        self.working_flag = True
        self.heartbeat_runner = HeartbeatRunner(self)
        self.checkpoint_manager = CheckpointManager(self)
        self.worker_map = {}

        self.run_thread = None
        self.heartbeat_thread = None
        self.checkpoint_thread = None

        self.logger.info("TLS consumer {} is initialized.".format(self.consumer_config.consumer_name))

    def start(self):
        self.working_flag = True
        self.heartbeat_runner.working_flag = True
        self.checkpoint_manager.working_flag = True

        self.init()

        thread_name_prefix = self.consumer_config.consumer_name
        self.heartbeat_thread = threading.Thread(target=self.heartbeat_runner.run,
                                                 name=thread_name_prefix + "-HeartbeatRunner")
        self.checkpoint_thread = threading.Thread(target=self.checkpoint_manager.run,
                                                  name=thread_name_prefix + "-CheckpointManager")
        self.run_thread = threading.Thread(target=self.run, name=thread_name_prefix)

        self.heartbeat_thread.start()
        self.checkpoint_thread.start()
        self.run_thread.start()
    
    def stop(self):
        stop_timeout = self.consumer_config.stop_timeout

        self.working_flag = False
        self.run_thread.join(timeout=stop_timeout)

        current_time = time.time()
        for worker in self.worker_map.values():
            while True:
                if not worker.thread_running_status:
                    break
                elapsed_time = time.time() - current_time
                if elapsed_time >= stop_timeout:
                    self.logger.error("Stopping the thread timeouts and has already wait for {} seconds.".format(elapsed_time))
                    break
                time.sleep(1)
        self.worker_map.clear()

        self.checkpoint_manager.working_flag = False
        self.checkpoint_thread.join(timeout=stop_timeout)

        self.heartbeat_runner.working_flag = False
        self.heartbeat_thread.join(timeout=stop_timeout)

        self.logger.info("TLS consumer {} is stopped.".format(self.consumer_config.consumer_name))
    
    def reset_access_key_token(self, access_key_id: str, access_key_secret: str, security_token: str = None):
        self.tls_service.reset_access_key_token(access_key_id, access_key_secret, security_token)

    def init(self):

        req = DescribeConsumerGroupsRequest(project_id=self.consumer_config.project_id,
                                           consumer_group_name=self.consumer_config.consumer_group_name)

        res = self.tls_service.describe_consumer_groups(req)

        for consumer_group in res.consumer_groups:
            if consumer_group.consumer_group_name == self.consumer_config.consumer_group_name:
                return

        req = CreateConsumerGroupRequest(project_id=self.consumer_config.project_id,
                                         consumer_group_name=self.consumer_config.consumer_group_name,
                                         topic_id_list=self.consumer_config.topic_id_list,
                                         heartbeat_ttl=3*self.consumer_config.heartbeat_interval_in_second,
                                         ordered_consume=self.consumer_config.ordered_consume)
        try:
            self.tls_service.create_consumer_group(req)
        except TLSException as e:
            if ERROR_CONSUMER_GROUP_ALREADY_EXISTS not in e.error_code:
                self.logger.error(e.__str__())
                raise e

    def run(self):
        self.logger.info("Consumer {} starts to work.".format(self.consumer_config.consumer_name))

        while self.working_flag:
            time.sleep(self.consumer_config.data_fetch_interval_in_millisecond / 1000)
            if not self.working_flag:
                break

            for worker in self.worker_map.values():
                if worker.load_status() == ConsumerStatus.WAIT_FOR_RESTART:
                    try:
                        self.heartbeat_runner.upload_heartbeat()
                        self.checkpoint_manager.upload_checkpoint()
                        break
                    except Exception as e:
                        self.logger.error(e)

            shards = self.heartbeat_runner.get_shards()
            self.handle_shards(shards)

    def handle_shards(self, shards: List[ConsumeShard]):
        if shards is None:
            return

        shard_map = {}
        for shard in shards:
            shard_map[shard.topic_id + str(shard.shard_id)] = shard

        invalid_shards = []
        for shard_name in self.worker_map.keys():
            if shard_name not in shard_map:
                invalid_shards.append(shard_name)
        for shard_name in invalid_shards:
            del self.worker_map[shard_name]

        for key in shard_map.keys():
            if key not in self.worker_map or self.worker_map[key].load_status() == ConsumerStatus.WAIT_FOR_RESTART:
                self.worker_map[key] = LogConsumer(self, shard_map[key])

        for worker in self.worker_map.values():
            worker.run()
