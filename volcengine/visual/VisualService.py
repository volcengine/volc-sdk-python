# coding:utf-8
import json
import threading

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.base.Service import Service
from volcengine.ServiceInfo import ServiceInfo


class VisualService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(VisualService, "_instance"):
            with VisualService._instance_lock:
                if not hasattr(VisualService, "_instance"):
                    VisualService._instance = object.__new__(cls)
        return VisualService._instance

    def __init__(self):
        self.service_info = VisualService.get_service_info()
        self.api_info = VisualService.get_api_info()
        super(VisualService, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info():
        service_info = ServiceInfo("visual.volcengineapi.com", {},
                                   Credentials('', '', 'cv', 'cn-north-1'), 10, 10)
        return service_info

    @staticmethod
    def get_api_info():
        api_info = {
            "JPCartoonCut": ApiInfo("POST", "/", {"Action": "JPCartoonCut", "Version": "2020-08-26"}, {}, {}),
            "JPCartoon": ApiInfo("POST", "/", {"Action": "JPCartoon", "Version": "2020-08-26"}, {}, {}),
            "IDCard": ApiInfo("POST", "/", {"Action": "IDCard", "Version": "2020-08-26"}, {}, {}),
            "FaceSwap": ApiInfo("POST", "/", {"Action": "FaceSwap", "Version": "2020-08-26"}, {}, {}),
            "OCRNormal": ApiInfo("POST", "/", {"Action": "OCRNormal", "Version": "2020-08-26"}, {}, {}),
            "BankCard": ApiInfo("POST", "/", {"Action": "BankCard", "Version": "2020-08-26"}, {}, {}),
            "HumanSegment": ApiInfo("POST", "/", {"Action": "HumanSegment", "Version": "2020-08-26"}, {}, {}),
            "GeneralSegment": ApiInfo("POST", "/", {"Action": "GeneralSegment", "Version": "2020-08-26"}, {}, {}),
            "EnhancePhoto": ApiInfo("POST", "/", {"Action": "EnhancePhoto", "Version": "2020-08-26"}, {}, {}),
            "ConvertPhoto": ApiInfo("POST", "/", {"Action": "ConvertPhoto", "Version": "2020-08-26"}, {}, {}),
            "VideoSceneDetect": ApiInfo("POST", "/", {"Action": "VideoSceneDetect", "Version": "2020-08-26"}, {}, {}),
            "OverResolution": ApiInfo("POST", "/", {"Action": "OverResolution", "Version": "2020-08-26"}, {}, {}),
            "GoodsSegment": ApiInfo("POST", "/", {"Action": "GoodsSegment", "Version": "2020-08-26"}, {}, {}),
            "ImageOutpaint": ApiInfo("POST", "/", {"Action": "ImageOutpaint", "Version": "2020-08-26"}, {}, {}),
            "ImageInpaint": ApiInfo("POST", "/", {"Action": "ImageInpaint", "Version": "2020-08-26"}, {}, {}),
            "ImageCut": ApiInfo("POST", "/", {"Action": "ImageCut", "Version": "2020-08-26"}, {}, {}),
            "EntityDetect": ApiInfo("POST", "/", {"Action": "EntityDetect", "Version": "2020-08-26"}, {}, {}),
            "GoodsDetect": ApiInfo("POST", "/", {"Action": "GoodsDetect", "Version": "2020-08-26"}, {}, {}),
            "VideoSummarizationSubmitTask": ApiInfo("POST", "/", {"Action": "VideoSummarizationSubmitTask", "Version": "2020-08-26"}, {}, {}),
            "VideoSummarizationQueryTask": ApiInfo("GET", "/", {"Action": "VideoSummarizationQueryTask", "Version": "2020-08-26"}, {}, {}),
            "VideoOverResolutionSubmitTask": ApiInfo("POST", "/", {"Action": "VideoOverResolutionSubmitTask", "Version": "2020-08-26"}, {}, {}),
            "VideoOverResolutionQueryTask": ApiInfo("GET", "/", {"Action": "VideoOverResolutionQueryTask", "Version": "2020-08-26"}, {}, {}),
            "VideoRetargetingSubmitTask": ApiInfo("POST", "/", {"Action": "VideoRetargetingSubmitTask", "Version": "2020-08-26"}, {}, {}),
            "VideoRetargetingQueryTask": ApiInfo("GET", "/", {"Action": "VideoRetargetingQueryTask", "Version": "2020-08-26"}, {}, {}),
            "VideoInpaintSubmitTask": ApiInfo("POST", "/", {"Action": "VideoInpaintSubmitTask", "Version": "2020-08-26"}, {}, {}),
            "VideoInpaintQueryTask": ApiInfo("GET", "/", {"Action": "VideoInpaintQueryTask", "Version": "2020-08-26"}, {}, {}),
        }
        return api_info

    def common_handler(self, api, form):
        params = dict()
        try:
            res = self.post(api, params, form)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            res = str(e)
            try:
                res_json = json.loads(res)
                return res_json
            except:
                raise Exception(str(e))

    def common_get_handler(self, api, params):
        try:
            res = self.get(api, params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            res = str(e)
            try:
                res_json = json.loads(res)
                return res_json
            except:
                raise Exception(str(e))

    def jpcartoon_cut(self, form):
        try:
            res_json = self.common_handler("JPCartoonCut", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def jpcartoon(self, form):
        try:
            res_json = self.common_handler("JPCartoon", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def id_card(self, form):
        try:
            res_json = self.common_handler("IDCard", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def face_swap(self, form):
        try:
            res_json = self.common_handler("FaceSwap", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def ocr_normal(self, form):
        try:
            res_json = self.common_handler("OCRNormal", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def bank_card(self, form):
        try:
            res_json = self.common_handler("BankCard", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def human_segment(self, form):
        try:
            res_json = self.common_handler("HumanSegment", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def general_segment(self, form):
        try:
            res_json = self.common_handler("GeneralSegment", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def enhance_photo(self, form):
        try:
            res_json = self.common_handler("EnhancePhoto", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def convert_photo(self, form):
        try:
            res_json = self.common_handler("ConvertPhoto", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def video_scene_detect(self, form):
        try:
            res_json = self.common_handler("VideoSceneDetect", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def over_resolution(self, form):
        try:
            res_json = self.common_handler("OverResolution", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def goods_segment(self, form):
        try:
            res_json = self.common_handler("GoodsSegment", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def image_outpaint(self, form):
        try:
            res_json = self.common_handler("ImageOutpaint", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def image_inpaint(self, form):
        try:
            res_json = self.common_handler("ImageInpaint", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def image_cut(self, form):
        try:
            res_json = self.common_handler("ImageCut", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def entity_detect(self, form):
        try:
            res_json = self.common_handler("EntityDetect", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def goods_detect(self, form):
        try:
            res_json = self.common_handler("GoodsDetect", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def video_summarization_submit_task(self, form):
        try:
            res_json = self.common_handler(
                "VideoSummarizationSubmitTask", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def video_summarization_query_task(self, params):
        try:
            res_json = self.common_get_handler(
                "VideoSummarizationQueryTask", params)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def video_over_resolution_submit_task(self, form):
        try:
            res_json = self.common_handler(
                "VideoOverResolutionSubmitTask", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def video_over_resolution_query_task(self, params):
        try:
            res_json = self.common_get_handler(
                "VideoOverResolutionQueryTask", params)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def video_retargeting_submit_task(self, form):
        try:
            res_json = self.common_handler(
                "VideoRetargetingSubmitTask", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def video_retargeting_query_task(self, params):
        try:
            res_json = self.common_get_handler(
                "VideoRetargetingQueryTask", params)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def video_inpaint_submit_task(self, form):
        try:
            res_json = self.common_handler(
                "VideoInpaintSubmitTask", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def video_inpaint_query_task(self, params):
        try:
            res_json = self.common_get_handler(
                "VideoInpaintQueryTask", params)
            return res_json
        except Exception as e:
            raise Exception(str(e))
