# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import threading
import time
import uuid
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
from volcengine.tls._stats.consumer_state import ConsumerStatsState


class LogProcessor:
    @abc.abstractmethod
    def process(self, topic_id: str, shard_id: int, log_group_list: LogGroupList):
        raise NotImplementedError("Please implement the process method.")


class TLSConsumer:
    """Consumer lifecycle owner and public health projection boundary."""

    def __init__(self, consumer_config: ConsumerConfig, tls_service: TLSService,
                 log_processor: LogProcessor):
        consumer_config.validate()
        self.logger = get_logger("tls-python-sdk-consumer-logger")

        self.consumer_config = consumer_config
        self.tls_service = tls_service
        self.log_processor = log_processor

        from volcengine import VERSION as _sdk_version
        self.stats_state = ConsumerStatsState(
            metrics_level=consumer_config.metrics_level,
            instance_id="consumer-{}".format(uuid.uuid4().hex),
            sdk_version=_sdk_version,
        )

        self.worker_map = {}
        self.working_flag = False
        self.heartbeat_runner = HeartbeatRunner(self)
        self.checkpoint_manager = CheckpointManager(self)

        self.run_thread = None
        self.heartbeat_thread = None
        self.checkpoint_thread = None

        self._stop_lock = threading.Lock()
        self._lifecycle_lock = threading.RLock()
        self._start_in_progress = False
        self._stop_requested = False
        self._start_done = threading.Event()
        self._start_done.set()
        self._worker_threads = set()
        self._resident_threads = set()
        self._finalizer_thread = None

        self.logger.info("TLS consumer {} is initialized.".format(
            self.consumer_config.consumer_name))

    # ---- public stats ---------------------------------------------------
    def set_metrics_level(self, level):
        """Change collection while this consumer is running."""
        self.stats_state.set_metrics_level(level)

    def get_stats(self, options):
        """Return the bounded public projection for explicit StatsOptions."""
        from volcengine.tls.stats.snapshot import project_snapshot
        raw = self.stats_state.get_stats()
        return project_snapshot(raw, options)

    # ---- thread registry ------------------------------------------------
    def _register_worker_thread(self, thread):
        if thread is None:
            return
        with self._lifecycle_lock:
            self._worker_threads.add(thread)

    def _unregister_worker_thread(self, thread):
        if thread is None:
            return
        with self._lifecycle_lock:
            self._worker_threads.discard(thread)

    def _register_resident_thread(self, thread):
        with self._lifecycle_lock:
            self._resident_threads.add(thread)

    def _unregister_resident_thread(self, thread):
        with self._lifecycle_lock:
            self._resident_threads.discard(thread)

    @staticmethod
    def _thread_alive(thread):
        if thread is None:
            return False
        try:
            return bool(thread.is_alive())
        except (AttributeError, RuntimeError):
            return False

    def _background_threads(self):
        with self._lifecycle_lock:
            refs = set(self._worker_threads) | set(self._resident_threads)
            # Tests and integrations may replace a role thread directly; the
            # public references remain a safe bounded fallback for shutdown.
            refs.update(thread for thread in (
                self.run_thread, self.heartbeat_thread, self.checkpoint_thread)
                        if thread is not None)
        return tuple(thread for thread in refs if thread is not threading.current_thread())

    def _all_background_stopped(self):
        return not any(self._thread_alive(thread) for thread in self._background_threads())

    def _business_workers_active(self):
        """Fallback for worker adapters whose native thread is not registered."""
        for worker in list(self.worker_map.values()):
            try:
                if worker.thread_running_status:
                    return True
            except (AttributeError, RuntimeError):
                continue
        return False

    # ---- lifecycle ------------------------------------------------------
    def start(self):
        with self._lifecycle_lock:
            if self.stats_state._current_state() == "closing":
                raise RuntimeError("consumer stop is still settling")
            if self._start_in_progress:
                raise RuntimeError("consumer start is already in progress")
            prior_state = self.stats_state._current_state()
            if (self._thread_alive(self._finalizer_thread)
                    or any(self._thread_alive(thread)
                           for thread in self._background_threads())
                    or self._business_workers_active()):
                raise RuntimeError("consumer has live worker threads")

            # A closed generation, or a failed generation that already created
            # role threads, must not reuse managers carrying old stop/revoke
            # state.  Failed init can retry the existing managers because no
            # role thread started.
            role_generation_started = any(thread is not None for thread in (
                self.run_thread, self.heartbeat_thread, self.checkpoint_thread))
            closed_generation = bool(getattr(self.stats_state, "_closed", False))
            refresh_managers = (
                prior_state == "closed"
                or closed_generation
                or (prior_state == "failed" and role_generation_started))
            if refresh_managers:
                self._clear_finished_workers()
                self.heartbeat_runner = HeartbeatRunner(self)
                self.checkpoint_manager = CheckpointManager(self)
                self.worker_map = {}
            self.stats_state.resume_for_start()

            self._start_in_progress = True
            self._stop_requested = False
            self._start_done.clear()
            self.working_flag = True
            self.heartbeat_runner.working_flag = True
            heartbeat_stop = getattr(self.heartbeat_runner, "_stop_event", None)
            if heartbeat_stop is not None:
                heartbeat_stop.clear()
            self.checkpoint_manager.working_flag = True
            self.checkpoint_manager.force_stop = False
            clear_stop = getattr(self.checkpoint_manager, "_stop_event", None)
            if clear_stop is not None:
                clear_stop.clear()

        try:
            self.init()
        except Exception:
            with self._lifecycle_lock:
                stop_won = self._stop_requested
                self._start_in_progress = False
                self._start_done.set()
                self.working_flag = False
                self.heartbeat_runner.working_flag = False
                self.checkpoint_manager.working_flag = False
                if not stop_won:
                    self.stats_state.mark_failed("lifecycle")
            if stop_won:
                return
            raise

        with self._lifecycle_lock:
            # stop() may have won while init was in flight.  Do not publish a
            # running state or create any role thread for that generation.
            if self._stop_requested:
                self.working_flag = False
                self.heartbeat_runner.working_flag = False
                self.checkpoint_manager.working_flag = False
                self._start_in_progress = False
                self._start_done.set()
                return

            self.stats_state.mark_started()
            prefix = self.consumer_config.consumer_name
            self.heartbeat_thread = threading.Thread(
                target=self._role_wrapper(
                    self.heartbeat_runner.run,
                    self.stats_state.set_heartbeat_running),
                name=prefix + "-HeartbeatRunner")
            self.checkpoint_thread = threading.Thread(
                target=self._role_wrapper(
                    self.checkpoint_manager.run,
                    self.stats_state.set_checkpoint_running),
                name=prefix + "-CheckpointManager")
            self.run_thread = threading.Thread(
                target=self._role_wrapper(
                    self.run, self.stats_state.set_main_running),
                name=prefix)
            role_threads = (
                self.heartbeat_thread, self.checkpoint_thread, self.run_thread)
            for thread in role_threads:
                self._register_resident_thread(thread)

            started = []
            try:
                for thread in role_threads:
                    thread.start()
                    started.append(thread)
            except Exception:
                self.working_flag = False
                self.heartbeat_runner.working_flag = False
                self.checkpoint_manager.working_flag = False
                self.checkpoint_manager.force_stop = True
                self.stats_state.mark_failed("lifecycle")
                deadline = time.monotonic() + self.consumer_config.stop_timeout
                for thread in started:
                    self._join_until(thread, deadline)
                    self._unregister_resident_thread(thread)
                for thread in role_threads:
                    if thread not in started:
                        self._unregister_resident_thread(thread)
                self._start_in_progress = False
                self._start_done.set()
                raise
            self._start_in_progress = False
            self._start_done.set()

    def _role_wrapper(self, target, set_running):
        def _runner():
            try:
                set_running(1)
            except Exception:
                pass
            try:
                target()
            except BaseException:
                try:
                    self._handle_role_failure()
                except BaseException:
                    # Preserve the role target's exception as the thread's
                    # observable failure even if bookkeeping is patched or
                    # otherwise unavailable.
                    pass
                raise
            finally:
                try:
                    set_running(0)
                except Exception:
                    pass
                self._unregister_resident_thread(threading.current_thread())
        return _runner

    def _handle_role_failure(self):
        """Stop sibling roles after an unexpected role-target exception.

        This path only publishes stop signals.  Joining from a role callback
        could synchronously join the callback's own thread and deadlock; the
        public stop path remains responsible for final joining/freezing.
        """
        # ``start`` holds ``_lifecycle_lock`` while starting role threads and
        # joins already-started threads if a later ``Thread.start`` fails.
        # Do not acquire that lock here: a failing role must never wait for a
        # start path that may be waiting for this role to exit.
        self._stop_requested = True
        self.working_flag = False
        self.heartbeat_runner.working_flag = False
        heartbeat_stop = getattr(self.heartbeat_runner, "_stop_event", None)
        if heartbeat_stop is not None:
            heartbeat_stop.set()
        self.checkpoint_manager.working_flag = False
        self.checkpoint_manager.force_stop = True
        checkpoint_stop = getattr(self.checkpoint_manager, "_stop_event", None)
        if checkpoint_stop is not None:
            checkpoint_stop.set()
        self.stats_state.mark_failed("lifecycle")

    def stop(self):
        # A second stop request must never block a callback that is finishing
        # under the first stop.  It only publishes the stop intent; the owner
        # of the first request completes the join/finalization.
        if not self._stop_lock.acquire(False):
            with self._lifecycle_lock:
                self._stop_requested = True
                self.stats_state.mark_closing()
                self.working_flag = False
                self.heartbeat_runner.working_flag = False
                heartbeat_stop = getattr(self.heartbeat_runner, "_stop_event", None)
                if heartbeat_stop is not None:
                    heartbeat_stop.set()
            return
        try:
            deadline = time.monotonic() + self.consumer_config.stop_timeout
            with self._lifecycle_lock:
                self._stop_requested = True
                self.stats_state.mark_closing()
                self.working_flag = False
                self.heartbeat_runner.working_flag = False
                heartbeat_stop = getattr(self.heartbeat_runner, "_stop_event", None)
                if heartbeat_stop is not None:
                    heartbeat_stop.set()
                wait_for_start = self._start_in_progress
                start_done = self._start_done

            if wait_for_start:
                remaining = max(0, deadline - time.monotonic())
                if not start_done.wait(remaining):
                    # ``init`` still owns this generation.  It has not yet
                    # created role threads, so freezing here would publish a
                    # final snapshot while initialization can still mutate
                    # lifecycle state.  The finalizer waits for start_done
                    # and freezes only after init observes the stop request.
                    self._start_finalizer()
                    return

            self._finish_stop(deadline)
        finally:
            self._stop_lock.release()

    def _finish_stop(self, deadline):
        # The main loop must stop before new shard tasks are admitted.
        timed_out = self._join_until(self.run_thread, deadline)
        # Registry membership survives rebalance/removal from worker_map.
        while True:
            live = [thread for thread in self._background_threads()
                    if thread is not self.checkpoint_thread
                    and self._thread_alive(thread)]
            if not live and not self._business_workers_active():
                break
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                timed_out = True
                break
            time.sleep(min(remaining, 0.02))

        if not timed_out:
            # A finishing shard may have published its final checkpoint. Only
            # after all shard/main/heartbeat work settles do we stop draining.
            self.checkpoint_manager.working_flag = False
            stop_event = getattr(self.checkpoint_manager, "_stop_event", None)
            if stop_event is not None:
                stop_event.set()
            if self._join_until(self.checkpoint_thread, deadline):
                timed_out = True

        if timed_out or not self._all_background_stopped():
            # Keep the state Closing/weak.  A daemon finalizer publishes the
            # immutable final snapshot only after every registered task exits.
            # Stop a best-effort checkpoint drain after the deadline.  This
            # does not interrupt a transport call already in progress.
            self.checkpoint_manager.force_stop = True
            self._start_finalizer()
            return

        self._clear_finished_workers()
        self.stats_state.freeze()
        self.logger.info("TLS consumer {} is stopped.".format(
            self.consumer_config.consumer_name))

    def _clear_finished_workers(self):
        for worker in list(self.worker_map.values()):
            release = getattr(worker, "release_held_on_revoke", None)
            if release is not None:
                try:
                    release()
                except Exception:
                    pass
        with self._lifecycle_lock:
            self.worker_map.clear()
            self._worker_threads = set(
                thread for thread in self._worker_threads
                if self._thread_alive(thread))
        # Releasing the last worker is the assignment boundary for the
        # lifecycle generation.  Publish the matching zero gauge so a final
        # snapshot cannot retain the last heartbeat assignment after the
        # worker registry has been drained.
        stats = self.stats_state
        if stats is not None:
            stats.set_assigned_shards(0, token=stats.token())

    def _start_finalizer(self):
        with self._lifecycle_lock:
            if self._finalizer_thread is not None and self._thread_alive(self._finalizer_thread):
                return
            thread = threading.Thread(target=self._finalize_after_timeout,
                                      name=self.consumer_config.consumer_name + "-Finalizer")
            thread.daemon = True
            self._finalizer_thread = thread
            thread.start()

    def _finalize_after_timeout(self):
        while True:
            with self._lifecycle_lock:
                if self._start_in_progress:
                    ready = False
                else:
                    ready = not any(
                        self._thread_alive(thread)
                        for thread in self._background_threads()
                        if thread is not threading.current_thread()
                        and thread is not self.checkpoint_thread) \
                        and not self._business_workers_active()
            if ready:
                break
            time.sleep(0.02)

        self.checkpoint_manager.force_stop = True
        self.checkpoint_manager.working_flag = False
        stop_event = getattr(self.checkpoint_manager, "_stop_event", None)
        if stop_event is not None:
            stop_event.set()
        # A checkpoint transport call is allowed to finish naturally; this
        # loop is intentionally not time limited.
        while self._thread_alive(self.checkpoint_thread):
            time.sleep(0.02)
        self._clear_finished_workers()
        self.stats_state.freeze()
        self.logger.info("TLS consumer {} is stopped.".format(
            self.consumer_config.consumer_name))

    @staticmethod
    def _join_until(thread, deadline):
        if thread is None or thread is threading.current_thread():
            return False
        try:
            if not thread.is_alive():
                return False
        except (AttributeError, RuntimeError):
            return False
        remaining = max(0, deadline - time.monotonic())
        try:
            thread.join(timeout=remaining)
        except RuntimeError:
            return False
        try:
            return bool(thread.is_alive())
        except (AttributeError, RuntimeError):
            return False

    def reset_access_key_token(self, access_key_id: str, access_key_secret: str,
                               security_token: str = None):
        self.tls_service.reset_access_key_token(
            access_key_id, access_key_secret, security_token)

    # ---- original consumer behavior ------------------------------------
    def init(self):
        req = DescribeConsumerGroupsRequest(
            project_id=self.consumer_config.project_id,
            consumer_group_name=self.consumer_config.consumer_group_name)
        res = self.tls_service.describe_consumer_groups(req)
        for consumer_group in res.consumer_groups:
            if consumer_group.consumer_group_name == self.consumer_config.consumer_group_name:
                return

        req = CreateConsumerGroupRequest(
            project_id=self.consumer_config.project_id,
            consumer_group_name=self.consumer_config.consumer_group_name,
            topic_id_list=self.consumer_config.topic_id_list,
            heartbeat_ttl=3 * self.consumer_config.heartbeat_interval_in_second,
            ordered_consume=self.consumer_config.ordered_consume)
        try:
            self.tls_service.create_consumer_group(req)
        except TLSException as error:
            if ERROR_CONSUMER_GROUP_ALREADY_EXISTS not in error.error_code:
                self.logger.error(error.__str__())
                raise

    def run(self):
        self.logger.info("Consumer {} starts to work.".format(
            self.consumer_config.consumer_name))
        while self.working_flag:
            time.sleep(self.consumer_config.data_fetch_interval_in_millisecond / 1000)
            if not self.working_flag:
                break

            for worker in list(self.worker_map.values()):
                if worker.load_status() == ConsumerStatus.WAIT_FOR_RESTART:
                    try:
                        self.heartbeat_runner.upload_heartbeat()
                        self.checkpoint_manager.upload_checkpoint()
                        break
                    except Exception as error:
                        self.logger.error(error)

            shards = self.heartbeat_runner.get_shards()
            self.handle_shards(shards)

    def handle_shards(self, shards: List[ConsumeShard]):
        if shards is None:
            return

        previous_shards = set(self.worker_map.keys())
        shard_map = {
            shard.topic_id + str(shard.shard_id): shard for shard in shards}

        for shard_name in list(self.worker_map.keys()):
            if shard_name not in shard_map:
                worker = self.worker_map[shard_name]
                release = getattr(worker, "release_held_on_revoke", None)
                if release is not None:
                    try:
                        release()
                    except Exception:
                        pass
                del self.worker_map[shard_name]

        for key, shard in shard_map.items():
            existing = self.worker_map.get(key)
            if (existing is not None
                    and existing.load_status() == ConsumerStatus.WAIT_FOR_RESTART):
                release = getattr(existing, "release_held_on_revoke", None)
                if release is not None:
                    try:
                        release()
                    except Exception:
                        pass
                self.worker_map[key] = LogConsumer(self, shard)
            elif existing is None:
                self.worker_map[key] = LogConsumer(self, shard)

        stats = self.stats_state
        generation = stats.token() if stats is not None else 0
        if stats is not None:
            stats.set_assigned_shards(len(shard_map), token=generation)
            if previous_shards != set(shard_map.keys()):
                stats.on_rebalance(token=generation)

        for worker in list(self.worker_map.values()):
            worker.run()
