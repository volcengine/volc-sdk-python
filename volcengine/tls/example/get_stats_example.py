# coding=utf-8
"""Run with python -m volcengine.tls.example.get_stats_example (offline)."""
import json
from uuid import uuid4

from volcengine.tls.producer.producer import TLSProducer
from volcengine.tls.producer.producer_model import ProducerConfig
from volcengine.tls.stats import StatsOptions, DeltaAdapter, evaluate_health


def main():
    # Offline-only credentials; this example never starts transport workers.
    access_key, access_secret = uuid4().hex, uuid4().hex
    producer = TLSProducer(ProducerConfig(
        "endpoint", "cn-beijing", access_key, access_secret,
        metrics_level="core"))
    options = StatsOptions("operational")
    previous = producer.get_stats(options)
    assert previous.lifecycle_state == "new"

    # An empty instance exercises observation without starting transport workers.
    current = producer.get_stats(options)
    assert current.operational.counters.accepted_logs_total == 0
    assert current.operational.owned_logs == 0
    copied = current.to_dict()
    copied["operational"]["counters"]["accepted_logs_total"] = -1
    assert current.operational.counters.accepted_logs_total == 0

    adapter = DeltaAdapter()
    assert adapter.observe(previous.counter_sample()).reset_reason == "initial_baseline"
    interval = adapter.observe(current.counter_sample())
    # Same-millisecond captures are deliberately invalid intervals.
    print(json.dumps(interval.to_dict(), sort_keys=True))
    assert evaluate_health(previous, current).status == "unknown"

    debug = producer.get_stats(StatsOptions("debug"))
    assert debug.partial and "latency_histograms" in debug.missing_sections
    off = TLSProducer(ProducerConfig("endpoint", "cn-beijing", access_key, access_secret))
    off_snapshot = off.get_stats(options)
    assert off_snapshot.metrics_disabled and off_snapshot.operational is None
    assert off_snapshot.counter_sample() is None
    producer.close()
    off.close()
    print(json.dumps(producer.get_stats(options).to_dict(), sort_keys=True))
    print("OK")


if __name__ == "__main__":
    main()
