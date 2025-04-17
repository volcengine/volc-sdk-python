import json
import threading
import redo

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo
from requests import exceptions


class RcLlmAgentService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(RcLlmAgentService, "_instance"):
            with RcLlmAgentService._instance_lock:
                if not hasattr(RcLlmAgentService, "_instance"):
                    RcLlmAgentService._instance = object.__new__(cls)
        return RcLlmAgentService._instance

    def __init__(self):
        self.service_info = RcLlmAgentService.get_service_info()
        self.api_info = RcLlmAgentService.get_api_info()
        super(RcLlmAgentService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info():
        service_info = ServiceInfo("contentservice.zijieapi.com", {'Accept': 'application/json'},
                                   Credentials('', '', 'BusinessSecurity', 'cn-north-1'), 5 * 60, 5 * 60, "https")
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            "LlmTextModeration": ApiInfo("POST", "/openapi/v1/rc_llm/text_moderation", {"Action": "LlmTextModeration", "Version": "2022-08-26"}, {}, {}),
            "AsyncLlmTextModeration": ApiInfo("POST", "/openapi/v1/rc_llm/async_text_moderation", {"Action": "AsyncLlmTextModeration", "Version": "2022-08-26"}, {}, {}),
            "GetTextModerationResult": ApiInfo("GET", "/openapi/v1/rc_llm/text_moderation_result", {"Action": "GetTextModerationResult", "Version": "2022-08-26"}, {}, {}),
            "LlmCustomizeRisk": ApiInfo("POST", "/openapi/v1/rc_llm/custom_risk", {"Action": "LlmCustomizeRisk", "Version": "2022-08-26"}, {}, {}),
            "AsyncLlmCustomizeRisk": ApiInfo("POST", "/openapi/v1/rc_llm/async_custom_risk", {"Action": "AsyncLlmCustomizeRisk", "Version": "2022-08-26"}, {}, {}),
            "GetCustomizeRiskResult": ApiInfo("GET", "/openapi/v1/rc_llm/custom_risk_result", {"Action": "GetCustomizeRiskResult", "Version": "2022-08-26"}, {},{}),
            }

        return api_info

    def set_socket_timeout(self, timeout):
        self.service_info.socket_timeout = timeout

    def set_connection_timeout(self, timeout):
        self.service_info.connection_timeout = timeout

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def llm_text_moderation(self, params, body):
        res = self.json("LlmTextModeration", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def async_llm_text_moderation(self, params, body):
        res = self.json("AsyncLlmTextModeration", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def get_text_moderation_result(self, params, body):
        res = self.get("GetTextModerationResult", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def llm_customize_risk(self, params, body):
        res = self.json("LlmCustomizeRisk", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def async_llm_customize_risk(self, params, body):
        res = self.json("AsyncLlmCustomizeRisk", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def get_customize_risk_result(self, params, body):
        res = self.get("GetCustomizeRiskResult", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
