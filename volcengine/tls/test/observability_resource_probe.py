# coding=utf-8
"""Bounded offline resource probe; emits one JSON result, never contacts TLS.

Run from the repository root:
  python -m volcengine.tls.test.observability_resource_probe producer core --seconds 30
  python -m volcengine.tls.test.observability_resource_probe consumer detailed --seconds 30 --monitor-seconds 15

Each invocation uses a fresh process. Compare the same component, duration and
load across levels. RSS includes the whole interpreter, dependencies and fake
service; it is not the SDK managed-memory budget.
"""
import argparse
import gc
import json
import logging
import os
import resource
import socket
import sys
import threading
import time
from types import SimpleNamespace
from uuid import uuid4

from volcengine.tls.consumer.consumer import TLSConsumer
from volcengine.tls.consumer.consumer_model import ConsumerConfig
from volcengine.tls.data import ConsumeShard
from volcengine.tls.log_pb2 import LogGroupList
from volcengine.tls.producer.producer import TLSProducer
from volcengine.tls.producer.producer_model import ProducerConfig
from volcengine.tls.stats import StatsOptions
from volcengine.tls.tls_requests import PutLogsV2LogContent


def _deny_network(*_args, **_kwargs):
    raise AssertionError("the resource probe must stay offline")


def _rss():
    if sys.platform.startswith("linux"):
        with open("/proc/self/statm", "r") as stream:
            return int(stream.read().split()[1]) * os.sysconf("SC_PAGE_SIZE")
    # macOS reports ru_maxrss in bytes. This fallback is a peak, not live RSS.
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def _offline_credentials():
    """Generate non-secret values for the offline producer fixture."""
    return "offline-" + uuid4().hex, "offline-" + uuid4().hex


class _Service:
    def __init__(self):
        self.lock = threading.Lock()
        self.sent = 0
        self.fetched = 0
        self.processed = 0
        self.callbacks = 0
        self.groups = LogGroupList()
        # Protobuf repeated fields are generated dynamically; pylint cannot infer them.
        group = self.groups.log_groups.add()  # pylint: disable=no-member
        for _ in range(10):
            log = group.logs.add()
            log.time = 1
            entry = log.contents.add()
            entry.key = "key"
            entry.value = "v" * 128

    def set_retry_policy(self, _policy):
        pass

    def put_logs(self, _request):
        time.sleep(0.001)
        with self.lock:
            self.sent += 1
        return SimpleNamespace(request_id="offline-probe")

    def on_complete(self, _result):
        with self.lock:
            self.callbacks += 1

    def describe_consumer_groups(self, _request):
        return SimpleNamespace(consumer_groups=[SimpleNamespace(consumer_group_name="probe")])

    def consumer_heartbeat(self, _request):
        return SimpleNamespace(shards=[ConsumeShard("probe-topic", 0)])

    def describe_checkpoint(self, _request):
        return SimpleNamespace(checkpoint="")

    def describe_cursor(self, _request):
        return SimpleNamespace(cursor="cursor")

    def consume_logs(self, _request):
        time.sleep(0.001)
        with self.lock:
            self.fetched += 1
        return SimpleNamespace(get_pb_message=lambda: self.groups,
                               get_x_tls_cursor=lambda: "cursor")

    def process(self, topic_id, shard_id, log_group_list):
        with self.lock:
            self.processed += 1

    def modify_checkpoint(self, _request):
        pass


def _make(component, level, service):
    if component == "producer":
        access_key, access_secret = _offline_credentials()
        # The generated values are never sent; the probe replaces the client with _Service.
        config = ProducerConfig("https://offline.invalid", "region", access_key, access_secret,
                                metrics_level=level)
        config.max_batch_count = 10
        config.total_size_in_bytes = 1024 * 1024
        config.max_producer_memory_bytes = 2 * 1024 * 1024
        config.max_batch_size_bytes = 64 * 1024
        config.max_block_ms = 100
        config.max_thread_count = 2
        config.valid_config()
        instance = TLSProducer(config)
        instance.dispatcher.client = service
        instance.mover.client = service
        return instance
    config = ConsumerConfig("probe-project", "probe", ["probe-topic"], "probe-consumer",
                            heartbeat_interval_in_second=1,
                            data_fetch_interval_in_millisecond=2,
                            flush_checkpoint_interval_in_second=1,
                            stop_timeout=5, metrics_level=level)
    return TLSConsumer(config, service, service)


def run(args):
    socket.socket.connect = _deny_network
    socket.create_connection = _deny_network
    logging.disable(logging.CRITICAL)
    baseline_threads = set(threading.enumerate())
    service = _Service()
    instance = _make(args.component, args.level, service)
    instance.start()
    options = StatsOptions("debug" if args.level == "detailed" else "operational")
    logs = [PutLogsV2LogContent(time=1, log_dict={"key": "v" * 128}) for _ in range(10)]
    rss = [_rss()]
    peak_threads = len(threading.enumerate())
    samples = 0
    submitted = 0
    begin = time.monotonic()
    cpu_begin = time.process_time()
    next_send = begin
    next_monitor = begin + args.monitor_seconds if args.monitor_seconds else float("inf")
    next_resource = begin + 1
    while time.monotonic() - begin < args.seconds:
        now = time.monotonic()
        if args.component == "producer" and now >= next_send:
            instance.send_logs_v2(None, "probe-topic", None, None, logs, service)
            submitted += 1
            next_send += 1.0 / args.requests_per_second
        if now >= next_monitor:
            json.dumps(instance.get_stats(options).to_dict())
            samples += 1
            next_monitor += args.monitor_seconds
        if now >= next_resource:
            rss.append(_rss())
            peak_threads = max(peak_threads, len(threading.enumerate()))
            next_resource += 1
        time.sleep(0.0005 if args.component == "producer" else 0.002)
    wall_seconds = time.monotonic() - begin
    cpu_seconds = time.process_time() - cpu_begin

    # Separate snapshot latency from the timed workload CPU measurement.
    latencies = []
    for _ in range(300):
        start_ns = time.perf_counter_ns()
        instance.get_stats(options)
        latencies.append((time.perf_counter_ns() - start_ns) / 1000.0)
    latencies.sort()
    instance.close(timeout_ms=10000) if args.component == "producer" else instance.stop()
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        final = instance.get_stats(options)
        if final.consistency == "final":
            break
        time.sleep(0.01)
    assert final.consistency == "final", final.to_dict()
    gc.collect()
    rss.append(_rss())
    # Joining SDK workers may lag publication by a few instructions.
    deadline = time.monotonic() + 2
    while time.monotonic() < deadline:
        extra_threads = [thread for thread in threading.enumerate()
                         if thread not in baseline_threads and thread.is_alive()]
        if not extra_threads:
            break
        time.sleep(0.01)
    assert not extra_threads, [thread.name for thread in extra_threads]
    if args.component == "producer":
        assert service.callbacks == submitted, (service.callbacks, submitted)
        assert instance.memory_limiter.used() == 0
    else:
        # Stop may release the one fetched batch which has not begun processing.
        assert service.processed > 0, "consumer did not process the steady workload"
        assert 0 <= service.fetched - service.processed <= 1, (service.processed, service.fetched)
    if final.operational is not None:
        op = final.operational
        if args.component == "producer":
            assert op.owned_logs == op.owned_groups == op.send_calls_in_flight == 0
            assert op.aggregate_batches == op.aggregate_groups == 0
            assert op.callbacks_pending == op.callbacks_in_flight == 0
            assert op.counters.accepted_logs_total == submitted * 10
            assert op.counters.terminal_success_logs_total == submitted * 10
        else:
            assert op.held_batch_references == op.ready_to_process == 0
            assert op.fetch_in_flight == op.process_in_flight == 0
            assert op.counters.processed_success_logs_total == service.processed * 10
            for name, count in op.counters.items():
                if name.endswith("_failure_total"):
                    assert count == 0, (name, count)
    return dict(component=args.component, level=args.level, seconds=wall_seconds,
                monitor_seconds=args.monitor_seconds, monitor_samples=samples,
                cpu_seconds=cpu_seconds, cpu_percent=100 * cpu_seconds / wall_seconds,
                rss_kind="live_bytes" if sys.platform.startswith("linux") else "peak_bytes",
                rss_first=rss[0], rss_final=rss[-1], rss_peak=max(rss),
                rss_samples=rss, peak_threads=peak_threads,
                extra_threads_after_close=0, submitted_groups=submitted,
                sent_batches=service.sent, fetched_batches=service.fetched,
                processed_batches=service.processed, callbacks=service.callbacks,
                snapshot_p50_us=latencies[149], snapshot_p99_us=latencies[296],
                final=final.to_dict(), python=sys.version.split()[0])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("component", choices=("producer", "consumer"))
    parser.add_argument("level", choices=("off", "core", "detailed"))
    parser.add_argument("--seconds", type=float, default=30)
    parser.add_argument("--monitor-seconds", type=float, default=0)
    parser.add_argument("--requests-per-second", type=float, default=200)
    args = parser.parse_args()
    if not 0 < args.seconds <= 3600 or args.monitor_seconds < 0 or args.requests_per_second <= 0:
        parser.error("duration must be in (0, 3600], monitor >= 0 and request rate > 0")
    print(json.dumps(run(args), sort_keys=True))


if __name__ == "__main__":
    main()
