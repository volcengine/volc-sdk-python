# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import hashlib
import logging
import threading

from requests.adapters import HTTPAdapter, Retry

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.auth.SignerV4 import SignerV4
from volcengine.base.Service import Service
from volcengine.tls.tls_requests import *
from volcengine.tls.tls_responses import *
from volcengine.tls.tls_exception import TLSException

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s \t %(levelname)s \t %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

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
    DESCRIBE_KAFKA_CONSUMER: ApiInfo(HTTP_GET, DESCRIBE_KAFKA_CONSUMER, {}, {}, {})}


class TLSService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(TLSService, "_instance"):
            with TLSService._instance_lock:
                if not hasattr(TLSService, "_instance"):
                    TLSService._instance = object.__new__(cls)

        return TLSService._instance

    def __init__(self, endpoint: str, access_key_id: str, access_key_secret: str, region: str,
                 security_token: str = None, scheme: str = "https", timeout: int = 60, max_retries: int = 10):
        self.__endpoint = endpoint
        self.__access_key_id = access_key_id
        self.__access_key_secret = access_key_secret
        self.__region = region
        self.__security_token = security_token
        self.__scheme = scheme
        self.__timeout = timeout

        super(TLSService, self).__init__(service_info=self.get_service_info(), api_info=API_INFO)

        self.__retry_strategy = Retry(total=max_retries, connect=max_retries, read=max_retries, status=max_retries,
                                      allowed_methods=frozenset([HTTP_GET]),
                                      status_forcelist=frozenset([429, 500, 502, 503, 504, 505]),
                                      backoff_factor=1, raise_on_redirect=False, raise_on_status=False)
        self.__http_adapter = HTTPAdapter(max_retries=self.__retry_strategy)
        self.session.mount(HTTP_PREFIX, self.__http_adapter)
        self.session.mount(HTTPS_PREFIX, self.__http_adapter)

        logging.info("Successfully initialized a TLS client.\n")

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
        logging.info("Requesting {}...\tParams = {}\tBody = {}".format(api, params, body))

        request = self.__prepare_request(api, params, body, request_headers)

        method = self.api_info[api].method
        url = request.build()

        try:
            response = self.session.request(method, url, headers=request.headers, data=request.body,
                                            timeout=self.__timeout)
        except Exception as e:
            raise TLSException(error_code=e.__class__.__name__, error_message=e.__str__())
        else:
            if response.status_code != OK_STATUS:
                raise TLSException(response)

            logging.info("Successfully got a response from TLS!\n")

            return response

    def reset_access_key_token(self, access_key_id: str, access_key_secret: str, security_token: str = None):
        self.__access_key_id = access_key_id
        self.__access_key_secret = access_key_secret
        self.__security_token = security_token
        self.service_info = self.get_service_info()

    def set_timeout(self, timeout: int):
        self.__timeout = timeout
        self.service_info = self.get_service_info()

    def create_project(self, create_project_request: CreateProjectRequest) -> CreateProjectResponse:
        response = self.__request(api=CREATE_PROJECT, body=create_project_request.get_api_input())

        return CreateProjectResponse(response)

    def delete_project(self, delete_project_request: DeleteProjectRequest) -> DeleteProjectResponse:
        response = self.__request(api=DELETE_PROJECT, body=delete_project_request.get_api_input())

        return DeleteProjectResponse(response)

    def modify_project(self, modify_project_request: ModifyProjectRequest) -> ModifyProjectResponse:
        response = self.__request(api=MODIFY_PROJECT, body=modify_project_request.get_api_input())

        return ModifyProjectResponse(response)

    def describe_project(self, describe_project_request: DescribeProjectRequest) -> DescribeProjectResponse:
        response = self.__request(api=DESCRIBE_PROJECT, params=describe_project_request.get_api_input())

        return DescribeProjectResponse(response)

    def describe_projects(self, describe_projects_request: DescribeProjectsRequest) -> DescribeProjectsResponse:
        response = self.__request(api=DESCRIBE_PROJECTS, params=describe_projects_request.get_api_input())

        return DescribeProjectsResponse(response)

    def create_topic(self, create_topic_request: CreateTopicRequest) -> CreateTopicResponse:
        response = self.__request(api=CREATE_TOPIC, body=create_topic_request.get_api_input())

        return CreateTopicResponse(response)

    def delete_topic(self, delete_topic_request: DeleteTopicRequest) -> DeleteTopicResponse:
        response = self.__request(api=DELETE_TOPIC, body=delete_topic_request.get_api_input())

        return DeleteTopicResponse(response)

    def modify_topic(self, modify_topic_request: ModifyTopicRequest) -> ModifyTopicResponse:
        response = self.__request(api=MODIFY_TOPIC, body=modify_topic_request.get_api_input())

        return ModifyTopicResponse(response)

    def describe_topic(self, describe_topic_request: DescribeTopicRequest) -> DescribeTopicResponse:
        response = self.__request(api=DESCRIBE_TOPIC, params=describe_topic_request.get_api_input())

        return DescribeTopicResponse(response)

    def describe_topics(self, describe_topics_request: DescribeTopicsRequest) -> DescribeTopicsResponse:
        response = self.__request(api=DESCRIBE_TOPICS, params=describe_topics_request.get_api_input())

        return DescribeTopicsResponse(response)

    def create_index(self, create_index_request: CreateIndexRequest) -> CreateIndexResponse:
        response = self.__request(api=CREATE_INDEX, body=create_index_request.get_api_input())

        return CreateIndexResponse(response)

    def delete_index(self, delete_index_request: DeleteIndexRequest) -> DeleteIndexResponse:
        response = self.__request(api=DELETE_INDEX, body=delete_index_request.get_api_input())

        return DeleteIndexResponse(response)

    def modify_index(self, modify_index_request: ModifyIndexRequest) -> ModifyIndexResponse:
        response = self.__request(api=MODIFY_INDEX, body=modify_index_request.get_api_input())

        return ModifyIndexResponse(response)

    def describe_index(self, describe_index_request: DescribeIndexRequest) -> DescribeIndexResponse:
        response = self.__request(api=DESCRIBE_INDEX, params=describe_index_request.get_api_input())

        return DescribeIndexResponse(response)

    def put_logs(self, put_logs_request: PutLogsRequest) -> PutLogsResponse:
        api_input = put_logs_request.get_api_input()
        response = self.__request(api=PUT_LOGS, params=api_input[PARAMS], body=api_input[BODY],
                                  request_headers=api_input[REQUEST_HEADERS])

        return PutLogsResponse(response)

    def describe_cursor(self, describe_cursor_request: DescribeCursorRequest) -> DescribeCursorResponse:
        api_input = describe_cursor_request.get_api_input()
        response = self.__request(api=DESCRIBE_CURSOR, params=api_input[PARAMS], body=api_input[BODY])

        return DescribeCursorResponse(response)

    def consume_logs(self, consume_logs_request: ConsumeLogsRequest) -> ConsumeLogsResponse:
        api_input = consume_logs_request.get_api_input()
        response = self.__request(api=CONSUME_LOGS, params=api_input[PARAMS], body=api_input[BODY])

        return ConsumeLogsResponse(response, compression=consume_logs_request.compression)

    def search_logs(self, search_logs_request: SearchLogsRequest) -> SearchLogsResponse:
        response = self.__request(api=SEARCH_LOGS, body=search_logs_request.get_api_input())

        return SearchLogsResponse(response)

    def describe_log_context(self, describe_log_context_request: DescribeLogContextRequest) \
            -> DescribeLogContextResponse:
        response = self.__request(api=DESCRIBE_LOG_CONTEXT, body=describe_log_context_request.get_api_input())

        return DescribeLogContextResponse(response)

    def web_tracks(self, web_tracks_request: WebTracksRequest) -> WebTracksResponse:
        api_input = web_tracks_request.get_api_input()
        response = self.__request(api=WEB_TRACKS, params=api_input[PARAMS], body=api_input[BODY],
                                  request_headers=api_input[REQUEST_HEADERS])

        return WebTracksResponse(response)

    def describe_histogram(self, describe_histogram_request: DescribeHistogramRequest) -> DescribeHistogramResponse:
        response = self.__request(api=DESCRIBE_HISTOGRAM, body=describe_histogram_request.get_api_input())

        return DescribeHistogramResponse(response)

    def create_download_task(self, create_download_task_request: CreateDownloadTaskRequest) \
            -> CreateDownloadTaskResponse:
        response = self.__request(api=CREATE_DOWNLOAD_TASK, body=create_download_task_request.get_api_input())

        return CreateDownloadTaskResponse(response)

    def describe_download_tasks(self, describe_download_tasks_request: DescribeDownloadTasksRequest) \
            -> DescribeDownloadTasksResponse:
        response = self.__request(api=DESCRIBE_DOWNLOAD_TASKS, params=describe_download_tasks_request.get_api_input())

        return DescribeDownloadTasksResponse(response)

    def describe_download_url(self, describe_download_url_request: DescribeDownloadUrlRequest)\
            -> DescribeDownloadUrlResponse:
        response = self.__request(api=DESCRIBE_DOWNLOAD_URL, params=describe_download_url_request.get_api_input())

        return DescribeDownloadUrlResponse(response)

    def describe_shards(self, describe_shards_request: DescribeShardsRequest) -> DescribeShardsResponse:
        response = self.__request(api=DESCRIBE_SHARDS, params=describe_shards_request.get_api_input())

        return DescribeShardsResponse(response)

    def create_host_group(self, create_host_group_request: CreateHostGroupRequest) -> CreateHostGroupResponse:
        response = self.__request(api=CREATE_HOST_GROUP, body=create_host_group_request.get_api_input())

        return CreateHostGroupResponse(response)

    def delete_host_group(self, delete_host_group_request: DeleteHostGroupRequest) -> DeleteHostGroupResponse:
        response = self.__request(api=DELETE_HOST_GROUP, body=delete_host_group_request.get_api_input())

        return DeleteHostGroupResponse(response)

    def modify_host_group(self, modify_host_group_request: ModifyHostGroupRequest) -> ModifyHostGroupResponse:
        response = self.__request(api=MODIFY_HOST_GROUP, body=modify_host_group_request.get_api_input())

        return ModifyHostGroupResponse(response)

    def describe_host_group(self, describe_host_group_request: DescribeHostGroupRequest) -> DescribeHostGroupResponse:
        response = self.__request(api=DESCRIBE_HOST_GROUP, params=describe_host_group_request.get_api_input())

        return DescribeHostGroupResponse(response)

    def describe_host_groups(self, describe_host_groups_request: DescribeHostGroupsRequest) \
            -> DescribeHostGroupsResponse:
        response = self.__request(api=DESCRIBE_HOST_GROUPS, params=describe_host_groups_request.get_api_input())

        return DescribeHostGroupsResponse(response)

    def describe_hosts(self, describe_hosts_request: DescribeHostsRequest) -> DescribeHostsResponse:
        response = self.__request(api=DESCRIBE_HOSTS, params=describe_hosts_request.get_api_input())

        return DescribeHostsResponse(response)

    def delete_host(self, delete_host_request: DeleteHostRequest) -> DeleteHostResponse:
        response = self.__request(api=DELETE_HOST, body=delete_host_request.get_api_input())

        return DeleteHostResponse(response)

    def describe_host_group_rules(self, describe_host_group_rules: DescribeHostGroupRulesRequest) \
            -> DescribeHostGroupRulesResponse:
        response = self.__request(api=DESCRIBE_HOST_GROUP_RULES, params=describe_host_group_rules.get_api_input())

        return DescribeHostGroupRulesResponse(response)

    def modify_host_groups_auto_update(self, modify_host_groups_auto_update_request: ModifyHostGroupsAutoUpdateRequest)\
            -> ModifyHostGroupsAutoUpdateResponse:
        response = self.__request(api=MODIFY_HOST_GROUPS_AUTO_UPDATE,
                                  body=modify_host_groups_auto_update_request.get_api_input())

        return ModifyHostGroupsAutoUpdateResponse(response)

    def create_rule(self, create_rule_request: CreateRuleRequest) -> CreateRuleResponse:
        response = self.__request(api=CREATE_RULE, body=create_rule_request.get_api_input())

        return CreateRuleResponse(response)

    def delete_rule(self, delete_rule_request: DeleteRuleRequest) -> DeleteRuleResponse:
        response = self.__request(api=DELETE_RULE, body=delete_rule_request.get_api_input())

        return DeleteRuleResponse(response)

    def modify_rule(self, modify_rule_request: ModifyRuleRequest) -> ModifyRuleResponse:
        response = self.__request(api=MODIFY_RULE, body=modify_rule_request.get_api_input())

        return ModifyRuleResponse(response)

    def describe_rule(self, describe_rule_request: DescribeRuleRequest) -> DescribeRuleResponse:
        response = self.__request(api=DESCRIBE_RULE, params=describe_rule_request.get_api_input())

        return DescribeRuleResponse(response)

    def describe_rules(self, describe_rules_request: DescribeRulesRequest) -> DescribeRulesResponse:
        response = self.__request(api=DESCRIBE_RULES, params=describe_rules_request.get_api_input())

        return DescribeRulesResponse(response)

    def apply_rule_to_host_groups(self, apply_rule_to_host_groups_request: ApplyRuleToHostGroupsRequest) \
            -> ApplyRuleToHostGroupsResponse:
        response = self.__request(api=APPLY_RULE_TO_HOST_GROUPS, body=apply_rule_to_host_groups_request.get_api_input())

        return ApplyRuleToHostGroupsResponse(response)

    def delete_rule_from_host_groups(self, delete_rule_from_host_groups_request: DeleteRuleFromHostGroupsRequest) \
            -> DeleteRuleFromHostGroupsResponse:
        response = self.__request(api=DELETE_RULE_FROM_HOST_GROUPS,
                                  body=delete_rule_from_host_groups_request.get_api_input())

        return DeleteRuleFromHostGroupsResponse(response)

    def create_alarm_notify_group(self, create_alarm_notify_group_request: CreateAlarmNotifyGroupRequest) \
            -> CreateAlarmNotifyGroupResponse:
        response = self.__request(api=CREATE_ALARM_NOTIFY_GROUP, body=create_alarm_notify_group_request.get_api_input())

        return CreateAlarmNotifyGroupResponse(response)

    def delete_alarm_notify_group(self, delete_alarm_notify_group_request: DeleteAlarmNotifyGroupRequest) \
            -> DeleteAlarmNotifyGroupResponse:
        response = self.__request(api=DELETE_ALARM_NOTIFY_GROUP, body=delete_alarm_notify_group_request.get_api_input())

        return DeleteAlarmNotifyGroupResponse(response)

    def modify_alarm_notify_group(self, modify_alarm_notify_group: ModifyAlarmNotifyGroupRequest) \
            -> ModifyAlarmNotifyGroupResponse:
        response = self.__request(api=MODIFY_ALARM_NOTIFY_GROUP, body=modify_alarm_notify_group.get_api_input())

        return ModifyAlarmNotifyGroupResponse(response)

    def describe_alarm_notify_groups(self, describe_alarm_notify_groups: DescribeAlarmNotifyGroupsRequest) \
            -> DescribeAlarmNotifyGroupsResponse:
        response = self.__request(api=DESCRIBE_ALARM_NOTIFY_GROUPS, params=describe_alarm_notify_groups.get_api_input())

        return DescribeAlarmNotifyGroupsResponse(response)

    def create_alarm(self, create_alarm_request: CreateAlarmRequest) -> CreateAlarmResponse:
        response = self.__request(api=CREATE_ALARM, body=create_alarm_request.get_api_input())

        return CreateAlarmResponse(response)

    def delete_alarm(self, delete_alarm_request: DeleteAlarmRequest) -> DeleteAlarmResponse:
        response = self.__request(api=DELETE_ALARM, body=delete_alarm_request.get_api_input())

        return DeleteAlarmResponse(response)

    def modify_alarm(self, modify_alarm_request: ModifyAlarmRequest) -> ModifyAlarmResponse:
        response = self.__request(api=MODIFY_ALARM, body=modify_alarm_request.get_api_input())

        return ModifyAlarmResponse(response)

    def describe_alarms(self, describe_alarms_request: DescribeAlarmsRequest) -> DescribeAlarmsResponse:
        response = self.__request(api=DESCRIBE_ALARMS, params=describe_alarms_request.get_api_input())

        return DescribeAlarmsResponse(response)

    def open_kafka_consumer(self, open_kafka_consumer_request: OpenKafkaConsumerRequest) -> OpenKafkaConsumerResponse:
        response = self.__request(api=OPEN_KAFKA_CONSUMER, body=open_kafka_consumer_request.get_api_input())

        return OpenKafkaConsumerResponse(response)

    def close_kafka_consumer(self, close_kafka_consumer_request: CloseKafkaConsumerRequest) \
            -> CloseKafkaConsumerResponse:
        response = self.__request(api=CLOSE_KAFKA_CONSUMER, body=close_kafka_consumer_request.get_api_input())

        return CloseKafkaConsumerResponse(response)

    def describe_kafka_consumer(self, describe_kafka_consumer_request: DescribeKafkaConsumerRequest)\
            -> DescribeKafkaConsumerResponse:
        response = self.__request(api=DESCRIBE_KAFKA_CONSUMER, params=describe_kafka_consumer_request.get_api_input())

        return DescribeKafkaConsumerResponse(response)
