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
        self.consumer = consumer
        self.consumer_config = consumer.consumer_config
        self.tls_service = consumer.tls_service
        self.log_processor = consumer.log_processor

        self.checkpoint_manager = consumer.checkpoint_manager
        self.stats_state = getattr(consumer, "stats_state", None)

        self.status = ConsumerStatus.PENDING
        self.shard = consume_shard

        self.next_checkpoint = None
        self.curr_log_group_list = None
        self.last_backoff_time = time.time()
        # Once-release token for the currently held fetched batch (if any).
        self._held_token = None
        # Monotonic instant the batch became held (for dispatch_delay latency).
        self._held_since_ns = None
        # Detail generation at the batch-ready boundary.  Dispatch latency is
        # only attributable when both the ready and callback-start events
        # belong to the same detail collection generation.
        self._held_detail_token = 0
        # Revocation races a blocked fetch.  This lock serializes only local
        # publication/release of a fetched batch; no transport call runs
        # while it is held.
        self._lifecycle_lock = threading.RLock()
        self._revoked = False

        self.status_lock = rwlock.RWLockFairD()
        self.thread_running_status = False
        self.thread = None
        self.logger = consumer.logger

    def _stats(self):
        s = self.stats_state
        return s if (s is not None and s.enabled) else None

    def _generation(self):
        s = self.stats_state
        return s.token() if s is not None else 0

    def _detail_generation(self):
        s = self.stats_state
        return s.detail_token() if s is not None else 0

    def _latency(self):
        """State for fixed-profile latency recording at Detailed level."""
        s = self.stats_state
        return s if (s is not None and s.latency_enabled) else None

    def run(self):
        status = self.load_status()

        if status == ConsumerStatus.PENDING:
            self.set_status(ConsumerStatus.INITIALIZING)
            self.thread_running_status = True
            self._spawn(self.init, ConsumerStatus.READY_TO_FETCH, ConsumerStatus.PENDING)
        elif status == ConsumerStatus.READY_TO_FETCH:
            self.set_status(ConsumerStatus.FETCHING)
            self.thread_running_status = True
            self._spawn(self.fetch_data, ConsumerStatus.READY_TO_CONSUME, ConsumerStatus.READY_TO_FETCH)
        elif status == ConsumerStatus.READY_TO_CONSUME:
            self.set_status(ConsumerStatus.CONSUMING)
            self.thread_running_status = True
            self._spawn(self.consume, ConsumerStatus.READY_TO_FETCH, ConsumerStatus.READY_TO_CONSUME)
        elif status == ConsumerStatus.BACKOFF:
            if self.backoff():
                self.set_status(ConsumerStatus.BACKOFF)
            else:
                self.set_status(ConsumerStatus.READY_TO_FETCH)

    def _spawn(self, func, done_status, err_status):
        """Create and start a shard worker thread, maintaining shard-task health
        gauges. On thread creation/start failure, roll back the submitted/in-flight
        bookkeeping and record an internal error so stats never corrupt the
        original control flow (plan §11.2)."""
        stats = self.stats_state
        generation = self._generation()
        if stats is not None:
            stats.on_shard_task_submitted(token=generation)
        try:
            thread = threading.Thread(target=self.run_with_status,
                                      args=(func, done_status, err_status, generation))
            self.thread = thread
            register = getattr(self.consumer, "_register_worker_thread", None)
            if register is not None:
                register(thread)
            thread.start()
        except Exception:
            # Thread could not be created/started: roll back gauges, mark this
            # worker not running, and restore the prior status so the main loop
            # can retry. Re-raise nothing new beyond what the runtime raised.
            if stats is not None:
                stats.on_shard_task_start_failed(token=generation)
            unregister = getattr(self.consumer, "_unregister_worker_thread", None)
            if unregister is not None:
                unregister(thread if "thread" in locals() else None)
            self.thread_running_status = False
            self.set_status(err_status)
            raise

    def run_with_status(self, func, done_status, err_status, generation=None):
        stats = self.stats_state
        if generation is None:
            generation = self._generation()
        if stats is not None:
            stats.on_shard_task_started(token=generation)
        try:
            func()
            self.set_status(done_status)
        except TLSException as e:
            if ERROR_CONSUMER_HEARTBEAT_EXPIRED in e.error_code:
                self.set_status(ConsumerStatus.WAIT_FOR_RESTART)
            elif e.http_code == 429:
                if stats is not None:
                    stats.on_backoff(token=generation)
                self.set_status(ConsumerStatus.BACKOFF)
            else:
                self.logger.error(e)
                self.set_status(err_status)
        except Exception as e:
            self.logger.error(e)
            self.set_status(err_status)
        finally:
            self.thread_running_status = False
            if stats is not None:
                stats.on_shard_task_done(token=generation)
            unregister = getattr(self.consumer, "_unregister_worker_thread", None)
            if unregister is not None:
                unregister(threading.current_thread())

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
        state = self.stats_state
        lat = self._latency()
        generation = self._generation()
        detail_generation = self._detail_generation()
        clock = state if state is not None and generation else (lat if lat is not None else None)
        start_ns = clock._clock.monotonic_ns() if clock is not None else None
        if state is not None:
            state.on_fetch_start(token=generation)
        fetch_ok = False
        group_count = 0
        log_count = 0
        curr_log_group_list = None
        next_checkpoint = None
        try:
            resp = self.tls_service.consume_logs(req)
            # Parse both response fields inside the measured operation.  A
            # malformed response is a failed fetch and must close its
            # in-flight gauge just like a transport exception.
            curr_log_group_list = resp.get_pb_message()
            next_checkpoint = resp.get_x_tls_cursor()
            if curr_log_group_list is not None:
                groups = getattr(curr_log_group_list, "log_groups", [])
                group_count = len(groups)
                if generation:
                    for group in groups:
                        log_count += len(getattr(group, "logs", []))
            fetch_ok = True
        except Exception:
            if state is not None:
                state.record_error("fetch", token=generation)
            raise
        finally:
            if lat is not None:
                lat.observe_ns("fetch_call_duration", lat._clock.monotonic_ns() - start_ns,
                               detail_token=detail_generation)
            if state is not None:
                state.on_fetch_end(success=fetch_ok, log_groups=group_count if fetch_ok else 0,
                                   logs=log_count if fetch_ok else 0,
                                   token=generation)
            if fetch_ok:
                # A revoke can happen while the transport call is blocked.
                # Publish the fetched batch and acquire its held token in the
                # same local lifecycle critical section as revoke/release.
                with self._lifecycle_lock:
                    if not self._revoked:
                        self.curr_log_group_list = curr_log_group_list
                        self.next_checkpoint = next_checkpoint
                    if not self._revoked and state is not None:
                        # Take ownership of a held batch only if it contains
                        # data to process. The detail token is sampled at
                        # readiness, rather than callback start, to prevent
                        # Core->Detailed transitions from manufacturing delay.
                        if group_count > 0:
                            self._held_token = state.acquire_held(
                                logs=log_count, groups=group_count,
                                token=generation)
                            self._held_since_ns = state._clock.monotonic_ns()
                            self._held_detail_token = state.detail_token()
                        else:
                            self._held_detail_token = 0
                    elif (not self._revoked and lat is not None
                          and group_count > 0):
                        # Preserve the readiness boundary if only the timing
                        # state is supplied by an internal caller.
                        self._held_since_ns = lat._clock.monotonic_ns()
                        self._held_detail_token = detail_generation

    def _release_held_locked(self):
        """Release the local held token while lifecycle ownership is locked."""
        stats = self._stats()
        if stats is not None and self._held_token is not None:
            stats.release_held(self._held_token)
        self._held_token = None
        self._held_since_ns = None
        self._held_detail_token = 0

    def _release_held(self):
        """Release the held batch exactly once (idempotent across stop/error)."""
        with self._lifecycle_lock:
            self._release_held_locked()

    def release_held_on_revoke(self):
        """Public hook: release a held batch when the worker is revoked/stopped."""
        # Lock order is worker lifecycle -> held token, matching fetch
        # publication and preventing a late fetch from acquiring after revoke.
        with self._lifecycle_lock:
            self._revoked = True
            self._release_held_locked()

    def consume(self):
        if self.curr_log_group_list is None or len(self.curr_log_group_list.log_groups) == 0:
            # Nothing to process; release any held token so it never leaks.
            self._release_held()
            return

        state = self.stats_state
        lat = self._latency()
        generation = self._generation()
        detail_generation = self._detail_generation()
        batch_detail_generation = self._held_detail_token
        groups = getattr(self.curr_log_group_list, "log_groups", [])
        group_count = len(groups)
        log_count = (sum(len(getattr(group, "logs", [])) for group in groups)
                     if generation else 0)
        # dispatch_delay: batch held -> process callback start (latency only).
        if lat is not None and self._held_since_ns is not None and batch_detail_generation:
            lat.observe_ns(
                "dispatch_delay",
                lat._clock.monotonic_ns() - self._held_since_ns,
                detail_token=batch_detail_generation)
        if state is not None:
            state.on_process_start(self._held_token, generation=generation)
        start_ns = lat._clock.monotonic_ns() if lat is not None else None
        ok = False
        try:
            self.log_processor.process(topic_id=self.shard.topic_id, shard_id=self.shard.shard_id,
                                       log_group_list=self.curr_log_group_list)
            ok = True
        finally:
            if lat is not None:
                lat.observe_ns(
                    "process_duration", lat._clock.monotonic_ns() - start_ns,
                    detail_token=detail_generation)
            if state is not None:
                state.on_process_end(
                    success=ok, token=self._held_token, generation=generation,
                    logs=log_count, groups=group_count)
            if not ok and state is not None:
                state.record_error("process", token=generation)
        if ok:
            # A failed callback leaves this same batch in READY_TO_CONSUME
            # for retry, so ownership remains held. Release only after the
            # callback succeeds or an explicit stop/revoke abandons it.
            self._release_held()

        self.checkpoint_manager.add_checkpoint(CheckpointInfo(self.next_checkpoint, self.shard))

    def backoff(self):
        return time.time() - self.last_backoff_time < 5
