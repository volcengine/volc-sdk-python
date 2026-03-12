import math
import random

RETRY_POLICY_TOTAL_TIMEOUT_MIN = 30
RETRY_POLICY_TOTAL_TIMEOUT_MAX = 15 * 60
RETRY_POLICY_INITIAL_INTERVAL_MIN = 0.1
RETRY_POLICY_INITIAL_INTERVAL_MAX = 30
RETRY_POLICY_MAX_INTERVAL_MIN = 1
RETRY_POLICY_MAX_INTERVAL_MAX = 60
RETRY_POLICY_MULTIPLIER_MIN = 1.0
RETRY_POLICY_MULTIPLIER_MAX = 3.0
RETRY_POLICY_RANDOMIZATION_MIN = 0.1
RETRY_POLICY_RANDOMIZATION_MAX = 1.0
RETRY_POLICY_MAX_ATTEMPTS_MIN = 0
RETRY_POLICY_MAX_ATTEMPTS_MAX = 50
DEFAULT_RETRY_RANDOMIZATION_FACTOR = 0.25
DEFAULT_RETRY_MULTIPLIER = 2.0
DEFAULT_RETRY_MAX_INTERVAL = 10
DEFAULT_RETRY_INTERVAL = 0.5
DEFAULT_RETRY_TIMEOUT = 90


class RetryPolicy(object):
    def __init__(self, total_timeout=None, initial_interval=None, max_interval=None, multiplier=None,
                 randomization_factor=None, max_attempts=0):
        self.total_timeout = total_timeout
        self.initial_interval = initial_interval
        self.max_interval = max_interval
        self.multiplier = multiplier
        self.randomization_factor = randomization_factor
        self.max_attempts = max_attempts

    @staticmethod
    def default_policy():
        return RetryPolicy(
            total_timeout=DEFAULT_RETRY_TIMEOUT,
            initial_interval=DEFAULT_RETRY_INTERVAL,
            max_interval=DEFAULT_RETRY_MAX_INTERVAL,
            multiplier=DEFAULT_RETRY_MULTIPLIER,
            randomization_factor=DEFAULT_RETRY_RANDOMIZATION_FACTOR,
            max_attempts=0,
        )

    def normalize(self):
        total_timeout = self.total_timeout
        if total_timeout is None or total_timeout <= 0 or (isinstance(total_timeout, float) and math.isnan(total_timeout)):
            total_timeout = DEFAULT_RETRY_TIMEOUT
        if total_timeout < RETRY_POLICY_TOTAL_TIMEOUT_MIN:
            total_timeout = RETRY_POLICY_TOTAL_TIMEOUT_MIN
        if total_timeout > RETRY_POLICY_TOTAL_TIMEOUT_MAX:
            total_timeout = RETRY_POLICY_TOTAL_TIMEOUT_MAX

        initial_interval = self.initial_interval
        if initial_interval is None or initial_interval <= 0 or (isinstance(initial_interval, float) and math.isnan(initial_interval)):
            initial_interval = DEFAULT_RETRY_INTERVAL
        if initial_interval < RETRY_POLICY_INITIAL_INTERVAL_MIN:
            initial_interval = RETRY_POLICY_INITIAL_INTERVAL_MIN
        if initial_interval > RETRY_POLICY_INITIAL_INTERVAL_MAX:
            initial_interval = RETRY_POLICY_INITIAL_INTERVAL_MAX

        max_interval = self.max_interval
        if max_interval is None or max_interval <= 0 or (isinstance(max_interval, float) and math.isnan(max_interval)):
            max_interval = DEFAULT_RETRY_MAX_INTERVAL
        if max_interval < RETRY_POLICY_MAX_INTERVAL_MIN:
            max_interval = RETRY_POLICY_MAX_INTERVAL_MIN
        if max_interval > RETRY_POLICY_MAX_INTERVAL_MAX:
            max_interval = RETRY_POLICY_MAX_INTERVAL_MAX
        if max_interval < initial_interval:
            max_interval = initial_interval

        multiplier = self.multiplier
        if multiplier is None or multiplier <= 0 or (isinstance(multiplier, float) and math.isnan(multiplier)):
            multiplier = DEFAULT_RETRY_MULTIPLIER
        if multiplier < RETRY_POLICY_MULTIPLIER_MIN:
            multiplier = RETRY_POLICY_MULTIPLIER_MIN
        if multiplier > RETRY_POLICY_MULTIPLIER_MAX:
            multiplier = RETRY_POLICY_MULTIPLIER_MAX

        randomization_factor = self.randomization_factor
        if randomization_factor is None or randomization_factor < 0 or (
                isinstance(randomization_factor, float) and math.isnan(randomization_factor)):
            randomization_factor = DEFAULT_RETRY_RANDOMIZATION_FACTOR
        if randomization_factor < RETRY_POLICY_RANDOMIZATION_MIN:
            randomization_factor = RETRY_POLICY_RANDOMIZATION_MIN
        if randomization_factor > RETRY_POLICY_RANDOMIZATION_MAX:
            randomization_factor = RETRY_POLICY_RANDOMIZATION_MAX

        max_attempts = self.max_attempts
        if max_attempts is None:
            max_attempts = RETRY_POLICY_MAX_ATTEMPTS_MIN
        if max_attempts < RETRY_POLICY_MAX_ATTEMPTS_MIN:
            max_attempts = RETRY_POLICY_MAX_ATTEMPTS_MIN
        if max_attempts > RETRY_POLICY_MAX_ATTEMPTS_MAX:
            max_attempts = RETRY_POLICY_MAX_ATTEMPTS_MAX

        return RetryPolicy(
            total_timeout=total_timeout,
            initial_interval=initial_interval,
            max_interval=max_interval,
            multiplier=multiplier,
            randomization_factor=randomization_factor,
            max_attempts=max_attempts,
        )

    def backoff_seconds(self, attempt):
        interval = self.initial_interval * (self.multiplier ** max(attempt - 1, 0))
        if interval > self.max_interval:
            interval = self.max_interval
        if self.randomization_factor > 0:
            delta = self.randomization_factor * interval
            interval = random.uniform(interval - delta, interval + delta)
        if interval < 0:
            interval = 0
        return interval
