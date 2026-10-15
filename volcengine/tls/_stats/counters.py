# coding=utf-8
"""Ordered internal counter schemas for producer and consumer state."""
from __future__ import absolute_import

__all__ = ["PRODUCER_COUNTER_KEYS", "CONSUMER_COUNTER_KEYS"]


PRODUCER_COUNTER_KEYS = (
    "accepted_logs", "accepted_groups",
    "terminal_success_logs", "terminal_failure_logs", "terminal_dropped_logs",
    "terminal_success_groups", "terminal_failure_groups", "terminal_dropped_groups",
    "owned_logs", "owned_groups",
    "rejected_invalid", "rejected_memory", "rejected_closed",
    "rejected_circuit", "rejected_internal",
    "aggregate_batches", "aggregate_groups",
    "send_calls_in_flight", "send_calls_in_flight_max",
    "send_calls_success", "send_calls_failure",
    "send_call_payload_logs", "send_call_payload_groups",
    "terminal_success_batches", "terminal_failure_batches", "terminal_dropped_batches",
    "retries_scheduled",
    "callbacks_pending", "callbacks_in_flight",
    "callbacks_success", "callbacks_failure",
    "dropped_force_close_logs", "dropped_memory_evict_logs",
    "dropped_ttl_expired_logs", "dropped_internal_logs",
    "dropped_force_close_groups", "dropped_memory_evict_groups",
    "dropped_ttl_expired_groups", "dropped_internal_groups",
)


CONSUMER_COUNTER_KEYS = (
    "assigned_shards",
    "held_batch_references", "ready_to_process",
    "fetch_in_flight", "process_in_flight",
    "checkpoint_flush_in_flight",
    "fetch_calls", "fetch_failures", "fetched_log_groups", "fetched_logs",
    "process_attempts", "process_failures",
    "processed_success_logs", "processed_success_groups",
    "heartbeat_calls", "heartbeat_failures",
    "checkpoint_calls", "checkpoint_failures",
    "backoff_events", "rebalance_events",
    "shard_tasks_submitted", "shard_tasks_started", "shard_tasks_completed",
    "shard_tasks_in_flight", "shard_tasks_in_flight_max", "shard_task_errors",
)
