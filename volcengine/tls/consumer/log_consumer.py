# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import threading
import time

from readerwriterlock import rwlock

from volcengine.tls.const import LZ4, ERROR_CONSUMER_HEARTBEAT_EXPIRED
from volcengine.tls.consumer.consumer_model import ConsumerStatus, CheckpointInfo
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import DescribeCheckpointRequest, DescribeCursorRequest, ConsumeLogsRequest


class LogConsumer:
    def __init__(self, consumer, consume_shard):
        self.consumer_config = consumer.consumer_config
        self.tls_service = consumer.tls_service
        self.log_processor = consumer.log_processor

        self.checkpoint_manager = consumer.checkpoint_manager

        self.status = ConsumerStatus.PENDING
        self.shard = consume_shard

        self.next_checkpoint = None
        self.curr_log_group_list = None
        self.last_backoff_time = time.time()

        self.status_lock = rwlock.RWLockFairD()
        self.thread_running_status = False
        self.logger = consumer.logger

    def run(self):
        status = self.load_status()

        if status == ConsumerStatus.PENDING:
            self.set_status(ConsumerStatus.INITIALIZING)
            self.thread_running_status = True
            threading.Thread(target=self.run_with_status,
                             args=(self.init, ConsumerStatus.READY_TO_FETCH, ConsumerStatus.PENDING)).start()
        elif status == ConsumerStatus.READY_TO_FETCH:
            self.set_status(ConsumerStatus.FETCHING)
            self.thread_running_status = True
            threading.Thread(target=self.run_with_status,
                             args=(self.fetch_data, ConsumerStatus.READY_TO_CONSUME, ConsumerStatus.READY_TO_FETCH)).start()
        elif status == ConsumerStatus.READY_TO_CONSUME:
            self.set_status(ConsumerStatus.CONSUMING)
            self.thread_running_status = True
            threading.Thread(target=self.run_with_status,
                             args=(self.consume, ConsumerStatus.READY_TO_FETCH, ConsumerStatus.READY_TO_CONSUME)).start()
        elif status == ConsumerStatus.BACKOFF:
            if self.backoff():
                self.set_status(ConsumerStatus.BACKOFF)
            else:
                self.set_status(ConsumerStatus.READY_TO_FETCH)

    def run_with_status(self, func, done_status, err_status):
        try:
            func()
            self.set_status(done_status)
        except TLSException as e:
            if ERROR_CONSUMER_HEARTBEAT_EXPIRED in e.error_code:
                self.set_status(ConsumerStatus.WAIT_FOR_RESTART)
            elif e.http_code == 429:
                self.set_status(ConsumerStatus.BACKOFF)
            else:
                self.logger.error(e)
                self.set_status(err_status)
        except Exception as e:
            self.logger.error(e)
            self.set_status(err_status)
        finally:
            self.thread_running_status = False

    def set_status(self, status):
        with self.status_lock.gen_wlock():
            self.status = status

    def load_status(self):
        with self.status_lock.gen_rlock():
            status = self.status

        return status

    def init(self):
        project_id = self.consumer_config.project_id
        topic_id = self.shard.topic_id
        shard_id = self.shard.shard_id
        consumer_group_name = self.consumer_config.consumer_group_name

        req = DescribeCheckpointRequest(project_id, topic_id, shard_id, consumer_group_name)
        resp = self.tls_service.describe_checkpoint(req)

        if resp.checkpoint is not None and len(resp.checkpoint) > 0:
            self.next_checkpoint = resp.checkpoint
            return

        req = DescribeCursorRequest(topic_id, shard_id, from_time=self.consumer_config.consume_from)
        resp = self.tls_service.describe_cursor(req)

        self.next_checkpoint = resp.cursor

    def fetch_data(self):
        self.last_backoff_time = time.time()
        req = ConsumeLogsRequest(topic_id=self.shard.topic_id,
                                 shard_id=self.shard.shard_id,
                                 cursor=self.next_checkpoint,
                                 log_group_count=self.consumer_config.max_fetch_log_group_count,
                                 compression=self.consumer_config.compression,
                                 consumer_group_name=self.consumer_config.consumer_group_name,
                                 consumer_name=self.consumer_config.consumer_name)
        resp = self.tls_service.consume_logs(req)

        self.curr_log_group_list = resp.get_pb_message()
        self.next_checkpoint = resp.get_x_tls_cursor()

    def consume(self):
        if self.curr_log_group_list is None or len(self.curr_log_group_list.log_groups) == 0:
            return

        self.log_processor.process(topic_id=self.shard.topic_id, shard_id=self.shard.shard_id,
                                   log_group_list=self.curr_log_group_list)

        self.checkpoint_manager.add_checkpoint(CheckpointInfo(self.next_checkpoint, self.shard))

    def backoff(self):
        return time.time() - self.last_backoff_time < 5
