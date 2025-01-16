# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import hashlib
import threading
import random

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.auth.SignerV4 import SignerV4
from volcengine.base.Service import Service
from volcengine.tls.tls_requests import *
from volcengine.tls.tls_responses import *
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.util import get_logger

API_INFO = {
    # APIs of log projects.
    CREATE_PROJECT: ApiInfo(HTTP_POST, CREATE_PROJECT, {}, {}, {}),
    DELETE_PROJECT: ApiInfo(HTTP_DELETE, DELETE_PROJECT, {}, {}, {}),
    MODIFY_PROJECT: ApiInfo(HTTP_PUT, MODIFY_PROJECT, {}, {}, {}),
    DESCRIBE_PROJECT: ApiInfo(HTTP_GET, DESCRIBE_PROJECT, {}, {}, {}),
    DESCRIBE_PROJECTS: ApiInfo(HTTP_GET, DESCRIBE_PROJECTS, {}, {}, {}),
    # APIs of log topics.
    CREATE_TOPIC: ApiInfo(HTTP_POST, CREATE_TOPIC, {}, {}, {}),
    DELETE_TOPIC: ApiInfo(HTTP_DELETE, DELETE_TOPIC, {}, {}, {}),
    MODIFY_TOPIC: ApiInfo(HTTP_PUT, MODIFY_TOPIC, {}, {}, {}),
    DESCRIBE_TOPIC: ApiInfo(HTTP_GET, DESCRIBE_TOPIC, {}, {}, {}),
    DESCRIBE_TOPICS: ApiInfo(HTTP_GET, DESCRIBE_TOPICS, {}, {}, {}),
    # APIs of log index.
    CREATE_INDEX: ApiInfo(HTTP_POST, CREATE_INDEX, {}, {}, {}),
    DELETE_INDEX: ApiInfo(HTTP_DELETE, DELETE_INDEX, {}, {}, {}),
    MODIFY_INDEX: ApiInfo(HTTP_PUT, MODIFY_INDEX, {}, {}, {}),
    DESCRIBE_INDEX: ApiInfo(HTTP_GET, DESCRIBE_INDEX, {}, {}, {}),
    # APIs of logs.
    PUT_LOGS: ApiInfo(HTTP_POST, PUT_LOGS, {}, {}, {}),
    DESCRIBE_CURSOR: ApiInfo(HTTP_GET, DESCRIBE_CURSOR, {}, {}, {}),
    CONSUME_LOGS: ApiInfo(HTTP_GET, CONSUME_LOGS, {}, {}, {}),
    SEARCH_LOGS: ApiInfo(HTTP_POST, SEARCH_LOGS, {}, {}, {}),
    DESCRIBE_LOG_CONTEXT: ApiInfo(HTTP_POST, DESCRIBE_LOG_CONTEXT, {}, {}, {}),
    WEB_TRACKS: ApiInfo(HTTP_POST, WEB_TRACKS, {}, {}, {}),
    DESCRIBE_HISTOGRAM: ApiInfo(HTTP_POST, DESCRIBE_HISTOGRAM, {}, {}, {}),
    DESCRIBE_HISTOGRAM_V1: ApiInfo(HTTP_POST, DESCRIBE_HISTOGRAM_V1, {}, {}, {}),
    CREATE_DOWNLOAD_TASK: ApiInfo(HTTP_POST, CREATE_DOWNLOAD_TASK, {}, {}, {}),
    DESCRIBE_DOWNLOAD_TASKS: ApiInfo(HTTP_GET, DESCRIBE_DOWNLOAD_TASKS, {}, {}, {}),
    DESCRIBE_DOWNLOAD_URL: ApiInfo(HTTP_GET, DESCRIBE_DOWNLOAD_URL, {}, {}, {}),
    # APIs of shards.
    DESCRIBE_SHARDS: ApiInfo(HTTP_GET, DESCRIBE_SHARDS, {}, {}, {}),
    # APIs of host groups.
    CREATE_HOST_GROUP: ApiInfo(HTTP_POST, CREATE_HOST_GROUP, {}, {}, {}),
    DELETE_HOST_GROUP: ApiInfo(HTTP_DELETE, DELETE_HOST_GROUP, {}, {}, {}),
    MODIFY_HOST_GROUP: ApiInfo(HTTP_PUT, MODIFY_HOST_GROUP, {}, {}, {}),
    DESCRIBE_HOST_GROUP: ApiInfo(HTTP_GET, DESCRIBE_HOST_GROUP, {}, {}, {}),
    DESCRIBE_HOST_GROUPS: ApiInfo(HTTP_GET, DESCRIBE_HOST_GROUPS, {}, {}, {}),
    DESCRIBE_HOSTS: ApiInfo(HTTP_GET, DESCRIBE_HOSTS, {}, {}, {}),
    DELETE_HOST: ApiInfo(HTTP_DELETE, DELETE_HOST, {}, {}, {}),
    DESCRIBE_HOST_GROUP_RULES: ApiInfo(HTTP_GET, DESCRIBE_HOST_GROUP_RULES, {}, {}, {}),
    MODIFY_HOST_GROUPS_AUTO_UPDATE: ApiInfo(HTTP_PUT, MODIFY_HOST_GROUPS_AUTO_UPDATE, {}, {}, {}),
    DELETE_ABNORMAL_HOSTS: ApiInfo(HTTP_DELETE, DELETE_ABNORMAL_HOSTS, {}, {}, {}),
    # APIs of rules.
    CREATE_RULE: ApiInfo(HTTP_POST, CREATE_RULE, {}, {}, {}),
    DELETE_RULE: ApiInfo(HTTP_DELETE, DELETE_RULE, {}, {}, {}),
    MODIFY_RULE: ApiInfo(HTTP_PUT, MODIFY_RULE, {}, {}, {}),
    DESCRIBE_RULE: ApiInfo(HTTP_GET, DESCRIBE_RULE, {}, {}, {}),
    DESCRIBE_RULES: ApiInfo(HTTP_GET, DESCRIBE_RULES, {}, {}, {}),
    APPLY_RULE_TO_HOST_GROUPS: ApiInfo(HTTP_PUT, APPLY_RULE_TO_HOST_GROUPS, {}, {}, {}),
    DELETE_RULE_FROM_HOST_GROUPS: ApiInfo(HTTP_PUT, DELETE_RULE_FROM_HOST_GROUPS, {}, {}, {}),
    # APIs of alarms.
    CREATE_ALARM_NOTIFY_GROUP: ApiInfo(HTTP_POST, CREATE_ALARM_NOTIFY_GROUP, {}, {}, {}),
    DELETE_ALARM_NOTIFY_GROUP: ApiInfo(HTTP_DELETE, DELETE_ALARM_NOTIFY_GROUP, {}, {}, {}),
    MODIFY_ALARM_NOTIFY_GROUP: ApiInfo(HTTP_PUT, MODIFY_ALARM_NOTIFY_GROUP, {}, {}, {}),
    DESCRIBE_ALARM_NOTIFY_GROUPS: ApiInfo(HTTP_GET, DESCRIBE_ALARM_NOTIFY_GROUPS, {}, {}, {}),
    CREATE_ALARM: ApiInfo(HTTP_POST, CREATE_ALARM, {}, {}, {}),
    DELETE_ALARM: ApiInfo(HTTP_DELETE, DELETE_ALARM, {}, {}, {}),
    MODIFY_ALARM: ApiInfo(HTTP_PUT, MODIFY_ALARM, {}, {}, {}),
    DESCRIBE_ALARMS: ApiInfo(HTTP_GET, DESCRIBE_ALARMS, {}, {}, {}),
    # APIs of Kafka consumer.
    OPEN_KAFKA_CONSUMER: ApiInfo(HTTP_PUT, OPEN_KAFKA_CONSUMER, {}, {}, {}),
    CLOSE_KAFKA_CONSUMER: ApiInfo(HTTP_PUT, CLOSE_KAFKA_CONSUMER, {}, {}, {}),
    DESCRIBE_KAFKA_CONSUMER: ApiInfo(HTTP_GET, DESCRIBE_KAFKA_CONSUMER, {}, {}, {}),
    # APIs of consumer group.
    CREATE_CONSUMER_GROUP: ApiInfo(HTTP_POST, CREATE_CONSUMER_GROUP, {}, {}, {}),
    DELETE_CONSUMER_GROUP: ApiInfo(HTTP_DELETE, DELETE_CONSUMER_GROUP, {}, {}, {}),
    MODIFY_CONSUMER_GROUP: ApiInfo(HTTP_PUT, MODIFY_CONSUMER_GROUP, {}, {}, {}),
    DESCRIBE_CONSUMER_GROUPS: ApiInfo(HTTP_GET, DESCRIBE_CONSUMER_GROUPS, {}, {}, {}),
    CONSUMER_HEARTBEAT: ApiInfo(HTTP_POST, CONSUMER_HEARTBEAT, {}, {}, {}),
    MODIFY_CHECKPOINT: ApiInfo(HTTP_PUT, MODIFY_CHECKPOINT, {}, {}, {}),
    RESET_CHECKPOINT: ApiInfo(HTTP_PUT, RESET_CHECKPOINT, {}, {}, {}),
    DESCRIBE_CHECKPOINT: ApiInfo(HTTP_GET, DESCRIBE_CHECKPOINT, {}, {}, {}),
    # APIs of resource labels.
    ADD_TAGS_TO_RESOURCE: ApiInfo(HTTP_POST, ADD_TAGS_TO_RESOURCE, {}, {}, {}),
    REMOVE_TAGS_FROM_RESOURCE: ApiInfo(HTTP_POST, REMOVE_TAGS_FROM_RESOURCE, {}, {}, {})
}

HEADER_API_VERSION = "x-tls-apiversion"
API_VERSION_V_0_3_0 = "0.3.0"
API_VERSION_V_0_2_0 = "0.2.0"


class TLSService(Service):
    _instance_lock = threading.Lock()
    _default_retry_interval_ms = 100
    _default_retry_counter = 0
    _default_retry_counter_maximum = 50

    @staticmethod
    def set_default_retry_counter_maximum(v):
        TLSService._default_retry_counter_maximum = v

    @staticmethod
    def increase_retry_counter_by_one():
        with TLSService._instance_lock:
            if TLSService._default_retry_counter < TLSService._default_retry_counter_maximum:
                TLSService._default_retry_counter += 1

    @staticmethod
    def decrease_retry_counter_by_one():
        with TLSService._instance_lock:
            if TLSService._default_retry_counter < TLSService._default_retry_counter_maximum:
                TLSService._default_retry_counter -= 1

    @staticmethod
    def calc_backoff_ms(expected_quit_timestamp_ms):
        current_timestamp_ms = int(time.time() * 1000)
        counter = TLSService._default_retry_counter
        sleep_ms = random.random() * counter * TLSService._default_retry_interval_ms
        if current_timestamp_ms + sleep_ms > expected_quit_timestamp_ms:
            sleep_ms = expected_quit_timestamp_ms - current_timestamp_ms
        if sleep_ms < 0:
            sleep_ms = 0
        return sleep_ms

    def __init__(self, endpoint: str, access_key_id: str, access_key_secret: str, region: str,
                 security_token: str = None, scheme: str = "https", timeout: int = 60,
                 api_version=API_VERSION_V_0_3_0):
        self.__endpoint = endpoint
        self.__access_key_id = access_key_id
        self.__access_key_secret = access_key_secret
        self.__region = region
        self.__security_token = security_token
        self.__scheme = scheme
        self.__timeout = timeout
        self.__api_version = api_version

        self.check_scheme_and_endpoint()

        self.__logger = get_logger("tls-python-sdk-logger")
        self.__logger.info("Successfully initialize the TLS client.")

        super(TLSService, self).__init__(service_info=self.get_service_info(), api_info=API_INFO)

    def check_scheme_and_endpoint(self):
        schemes = {
            "http://": "http",
            "https://": "https",
        }

        for prefix, scheme in schemes.items():
            if self.__endpoint.startswith(prefix):
                self.__scheme = scheme
                self.__endpoint = self.__endpoint[len(prefix):]
                return

    def get_region(self):
        return self.__region

    def get_service_info(self):
        header = {}

        if self.__security_token is not None:
            header[X_SECURITY_TOKEN] = self.__security_token
        credentials = Credentials(ak=self.__access_key_id, sk=self.__access_key_secret,
                                  service="TLS", region=self.__region)
        service_info = ServiceInfo(host=self.__endpoint, header=header, credentials=credentials, scheme=self.__scheme,
                                   connection_timeout=self.__timeout, socket_timeout=self.__timeout)

        return service_info

    def __prepare_request(self, api: str, params: dict = None, body: dict = None, request_headers: dict = None):
        if params is None:
            params = {}
        if body is None:
            body = {}

        request = self.prepare_request(self.api_info[api], params)

        if request_headers is None:
            request_headers = {CONTENT_TYPE: APPLICATION_JSON}
        request.headers.update(request_headers)

        if "json" in request.headers[CONTENT_TYPE] and api != WEB_TRACKS:
            request.body = json.dumps(body)
        else:
            request.body = body[DATA]

        if len(request.body) != 0:
            if isinstance(request.body, str):
                request.headers[CONTENT_MD5] = hashlib.md5(request.body.encode("utf-8")).hexdigest()
            else:
                request.headers[CONTENT_MD5] = hashlib.md5(request.body).hexdigest()

        SignerV4.sign(request, self.service_info.credentials)

        return request

    def __request(self, api: str, params: dict = None, body: dict = None, request_headers: dict = None):
        if request_headers is None:
            request_headers = {HEADER_API_VERSION: self.__api_version}
        elif HEADER_API_VERSION not in request_headers:
            request_headers[HEADER_API_VERSION] = self.__api_version
        if CONTENT_TYPE not in request_headers:
            request_headers[CONTENT_TYPE] = APPLICATION_JSON
        request = self.__prepare_request(api, params, body, request_headers)

        method = self.api_info[api].method
        url = request.build()

        expected_quit_timestamp = int(time.time() * 1000 + self.__timeout * 1500)
        try_count = 0
        while True:
            try_count += 1
            try:
                # if try_count == 1:
                #     self.__logger.info("TLS client is trying to request {}.".format(api))
                response = self.session.request(method, url, headers=request.headers, data=request.body,
                                                timeout=self.__timeout)
            except Exception as e:
                TLSService.increase_retry_counter_by_one()
                sleep_ms = TLSService.calc_backoff_ms(expected_quit_timestamp)
                if try_count < 5 and sleep_ms > 0:
                    # HTTP请求未响应, 尝试重试
                    time.sleep(sleep_ms / 1000)
                else:
                    # 已超出重试上限, 退出
                    raise TLSException(error_code=e.__class__.__name__, error_message=e.__str__())
            else:
                if response.status_code == 200:
                    # self.__logger.info("TLS client successfully got the response for requesting {}".format(api))
                    TLSService.decrease_retry_counter_by_one()
                    return response
                elif try_count < 5 and response.status_code in [429, 500, 502, 503]:
                    TLSService.increase_retry_counter_by_one()
                    sleep_ms = TLSService.calc_backoff_ms(expected_quit_timestamp)
                    if sleep_ms > 0:
                        # HTTP请求未响应, 尝试重试
                        time.sleep(sleep_ms / 1000)
                    else:
                        raise TLSException(response)
                else:
                    raise TLSException(response)

    def reset_access_key_token(self, access_key_id: str, access_key_secret: str, security_token: str = None):
        self.__access_key_id = access_key_id
        self.__access_key_secret = access_key_secret
        self.__security_token = security_token
        self.service_info = self.get_service_info()

    def set_timeout(self, timeout: int):
        self.__timeout = timeout
        self.service_info = self.get_service_info()

    def create_project(self, create_project_request: CreateProjectRequest) -> CreateProjectResponse:
        if create_project_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=CREATE_PROJECT, body=create_project_request.get_api_input())

        return CreateProjectResponse(response)

    def delete_project(self, delete_project_request: DeleteProjectRequest) -> DeleteProjectResponse:
        if delete_project_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DELETE_PROJECT, body=delete_project_request.get_api_input())

        return DeleteProjectResponse(response)

    def modify_project(self, modify_project_request: ModifyProjectRequest) -> ModifyProjectResponse:
        if modify_project_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=MODIFY_PROJECT, body=modify_project_request.get_api_input())

        return ModifyProjectResponse(response)

    def describe_project(self, describe_project_request: DescribeProjectRequest) -> DescribeProjectResponse:
        if describe_project_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DESCRIBE_PROJECT, params=describe_project_request.get_api_input())

        return DescribeProjectResponse(response)

    def describe_projects(self, describe_projects_request: DescribeProjectsRequest) -> DescribeProjectsResponse:
        if describe_projects_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DESCRIBE_PROJECTS, params=describe_projects_request.get_api_input())

        return DescribeProjectsResponse(response)

    def create_topic(self, create_topic_request: CreateTopicRequest) -> CreateTopicResponse:
        if create_topic_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=CREATE_TOPIC, body=create_topic_request.get_api_input())

        return CreateTopicResponse(response)

    def delete_topic(self, delete_topic_request: DeleteTopicRequest) -> DeleteTopicResponse:
        if delete_topic_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DELETE_TOPIC, body=delete_topic_request.get_api_input())

        return DeleteTopicResponse(response)

    def modify_topic(self, modify_topic_request: ModifyTopicRequest) -> ModifyTopicResponse:
        if modify_topic_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=MODIFY_TOPIC, body=modify_topic_request.get_api_input())

        return ModifyTopicResponse(response)

    def describe_topic(self, describe_topic_request: DescribeTopicRequest) -> DescribeTopicResponse:
        if describe_topic_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DESCRIBE_TOPIC, params=describe_topic_request.get_api_input())

        return DescribeTopicResponse(response)

    def describe_topics(self, describe_topics_request: DescribeTopicsRequest) -> DescribeTopicsResponse:
        if describe_topics_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DESCRIBE_TOPICS, params=describe_topics_request.get_api_input())

        return DescribeTopicsResponse(response)

    def create_index(self, create_index_request: CreateIndexRequest) -> CreateIndexResponse:
        if create_index_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=CREATE_INDEX, body=create_index_request.get_api_input())

        return CreateIndexResponse(response)

    def delete_index(self, delete_index_request: DeleteIndexRequest) -> DeleteIndexResponse:
        if delete_index_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DELETE_INDEX, body=delete_index_request.get_api_input())

        return DeleteIndexResponse(response)

    def modify_index(self, modify_index_request: ModifyIndexRequest) -> ModifyIndexResponse:
        if modify_index_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=MODIFY_INDEX, body=modify_index_request.get_api_input())

        return ModifyIndexResponse(response)

    def describe_index(self, describe_index_request: DescribeIndexRequest) -> DescribeIndexResponse:
        if describe_index_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DESCRIBE_INDEX, params=describe_index_request.get_api_input())

        return DescribeIndexResponse(response)

    def put_logs(self, put_logs_request: PutLogsRequest) -> PutLogsResponse:
        if put_logs_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        api_input = put_logs_request.get_api_input()
        response = self.__request(api=PUT_LOGS, params=api_input[PARAMS], body=api_input[BODY],
                                  request_headers=api_input[REQUEST_HEADERS])

        return PutLogsResponse(response)

    def put_logs_v2(self, request: PutLogsV2Request) -> PutLogsResponse:
        log_group_list = LogGroupList()
        log_group = log_group_list.log_groups.add()
        if request.logs.source is not None:
            log_group.source = request.logs.source
        if request.logs.filename is not None:
            log_group.filename = request.logs.filename
        for v in request.logs.logs:
            new_log = log_group.logs.add()
            if v.time <= 0:
                new_log.time = int(time.time() * 1000)
            else:
                new_log.time = v.time
            for key in v.log_dict.keys():
                log_content = new_log.contents.add()
                log_content.key = str(key)
                log_content.value = str(v.log_dict[key])
        put_logs_request = PutLogsRequest(request.topic_id, log_group_list, request.hash_key, request.compression)
        return self.put_logs(put_logs_request)

    def describe_cursor(self, describe_cursor_request: DescribeCursorRequest) -> DescribeCursorResponse:
        if describe_cursor_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        api_input = describe_cursor_request.get_api_input()
        response = self.__request(api=DESCRIBE_CURSOR, params=api_input[PARAMS], body=api_input[BODY])

        return DescribeCursorResponse(response)

    def consume_logs(self, consume_logs_request: ConsumeLogsRequest) -> ConsumeLogsResponse:
        if consume_logs_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        api_input = consume_logs_request.get_api_input()
        response = self.__request(api=CONSUME_LOGS, params=api_input[PARAMS], body=api_input[BODY],
                                  request_headers=api_input[REQUEST_HEADERS])

        return ConsumeLogsResponse(response, compression=consume_logs_request.compression)

    def search_logs(self, search_logs_request: SearchLogsRequest) -> SearchLogsResponse:
        if search_logs_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        headers = {HEADER_API_VERSION: API_VERSION_V_0_2_0}

        response = self.__request(api=SEARCH_LOGS, body=search_logs_request.get_api_input(), request_headers=headers)

        return SearchLogsResponse(response)

    def search_logs_v2(self, search_logs_request: SearchLogsRequest) -> SearchLogsResponse:
        """
        :param search_logs_request:搜索日志，按照api-version 0.3.0进行
        :type search_logs_request:
        :return: SearchLogsResponse:搜索日志
        :rtype: SearchLogsResponse
        """
        if search_logs_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        headers = {HEADER_API_VERSION: API_VERSION_V_0_3_0}
        response = self.__request(api=SEARCH_LOGS, body=search_logs_request.get_api_input(), request_headers=headers)

        return SearchLogsResponse(response)

    def describe_log_context(self, describe_log_context_request: DescribeLogContextRequest) \
            -> DescribeLogContextResponse:
        if describe_log_context_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DESCRIBE_LOG_CONTEXT, body=describe_log_context_request.get_api_input())

        return DescribeLogContextResponse(response)

    def web_tracks(self, web_tracks_request: WebTracksRequest) -> WebTracksResponse:
        if web_tracks_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        api_input = web_tracks_request.get_api_input()
        response = self.__request(api=WEB_TRACKS, params=api_input[PARAMS], body=api_input[BODY],
                                  request_headers=api_input[REQUEST_HEADERS])

        return WebTracksResponse(response)

    def describe_histogram(self, describe_histogram_request: DescribeHistogramRequest) -> DescribeHistogramResponse:
        """
        Deprecated, use describe_histogram_v1 instead.
        """
        if describe_histogram_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DESCRIBE_HISTOGRAM, body=describe_histogram_request.get_api_input())

        return DescribeHistogramResponse(response)

    def describe_histogram_v1(self, describe_histogram_v1_request: DescribeHistogramV1Request) -> DescribeHistogramV1Response:
        if describe_histogram_v1_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DESCRIBE_HISTOGRAM_V1, body=describe_histogram_v1_request.get_api_input())

        return DescribeHistogramV1Response(response)

    def create_download_task(self, create_download_task_request: CreateDownloadTaskRequest) \
            -> CreateDownloadTaskResponse:
        if create_download_task_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=CREATE_DOWNLOAD_TASK, body=create_download_task_request.get_api_input())

        return CreateDownloadTaskResponse(response)

    def describe_download_tasks(self, describe_download_tasks_request: DescribeDownloadTasksRequest) \
            -> DescribeDownloadTasksResponse:
        if describe_download_tasks_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DESCRIBE_DOWNLOAD_TASKS, params=describe_download_tasks_request.get_api_input())

        return DescribeDownloadTasksResponse(response)

    def describe_download_url(self, describe_download_url_request: DescribeDownloadUrlRequest) \
            -> DescribeDownloadUrlResponse:
        if describe_download_url_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DESCRIBE_DOWNLOAD_URL, params=describe_download_url_request.get_api_input())

        return DescribeDownloadUrlResponse(response)

    def describe_shards(self, describe_shards_request: DescribeShardsRequest) -> DescribeShardsResponse:
        if describe_shards_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DESCRIBE_SHARDS, params=describe_shards_request.get_api_input())

        return DescribeShardsResponse(response)

    def create_host_group(self, create_host_group_request: CreateHostGroupRequest) -> CreateHostGroupResponse:
        if create_host_group_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=CREATE_HOST_GROUP, body=create_host_group_request.get_api_input())

        return CreateHostGroupResponse(response)

    def delete_host_group(self, delete_host_group_request: DeleteHostGroupRequest) -> DeleteHostGroupResponse:
        if delete_host_group_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DELETE_HOST_GROUP, body=delete_host_group_request.get_api_input())

        return DeleteHostGroupResponse(response)

    def modify_host_group(self, modify_host_group_request: ModifyHostGroupRequest) -> ModifyHostGroupResponse:
        if modify_host_group_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=MODIFY_HOST_GROUP, body=modify_host_group_request.get_api_input())

        return ModifyHostGroupResponse(response)

    def describe_host_group(self, describe_host_group_request: DescribeHostGroupRequest) -> DescribeHostGroupResponse:
        if describe_host_group_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DESCRIBE_HOST_GROUP, params=describe_host_group_request.get_api_input())

        return DescribeHostGroupResponse(response)

    def describe_host_groups(self, describe_host_groups_request: DescribeHostGroupsRequest) \
            -> DescribeHostGroupsResponse:
        if describe_host_groups_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DESCRIBE_HOST_GROUPS, params=describe_host_groups_request.get_api_input())

        return DescribeHostGroupsResponse(response)

    def describe_hosts(self, describe_hosts_request: DescribeHostsRequest) -> DescribeHostsResponse:
        if describe_hosts_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DESCRIBE_HOSTS, params=describe_hosts_request.get_api_input())

        return DescribeHostsResponse(response)

    def delete_host(self, delete_host_request: DeleteHostRequest) -> DeleteHostResponse:
        if delete_host_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DELETE_HOST, body=delete_host_request.get_api_input())

        return DeleteHostResponse(response)

    def describe_host_group_rules(self, describe_host_group_rules_request: DescribeHostGroupRulesRequest) \
            -> DescribeHostGroupRulesResponse:
        if describe_host_group_rules_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DESCRIBE_HOST_GROUP_RULES, params=describe_host_group_rules_request.get_api_input())

        return DescribeHostGroupRulesResponse(response)

    def modify_host_groups_auto_update(self, modify_host_groups_auto_update_request: ModifyHostGroupsAutoUpdateRequest) \
            -> ModifyHostGroupsAutoUpdateResponse:
        if modify_host_groups_auto_update_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=MODIFY_HOST_GROUPS_AUTO_UPDATE,
                                  body=modify_host_groups_auto_update_request.get_api_input())

        return ModifyHostGroupsAutoUpdateResponse(response)

    def delete_abnormal_hosts(self, delete_abnormal_hosts_request: DeleteAbnormalHostsRequest) \
            -> DeleteAbnormalHostsResponse:
        if not delete_abnormal_hosts_request.check_validation():
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DELETE_ABNORMAL_HOSTS, body=delete_abnormal_hosts_request.get_api_input())

        return DeleteAbnormalHostsResponse(response)

    def create_rule(self, create_rule_request: CreateRuleRequest) -> CreateRuleResponse:
        if create_rule_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=CREATE_RULE, body=create_rule_request.get_api_input())

        return CreateRuleResponse(response)

    def delete_rule(self, delete_rule_request: DeleteRuleRequest) -> DeleteRuleResponse:
        if delete_rule_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DELETE_RULE, body=delete_rule_request.get_api_input())

        return DeleteRuleResponse(response)

    def modify_rule(self, modify_rule_request: ModifyRuleRequest) -> ModifyRuleResponse:
        if modify_rule_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=MODIFY_RULE, body=modify_rule_request.get_api_input())

        return ModifyRuleResponse(response)

    def describe_rule(self, describe_rule_request: DescribeRuleRequest) -> DescribeRuleResponse:
        if describe_rule_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DESCRIBE_RULE, params=describe_rule_request.get_api_input())

        return DescribeRuleResponse(response)

    def describe_rules(self, describe_rules_request: DescribeRulesRequest) -> DescribeRulesResponse:
        if describe_rules_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DESCRIBE_RULES, params=describe_rules_request.get_api_input())

        return DescribeRulesResponse(response)

    def apply_rule_to_host_groups(self, apply_rule_to_host_groups_request: ApplyRuleToHostGroupsRequest) \
            -> ApplyRuleToHostGroupsResponse:
        if apply_rule_to_host_groups_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=APPLY_RULE_TO_HOST_GROUPS, body=apply_rule_to_host_groups_request.get_api_input())

        return ApplyRuleToHostGroupsResponse(response)

    def delete_rule_from_host_groups(self, delete_rule_from_host_groups_request: DeleteRuleFromHostGroupsRequest) \
            -> DeleteRuleFromHostGroupsResponse:
        if delete_rule_from_host_groups_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DELETE_RULE_FROM_HOST_GROUPS,
                                  body=delete_rule_from_host_groups_request.get_api_input())

        return DeleteRuleFromHostGroupsResponse(response)

    def create_alarm_notify_group(self, create_alarm_notify_group_request: CreateAlarmNotifyGroupRequest) \
            -> CreateAlarmNotifyGroupResponse:
        if create_alarm_notify_group_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=CREATE_ALARM_NOTIFY_GROUP, body=create_alarm_notify_group_request.get_api_input())

        return CreateAlarmNotifyGroupResponse(response)

    def delete_alarm_notify_group(self, delete_alarm_notify_group_request: DeleteAlarmNotifyGroupRequest) \
            -> DeleteAlarmNotifyGroupResponse:
        if delete_alarm_notify_group_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DELETE_ALARM_NOTIFY_GROUP, body=delete_alarm_notify_group_request.get_api_input())

        return DeleteAlarmNotifyGroupResponse(response)

    def modify_alarm_notify_group(self, modify_alarm_notify_group_request: ModifyAlarmNotifyGroupRequest) \
            -> ModifyAlarmNotifyGroupResponse:
        if modify_alarm_notify_group_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=MODIFY_ALARM_NOTIFY_GROUP, body=modify_alarm_notify_group_request.get_api_input())

        return ModifyAlarmNotifyGroupResponse(response)

    def describe_alarm_notify_groups(self, describe_alarm_notify_groups_request: DescribeAlarmNotifyGroupsRequest) \
            -> DescribeAlarmNotifyGroupsResponse:
        if describe_alarm_notify_groups_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DESCRIBE_ALARM_NOTIFY_GROUPS, params=describe_alarm_notify_groups_request.get_api_input())

        return DescribeAlarmNotifyGroupsResponse(response)

    def create_alarm(self, create_alarm_request: CreateAlarmRequest) -> CreateAlarmResponse:
        if create_alarm_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=CREATE_ALARM, body=create_alarm_request.get_api_input())

        return CreateAlarmResponse(response)

    def delete_alarm(self, delete_alarm_request: DeleteAlarmRequest) -> DeleteAlarmResponse:
        if delete_alarm_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DELETE_ALARM, body=delete_alarm_request.get_api_input())

        return DeleteAlarmResponse(response)

    def modify_alarm(self, modify_alarm_request: ModifyAlarmRequest) -> ModifyAlarmResponse:
        if modify_alarm_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=MODIFY_ALARM, body=modify_alarm_request.get_api_input())

        return ModifyAlarmResponse(response)

    def describe_alarms(self, describe_alarms_request: DescribeAlarmsRequest) -> DescribeAlarmsResponse:
        if describe_alarms_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DESCRIBE_ALARMS, params=describe_alarms_request.get_api_input())

        return DescribeAlarmsResponse(response)

    def open_kafka_consumer(self, open_kafka_consumer_request: OpenKafkaConsumerRequest) -> OpenKafkaConsumerResponse:
        if open_kafka_consumer_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=OPEN_KAFKA_CONSUMER, body=open_kafka_consumer_request.get_api_input())

        return OpenKafkaConsumerResponse(response)

    def close_kafka_consumer(self, close_kafka_consumer_request: CloseKafkaConsumerRequest) \
            -> CloseKafkaConsumerResponse:
        if close_kafka_consumer_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=CLOSE_KAFKA_CONSUMER, body=close_kafka_consumer_request.get_api_input())

        return CloseKafkaConsumerResponse(response)

    def describe_kafka_consumer(self, describe_kafka_consumer_request: DescribeKafkaConsumerRequest) \
            -> DescribeKafkaConsumerResponse:
        if describe_kafka_consumer_request.check_validation() is False:
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DESCRIBE_KAFKA_CONSUMER, params=describe_kafka_consumer_request.get_api_input())

        return DescribeKafkaConsumerResponse(response)

    def create_consumer_group(self, create_consumer_group_request: CreateConsumerGroupRequest) \
            -> CreateConsumerGroupResponse:
        if not create_consumer_group_request.check_validation():
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=CREATE_CONSUMER_GROUP, body=create_consumer_group_request.get_api_input())

        return CreateConsumerGroupResponse(response)

    def delete_consumer_group(self, delete_consumer_group_request: DeleteConsumerGroupRequest) \
            -> DeleteConsumerGroupResponse:
        if not delete_consumer_group_request.check_validation():
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DELETE_CONSUMER_GROUP, body=delete_consumer_group_request.get_api_input())

        return DeleteConsumerGroupResponse(response)

    def modify_consumer_group(self, modify_consumer_group_request: ModifyConsumerGroupRequest) \
            -> ModifyConsumerGroupResponse:
        if not modify_consumer_group_request.check_validation():
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=MODIFY_CONSUMER_GROUP, body=modify_consumer_group_request.get_api_input())

        return ModifyConsumerGroupResponse(response)

    def describe_consumer_groups(self, describe_consumer_groups_request: DescribeConsumerGroupsRequest) \
            -> DescribeConsumerGroupsResponse:
        if not describe_consumer_groups_request.check_validation():
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=DESCRIBE_CONSUMER_GROUPS, params=describe_consumer_groups_request.get_api_input())

        return DescribeConsumerGroupsResponse(response)

    def consumer_heartbeat(self, consumer_heartbeat_request: ConsumerHeartbeatRequest) -> ConsumerHeartbeatResponse:
        if not consumer_heartbeat_request.check_validation():
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=CONSUMER_HEARTBEAT, body=consumer_heartbeat_request.get_api_input())

        return ConsumerHeartbeatResponse(response)

    def modify_checkpoint(self, modify_checkpoint_request: ModifyCheckpointRequest) -> ModifyCheckpointResponse:
        if not modify_checkpoint_request.check_validation():
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=MODIFY_CHECKPOINT, body=modify_checkpoint_request.get_api_input())

        return ModifyCheckpointResponse(response)

    def reset_checkpoint(self, reset_checkpoint_request: ResetCheckpointRequest) -> ResetCheckpointResponse:
        if not reset_checkpoint_request.check_validation():
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=RESET_CHECKPOINT, body=reset_checkpoint_request.get_api_input())

        return ResetCheckpointResponse(response)

    def describe_checkpoint(self, describe_checkpoint_request: DescribeCheckpointRequest) -> DescribeCheckpointResponse:
        if not describe_checkpoint_request.check_validation():
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        api_input = describe_checkpoint_request.get_api_input()
        response = self.__request(api=DESCRIBE_CHECKPOINT, params=api_input[PARAMS], body=api_input[BODY])

        return DescribeCheckpointResponse(response)

    def add_tags_to_resource(self, add_tags_to_resource_request: AddTagsToResourceRequest) -> AddTagsToResourceResponse:
        if not add_tags_to_resource_request.check_validation():
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=ADD_TAGS_TO_RESOURCE, body=add_tags_to_resource_request.get_api_input())

        return AddTagsToResourceResponse(response)

    def remove_tags_from_resource(self, remove_tags_from_resource_request: RemoveTagsFromResourceRequest) \
            -> RemoveTagsFromResourceResponse:
        if not remove_tags_from_resource_request.check_validation():
            raise TLSException(error_code="InvalidArgument", error_message="Invalid request, please check it")
        response = self.__request(api=REMOVE_TAGS_FROM_RESOURCE, body=remove_tags_from_resource_request.get_api_input())

        return RemoveTagsFromResourceResponse(response)
