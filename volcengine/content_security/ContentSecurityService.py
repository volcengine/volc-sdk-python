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

    def set_socket_timeout(self, timeout):
        self.service_info.socket_timeout = timeout

    def set_connection_timeout(self, timeout):
        self.service_info.connection_timeout = timeout

    @staticmethod
    def get_api_info():
        api_info = {"AsyncVideoRisk": ApiInfo("POST", "/", {"Action": "AsyncVideoRisk", "Version": "2021-11-29"}, {}, {}),
                    "VideoResult": ApiInfo("GET", "/", {"Action": "VideoResult", "Version": "2021-11-29"}, {}, {}),
                    "ImageContentRisk": ApiInfo("POST", "/", {"Action": "ImageContentRisk", "Version": "2021-11-29"}, {}, {}),
                    "ImageContentRiskV2": ApiInfo("POST", "/", {"Action": "ImageContentRiskV2", "Version": "2021-11-29"}, {}, {}),
                    "AsyncImageRisk": ApiInfo("POST", "/", {"Action": "AsyncImageRisk", "Version": "2021-11-29"}, {}, {}),
                    "ImageResult": ApiInfo("GET", "/", {"Action": "GetImageResult", "Version": "2021-11-29"}, {}, {}),
                    "TextRisk": ApiInfo("POST", "/", {"Action": "TextRisk", "Version": "2022-01-26"}, {}, {}),
                    "CreateCustomContents": ApiInfo("POST", "/", {"Action": "CreateCustomContents", "Version": "2022-01-22"}, {}, {}),
                    "UploadCustomContents": ApiInfo("POST", "/", {"Action": "UploadCustomContents", "Version": "2022-02-07"}, {}, {}),
                    "EnableCustomContents": ApiInfo("PUT", "/", {"Action": "EnableCustomContents", "Version": "2022-04-28"}, {}, {}),
                    "DisableCustomContents": ApiInfo("PUT", "/", {"Action": "DisableCustomContents", "Version": "2022-04-28"}, {}, {}),
                    "DeleteCustomContents": ApiInfo("PUT", "/", {"Action": "DeleteCustomContents", "Version": "2022-04-28"}, {}, {}),
                    "AsyncAudioRisk": ApiInfo("POST", "/", {"Action": "AsyncAudioRisk", "Version": "2022-04-01"}, {}, {}),
                    "GetAudioResult": ApiInfo("GET", "/", {"Action": "GetAudioResult", "Version": "2022-04-01"}, {}, {}),
                    "AudioRisk": ApiInfo("POST", "/", {"Action": "AudioRisk", "Version": "2022-04-01"}, {}, {}),
                    "AsyncLiveVideoRisk": ApiInfo("POST", "/", {"Action": "AsyncLiveVideoRisk", "Version": "2022-04-25"}, {}, {}),
                    "GetVideoLiveResult": ApiInfo("GET", "/", {"Action": "GetVideoLiveResult", "Version": "2022-04-25"}, {}, {}),
                    "AsyncLiveAudioRisk": ApiInfo("POST", "/", {"Action": "AsyncLiveAudioRisk", "Version": "2022-04-25"}, {}, {}),
                    "GetAudioLiveResult": ApiInfo("GET", "/", {"Action": "GetAudioLiveResult", "Version": "2022-04-25"}, {}, {}),
                    "TextSliceRisk": ApiInfo("POST", "/", {"Action": "TextSliceRisk", "Version": "2022-11-07"}, {}, {}),
                    "AsyncImageRiskV2": ApiInfo("POST", "/", {"Action": "AsyncImageRisk", "Version": "2022-08-26"}, {}, {}),
                    "ImageResultV2": ApiInfo("GET", "/", {"Action": "ImageResult", "Version": "2022-08-26"}, {}, {}),
                    "CloseAudioLiveRisk": ApiInfo("POST", "/", {"Action": "CloseAudioLive", "Version": "2022-04-25"}, {}, {}),
                    "CloseVideoLiveRisk": ApiInfo("POST", "/", {"Action": "CloseVideoLive", "Version": "2022-04-25"}, {}, {}),
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

    # deprecated, use image_content_risk_v2 instead
    def image_content_risk(self, params, body):
        res = self.json("ImageContentRisk", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def image_content_risk_v2(self, params, body):
        res = self.json("ImageContentRiskV2", params, json.dumps(body))
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
    def async_image_risk_v2(self, params, body):
        res = self.json("AsyncImageRiskV2", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    def image_result_v2(self, params, body):
        res = self.get("ImageResultV2", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json


    @redo.retriable(sleeptime=0.1, jitter=0.01, attempts=2,
                    retry_exceptions=(exceptions.ConnectionError, exceptions.ConnectTimeout))
    # deprecated, use text_slice_risk instead
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

    def enable_custom_contents(self, params, body):
        res = self.json("EnableCustomContents", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def disable_custom_contents(self, params, body):
        res = self.json("DisableCustomContents", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def delete_custom_contents(self, params, body):
        res = self.json("DeleteCustomContents", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def async_live_video_risk(self, params, body):
        res = self.json("AsyncLiveVideoRisk", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def async_audio_risk(self, params, body):
        res = self.json("AsyncAudioRisk", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def audio_result(self, params, body):
        res = self.get("GetAudioResult", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def audio_risk(self, params, body):
        res = self.json("AudioRisk", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def async_live_audio_risk(self, params, body):
        res = self.json("AsyncLiveAudioRisk", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def live_audio_result(self, params, body):
        res = self.get("GetAudioLiveResult", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def live_video_result(self, params, body):
        res = self.get("GetVideoLiveResult", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def text_slice_risk(self, params, body):
        res = self.json("TextSliceRisk", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def close_video_live_risk(self, params, body):
        res = self.json("CloseVideoLiveRisk", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json

    def close_audio_live_risk(self, params, body):
        res = self.json("CloseAudioLiveRisk", params, json.dumps(body))
        if res == '':
            raise Exception("empty response")
        res_json = json.loads(res)
        return res_json
