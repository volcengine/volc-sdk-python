from volcengine.tls.TLSService import TLSService
from volcengine.tls.producer.batch_semaphore import MemoryLimiter
from volcengine.tls.producer.producer_model import (
    BatchLog,
    ProducerConfig,
    Attempt,
    Result,
    FailureClassifier,
    FailureController,
    FailureType,
)
from volcengine.tls.producer.retry_queue import RetryQueue
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import PutLogsRequest
from volcengine.tls.tls_responses import PutLogsResponse
from volcengine.tls.util import get_logger

# 常量定义
HTTP_STATUS_OK = 200


class SendBatchSubmitError(RuntimeError):
    """Executor rejected an already accepted batch that has been settled."""

    stats_owned = True
    current_group_owned = True


class SendBatchTask:
    def __init__(self,
                 batch_log: BatchLog,
                 producer_config: ProducerConfig,
                 memory_lock: MemoryLimiter,
                 client: TLSService,
                 retry_queue: RetryQueue,
                 failure_controller: FailureController = None):
        self.LOG = get_logger(__name__)
        self.producer_config = producer_config
        self.memory_lock = memory_lock
        self.client = client
        self.retry_queue = retry_queue
        self.batch_log = batch_log
        self.failure_controller = failure_controller
        self.stats_state = getattr(producer_config, "stats_state", None)
        self.stats_token = int(getattr(batch_log, "stats_generation", 0) or 0)
        self.detail_token = int(getattr(batch_log, "detail_generation", 0) or 0)
        self._enqueued = False
        self._submitted = False

    def _mark_latency_ready(self):
        marker = getattr(self.batch_log, "mark_latency_ready", None)
        if marker is not None:
            marker(self.stats_state)
        self.detail_token = int(
            getattr(self.batch_log, "detail_generation", 0) or 0)

    def _batch_latency_on(self):
        # Queue/delivery samples belong to both the fixed detailed cohort and
        # the batch admission collection. Transport-call timing is independent
        # and remains current-attempt scoped below.
        return (self._latency_on(self.detail_token) and
                self._stats_on(self.stats_token))

    def _stats_on(self, token=None):
        if self.stats_state is None:
            return False
        try:
            return self.stats_state.enabled and token not in (0, None) and \
                self.stats_state.token() == token
        except Exception:
            return False

    def _latency_on(self, detail_token=None):
        if self.stats_state is None or detail_token in (0, None):
            return False
        try:
            return self.stats_state.latency_enabled and \
                self.stats_state.detail_token() == detail_token
        except Exception:
            return False

    def _mark_enqueued(self):
        if self._enqueued:
            return
        self._enqueued = True
        self._mark_latency_ready()
        if self.stats_state is not None:
            try:
                if self.batch_log.take_stats_ingress_release_once():
                    self.stats_state.on_ingress_release(
                        self.batch_log.group_count(), token=self.stats_token)
                    self.stats_state.on_aggregate_queue_release(
                        groups=self.batch_log.group_count(), token=self.stats_token)
                self.stats_state.on_send_enqueue(token=self.stats_token)
            except Exception:
                pass
        try:
            self.memory_lock.move_payload(
                self.batch_log.reserved_bytes,
                getattr(self.batch_log, "memory_phase", "aggregate"),
                "send", generation=self.stats_token)
            self.batch_log.memory_phase = "send"
        except Exception:
            pass

    def _mark_submitted(self):
        if self._submitted:
            return
        self._submitted = True
        if self.stats_state is not None:
            try:
                self.stats_state.on_sender_task_submitted(token=self.stats_token)
            except Exception:
                pass

    def submit(self, executor_service):
        """Submit after the batch is accepted; settle cleanly on rejection."""
        self._mark_enqueued()
        self._mark_submitted()
        try:
            return executor_service.submit(self.run)
        except Exception as exc:
            if self.stats_state is not None:
                try:
                    self.stats_state.on_sender_task_done(token=self.stats_token)
                except Exception:
                    pass
            if self._stats_on(self.stats_token):
                try:
                    self.stats_state.on_send_dequeue(token=self.stats_token)
                except Exception:
                    pass
            # A synchronous executor may have run the task and surfaced a user
            # callback exception. In that case terminal settlement already
            # happened and must not be repeated.
            if not self.batch_log.terminal_is_settled():
                try:
                    self.handle_local_failure(
                        "ExecutorSubmitFailed",
                        "sender executor rejected an accepted batch",
                        FailureType.LOCAL_RESOURCE,
                    )
                except Exception as settle_exc:
                    self.LOG.error(
                        "settling rejected sender task failed",
                        exc_info=settle_exc)
            raise SendBatchSubmitError(str(exc)) from exc

    def run(self) -> None:
        """线程执行入口，发送请求"""
        owner = getattr(self.producer_config, "_producer_owner", None)
        if owner is not None:
            try:
                owner._work_started()
            except Exception:
                owner = None
        self._mark_enqueued()
        self._mark_submitted()
        if self.stats_state is not None:
            try:
                self.stats_state.on_sender_task_start(token=self.stats_token)
            except Exception:
                pass
        # Sender started: batch leaves the send queue (plan §11.1 'send queue-').
        if self._stats_on(self.stats_token):
            try:
                self.stats_state.on_send_dequeue(token=self.stats_token)
            except Exception:
                pass
        try:
            self.send_request()
        finally:
            if self.stats_state is not None:
                for update in (
                        lambda: self.stats_state.on_sender_task_end(token=self.stats_token),
                        lambda: self.stats_state.on_sender_task_done(token=self.stats_token)):
                    try:
                        update()
                    except Exception:
                        pass
            if owner is not None:
                try:
                    owner._work_finished()
                except Exception:
                    pass

    def send_request(self) -> None:
        """构建并发送日志请求"""
        # A send attempt begins before temporary admission.  This preserves
        # batch delivery timing even when a local memory gate prevents the
        # transport call from starting.
        self._mark_latency_ready()
        attempt_latency_on = self._batch_latency_on()
        if attempt_latency_on:
            attempt_start_ns = self.stats_state._clock.monotonic_ns()
            ready_ns = self.batch_log.take_queue_delay_ready_ns()
            if ready_ns is not None:
                self.stats_state.observe_ns(
                    "batch_queue_delay",
                    attempt_start_ns - ready_ns,
                    detail_token=self.detail_token)
            self.batch_log.mark_first_send_attempt(attempt_start_ns)
        call_token = 0
        call_detail_token = 0
        stats_on = False
        circuit_permit_count = int(self.batch_log.circuit_permit_count)
        if self.failure_controller is not None and circuit_permit_count <= 0:
            circuit_permit_count = self.failure_controller.acquire_permit()
            if circuit_permit_count < 0:
                self.handle_local_failure(
                    "CircuitOpenException",
                    "producer circuit breaker is open",
                    FailureType.CIRCUIT_OPEN,
                    permit_count=0,
                )
                return
            self.batch_log.add_circuit_permit_count(circuit_permit_count)

        temporary_size = self.estimate_temporary_reservation_bytes()
        if not self.memory_lock.acquire_temporary(
                temporary_size, self.producer_config.max_block_ms,
                generation=self.stats_token):
            self.handle_local_failure(
                "MemoryLimitExceeded",
                f"failed to acquire temporary producer memory, requiredSizeInBytes={temporary_size}",
                FailureType.LOCAL_RESOURCE,
            )
            return

        batch_key = self.batch_log.batch_key
        try:
            put_logs_request = PutLogsRequest(
                batch_key.topic_id,
                self.batch_log.log_group_list,
                batch_key.shard_hash,
                log_count=self.batch_log.current_batch_count,
                earliest_log_time=self.batch_log.earliest_log_time,
                latest_log_time=self.batch_log.latest_log_time,
                enable_nanosecond=self.producer_config.enable_nanosecond,
            )

            if not self.calibrate_batch_size():
                return
            # Transport-call observations use the generation active when this
            # attempt starts.  A batch admitted in an older generation may
            # still send in the current generation; count the call there,
            # while terminal settlement remains cohort-gated below.
            call_token = self.stats_state.token() if self.stats_state is not None else 0
            call_detail_token = (self.stats_state.detail_token()
                                 if self.stats_state is not None else 0)
            latency_on = call_detail_token != 0
            stats_on = call_token != 0
            if stats_on:
                self.stats_state.on_send_start(token=call_token)
            _send_start_ns = self.stats_state._clock.monotonic_ns() if latency_on else None
            try:
                put_logs_response = self.client.put_logs(put_logs_request)
            finally:
                # The call duration uses the independent current detail cohort.
                if latency_on:
                    _dur_ns = self.stats_state._clock.monotonic_ns() - _send_start_ns
                    self.stats_state.observe_ns(
                        "send_call_duration", _dur_ns,
                        detail_token=call_detail_token)
        except TLSException as e:
            if stats_on:
                self.stats_state.on_send_end(
                    success=False,
                    payload_logs=int(self.batch_log.current_batch_count),
                    payload_groups=self.batch_log.group_count(),
                    error_category=FailureClassifier.classify_exception(e).value,
                    token=call_token,
                )
            self.handle_log_exception(e)
            return
        except Exception as e:
            if stats_on:
                self.stats_state.on_send_end(
                    success=False,
                    payload_logs=int(self.batch_log.current_batch_count),
                    payload_groups=self.batch_log.group_count(),
                    error_category=FailureType.NETWORK.value,
                    token=call_token,
                )
            self.handle_exception(e)
            return
        finally:
            self.memory_lock.release_temporary(
                temporary_size, generation=self.stats_token)

        if stats_on:
            self.stats_state.on_send_end(
                success=True,
                payload_logs=int(self.batch_log.current_batch_count),
                payload_groups=self.batch_log.group_count(),
                token=call_token,
            )
        self.handle_success(put_logs_response)

    def estimate_temporary_reservation_bytes(self) -> int:
        return int(self.batch_log.current_batch_size) * 2 + ProducerConfig.TEMPORARY_RESERVATION_OVERHEAD_BYTES

    def calibrate_batch_size(self) -> bool:
        estimated = int(self.batch_log.current_batch_size)
        actual = int(self.batch_log.log_group_list.ByteSize())
        delta = actual - estimated
        if delta > 0:
            if not self.memory_lock.acquire_payload(
                    delta, self.producer_config.max_block_ms,
                    generation=self.stats_token,
                    phase=getattr(self.batch_log, "memory_phase", "send")):
                self.handle_local_failure(
                    "MemoryLimitExceeded",
                    "buffer full when calibrating batch size",
                    FailureType.LOCAL_RESOURCE,
                )
                return False
            self.batch_log.reserved_bytes += delta
        elif delta < 0:
            self.memory_lock.release_payload(
                -delta, generation=self.stats_token,
                phase=getattr(self.batch_log, "memory_phase", "send"))
            self.batch_log.reserved_bytes += delta
        self.batch_log.current_batch_size = actual
        return True

    def handle_failure(self) -> None:
        """处理失败日志"""
        self.LOG.info(f"send batch failed, batch: {self.batch_log}")
        try:
            self._settle_terminal_and_fire("failure")
        finally:
            self._release_payload_once()

    def _release_payload_once(self) -> None:
        reserved_bytes = getattr(self.batch_log, "reserved_bytes", self.batch_log.current_batch_size)
        if reserved_bytes <= 0:
            return
        self.memory_lock.release_payload(
            reserved_bytes, generation=self.stats_token,
            phase=getattr(self.batch_log, "memory_phase", None))
        self.batch_log.reserved_bytes = 0
        self.batch_log.memory_phase = "released"

    def _move_payload_to_retry(self):
        try:
            self.memory_lock.move_payload(
                self.batch_log.reserved_bytes,
                getattr(self.batch_log, "memory_phase", "send"),
                "retry", generation=self.stats_token)
            self.batch_log.memory_phase = "retry"
        except Exception:
            pass

    def _settle_terminal_and_fire(self, outcome: str) -> None:
        """Record a once-only terminal for the batch, then fire callbacks with
        callback stats. Stats never alter delivery behavior or raise.

        Business counters and batch delivery latency are gated by the batch's
        admission cohorts; transport and callback observations use the current
        attempt cohorts."""
        # The same once gate protects terminal counters and callbacks. Retry
        # attempts do not enter this method until a real terminal outcome.
        if not self.batch_log.take_terminal_once():
            return
        stats = self.stats_state
        metrics_on = self._stats_on(self.stats_token)
        latency_on = self._batch_latency_on()
        if stats is not None and (metrics_on or latency_on):
            if metrics_on:
                logs = int(self.batch_log.current_batch_count)
                groups = self.batch_log.group_count()
                stats.on_terminal(outcome, logs, groups, token=self.stats_token)
            # batch_delivery: first send attempt -> terminal outcome.
            if latency_on:
                create_ns = getattr(self.batch_log, "first_send_attempt_mono_ns", None)
                if create_ns is not None:
                    stats.observe_ns(
                        "batch_delivery_duration",
                        stats._clock.monotonic_ns() - create_ns,
                        detail_token=self.detail_token)
        self._fire_callbacks_with_stats(stats, metrics_on)

    def _fire_callbacks_with_stats(self, stats, metrics_on=False) -> None:
        if stats is None:
            self.batch_log.fire_callbacks()
            return
        callbacks = getattr(self.batch_log, "call_back_list", None) or []
        n = len(callbacks)
        if n == 0:
            self.batch_log.fire_callbacks()
            return
        attempts = getattr(self.batch_log, "reserved_attempts", None) or []
        if not attempts:
            self.batch_log.fire_callbacks()
            return
        result = Result(attempts[-1].success, attempts, self.batch_log.attempt_count)
        for index, callback in enumerate(callbacks):
            if metrics_on:
                stats.on_callback_start(token=self.stats_token)
            callback_detail_token = stats.detail_token()
            callback_latency_on = callback_detail_token != 0
            start_ns = stats._clock.monotonic_ns() if callback_latency_on else None
            success = False
            try:
                callback.on_complete(result)
                success = True
            except Exception:
                if stats is not None:
                    stats.record_error("callback", token=self.stats_token)
                if metrics_on and index + 1 < n:
                    stats.on_callback_cancelled(
                        n - index - 1, token=self.stats_token)
                raise
            finally:
                if callback_latency_on:
                    stats.observe_ns(
                        "callback_duration",
                        stats._clock.monotonic_ns() - start_ns,
                        detail_token=callback_detail_token)
                if metrics_on:
                    stats.on_callback_end(
                        success=success, token=self.stats_token)

    def need_retry(self, failure_type: FailureType) -> bool:
        """判断是否需要重试"""
        return (FailureClassifier.should_retry(failure_type) and
                self.batch_log.attempt_count <= self.producer_config.retry_count and
                not self.retry_queue.closed)

    def handle_log_exception(self, e: TLSException) -> None:
        """处理日志异常"""
        self.LOG.error(f"send batch failed, batch:{self.batch_log}", exc_info=e)
        failure_type = FailureClassifier.classify_exception(e)
        if self.stats_state is not None:
            self.stats_state.record_error(
                failure_type.value, token=self.stats_token)
        if self.failure_controller is not None:
            self.failure_controller.after_send(e, success=False,
                                               permit_count=self.batch_log.take_circuit_permit_count())

        # 创建失败尝试记录
        fail_attempt = Attempt(
            success=False,
            request_id=e.request_id,
            error_code=e.error_code,
            error_message=e.error_message,
            http_code=e.http_code
        )
        self.batch_log.add_attempt(fail_attempt)
        self.batch_log.handle_next_try()

        # 检查是否需要重试
        if self.need_retry(failure_type):
            try:
                added = self.retry_queue.add_to_retry_queue(self.batch_log)
                if added is not False:
                    if self._stats_on(self.stats_token):
                        self.stats_state.on_retry_scheduled(token=self.stats_token)
                    self._move_payload_to_retry()
                    self.LOG.info(f"retry queue add batch success, batch: {self.batch_log}")
                    return
            except TLSException as ex:
                self.LOG.warn("retry manager is closed and put batch log to failure queue", exc_info=ex)

        # 不需要重试或重试失败，处理失败日志
        self.handle_failure()

    def handle_exception(self, e: Exception) -> None:
        """处理通用异常"""
        self.LOG.error(f"send batch failed, batch:{self.batch_log}", exc_info=e)
        if self.stats_state is not None:
            self.stats_state.record_error(
                FailureType.NETWORK.value, token=self.stats_token)
        if self.failure_controller is not None:
            self.failure_controller.after_send(FailureType.NETWORK, success=False,
                                               permit_count=self.batch_log.take_circuit_permit_count())

        # 创建失败尝试记录
        fail_attempt = Attempt(
            success=False,
            error_code=e.__class__.__name__,
            error_message=str(e)
        )
        self.batch_log.add_attempt(fail_attempt)
        self.batch_log.handle_next_try()
        if self.need_retry(FailureType.NETWORK):
            try:
                added = self.retry_queue.add_to_retry_queue(self.batch_log)
                if added is not False:
                    if self._stats_on(self.stats_token):
                        self.stats_state.on_retry_scheduled(token=self.stats_token)
                    self._move_payload_to_retry()
                    self.LOG.info(f"retry queue add batch success, batch: {self.batch_log}")
                    return
            except TLSException as ex:
                self.LOG.warn("retry manager is closed and put batch log to failure queue", exc_info=ex)
        self.handle_failure()

    def handle_local_failure(self, error_code: str, error_message: str, failure_type: FailureType,
                             permit_count: int = None) -> None:
        if self.stats_state is not None:
            self.stats_state.record_error(
                failure_type.value, token=self.stats_token)
        fail_attempt = Attempt(
            success=False,
            error_code=error_code,
            error_message=error_message,
        )
        self.batch_log.add_attempt(fail_attempt)
        if self.failure_controller is not None:
            if permit_count is None:
                permit_count = self.batch_log.take_circuit_permit_count()
            self.failure_controller.after_send(failure_type, success=False, permit_count=permit_count)
        self.handle_failure()

    def handle_success(self, put_logs_response: PutLogsResponse) -> None:
        """处理成功响应"""
        if self.failure_controller is not None:
            self.failure_controller.after_send(success=True,
                                               permit_count=self.batch_log.take_circuit_permit_count())
        success_attempt = Attempt(
            success=True,
            request_id=put_logs_response.request_id,
            http_code=HTTP_STATUS_OK
        )
        self.batch_log.add_attempt(success_attempt)
        self.batch_log.retry_backoff_ms = 0
        try:
            self._settle_terminal_and_fire("success")
        finally:
            self._release_payload_once()
        self.LOG.debug(f"send batch success, batch: {self.batch_log}")
