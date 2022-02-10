import json
import threading
import redo

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo
from requests import exceptions


class ContentSecurityService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(ContentSecurityService, "_instance"):
            with ContentSecurityService._instance_lock:
                if not hasattr(ContentSecurityService, "_instance"):
                    ContentSecurityService._instance = object.__new__(cls)
        return ContentSecurityService._instance

    def __init__(self):
        self.service_info = ContentSecurityService.get_service_info()
        self.api_info = ContentSecurityService.get_api_info()
        super(ContentSecurityService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info():
        service_info = ServiceInfo("open.volcengineapi.com", {'Accept': 'application/json'},
                                   Credentials('', '', 'BusinessSecurity', 'cn-north-1'), 5, 5)
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {"AsyncVideoRisk": ApiInfo("POST", "/", {"Action": "AsyncVideoRisk", "Version": "2021-11-29"}, {}, {}),
                    "VideoResult": ApiInfo("GET", "/", {"Action": "VideoResult", "Version": "2021-11-29"}, {}, {}),
                    "ImageContentRisk": ApiInfo("POST", "/", {"Action": "ImageContentRisk", "Version": "2021-11-29"}, {}, {}),
                    "AsyncImageRisk": ApiInfo("POST", "/", {"Action": "AsyncImageRisk", "Version": "2021-11-29"}, {}, {}),
                    "ImageResult": ApiInfo("GET", "/", {"Action": "GetImageResult", "Version": "2021-11-29"}, {}, {}),
                    "TextRisk": ApiInfo("POST", "/", {"Action": "TextRisk", "Version": "2022-01-26"}, {}, {}),
                    "CreateCustomContents": ApiInfo("POST", "/", {"Action": "CreateCustomContents", "Version": "2022-01-22"}, {}, {}),
                    "UploadCustomContents": ApiInfo("POST", "/", {"Action": "UploadCustomContents", "Version": "2022-02-07"}, {}, {})
                    }

        return api_info

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def async_video_risk(self, params, body):
        res = self.json("AsyncVideoRisk", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def video_result(self, params, body):
        res = self.get("VideoResult", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def image_content_risk(self, params, body):
        res = self.json("ImageContentRisk", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def async_image_risk(self, params, body):
        res = self.json("AsyncImageRisk", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def image_result(self, params, body):
        res = self.get("ImageResult", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def text_risk(self, params, body):
        res = self.json("TextRisk", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def create_custom_contents(self, params, body):
        res = self.json("CreateCustomContents", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def upload_custom_contents(self, params, body):
        res = self.json("UploadCustomContents", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
