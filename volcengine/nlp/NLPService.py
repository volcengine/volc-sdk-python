# coding:utf-8
import json
import threading

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo


class NLPService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(NLPService, "_instance"):
            with NLPService._instance_lock:
                if not hasattr(NLPService, "_instance"):
                    NLPService._instance = object.__new__(cls)
        return NLPService._instance

    def __init__(self):
        self.service_info = NLPService.get_service_info()
        self.api_info = NLPService.get_api_info()
        super(NLPService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info():
        service_info = ServiceInfo("open.volcengineapi.com", {},
                                   Credentials('', '', 'nlp_gateway', 'cn-north-1'), 10, 10)
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            "KeyphraseExtractionExtract": ApiInfo("POST", "/", {"Action": "KeyphraseExtractionExtract", "Version": "2020-09-01"}, {}, {}),
            "TextCorrectionZhCorrect": ApiInfo("POST", "/", {"Action": "TextCorrectionZhCorrect", "Version": "2020-09-01"}, {}, {}),
            "TextCorrectionEnCorrect": ApiInfo("POST", "/", {"Action": "TextCorrectionEnCorrect", "Version": "2020-09-01"}, {}, {}),
            "SentimentAnalysis": ApiInfo("POST", "/", {"Action": "SentimentAnalysis", "Version": "2020-12-01"}, {}, {}),
            "TextSummarization": ApiInfo("POST", "/", {"Action": "TextSummarization", "Version": "2020-12-01"}, {}, {}),
            "EssayAutoGrade": ApiInfo("POST", "/", {"Action": "EssayAutoGrade", "Version": "2021-05-20"}, {}, {}),
            "NovelCorrection": ApiInfo("POST", "/", {"Action": "NovelCorrection", "Version": "2021-07-22"}, {}, {}),
        }
        return api_info

    def common_json_handler(self, api, body):
        params = dict()
        try:
            body = json.dumps(body)
            res = self.json(api, params, body)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            res = str(e)
            try:
                res_json = json.loads(res)
                return res_json
            except:
                raise Exception(str(e))

    def keyphrase_extraction_extract(self, body):
        try:
            res_json = self.common_json_handler("KeyphraseExtractionExtract", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def text_correction_zh_correct(self, body):
        try:
            res_json = self.common_json_handler("TextCorrectionZhCorrect", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def text_correction_en_correct(self, body):
        try:
            res_json = self.common_json_handler("TextCorrectionEnCorrect", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def sentiment_analysis(self, body):
        try:
            res_json = self.common_json_handler("SentimentAnalysis", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def text_summarization(self, body):
        try:
            res_json = self.common_json_handler("TextSummarization", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def essay_auto_grade(self, body):
        try:
            res_json = self.common_json_handler("EssayAutoGrade", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def novel_correction(self, body):
        try:
            res_json = self.common_json_handler("NovelCorrection", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))
