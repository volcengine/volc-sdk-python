# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from enum import Enum
from typing import List

from volcengine.tls.const import *
from volcengine.tls.data import ConsumeShard
from volcengine.tls.tls_exception import TLSException


def check_empty_string(value: str, field: str):
    if value is None or len(value) == 0:
        raise TLSException(error_code="InvalidArgument", error_message="{} should not be empty.".format(field))


def check_int_value_range(value: int, lower: int, upper: int, field: str):
    if value < lower or value > upper:
        raise TLSException(error_code="InvalidArgument",
                           error_message="{} value should between {} and {}.".format(field, lower, upper))


class ConsumerConfig:
    def __setattr__(self, name, value):
        if (name in ("metrics_level",)
                and self.__dict__.get("_health_config_frozen", False)
                and name in self.__dict__
                and self.__dict__[name] != value):
            raise AttributeError(
                "{} is immutable after validation".format(name))
        object.__setattr__(self, name, value)

    def __init__(self, project_id: str, consumer_group_name: str, topic_id_list: List[str], consumer_name: str,
                 consume_from: str = "begin", heartbeat_interval_in_second: int = 20,
                 data_fetch_interval_in_millisecond: int = 200, flush_checkpoint_interval_in_second: int = 5,
                 max_fetch_log_group_count: int = 100, ordered_consume: bool = False, stop_timeout: int = 15,
                 compression: str = LZ4, metrics_level: str = "off"):
        self._health_config_frozen = False
        self.project_id = project_id
        self.consumer_group_name = consumer_group_name
        self.topic_id_list = topic_id_list
        self.consumer_name = consumer_name

        self.consume_from = consume_from
        self.heartbeat_interval_in_second = heartbeat_interval_in_second
        self.data_fetch_interval_in_millisecond = data_fetch_interval_in_millisecond
        self.flush_checkpoint_interval_in_second = flush_checkpoint_interval_in_second
        self.max_fetch_log_group_count = max_fetch_log_group_count
        self.ordered_consume = ordered_consume

        self.stop_timeout = stop_timeout
        self.compression = compression
        # The health tail is intentionally a single public switch. Detailed
        # mode selects fixed histogram bounds internally.
        from volcengine.tls.stats import constants as _stats_const
        self.metrics_level = _stats_const.normalize_metrics_level(metrics_level)
        self._health_config_frozen = True

    def validate(self):
        check_empty_string(self.project_id, PROJECT_ID_UPPERCASE)
        check_empty_string(self.consumer_group_name, CONSUMER_GROUP_NAME)
        check_empty_string(self.consumer_name, CONSUMER_NAME)

        if self.topic_id_list is None or len(self.topic_id_list) == 0:
            raise TLSException(error_code="InvalidArgument", error_message="TopicIDList should not be empty.")
        for topic_id in self.topic_id_list:
            check_empty_string(topic_id, TOPIC_ID_UPPERCASE)

        check_empty_string(self.consumer_name, CONSUME_FROM)
        check_int_value_range(self.heartbeat_interval_in_second, 1, 300, HEARTBEAT_INTERVAL_IN_SECOND)
        check_int_value_range(self.data_fetch_interval_in_millisecond, 1, 300000, DATA_FETCH_INTERVAL_IN_MILLISECOND)
        check_int_value_range(self.flush_checkpoint_interval_in_second, 1, 300, FLUSH_CHECKPOINT_INTERVAL_IN_SECOND)
        check_int_value_range(self.max_fetch_log_group_count, 1, 1000, MAX_FETCH_LOG_GROUP_COUNT)
        check_int_value_range(self.stop_timeout, 1, 300, STOP_TIMEOUT)

        # Normalize health-stats switches (independent, immutable after this).
        from volcengine.tls.stats import constants as _stats_const
        self.metrics_level = _stats_const.normalize_metrics_level(self.metrics_level)
        self._health_config_frozen = True


class CheckpointInfo:
    def __init__(self, checkpoint: str, shard_info: ConsumeShard):
        self.checkpoint = checkpoint
        self.shard_info = shard_info


class ConsumerStatus(Enum):
    PENDING = "pending"
    INITIALIZING = "Initializing"
    READY_TO_FETCH = "ready_to_fetch"
    FETCHING = "fetching"
    READY_TO_CONSUME = "ready_to_consume"
    CONSUMING = "consuming"
    BACKOFF = "backoff"
    WAIT_FOR_RESTART = "wait_for_restart"
