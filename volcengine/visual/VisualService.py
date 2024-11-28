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
                                   Credentials('', '', 'cv', 'cn-north-1'), 30, 30)
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
            "ConvertPhotoV2": ApiInfo("POST", "/", {"Action": "ConvertPhotoV2", "Version": "2022-08-31"}, {}, {}),
            "VideoSceneDetect": ApiInfo("POST", "/", {"Action": "VideoSceneDetect", "Version": "2020-08-26"}, {}, {}),
            "OverResolution": ApiInfo("POST", "/", {"Action": "OverResolution", "Version": "2020-08-26"}, {}, {}),
            "GoodsSegment": ApiInfo("POST", "/", {"Action": "GoodsSegment", "Version": "2020-08-26"}, {}, {}),
            "ImageOutpaint": ApiInfo("POST", "/", {"Action": "ImageOutpaint", "Version": "2020-08-26"}, {}, {}),
            "ImageInpaint": ApiInfo("POST", "/", {"Action": "ImageInpaint", "Version": "2020-08-26"}, {}, {}),
            "ImageCut": ApiInfo("POST", "/", {"Action": "ImageCut", "Version": "2020-08-26"}, {}, {}),
            "EntityDetect": ApiInfo("POST", "/", {"Action": "EntityDetect", "Version": "2020-08-26"}, {}, {}),
            "GoodsDetect": ApiInfo("POST", "/", {"Action": "GoodsDetect", "Version": "2020-08-26"}, {}, {}),
            "VideoSummarizationSubmitTask": ApiInfo("POST", "/",{"Action": "VideoSummarizationSubmitTask", "Version": "2020-08-26"},{}, {}),
            "VideoSummarizationQueryTask": ApiInfo("GET", "/",{"Action": "VideoSummarizationQueryTask", "Version": "2020-08-26"},{}, {}),
            "VideoOverResolutionSubmitTask": ApiInfo("POST", "/", {"Action": "VideoOverResolutionSubmitTask","Version": "2020-08-26"}, {}, {}),
            "VideoOverResolutionQueryTask": ApiInfo("GET", "/",{"Action": "VideoOverResolutionQueryTask", "Version": "2020-08-26"},{}, {}),
            "VideoRetargetingSubmitTask": ApiInfo("POST", "/",{"Action": "VideoRetargetingSubmitTask", "Version": "2020-08-26"}, {},{}),
            "VideoRetargetingQueryTask": ApiInfo("GET", "/",{"Action": "VideoRetargetingQueryTask", "Version": "2020-08-26"}, {},{}),
            "VideoInpaintSubmitTask": ApiInfo("POST", "/",{"Action": "VideoInpaintSubmitTask", "Version": "2020-08-26"}, {}, {}),
            "VideoInpaintQueryTask": ApiInfo("GET", "/", {"Action": "VideoInpaintQueryTask", "Version": "2020-08-26"},{}, {}),
            "CarPlateDetection": ApiInfo("POST", "/", {"Action": "CarPlateDetection", "Version": "2020-08-26"}, {}, {}),
            "DistortionFree": ApiInfo("POST", "/", {"Action": "DistortionFree", "Version": "2020-08-26"}, {}, {}),
            "StretchRecovery": ApiInfo("POST", "/", {"Action": "StretchRecovery", "Version": "2020-08-26"}, {}, {}),
            "ImageFlow": ApiInfo("POST", "/", {"Action": "ImageFlow", "Version": "2020-08-26"}, {}, {}),
            "ImageScore": ApiInfo("POST", "/", {"Action": "ImageScore", "Version": "2020-08-26"}, {}, {}),
            "PoemMaterial": ApiInfo("POST", "/", {"Action": "PoemMaterial", "Version": "2020-08-26"}, {}, {}),
            "EmoticonEdit": ApiInfo("POST", "/", {"Action": "EmoticonEdit", "Version": "2020-08-26"}, {}, {}),
            "EyeClose2Open": ApiInfo("POST", "/", {"Action": "EyeClose2Open", "Version": "2020-08-26"}, {}, {}),
            "CarSegment": ApiInfo("POST", "/", {"Action": "CarSegment", "Version": "2020-08-26"}, {}, {}),
            "CarDetection": ApiInfo("POST", "/", {"Action": "CarDetection", "Version": "2020-08-26"}, {}, {}),
            "SkySegment": ApiInfo("POST", "/", {"Action": "SkySegment", "Version": "2020-08-26"}, {}, {}),
            "ImageSearchImageAdd": ApiInfo("POST", "/", {"Action": "ImageSearchImageAdd", "Version": "2020-08-26"}, {},{}),
            "ImageSearchImageDelete": ApiInfo("POST", "/",{"Action": "ImageSearchImageDelete", "Version": "2020-08-26"}, {}, {}),
            "ImageSearchImageSearch": ApiInfo("POST", "/",{"Action": "ImageSearchImageSearch", "Version": "2020-08-26"}, {}, {}),
            "ProductSearchAddImage": ApiInfo("POST", "/", {"Action": "ProductSearchAddImage", "Version": "2022-06-16"},{}, {}),
            "ProductSearchDeleteImage": ApiInfo("POST", "/",{"Action": "ProductSearchDeleteImage", "Version": "2022-06-16"}, {},{}),
            "ProductSearchSearchImage": ApiInfo("POST", "/",{"Action": "ProductSearchSearchImage", "Version": "2022-06-16"}, {},{}),
            "ClueLicense": ApiInfo("POST", "/", {"Action": "OcrClueLicense", "Version": "2020-08-26"}, {}, {}),
            "DrivingLicense": ApiInfo("POST", "/", {"Action": "DrivingLicense", "Version": "2020-08-26"}, {}, {}),
            "VehicleLicense": ApiInfo("POST", "/", {"Action": "VehicleLicense", "Version": "2020-08-26"}, {}, {}),
            "TaxiInvoice": ApiInfo("POST", "/", {"Action": "OcrTaxiInvoice", "Version": "2020-08-26"}, {}, {}),
            "TrainTicket": ApiInfo("POST", "/", {"Action": "OcrTrainTicket", "Version": "2020-08-26"}, {}, {}),
            "FlightInvoice": ApiInfo("POST", "/", {"Action": "OcrFlightInvoice", "Version": "2020-08-26"}, {}, {}),
            "VatInvoice": ApiInfo("POST", "/", {"Action": "OcrVatInvoice", "Version": "2020-08-26"}, {}, {}),
            "QuotaInvoice": ApiInfo("POST", "/", {"Action": "OcrQuotaInvoice", "Version": "2020-08-26"}, {}, {}),
            "HairStyle": ApiInfo("POST", "/", {"Action": "HairStyle", "Version": "2020-08-26"}, {}, {}),
            "HairStyleV2": ApiInfo("POST", "/", {"Action": "HairStyle", "Version": "2022-08-31"}, {}, {}),
            "FacePretty": ApiInfo("POST", "/", {"Action": "FacePretty", "Version": "2020-08-26"}, {}, {}),
            "ImageAnimation": ApiInfo("POST", "/", {"Action": "ImageAnimation", "Version": "2020-08-26"}, {}, {}),
            "CoverVideo": ApiInfo("POST", "/", {"Action": "CoverVideo", "Version": "2020-08-26"}, {}, {}),
            "DollyZoom": ApiInfo("POST", "/", {"Action": "DollyZoom", "Version": "2020-08-26"}, {}, {}),
            "Img2Video3D": ApiInfo("POST", "/", {"Action": "Img2Video3D", "Version": "2022-08-31"}, {}, {}),
            "PotraitEffect": ApiInfo("POST", "/", {"Action": "PotraitEffect", "Version": "2020-08-26"}, {}, {}),
            "ImageStyleConversion": ApiInfo("POST", "/", {"Action": "ImageStyleConversion", "Version": "2020-08-26"},{}, {}),
            "3DGameCartoon": ApiInfo("POST", "/", {"Action": "3DGameCartoon", "Version": "2020-08-26"}, {}, {}),
            "HairSegment": ApiInfo("POST", "/", {"Action": "HairSegment", "Version": "2020-08-26"}, {}, {}),
            "OcrSeal": ApiInfo("POST", "/", {"Action": "OcrSeal", "Version": "2021-08-23"}, {}, {}),
            "OcrPassInvoice": ApiInfo("POST", "/", {"Action": "OcrPassInvoice", "Version": "2021-08-23"}, {}, {}),
            "OCRTrade": ApiInfo("POST", "/", {"Action": "OCRTrade", "Version": "2020-12-21"}, {}, {}),
            "OCRRuanzhu": ApiInfo("POST", "/", {"Action": "OCRRuanzhu", "Version": "2020-12-21"}, {}, {}),
            "OCRCosmeticProduct": ApiInfo("POST", "/", {"Action": "OCRCosmeticProduct", "Version": "2020-12-21"}, {},{}),
            "OCRPdf": ApiInfo("POST", "/", {"Action": "OCRPdf", "Version": "2021-08-23"}, {}, {}),
            "OCRTable": ApiInfo("POST", "/", {"Action": "OCRTable", "Version": "2021-08-23"}, {}, {}),
            "VideoCoverSelection": ApiInfo("POST", "/", {"Action": "VideoCoverSelection", "Version": "2020-08-26"}, {},{}),
            "VideoHighlightExtractionSubmitTask": ApiInfo("POST", "/", {"Action": "VideoHighlightExtractionSubmitTask","Version": "2020-08-26"}, {}, {}),
            "VideoHighlightExtractionQueryTask": ApiInfo("GET", "/", {"Action": "VideoHighlightExtractionQueryTask","Version": "2020-08-26"}, {}, {}),
            "CertToken": ApiInfo("POST", "/", {"Action": "CertToken", "Version": "2022-08-31"}, {}, {}),
            "CertVerifyQuery": ApiInfo("POST", "/", {"Action": "CertVerifyQuery", "Version": "2022-08-31"}, {}, {}),
            "T2ILDM": ApiInfo("POST", "/", {"Action": "T2ILDM", "Version": "2022-08-31"}, {}, {}),
            "Img2ImgStyle": ApiInfo("POST", "/", {"Action": "Img2ImgStyle", "Version": "2022-08-31"}, {}, {}),
            "Img2ImgAnime": ApiInfo("POST", "/", {"Action": "Img2ImgAnime", "Version": "2022-08-31"}, {}, {}),
            "ImageScoreV2": ApiInfo("POST", "/", {"Action": "ImageScoreV2", "Version": "2022-08-31"}, {}, {}),
            "EnhancePhotoV2": ApiInfo("POST", "/", {"Action": "EnhancePhotoV2", "Version": "2022-08-31"}, {}, {}),
            "OverResolutionV2": ApiInfo("POST", "/", {"Action": "OverResolutionV2", "Version": "2022-08-31"}, {}, {}),
            "VideoOverResolutionSubmitTaskV2": ApiInfo("POST", "/", {"Action": "VideoOverResolutionSubmitTaskV2","Version": "2022-08-31"}, {}, {}),
            "VideoOverResolutionQueryTaskV2": ApiInfo("POST", "/", {"Action": "VideoOverResolutionQueryTaskV2","Version": "2022-08-31"}, {}, {}),
            "ImageCorrection": ApiInfo("POST", "/", {"Action": "ImageCorrection", "Version": "2022-08-31"}, {}, {}),
            "AllAgeGeneration": ApiInfo("POST", "/", {"Action": "AllAgeGeneration", "Version": "2022-08-31"}, {}, {}),
            "BodyDetection": ApiInfo("POST", "/", {"Action": "BodyDetection", "Version": "2022-08-31"}, {}, {}),
            "FaceFusionMovieSubmitTask": ApiInfo("POST", "/", {"Action": "FaceFusionMovieSubmitTask", "Version": "2022-08-31"}, {},{}),
            "FaceFusionMovieGetResult": ApiInfo("POST", "/", {"Action": "FaceFusionMovieGetResult", "Version": "2022-08-31"}, {},{}),
            "FaceFusionMovie": ApiInfo("POST", "/", {"Action": "FaceFusionMovie", "Version": "2022-08-31"}, {}, {}),
            "TupoCartoon": ApiInfo("POST", "/", {"Action": "TupoCartoon", "Version": "2022-08-31"}, {}, {}),
            "LensVidaVideoSubmitTaskV2": ApiInfo("POST", "/",{"Action": "LensVidaVideoSubmitTaskV2", "Version": "2022-08-31"}, {},{}),
            "LensVidaVideoGetResultV2": ApiInfo("POST", "/",{"Action": "LensVidaVideoGetResultV2", "Version": "2022-08-31"}, {},{}),
            "CertSrcFaceComp": ApiInfo("POST", "/", {"Action": "CertSrcFaceComp", "Version": "2022-08-31"}, {}, {}),
            "AIGufeng": ApiInfo("POST", "/", {"Action": "AIGufeng", "Version": "2022-08-31"}, {}, {}),
            "CertConfigInit": ApiInfo("POST", "/", {"Action": "CertConfigInit", "Version": "2022-08-31"}, {}, {}),
            "CertConfigGet": ApiInfo("POST", "/", {"Action": "CertConfigInit", "Version": "2022-08-31"}, {}, {}),
            "FaceCompare": ApiInfo("POST", "/", {"Action": "FaceCompare", "Version": "2022-08-31"}, {}, {}),
            "StillLivenessImg": ApiInfo("POST", "/", {"Action": "StillLivenessImg", "Version": "2022-08-31"}, {}, {}),
            "CertAuth": ApiInfo("POST", "/", {"Action": "CertAuth", "Version": "2022-08-31"}, {}, {}),
            "CertVerify": ApiInfo("POST", "/", {"Action": "CertVerify", "Version": "2022-08-31"}, {}, {}),
            "FaceSwapV2": ApiInfo("POST", "/", {"Action": "FaceSwap", "Version": "2022-08-31"}, {}, {}),
            "FaceswapAI": ApiInfo("POST", "/", {"Action": "FaceswapAI", "Version": "2022-08-31"}, {}, {}),
            "CertH5ConfigInit": ApiInfo("POST", "/", {"Action": "CertH5ConfigInit", "Version": "2022-08-31"}, {}, {}),
            "CertH5Token": ApiInfo("POST", "/", {"Action": "CertH5Token", "Version": "2022-08-31"}, {}, {}),
            "HighAesSmartDrawing": ApiInfo("POST", "/", {"Action": "HighAesSmartDrawing", "Version": "2022-08-31"}, {},{}),
            "EmotionPortrait": ApiInfo("POST", "/", {"Action": "EmotionPortrait", "Version": "2022-08-31"}, {}, {}),
            "Img2ImgInpainting": ApiInfo("POST", "/", {"Action": "Img2ImgInpainting", "Version": "2022-08-31"}, {}, {}),
            "Img2ImgInpaintingEdit": ApiInfo("POST", "/", {"Action": "Img2ImgInpaintingEdit", "Version": "2022-08-31"},{}, {}),
            "Img2ImgOutpainting": ApiInfo("POST", "/", {"Action": "Img2ImgOutpainting", "Version": "2022-08-31"}, {},{}),
            "Img2ImgCreateDisneyStyleNoFace": ApiInfo("POST", "/", {"Action": "Img2ImgCreateDisneyStyleNoFace","Version": "2022-08-31"}, {}, {}),
            "Img2ImgCreatePastelBoys2D": ApiInfo("POST", "/",{"Action": "Img2ImgCreatePastelBoys2D", "Version": "2022-08-31"}, {},{}),
            "Img2ImgCreateAesBlueline": ApiInfo("POST", "/",{"Action": "Img2ImgCreateAesBlueline", "Version": "2022-08-31"}, {},{}),
            "Img2ImgCreateEtherRealMix": ApiInfo("POST", "/",{"Action": "Img2ImgCreateEtherRealMix", "Version": "2022-08-31"}, {},{}),
            "Img2ImgCreateToonyou": ApiInfo("POST", "/", {"Action": "Img2ImgCreateToonyou", "Version": "2022-08-31"},{}, {}),
            "Img2ImgCreateAnyloraMakoto": ApiInfo("POST", "/",{"Action": "Img2ImgCreateAnyloraMakoto", "Version": "2022-08-31"}, {},{}),
            "Img2ImgCreateRevAnimated": ApiInfo("POST", "/",{"Action": "Img2ImgCreateRevAnimated", "Version": "2022-08-31"}, {},{}),
            "Img2ImgCreateInkAndWater": ApiInfo("POST", "/",{"Action": "Img2ImgCreateInkAndWater", "Version": "2022-08-31"}, {},{}),
            "Img2ImgWaterColorStyle": ApiInfo("POST", "/",{"Action": "Img2ImgWaterColorStyle", "Version": "2022-08-31"}, {}, {}),
            "OCRPdfSubmitTask": ApiInfo("POST", "/", {"Action": "OCRPdfSubmitTask", "Version": "2021-08-23"}, {}, {}),
            "OCRPdfQueryTask": ApiInfo("POST", "/", {"Action": "OCRPdfQueryTask", "Version": "2021-08-23"}, {}, {}),
            "EntitySegment": ApiInfo("POST", "/", {"Action": "EntitySegment", "Version": "2022-08-31"}, {}, {}),
            "Img2ImgAnimeAcceleratedMaintainID": ApiInfo("POST", "/", {"Action": "Img2ImgAnimeAcceleratedMaintainID","Version": "2022-08-31"}, {}, {}),
            "Img2ImgComicsStyle": ApiInfo("POST", "/", {"Action": "Img2ImgComicsStyle", "Version": "2022-08-31"}, {},{}),
            "Img2ImgExquisiteStyle": ApiInfo("POST", "/", {"Action": "Img2ImgExquisiteStyle", "Version": "2022-08-31"},{}, {}),
            "Text2ImgXLSft": ApiInfo("POST", "/", {"Action": "Text2ImgXLSft", "Version": "2022-08-31"}, {}, {}),
            "Img2ImgXLSft": ApiInfo("POST", "/", {"Action": "Img2ImgXLSft", "Version": "2022-08-31"}, {}, {}),
            "CVGetResult": ApiInfo("POST", "/", {"Action": "CVGetResult", "Version": "2022-08-31"}, {}, {}),
            "CVSubmitTask": ApiInfo("POST", "/", {"Action": "CVSubmitTask", "Version": "2022-08-31"}, {}, {}),
            "CVSync2AsyncGetResult": ApiInfo("POST", "/", {"Action": "CVSync2AsyncGetResult", "Version": "2022-08-31"},{}, {}),
            "CVSync2AsyncSubmitTask": ApiInfo("POST", "/",{"Action": "CVSync2AsyncSubmitTask", "Version": "2022-08-31"}, {}, {}),
            "CVProcess": ApiInfo("POST", "/", {"Action": "CVProcess", "Version": "2022-08-31"}, {}, {}),
            "CertLivenessVerifyQuery": ApiInfo("POST", "/",
                                               {"Action": "CertLivenessVerifyQuery", "Version": "2022-08-31"}, {}, {}),
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

    def common_json_handler(self, api, form):
        params = dict()
        try:
            res = self.json(api, params, json.dumps(form))
            res_json = json.loads(res)

            return res_json
        except Exception as e:
            res = str(e)
            try:
                res_json = json.loads(res)
                return res_json
            except:
                raise Exception(str(e))

    def cv_json_api(self, action, form):
        try:
            res_json = self.common_json_handler(action, form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def cv_form_api(self, action, form):
        try:
            res_json = self.common_handler(action, form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def cv_process(self, form):
        try:
            res_json = self.common_json_handler("CVProcess", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def cv_submit_task(self, form):
        try:
            res_json = self.common_json_handler("CVSubmitTask", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def cv_get_result(self, form):
        try:
            res_json = self.common_json_handler("CVGetResult", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def cv_sync2async_submit_task(self, form):
        try:
            res_json = self.common_json_handler("CVSync2AsyncSubmitTask", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def cv_sync2async_get_result(self, form):
        try:
            res_json = self.common_json_handler("CVSync2AsyncGetResult", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def cert_pro_liveness_verify_query(self, form):
        try:
            res_json = self.common_json_handler("CertLivenessVerifyQuery", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def img2img_xl_sft(self, form):
        try:
            res_json = self.common_json_handler("Img2ImgXLSft", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def text2img_xl_sft(self, form):
        try:
            res_json = self.common_json_handler("Text2ImgXLSft", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def img2img_comics_style(self, form):
        try:
            res_json = self.common_json_handler("Img2ImgComicsStyle", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def img2img_exquisite_style(self, form):
        try:
            res_json = self.common_json_handler("Img2ImgExquisiteStyle", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def img2img_anime_accelerated_maintain_id(self, form):
        try:
            res_json = self.common_json_handler("Img2ImgAnimeAcceleratedMaintainID", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def entity_segment(self, form):
        try:
            res_json = self.common_json_handler("EntitySegment", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def ocr_pdf_submit_task(self, form):
        try:
            res_json = self.common_json_handler("OCRPdfSubmitTask", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def ocr_pdf_query_task(self, form):
        try:
            res_json = self.common_json_handler("OCRPdfQueryTask", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def img2img_create_disney_style_no_face(self, form):
        try:
            res_json = self.common_json_handler("Img2ImgCreateDisneyStyleNoFace", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def img2img_create_pastel_boys2d(self, form):
        try:
            res_json = self.common_json_handler("Img2ImgCreatePastelBoys2D", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def img2img_create_ether_real_mix(self, form):
        try:
            res_json = self.common_json_handler("Img2ImgCreateEtherRealMix", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def img2img_create_toonyou(self, form):
        try:
            res_json = self.common_json_handler("Img2ImgCreateToonyou", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def img2img_create_anylora_makoto(self, form):
        try:
            res_json = self.common_json_handler("Img2ImgCreateAnyloraMakoto", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def img2img_create_rev_animated(self, form):
        try:
            res_json = self.common_json_handler("Img2ImgCreateRevAnimated", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def img2img_create_aes_blueline(self, form):
        try:
            res_json = self.common_json_handler("Img2ImgCreateAesBlueline", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def img2img_create_ink_and_water(self, form):
        try:
            res_json = self.common_json_handler("Img2ImgCreateInkAndWater", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def img2img_water_color_style(self, form):
        try:
            res_json = self.common_json_handler("Img2ImgWaterColorStyle", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def high_aes_smart_drawing_v2(self, form):
        try:
            res_json = self.common_json_handler("HighAesSmartDrawing", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def jpcartoon_cut(self, form):
        try:
            res_json = self.common_handler("JPCartoonCut", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def img2img_inpainting(self, form):
        try:
            res_json = self.common_json_handler("Img2ImgInpainting", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def img2img_inpainting_edit(self, form):
        try:
            res_json = self.common_json_handler("Img2ImgInpaintingEdit", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def img2img_outpainting(self, form):
        try:
            res_json = self.common_json_handler("Img2ImgOutpainting", form)
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

    def high_aes_smart_drawing(self, form):
        try:
            res_json = self.common_json_handler("HighAesSmartDrawing", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def face_swap(self, form):
        try:
            res_json = self.common_handler("FaceSwap", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def face_swap_v2(self, form):
        try:
            res_json = self.common_json_handler("FaceSwapV2", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def faceswap_ai(self, form):
        try:
            res_json = self.common_json_handler("FaceswapAI", form)
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

    def convert_photo_v2(self, form):
        try:
            res_json = self.common_json_handler("ConvertPhotoV2", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def cert_h5_config_init(self, form):
        try:
            res_json = self.common_json_handler("CertH5ConfigInit", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def cert_h5_token(self, form):
        try:
            res_json = self.common_json_handler("CertH5Token", form)
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

    def car_plate_detection(self, form):
        try:
            res_json = self.common_handler("CarPlateDetection", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def distortion_free(self, form):
        try:
            res_json = self.common_handler("DistortionFree", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def stretch_recovery(self, form):
        try:
            res_json = self.common_handler("StretchRecovery", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def image_flow(self, form):
        try:
            res_json = self.common_handler("ImageFlow", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def image_score(self, form):
        try:
            res_json = self.common_handler("ImageScore", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def poem_material(self, form):
        try:
            res_json = self.common_handler("PoemMaterial", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def emoticon_edit(self, form):
        try:
            res_json = self.common_handler("EmoticonEdit", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def eye_close2open(self, form):
        try:
            res_json = self.common_handler("EyeClose2Open", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def car_segment(self, form):
        try:
            res_json = self.common_handler("CarSegment", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def car_detection(self, form):
        try:
            res_json = self.common_handler("CarDetection", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def sky_segment(self, form):
        try:
            res_json = self.common_handler("SkySegment", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def image_search_image_add(self, form):
        try:
            res_json = self.common_handler("ImageSearchImageAdd", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def image_search_image_delete(self, form):
        try:
            res_json = self.common_handler("ImageSearchImageDelete", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def image_search_image_search(self, form):
        try:
            res_json = self.common_handler("ImageSearchImageSearch", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def product_search_add_image(self, params):
        try:
            res_json = self.json("ProductSearchAddImage", [], json.dumps(params))
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def product_search_delete_image(self, params):
        try:
            res_json = self.json("ProductSearchDeleteImage", [], json.dumps(params))
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def product_search_search_image(self, params):
        try:
            res_json = self.json("ProductSearchSearchImage", [], json.dumps(params))
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def clue_license(self, form):
        try:
            res_json = self.common_handler("ClueLicense", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def driving_license(self, form):
        try:
            res_json = self.common_handler("DrivingLicense", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def vehicle_license(self, form):
        try:
            res_json = self.common_handler("VehicleLicense", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def taxi_invoice(self, form):
        try:
            res_json = self.common_handler("TaxiInvoice", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def train_ticket(self, form):
        try:
            res_json = self.common_handler("TrainTicket", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def flight_invoice(self, form):
        try:
            res_json = self.common_handler("FlightInvoice", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def vat_invoice(self, form):
        try:
            res_json = self.common_handler("VatInvoice", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def quota_invoice(self, form):
        try:
            res_json = self.common_handler("QuotaInvoice", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def hair_style(self, form):
        try:
            res_json = self.common_handler("HairStyle", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def hair_style_v2(self, form):
        try:
            res_json = self.common_json_handler("HairStyleV2", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def face_pretty(self, form):
        try:
            res_json = self.common_handler("FacePretty", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def image_animation(self, form):
        try:
            res_json = self.common_handler("ImageAnimation", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def cover_video(self, form):
        try:
            res_json = self.common_handler("CoverVideo", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def dolly_zoom(self, form):
        try:
            res_json = self.common_handler("DollyZoom", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def img2video3d(self, form):
        try:
            res_json = self.common_json_handler("Img2Video3D", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def ai_gufeng(self, form):
        try:
            res_json = self.common_json_handler("AIGufeng", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def potrait_effect(self, form):
        try:
            res_json = self.common_handler("PotraitEffect", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def image_style_conversion(self, form):
        try:
            res_json = self.common_handler("ImageStyleConversion", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def three_d_game_cartoon(self, form):
        try:
            res_json = self.common_handler("3DGameCartoon", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def hair_segment(self, form):
        try:
            res_json = self.common_handler("HairSegment", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def ocr_seal(self, form):
        try:
            res_json = self.common_handler("OcrSeal", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def ocr_pass_invoice(self, form):
        try:
            res_json = self.common_handler("OcrPassInvoice", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def ocr_trade(self, form):
        try:
            res_json = self.common_handler("OCRTrade", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def ocr_ruanzhu(self, form):
        try:
            res_json = self.common_handler("OCRRuanzhu", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def ocr_cosmetic_product(self, form):
        try:
            res_json = self.common_handler("OCRCosmeticProduct", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def ocr_pdf(self, form):
        try:
            res_json = self.common_handler("OCRPdf", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def ocr_table(self, form):
        try:
            res_json = self.common_handler("OCRTable", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def video_cover_selection(self, form):
        try:
            res_json = self.common_handler("VideoCoverSelection", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def video_highlight_extraction_submit_task(self, form):
        try:
            res_json = self.common_handler(
                "VideoHighlightExtractionSubmitTask", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def video_highlight_extraction_query_task(self, params):
        try:
            res_json = self.common_get_handler(
                "VideoHighlightExtractionQueryTask", params)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def cert_token(self, form):
        try:
            res_json = self.common_json_handler("CertToken", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def cert_verify_query(self, form):
        try:
            res_json = self.common_json_handler("CertVerifyQuery", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def t2i_ldm(self, form):
        try:
            res_json = self.common_json_handler("T2ILDM", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def img2img_style(self, form):
        try:
            res_json = self.common_json_handler("Img2ImgStyle", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def img2img_anime(self, form):
        try:
            res_json = self.common_json_handler("Img2ImgAnime", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def ocr_api(self, action, form):
        try:
            res_json = self.common_handler(action, form)
            return res_json
        except Exception as e:
            raise Exception(str(e))
        
    def ocr_async_api(self, action, form):
        try:
            res_json = self.common_json_handler(action, form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def image_score_v2(self, body):
        try:
            res_json = self.common_json_handler("ImageScoreV2", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def enhance_photo_v2(self, body):
        try:
            res_json = self.common_json_handler("EnhancePhotoV2", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def over_resolution_v2(self, body):
        try:
            res_json = self.common_json_handler("OverResolutionV2", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def video_over_resolution_submit_task_v2(self, body):
        try:
            res_json = self.common_json_handler("VideoOverResolutionSubmitTaskV2", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def video_over_resolution_get_result_v2(self, body):
        try:
            res_json = self.common_json_handler("VideoOverResolutionQueryTaskV2", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def image_correction(self, body):
        try:
            res_json = self.common_json_handler("ImageCorrection", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def all_age_generation(self, body):
        try:
            res_json = self.common_json_handler("AllAgeGeneration", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def body_detection(self, body):
        try:
            res_json = self.common_json_handler("BodyDetection", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def face_fusion_movie_submit_task(self, body):
        try:
            res_json = self.common_json_handler("FaceFusionMovieSubmitTask", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def face_fusion_movie_get_result(self, body):
        try:
            res_json = self.common_json_handler("FaceFusionMovieGetResult", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def face_fusion_movie(self, body):
        try:
            res_json = self.common_json_handler("FaceFusionMovie", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def tupo_cartoon(self, body):
        try:
            res_json = self.common_json_handler("TupoCartoon", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def lens_vida_video_submit_task_v2(self, body):
        try:
            res_json = self.common_json_handler("LensVidaVideoSubmitTaskV2", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def lens_vida_video_get_result_v2(self, body):
        try:
            res_json = self.common_json_handler("LensVidaVideoGetResultV2", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def cert_src_face_comp(self, body):
        try:
            res_json = self.common_json_handler("CertSrcFaceComp", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def cert_config_init(self, form):
        try:
            res_json = self.common_json_handler("CertConfigInit", form)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def cert_config_get(self, body):
        try:
            res_json = self.common_json_handler("CertConfigGet", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def face_compare(self, body):
        try:
            res_json = self.common_json_handler("FaceCompare", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def still_liveness_img(self, body):
        try:
            res_json = self.common_json_handler("StillLivenessImg", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def emotion_portrait(self, body):
        try:
            res_json = self.common_json_handler("EmotionPortrait", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def cert_auth(self, body):
        try:
            res_json = self.common_json_handler("CertAuth", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def cert_verify(self, body):
        try:
            res_json = self.common_json_handler("CertVerify", body)
            return res_json
        except Exception as e:
            raise Exception(str(e))

    def set_api_info(self, action, version):
        self.api_info[action] = ApiInfo("POST", "/", {"Action": action, "Version": version}, {}, {})