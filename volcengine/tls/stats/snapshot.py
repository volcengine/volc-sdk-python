"""Immutable values and fixed-size, local view projection."""
from collections.abc import Mapping
from types import MappingProxyType

from volcengine.tls.stats import constants as _c
from volcengine.tls.stats._immutable import _ImmutableSnapshot
from volcengine.tls.stats.options import StatsOptions


def _freeze(value):
    if isinstance(value, Mapping):
        return SnapshotValue(value)
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value):
    if isinstance(value, SnapshotValue):
        return value.to_dict()
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


class SnapshotValue(_ImmutableSnapshot, Mapping):
    __slots__ = ("_values",)

    def __init__(self, values):
        self._values = MappingProxyType({key: _freeze(value) for key, value in values.items()})

    def __getattr__(self, name):
        try:
            return object.__getattribute__(self, "_values")[name]
        except (KeyError, AttributeError):
            raise AttributeError(name) from None

    def __getitem__(self, key):
        return self._values[key]

    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)

    def to_dict(self):
        return {key: _thaw(value) for key, value in self._values.items()}


class StatsSnapshot(SnapshotValue):
    __slots__ = ()

    @property
    def missing_sections(self):
        return self._values.get("missing_sections", ())

    def __getattr__(self, name):
        if name in _SECTIONS:
            return self._values.get(name)
        return super(StatsSnapshot, self).__getattr__(name)

    def counter_sample(self):
        if self.metrics_disabled or self.operational is None:
            return None
        from volcengine.tls.stats.delta import CounterSample
        d = self.to_dict()
        return CounterSample({key: value for key, value in d.items()
                              if key not in _SECTIONS and key != "missing_sections"},
                             d["operational"]["counters"])

    def __repr__(self):
        return "StatsSnapshot(component={!r}, level={!r}, view={!r}, state={!r})".format(
            self.component_type, self.collected_level, self.requested_view, self.lifecycle_state)


_SECTIONS = ("health", "operational", "managed_memory",
             "worker_details", "retry_details", "latency_histograms", "memory_breakdown")
_DETAIL_SECTIONS = ("worker_details", "retry_details", "latency_histograms", "memory_breakdown")


def _workers(d):
    roles = d.get("worker_roles", [])
    critical = ("mover", "main_loop", "heartbeat", "checkpoint")
    return dict(expected=sum(role["expected"] for role in roles),
                running=sum(role["running"] for role in roles),
                in_flight=sum(role["in_flight"] for role in roles),
                missing_critical_roles=sum(1 for role in roles if role["role"] in critical
                                           and role["running"] < role["expected"]))


def _queue(d):
    if d is None:
        return None
    return {key: d[key] for key in ("current_items", "capacity_items", "high_watermark_items", "bounded")
            if key in d}


def _managed(d):
    memory = d.get("memory")
    if memory is None:
        return None, None
    names = {"limit_bytes": "accounted_limit_bytes", "used_bytes": "accounted_used_bytes",
             "payload_owned_bytes": "payload_bytes", "high_watermark_bytes": "high_watermark_bytes",
             "payload_admission_limit_bytes": "payload_admission_limit_bytes",
             "bounded_runtime_buffer_bytes": "bounded_runtime_buffer_bytes",
             "payload_admission_rejected_total": "payload_admission_rejected_total",
             "runtime_buffer_rejected_total": "runtime_buffer_rejected_total", "rejected_total": "rejected_total"}
    if any(key not in memory for key in names.values()):
        return None, None
    result = {dest: memory[src] for dest, src in names.items()}
    if (result["payload_admission_limit_bytes"] > result["limit_bytes"]
            or result["used_bytes"] != result["payload_owned_bytes"] + result["bounded_runtime_buffer_bytes"]
            or result["used_bytes"] > result["limit_bytes"]
            or result["rejected_total"] != result["payload_admission_rejected_total"] + result["runtime_buffer_rejected_total"]):
        return None, None
    keys = ("ingress_owned_bytes", "aggregate_owned_bytes", "send_owned_bytes", "retry_owned_bytes",
            "bounded_runtime_buffer_bytes")
    breakdown = {key: memory[key] for key in keys} if all(key in memory for key in keys) else None
    if breakdown is not None and sum(breakdown[key] for key in keys[:-1]) != result["payload_owned_bytes"]:
        breakdown = None
    return result, breakdown


def _signals(d, workers, memory):
    result = {"worker_summary": workers, "critical_flags": d.get("critical_flags", [])}
    for name in ("last_success_age_ms", "last_error_age_ms"):
        if d.get(name) is not None:
            result[name] = d[name]
    pressures = [q["current_items"] / q["capacity_items"] for name in
                 ("ingress_queue", "send_queue", "retry_queue", "checkpoint_pending")
                 for q in [d.get(name)] if q and q.get("bounded") and q.get("capacity_items")]
    if pressures:
        result["queue_pressure"] = max(pressures)
    if memory is not None and memory["limit_bytes"]:
        total = memory["used_bytes"] / memory["limit_bytes"]
        result["managed_memory_pressure"] = total
        payload_limit = memory["payload_admission_limit_bytes"]
        payload = memory["payload_owned_bytes"] / payload_limit if payload_limit else None
        result["memory_pressure"] = max(total, payload) if payload is not None else total
        result["memory_pressure_source"] = ("managed_payload_admission"
                                            if payload is not None and payload >= total else "managed_lifecycle")
    return result


_PRODUCER_COUNTERS = {
    "accepted_logs_total": "accepted_logs", "accepted_groups_total": "accepted_groups",
    "terminal_success_logs_total": "terminal_success_logs", "terminal_failure_logs_total": "terminal_failure_logs",
    "terminal_dropped_logs_total": "terminal_dropped_logs", "terminal_success_groups_total": "terminal_success_groups",
    "terminal_failure_groups_total": "terminal_failure_groups", "terminal_dropped_groups_total": "terminal_dropped_groups",
    "send_calls_success_total": "send_calls_success", "send_calls_failure_total": "send_calls_failure",
    "send_call_payload_logs_total": "send_call_payload_logs", "send_call_payload_groups_total": "send_call_payload_groups",
    "retries_scheduled_total": "retries_scheduled", "rejected_invalid_argument_total": "rejected_invalid",
    "rejected_memory_full_total": "rejected_memory", "rejected_managed_admission_total": "rejected_memory",
    "rejected_closed_total": "rejected_closed", "rejected_circuit_open_total": "rejected_circuit",
}


def _operational(d, workers, producer):
    if producer:
        result = {"counters": {dst: d[src] for dst, src in _PRODUCER_COUNTERS.items()}}
        for name in ("aggregate_batches", "aggregate_groups", "send_calls_in_flight", "callbacks_pending",
                     "callbacks_in_flight", "owned_logs", "owned_groups"):
            result[name] = d[name]
        queues = ("ingress_queue", "send_queue", "retry_queue")
    else:
        counters = {}
        for public, calls, failures in (("fetch_calls", "fetch_calls", "fetch_failures"),
                                       ("process_attempts", "process_attempts", "process_failures"),
                                       ("heartbeat_calls", "heartbeat_calls", "heartbeat_failures"),
                                       ("checkpoint_calls", "checkpoint_calls", "checkpoint_failures")):
            # Before a component implementation can provide an outcome it must
            # not fabricate a zero failure count. Missing raw fields omit the pair.
            if calls in d and failures in d:
                counters[public + "_success_total"] = max(0, d[calls] - d[failures])
                counters[public + "_failure_total"] = d[failures]
        for public, raw in (("fetched_logs_total", "fetched_logs"), ("fetched_groups_total", "fetched_log_groups"),
                            ("processed_success_logs_total", "processed_success_logs"),
                            ("processed_success_groups_total", "processed_success_groups"), ("rebalance_total", "rebalance_events")):
            if raw in d:
                counters[public] = d[raw]
        result = {"counters": counters}
        for name in ("assigned_shards", "held_batch_references", "ready_to_process", "fetch_in_flight", "process_in_flight"):
            result[name] = d[name]
        queues = ("checkpoint_pending",)
    result["workers"] = workers
    for name in queues:
        queue = _queue(d.get(name))
        if queue is not None:
            result[name] = queue
    return result


_HISTOGRAMS = {
    "producer": (("batch_queue_delay", "batch_ready", "send_attempt_start", "batch", False),
                 ("send_call_duration", "transport_call_start", "transport_call_end", "call", False),
                 ("batch_delivery_duration", "first_send_attempt_start", "terminal_outcome", "batch", True),
                 ("callback_duration", "callback_start", "callback_end", "callback", False)),
    "consumer": (("fetch_call_duration", "consume_logs_call_start", "consume_logs_call_end", "call", True),
                 ("dispatch_delay", "batch_ready", "callback_start", "batch", False),
                 ("process_duration", "callback_start", "callback_end", "batch", False),
                 ("checkpoint_call_duration", "checkpoint_call_start", "checkpoint_call_end", "call", True)),
}


def _histogram(histogram):
    bounds = histogram["bounds_ms"]
    return {"bucket_profile": "fast" if bounds[0] == 1 else "slow",
            "upper_bounds_ms": bounds,
            "cumulative_bucket_counts": histogram["cumulative_counts"],
            "count": histogram["count"], "sum_ms": histogram["sum_ms"]}


def project_snapshot(raw, options):
    """Project a bounded private measurement snapshot without touching live state."""
    if not isinstance(options, StatsOptions):
        raise TypeError("get_stats requires StatsOptions(view)")
    d = raw.to_dict()
    producer = d["component_type"] == "producer"
    level, view = d["metrics_level"], options.view
    capabilities = 1 | 2 | 4 | 8 | 16 | 128 | ((32 | 64) if producer else 0)
    requested = ["health"]
    if view != "health":
        requested.append("operational")
    if producer:
        requested.append("managed_memory")
    if view == "debug":
        requested.extend(section for section in _DETAIL_SECTIONS if producer or section != "memory_breakdown")
    missing = [section for section in requested if level == "off" or
               (level != "detailed" and section in _DETAIL_SECTIONS)]
    header = {name: d[name] for name in ("instance_id", "sdk_name", "sdk_language", "sdk_version", "component_type",
                                        "captured_at_unix_ms", "uptime_ms", "snapshot_sequence", "collection_generation",
                                        "collection_started_at_unix_ms", "consistency")}
    header.update(schema_version=_c.SCHEMA_VERSION, lifecycle_state=d["state"], collected_level=level,
                  requested_view=view, metrics_disabled=level == "off", capabilities=capabilities)
    if level != "off":
        memory, breakdown = _managed(d) if producer else (None, None)
        if producer:
            if memory is None:
                missing.append("managed_memory")
            else:
                header["managed_memory"] = memory
        workers = _workers(d)
        header["health"] = {"signals": _signals(d, workers, memory)}
        if view != "health":
            header["operational"] = _operational(d, workers, producer)
        if view == "debug" and level == "detailed":
            header["worker_details"] = {"items": d.get("worker_roles", []), "truncated": False}
            header["retry_details"] = ({"retries_scheduled_total": d["retries_scheduled"]} if producer else
                                       {"backoff_events_total": d["backoff_events"]})
            if producer and d.get("retry_queue"):
                header["retry_details"]["queue"] = _queue(d["retry_queue"])
            histograms = {}
            for name, start, end, obj, retry in _HISTOGRAMS[d["component_type"]]:
                histogram = d.get(name + "_ms")
                if histogram is not None:
                    histograms[name] = dict(start=start, end=end, unit="ms", object=obj,
                                            includes_retry=retry, histogram=_histogram(histogram))
            if len(histograms) == 4:
                header["latency_histograms"] = histograms
            else:
                missing.append("latency_histograms")
            if producer:
                if breakdown is None:
                    missing.append("memory_breakdown")
                else:
                    header["memory_breakdown"] = breakdown
    header["partial"] = bool(missing)
    if missing:
        header["missing_sections"] = missing
    return StatsSnapshot(header)
