"""Run the offline observation and producer/consumer regression suite.

Usage: python -m volcengine.tls.test.run_observability_tests
"""
import json
import logging
import os
import socket
import sys
import threading
import time
import unittest
from unittest.mock import patch


TEST_MODULES = (
    "consumer_stats_test", "producer_stats_test",
    "consumer_lifecycle_test", "producer_lifecycle_test",
    "stats_integrity_test", "stats_runtime_test",
    "stats_concurrency_test", "stats_contract_test", "stats_docs_test",
    "stats_histogram_test", "stats_latency_test",
    "stats_snapshot_test", "stats_adapter_test",
    "producer_memory_resilience_test", "producer_split_unit_test",
    "test_producer_batch_manager", "retry_policy_test", "put_logs_validation_unit_test",
)


def main():
    network_attempts = []

    def deny_network(*_args, **_kwargs):
        network_attempts.append(True)
        raise AssertionError("unexpected network in offline tests")

    baseline = set(threading.enumerate())
    previous_logging_level = logging.root.manager.disable
    logging.disable(logging.CRITICAL)
    try:
        with patch.object(socket.socket, "connect", deny_network), \
                patch.object(socket, "create_connection", deny_network):
            suite = unittest.defaultTestLoader.loadTestsFromNames(
                ["volcengine.tls.test." + name for name in TEST_MODULES])
            result = unittest.TextTestRunner(verbosity=2).run(suite)
            deadline = time.monotonic() + 10
            while True:
                leaked = [thread for thread in threading.enumerate()
                          if thread not in baseline and thread.is_alive()]
                if not leaked or time.monotonic() >= deadline:
                    break
                time.sleep(0.05)
    finally:
        logging.disable(previous_logging_level)

    summary = dict(
        python=sys.version.split()[0], tests=result.testsRun,
        failures=len(result.failures), errors=len(result.errors),
        skipped=len(result.skipped), unexpected_network_attempts=len(network_attempts),
        leaked_threads=[thread.name for thread in leaked],
    )
    print("ACCEPTANCE_SUMMARY " + json.dumps(summary, sort_keys=True))
    code = 0 if result.wasSuccessful() and not network_attempts and not leaked else 1
    if leaked:
        # A leaked non-daemon test thread must fail without hanging the command.
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(code)
    return code


if __name__ == "__main__":
    sys.exit(main())
