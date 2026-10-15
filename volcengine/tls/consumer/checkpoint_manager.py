# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time
import threading

from readerwriterlock import rwlock

from volcengine.tls.consumer.consumer_model import CheckpointInfo
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import ModifyCheckpointRequest


class CheckpointManager:
    def __init__(self, consumer):
        self.consumer = consumer
        self.consumer_config = consumer.consumer_config
        self.tls_service = consumer.tls_service

        self.checkpoint_info_map = {}
        self.map_lock = rwlock.RWLockFairD()

        self.working_flag = True
        self.force_stop = False
        self._stop_event = threading.Event()

        self.logger = consumer.logger
        self.stats_state = getattr(consumer, "stats_state", None)
        bind_provider = getattr(self.stats_state, "bind_checkpoint_provider", None)
        if bind_provider is not None:
            bind_provider(self._checkpoint_snapshot,
                          lambda: len(getattr(consumer, "worker_map", {})))

    def _retry_delay(self):
        # Keep failed checkpoint retries bounded and yield CPU in both the
        # regular loop and the stop-time drain loop.
        return max(
            0.01,
            min(1.0, self.consumer_config.flush_checkpoint_interval_in_second))

    def _latency(self):
        s = self.stats_state
        return s if (s is not None and s.latency_enabled) else None

    def _checkpoint_snapshot(self):
        """Return only the pending size owned by this manager.

        The manager intentionally does not guess an oldest shard after a
        prefix deletion.  The state keeps the bounded HWM; oldest age remains
        absent unless a future owner can provide it without a map scan.
        """
        with self.map_lock.gen_rlock():
            return len(self.checkpoint_info_map)

    def run(self):
        self.logger.info("CheckpointManager for {} starts to work.".format(self.consumer_config.consumer_name))

        while self.working_flag:
            try:
                last_upload_time = time.time()
                self.upload_checkpoint()

                sleep_time = self.consumer_config.flush_checkpoint_interval_in_second - (time.time() - last_upload_time)
                while sleep_time > 0 and self.working_flag:
                    self._stop_event.wait(min(sleep_time, 1))
                    sleep_time = self.consumer_config.flush_checkpoint_interval_in_second - (time.time() - last_upload_time)
            except Exception as e:
                self.logger.error(e)
                if self.working_flag:
                    time.sleep(self._retry_delay())

        while len(self.checkpoint_info_map) > 0 and not self.force_stop:
            try:
                self.upload_checkpoint()
            except Exception as e:
                self.logger.error(e)
                # Stop drains checkpoints after the regular loop exits.  A
                # persistent backend failure must yield between retries; the
                # stop event is already set, so waiting on it would return
                # immediately and recreate the old busy loop.
                time.sleep(self._retry_delay())

        self.logger.info("CheckpointManager for {} stops.".format(self.consumer_config.consumer_name))

    def add_checkpoint(self, checkpoint_info: CheckpointInfo):
        with self.map_lock.gen_wlock():
            shard_info = checkpoint_info.shard_info
            topic_id = shard_info.topic_id
            shard_id = shard_info.shard_id

            key = topic_id + str(shard_id)
            self.checkpoint_info_map[key] = checkpoint_info
        # Pending count uses the actual checkpoint map; oldest age is unknown.
        stats = self.stats_state
        if stats is not None:
            stats.checkpoint_add(key, token=stats.token())

    def upload_checkpoint(self):
        with self.map_lock.gen_wlock():
            checkpoint_snapshot = self.checkpoint_info_map.copy()
        project_id = self.consumer_config.project_id
        consumer_group_name = self.consumer_config.consumer_group_name
        uploaded_checkpoint_map = {}
        stats = self.stats_state

        try:
            for key, value in checkpoint_snapshot.items():
                shard_info = value.shard_info
                topic_id = shard_info.topic_id
                shard_id = shard_info.shard_id
                checkpoint = value.checkpoint

                req = ModifyCheckpointRequest(project_id, topic_id, shard_id, consumer_group_name, checkpoint)
                # Each transport call is its own observation boundary.  A
                # metrics switch during an earlier request must not make the
                # next request's current-generation result look stale.
                generation = stats.token() if stats is not None else 0
                lat = self._latency()
                detail_generation = stats.detail_token() if stats is not None else 0
                if stats is not None:
                    stats.on_checkpoint_flush_start(token=generation)
                # checkpoint_call_duration: modify_checkpoint start -> return/raise
                # (plan §9). Recorded on the latency switch alone.
                _ck_start_ns = lat._clock.monotonic_ns() if lat is not None else None
                try:
                    self.tls_service.modify_checkpoint(req)
                    if stats is not None:
                        stats.on_checkpoint_call(success=True, token=generation)
                except Exception:
                    if self.stats_state is not None:
                        self.stats_state.record_error("checkpoint", token=generation)
                    if stats is not None:
                        stats.on_checkpoint_call(success=False, token=generation)
                    raise
                finally:
                    if lat is not None:
                        lat.observe_ns("checkpoint_call_duration",
                                       lat._clock.monotonic_ns() - _ck_start_ns,
                                       detail_token=detail_generation)
                    if stats is not None:
                        stats.on_checkpoint_flush_end(token=generation)

                uploaded_checkpoint_map[key] = value
        except Exception:
            self.logger.error("Uploading checkpoint failed.")
            raise
        finally:
            cleared_keys = []
            with self.map_lock.gen_wlock():
                for key, value in uploaded_checkpoint_map.items():
                    current = self.checkpoint_info_map.get(key)
                    if current is not None and value.checkpoint == current.checkpoint:
                        del self.checkpoint_info_map[key]
                        cleared_keys.append(key)
            if stats is not None:
                for key in cleared_keys:
                    # Map deletion is business state and already happened
                    # above.  Observe the clear using the generation current
                    # at the clear boundary, rather than a completed request's
                    # potentially stale token.
                    stats.checkpoint_clear(key, token=stats.token())
