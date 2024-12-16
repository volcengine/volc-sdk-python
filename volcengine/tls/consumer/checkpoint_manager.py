# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time

from readerwriterlock import rwlock

from volcengine.tls.consumer.consumer_model import CheckpointInfo
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import ModifyCheckpointRequest


class CheckpointManager:
    def __init__(self, consumer):
        self.consumer_config = consumer.consumer_config
        self.tls_service = consumer.tls_service

        self.checkpoint_info_map = {}
        self.map_lock = rwlock.RWLockFairD()

        self.working_flag = True

        self.logger = consumer.logger

    def run(self):
        self.logger.info("CheckpointManager for {} starts to work.".format(self.consumer_config.consumer_name))

        while self.working_flag:
            try:
                last_upload_time = time.time()
                self.upload_checkpoint()

                sleep_time = self.consumer_config.flush_checkpoint_interval_in_second - (time.time() - last_upload_time)
                while sleep_time > 0 and self.working_flag:
                    time.sleep(min(sleep_time, 1))
                    sleep_time = self.consumer_config.flush_checkpoint_interval_in_second - (time.time() - last_upload_time)
            except Exception as e:
                self.logger.error(e)

        while len(self.checkpoint_info_map) > 0:
            try:
                self.upload_checkpoint()
            except Exception as e:
                self.logger.error(e)

        self.logger.info("CheckpointManager for {} stops.".format(self.consumer_config.consumer_name))

    def add_checkpoint(self, checkpoint_info: CheckpointInfo):
        with self.map_lock.gen_wlock():
            shard_info = checkpoint_info.shard_info
            topic_id = shard_info.topic_id
            shard_id = shard_info.shard_id

            self.checkpoint_info_map[topic_id + str(shard_id)] = checkpoint_info

    def upload_checkpoint(self):
        with self.map_lock.gen_wlock():
            checkpoint_snapshot = self.checkpoint_info_map.copy()
        project_id = self.consumer_config.project_id
        consumer_group_name = self.consumer_config.consumer_group_name
        uploaded_checkpoint_map = {}

        try:
            for key, value in checkpoint_snapshot.items():
                shard_info = value.shard_info
                topic_id = shard_info.topic_id
                shard_id = shard_info.shard_id
                checkpoint = value.checkpoint

                req = ModifyCheckpointRequest(project_id, topic_id, shard_id, consumer_group_name, checkpoint)
                self.tls_service.modify_checkpoint(req)

                uploaded_checkpoint_map[key] = value
        except TLSException as e:
            self.logger.error("Uploading checkpoint failed.")
            raise e
        finally:
            with self.map_lock.gen_wlock():
                for key, value in uploaded_checkpoint_map.items():
                    if value.checkpoint == self.checkpoint_info_map[key].checkpoint:
                        del self.checkpoint_info_map[key]
