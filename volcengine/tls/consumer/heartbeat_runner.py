# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time
from typing import List

from readerwriterlock import rwlock

from volcengine.tls.data import ConsumeShard
from volcengine.tls.tls_requests import ConsumerHeartbeatRequest


class HeartbeatRunner:
    def __init__(self, consumer):
        self.consumer_config = consumer.consumer_config
        self.tls_service = consumer.tls_service

        self.shards = []

        self.lock = rwlock.RWLockFairD()
        self.working_flag = True

        self.logger = consumer.logger

    def run(self):
        self.logger.info("HeartbeatRunner for {} starts to work.".format(self.consumer_config.consumer_name))

        while self.working_flag:
            try:
                last_heartbeat_time = time.time()
                self.upload_heartbeat()

                sleep_time = self.consumer_config.heartbeat_interval_in_second - (time.time() - last_heartbeat_time)
                while sleep_time > 0 and self.working_flag:
                    time.sleep(min(sleep_time, 1))
                    sleep_time = self.consumer_config.heartbeat_interval_in_second - (time.time() - last_heartbeat_time)
            except Exception as e:
                self.logger.error(e)

        self.logger.info("HeartbeatRunner for {} stops.".format(self.consumer_config.consumer_name))

    def get_shards(self):
        with self.lock.gen_rlock():
            shards = self.shards

        return shards

    def set_shards(self, shards: List[ConsumeShard]):
        with self.lock.gen_wlock():
            self.shards = shards

    def upload_heartbeat(self):
        req = ConsumerHeartbeatRequest(project_id=self.consumer_config.project_id,
                                       consumer_group_name=self.consumer_config.consumer_group_name,
                                       consumer_name=self.consumer_config.consumer_name)
        resp = self.tls_service.consumer_heartbeat(req)

        self.set_shards(resp.shards)
